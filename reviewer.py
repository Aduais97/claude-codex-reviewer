#!/usr/bin/env python3
"""
reviewer.py - Cross-Model Code Review & Fix Agent (macOS)

Dispatch Rules:
  1. Claude BUILDS the prompt/spec from user requirements
  2. Codex REVIEWS the prompt for gaps and completeness
  3. Codex WRITES the code based on the finalized prompt
  4. Claude REVIEWS the code for bugs, security, and correctness
  5. Codex FIXES issues found by Claude's review
  6. Claude RE-REVIEWS until clean or max rounds hit

Usage:
    python3 reviewer.py full    --config config.json   # full pipeline (prompt build + review + code + fix + merge)
    python3 reviewer.py prompt  --config config.json   # build & validate prompt only
    python3 reviewer.py review  --config config.json   # code review only
    python3 reviewer.py fix     --config config.json   # fix from saved reviews
    python3 reviewer.py merge   --config config.json   # merge only

Config format (review_config.json):
{
    "base_branch": "main",
    "merge_directory": "/Users/ahmadduais/projects/my-project",
    "max_rounds": 2,
    "auto_merge": true,
    "branches": [
        {
            "name": "feature/roster-system",
            "directory": "/Users/ahmadduais/projects/my-project",
            "author_model": "codex",
            "prompt_file": "/Users/ahmadduais/projects/my-project/PROMPT.md",
            "user_requirements": "Build a guard roster system with shift scheduling and SMS notifications"
        }
    ]
}

Fields:
  - user_requirements: Plain English description of what you want built.
    Claude will expand this into a full technical spec (prompt_file).
  - prompt_file: Where the generated/finalized spec is saved.
    Codex reviews it for gaps, then uses it to write code.
  - author_model: Should be "codex" (Codex writes, Claude reviews).
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import platform
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Platform detection & configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IS_MACOS = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"
HOME = Path.home()


def _find_executable(name: str, env_var: str, fallbacks: list[str]) -> str:
    """Find an executable by env var, PATH lookup, or known fallback locations."""
    from_env = os.environ.get(env_var)
    if from_env and (Path(from_env).exists() or shutil.which(from_env)):
        return from_env
    found = shutil.which(name)
    if found:
        return found
    for fb in fallbacks:
        expanded = os.path.expanduser(fb)
        if Path(expanded).exists():
            return expanded
    return name


CLAUDE_EXE = _find_executable(
    "claude",
    "CLAUDE_EXE",
    [
        "~/.local/bin/claude",
        "~/.claude/local/claude",
        "/opt/homebrew/bin/claude",
        "/usr/local/bin/claude",
    ],
)

CODEX_CMD = _find_executable(
    "codex",
    "CODEX_CMD",
    [
        "~/.npm-global/bin/codex",
        "/opt/homebrew/bin/codex",
        "/usr/local/bin/codex",
    ],
)

LOG_DIR = Path(
    os.environ.get("REVIEWER_LOG_DIR", str(HOME / "reviewer-logs"))
)

MAX_DIFF_SIZE = 120_000  # chars — truncate diffs beyond this

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Logging
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "reviewer.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("reviewer")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Shell helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_cmd(
    cmd: list[str] | str,
    cwd: str,
    timeout: int = 120,
    shell: bool = True,
) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            timeout=timeout,
            shell=shell,
        )
        stdout = result.stdout.decode("utf-8", errors="replace") if result.stdout else ""
        stderr = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
        return result.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Timed out after {timeout}s"
    except Exception as e:
        return -1, "", str(e)


def _git_working_tree_hash(cwd: str) -> str:
    """Return a working-tree activity fingerprint.

    Fingerprints modified/untracked paths together with their mtimes
    and sizes to detect active model work reliably.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=cwd,
            capture_output=True,
            timeout=10,
            text=True,
        )
        if result.returncode != 0:
            return ""

        entries: list[str] = []
        for raw_line in result.stdout.splitlines():
            if not raw_line:
                continue
            path_text = raw_line[3:]
            if not path_text:
                continue
            if " -> " in path_text:
                path_text = path_text.split(" -> ", 1)[1]
            full_path = Path(cwd) / path_text
            try:
                stat = full_path.stat()
                entries.append(f"{path_text}:{stat.st_mtime_ns}:{stat.st_size}")
            except OSError:
                entries.append(f"{path_text}:missing")

        return "\n".join(sorted(entries))
    except Exception:
        return ""


def run_cmd_streaming(
    cmd: list[str] | str,
    cwd: str,
    timeout: int = 120,
    shell: bool = True,
    idle_timeout: int | None = None,
    heartbeat_interval: int = 30,
    log_label: str = "command",
    track_fs_activity: bool = False,
    fs_check_interval: int = 30,
    fs_timeout_extension: int = 300,
    max_fs_extensions: int = 10,
) -> tuple[int, str, str]:
    """Run a command with heartbeats, idle-timeout, and optional filesystem activity tracking.

    When track_fs_activity=True, the working tree is polled every fs_check_interval
    seconds. If file changes are detected, the hard timeout is extended by
    fs_timeout_extension seconds (up to max_fs_extensions times).
    """
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            shell=shell,
        )
    except Exception as e:
        return -1, "", str(e)

    event_q: queue.Queue[tuple[str, str | None]] = queue.Queue()

    def _reader(stream, stream_name: str) -> None:
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="replace")
                event_q.put((stream_name, text))
        finally:
            event_q.put((stream_name, None))

    stdout_thread = threading.Thread(target=_reader, args=(proc.stdout, "stdout"), daemon=True)
    stderr_thread = threading.Thread(target=_reader, args=(proc.stderr, "stderr"), daemon=True)
    stdout_thread.start()
    stderr_thread.start()

    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    open_streams = {"stdout", "stderr"}
    start = time.monotonic()
    last_output = start
    last_heartbeat = start
    saw_output = False

    # Filesystem activity tracking state
    effective_timeout = timeout
    last_fs_check = start
    last_fs_hash = _git_working_tree_hash(cwd) if track_fs_activity else ""
    fs_extensions_used = 0
    last_fs_activity = start

    while True:
        now = time.monotonic()

        drained = False
        while True:
            try:
                stream_name, chunk = event_q.get_nowait()
            except queue.Empty:
                break
            drained = True
            if chunk is None:
                open_streams.discard(stream_name)
                continue
            saw_output = True
            last_output = now
            if stream_name == "stdout":
                stdout_parts.append(chunk)
            else:
                stderr_parts.append(chunk)

        # Filesystem activity check
        fs_active = False
        if track_fs_activity and now - last_fs_check >= fs_check_interval:
            last_fs_check = now
            current_hash = _git_working_tree_hash(cwd)
            if current_hash != last_fs_hash:
                fs_active = True
                last_fs_hash = current_hash
                last_fs_activity = now
                last_output = now
                saw_output = True

                if fs_extensions_used < max_fs_extensions:
                    old_timeout = effective_timeout
                    effective_timeout += fs_timeout_extension
                    fs_extensions_used += 1
                    log.info(
                        f"  {log_label} FS ACTIVITY detected: files changed in working tree. "
                        f"Extending timeout {old_timeout}s -> {effective_timeout}s "
                        f"(extension {fs_extensions_used}/{max_fs_extensions})"
                    )
                else:
                    log.info(
                        f"  {log_label} FS ACTIVITY detected but max extensions reached "
                        f"({max_fs_extensions}). Timeout stays at {effective_timeout}s"
                    )

        if now - last_heartbeat >= heartbeat_interval:
            elapsed = int(now - start)
            idle = int(now - last_output)
            char_count = sum(len(p) for p in stdout_parts) + sum(len(p) for p in stderr_parts)
            fs_idle = int(now - last_fs_activity) if track_fs_activity else -1
            fs_info = f" fs_idle={fs_idle}s ext={fs_extensions_used}" if track_fs_activity else ""
            log.info(
                f"  {log_label} still running: elapsed={elapsed}s timeout={effective_timeout}s "
                f"idle={idle}s saw_output={'yes' if saw_output else 'no'} chars={char_count}{fs_info}"
            )
            last_heartbeat = now

        if saw_output and idle_timeout and now - last_output > idle_timeout:
            proc.kill()
            return -2, "".join(stdout_parts), (
                f"Stale after {int(now - last_output)}s without output "
                f"(elapsed {int(now - start)}s, idle timeout {idle_timeout}s)"
            )

        if now - start > effective_timeout:
            proc.kill()
            return -1, "".join(stdout_parts), (
                f"Timed out after {int(now - start)}s (base={timeout}s, "
                f"extended={effective_timeout}s, fs_extensions={fs_extensions_used})"
            )

        rc = proc.poll()
        if rc is not None and not open_streams:
            break

        if not drained:
            time.sleep(0.5)

    # Final drain
    while True:
        try:
            stream_name, chunk = event_q.get_nowait()
        except queue.Empty:
            break
        if chunk is None:
            continue
        if stream_name == "stdout":
            stdout_parts.append(chunk)
        else:
            stderr_parts.append(chunk)

    stdout_thread.join(timeout=1)
    stderr_thread.join(timeout=1)
    return proc.returncode or 0, "".join(stdout_parts), "".join(stderr_parts)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Git helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def git(args: str, cwd: str, timeout: int = 60) -> tuple[int, str]:
    """Run a git command, return (rc, stdout)."""
    rc, out, err = run_cmd(f"git {args}", cwd=cwd, timeout=timeout)
    return rc, ((out or "") + (err or "")).strip()


def git_diff(directory: str, base: str) -> str:
    """Get diff between base branch and HEAD, with stat header."""
    _, stat = git(f"diff {base}...HEAD --stat", cwd=directory)
    _, diff = git(f"diff {base}...HEAD", cwd=directory)
    full = f"DIFF STAT:\n{stat}\n\nFULL DIFF:\n{diff}"
    if len(full) > MAX_DIFF_SIZE:
        full = full[:MAX_DIFF_SIZE] + f"\n\n... TRUNCATED (>{MAX_DIFF_SIZE} chars) ..."
    return full


def git_log(directory: str, base: str) -> str:
    _, out = git(f"log {base}..HEAD --oneline", cwd=directory)
    return out


def git_commit_count(directory: str) -> int:
    _, out = git("rev-list --count HEAD", cwd=directory)
    try:
        return int(out.strip())
    except ValueError:
        return 0


def git_conflict_files(directory: str) -> str:
    _, out = git("diff --name-only --diff-filter=U", cwd=directory)
    return out.strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Model runners
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def scaled_timeout(base_timeout: int, context_size: int, max_timeout: int = 1800) -> int:
    """Scale timeout with context size so larger diffs/specs get more time."""
    extra = math.ceil(max(context_size, 0) / 250)
    return max(base_timeout, min(max_timeout, base_timeout + extra))


def scaled_idle_timeout(total_timeout: int) -> int:
    """Idle timeout should be generous but bounded."""
    return max(180, min(900, total_timeout // 2))


def _escape_prompt(prompt: str) -> str:
    """Escape a prompt for safe embedding in a shell command string.

    Uses single quotes with proper escaping for POSIX shells (bash/zsh).
    This is safer than double-quote escaping on macOS.
    """
    # For shell safety: replace single quotes with '\'' (end quote, escaped quote, start quote)
    escaped = prompt.replace("'", "'\\''")
    return escaped


def _build_claude_cmd(prompt: str, use_prompt_file: bool = True, cwd: str = ".") -> str:
    """Build the Claude CLI command string."""
    if use_prompt_file:
        prompt_path = os.path.join(cwd, "_prompt_input.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        return f"cat '{prompt_path}' | {CLAUDE_EXE} --dangerously-skip-permissions -p -"
    return f"{CLAUDE_EXE} --dangerously-skip-permissions -p '{_escape_prompt(prompt)}'"


def _build_codex_cmd(prompt: str, use_prompt_file: bool = True, cwd: str = ".") -> str:
    """Build the Codex CLI command string."""
    if use_prompt_file:
        prompt_path = os.path.join(cwd, "_prompt_input.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        return f"cat '{prompt_path}' | {CODEX_CMD} exec --dangerously-bypass-approvals-and-sandbox --json -"
    return f"{CODEX_CMD} exec --dangerously-bypass-approvals-and-sandbox --json '{_escape_prompt(prompt)}'"


def run_claude(
    prompt: str,
    cwd: str,
    timeout: int = 600,
    idle_timeout: int | None = None,
    log_label: str = "Claude",
) -> str:
    """Run Claude CLI and return combined output."""
    log.info(f"  Running Claude in {cwd} (timeout={timeout}s)")
    cmd = _build_claude_cmd(prompt, use_prompt_file=True, cwd=cwd)
    rc, out, err = run_cmd_streaming(
        cmd,
        cwd=cwd,
        timeout=timeout,
        idle_timeout=idle_timeout,
        heartbeat_interval=30,
        log_label=log_label,
        track_fs_activity=True,
        fs_check_interval=30,
        fs_timeout_extension=300,
        max_fs_extensions=10,
    )
    # Clean up prompt file
    cleanup_file(os.path.join(cwd, "_prompt_input.txt"))
    result = (out or "") + (err or "")
    log.info(f"  Claude done (rc={rc}, {len(result)} chars)")
    return result


def run_codex(
    prompt: str,
    cwd: str,
    timeout: int = 600,
    idle_timeout: int | None = None,
    log_label: str = "Codex",
) -> str:
    """Run Codex CLI and return combined output."""
    log.info(f"  Running Codex in {cwd} (timeout={timeout}s)")
    cmd = _build_codex_cmd(prompt, use_prompt_file=True, cwd=cwd)
    rc, out, err = run_cmd_streaming(
        cmd,
        cwd=cwd,
        timeout=timeout,
        idle_timeout=idle_timeout,
        heartbeat_interval=30,
        log_label=log_label,
        track_fs_activity=True,
        fs_check_interval=30,
        fs_timeout_extension=300,
        max_fs_extensions=10,
    )
    # Clean up prompt file
    cleanup_file(os.path.join(cwd, "_prompt_input.txt"))
    result = (out or "") + (err or "")
    log.info(f"  Codex done (rc={rc}, {len(result)} chars)")
    return result


def run_model(
    model: str,
    prompt: str,
    cwd: str,
    timeout: int = 600,
    idle_timeout: int | None = None,
    log_label: str | None = None,
) -> str:
    """Run the specified model."""
    if model == "claude":
        return run_claude(prompt, cwd, timeout, idle_timeout=idle_timeout, log_label=log_label or "Claude")
    elif model == "codex":
        return run_codex(prompt, cwd, timeout, idle_timeout=idle_timeout, log_label=log_label or "Codex")
    else:
        raise ValueError(f"Unknown model: {model}")


def opposite_model(model: str) -> str:
    return "codex" if model == "claude" else "claude"


def get_reviewer_model(branch_config: dict, config: dict | None = None) -> str:
    """Get the reviewer model for a branch.

    Default dispatch: Codex writes code, Claude reviews code.
    Priority: branch.reviewer_model > config.reviewer_model > "claude"
    """
    if branch_config.get("reviewer_model"):
        return branch_config["reviewer_model"]
    if config and config.get("reviewer_model"):
        return config["reviewer_model"]
    # Default: Claude always reviews (Codex is the author)
    return "claude"


def write_prompt_file(directory: str, filename: str, content: str) -> str:
    """Write prompt content to a file, return path."""
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def cleanup_file(path: str) -> None:
    """Remove a file if it exists."""
    try:
        os.remove(path)
    except OSError:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Review parsing
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _extract_balanced_json_object(text: str, start: int) -> dict | None:
    """Parse the first balanced JSON object starting at `start`."""
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _parse_expected_json(text: str, required_key: str) -> dict | None:
    """Extract a structured JSON object containing `required_key`."""
    stripped = (text or "").strip()
    if not stripped:
        return None

    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict) and required_key in parsed:
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass

    m = re.search(r"```(?:json)?\s*\n(\{.*?\})\s*\n```", text, re.DOTALL)
    if m:
        try:
            parsed = json.loads(m.group(1))
            if isinstance(parsed, dict) and required_key in parsed:
                return parsed
        except json.JSONDecodeError:
            pass

    for marker in (f'"{required_key}"',):
        search_from = 0
        while True:
            key_pos = text.find(marker, search_from)
            if key_pos == -1:
                break
            brace_pos = text.rfind("{", 0, key_pos)
            while brace_pos != -1:
                parsed = _extract_balanced_json_object(text, brace_pos)
                if isinstance(parsed, dict) and required_key in parsed:
                    return parsed
                brace_pos = text.rfind("{", 0, brace_pos)
            search_from = key_pos + len(marker)

    return None


def _extract_codex_event_messages(output: str) -> list[str]:
    """Extract agent messages from Codex JSONL event streams."""
    messages: list[str] = []
    saw_event = False
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict) or "type" not in payload:
            continue
        saw_event = True
        item = payload.get("item")
        if not isinstance(item, dict):
            continue
        if item.get("type") == "agent_message":
            text = item.get("text")
            if isinstance(text, str) and text.strip():
                messages.append(text)
    return messages if saw_event else []


def _structured_output_candidates(output: str, required_key: str) -> list[str]:
    """Return likely text candidates that may contain the requested JSON payload."""
    candidates: list[str] = []
    seen: set[str] = set()

    def add(candidate: str | None) -> None:
        if not isinstance(candidate, str):
            return
        text = candidate.strip()
        if not text or text in seen:
            return
        seen.add(text)
        candidates.append(text)

    codex_messages = _extract_codex_event_messages(output)
    for message in reversed(codex_messages):
        add(message)
    if codex_messages:
        add("\n\n".join(codex_messages))

    try:
        wrapper = json.loads(output)
        if isinstance(wrapper, dict):
            for key in ("content", "output", "result", "message", "text"):
                if key in wrapper and isinstance(wrapper[key], str):
                    add(wrapper[key])
            if required_key in wrapper:
                add(json.dumps(wrapper))
    except (json.JSONDecodeError, TypeError):
        pass

    add(output)
    return candidates


def parse_review_output(output: str) -> dict:
    """Extract structured review JSON from model output."""
    for candidate in _structured_output_candidates(output, "verdict"):
        parsed = _parse_expected_json(candidate, "verdict")
        if parsed is not None:
            return parsed

    log.warning("Could not parse review output as JSON")
    failure_mode = "parse_error"
    summary = f"Could not parse review output. Raw length: {len(output)} chars."
    if output.startswith("Timed out after "):
        failure_mode = "timeout"
        summary = output.strip()
    elif output.startswith("Stale after "):
        failure_mode = "stale_timeout"
        summary = output.strip()
    return {
        "verdict": "parse_error",
        "issues": [],
        "summary": summary,
        "failure_mode": failure_mode,
        "raw_excerpt": output[:1000],
    }


def parse_spec_output(output: str) -> dict:
    """Parse spec compliance output."""
    for candidate in _structured_output_candidates(output, "compliance"):
        parsed = _parse_expected_json(candidate, "compliance")
        if parsed is not None:
            return parsed

    log.warning("Could not parse spec compliance output")
    return {
        "compliance": "parse_error",
        "requirements": [],
        "missing_items": [],
        "summary": f"Could not parse output. Raw length: {len(output)} chars.",
    }


def save_raw_review_output(branch: str, ts: str, output: str) -> str:
    """Persist raw reviewer output to help debug parse failures."""
    raw_path = LOG_DIR / f"reviewraw_{branch.replace('/', '_')}_{ts}.txt"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(output)
    return str(raw_path)


def normalize_review_result(review: dict, spec_missing_items: list[str] | None = None) -> dict:
    """Apply the same review normalization rules in every review path."""
    normalized = dict(review or {})
    normalized.setdefault("issues", [])
    normalized.setdefault("summary", "")

    if normalized.get("verdict") == "pass" and normalized["issues"]:
        normalized["verdict"] = "needs_fixes"
        normalized["summary"] = (
            normalized.get("summary", "") + " (promoted to needs_fixes because review issues remain)"
        ).strip()

    if spec_missing_items and normalized.get("verdict") != "parse_error":
        existing = {
            issue.get("description", "")
            for issue in normalized["issues"]
            if isinstance(issue, dict)
        }
        injected = 0
        for item in spec_missing_items:
            description = f"SPEC GAP: {item}"
            if description in existing:
                continue
            normalized["issues"].append(
                {
                    "severity": "major",
                    "file": "_review_spec.txt",
                    "description": description,
                    "suggestion": "Implement the missing spec item and add/adjust tests if required.",
                }
            )
            injected += 1
        if injected:
            normalized["verdict"] = "needs_fixes"
            normalized["summary"] = (
                normalized.get("summary", "") + " (promoted to needs_fixes because spec gaps remain)"
            ).strip()

    return normalized


def phase_review_with_retries(
    branch_config: dict,
    base: str,
    review_dir: str,
    config: dict | None = None,
    spec_missing_items: list[str] | None = None,
    retry_label: str = "Review",
) -> dict:
    """Run review with retry handling and normalization."""
    branch = branch_config["name"]
    review = phase_review(branch_config, base, review_dir, config)

    if review["verdict"] == "parse_error":
        for retry in range(1, 3):
            log.warning(f"  {retry_label} parse error for '{branch}', retrying ({retry}/2)...")
            review = phase_review(branch_config, base, review_dir, config)
            if review["verdict"] != "parse_error":
                break
        if review["verdict"] == "parse_error":
            log.error(f"  {retry_label} parse error persisted after 2 retries for '{branch}', leaving review unresolved")
            review["summary"] = (
                review.get("summary", "") + f" ({retry_label.lower()} parse error persisted after retries)"
            ).strip()

    return normalize_review_result(review, spec_missing_items)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Prompt templates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROMPT_BUILD_PROMPT = """You are Claude, acting as a technical architect and prompt engineer.

The user has provided these requirements for a feature/project:

USER REQUIREMENTS:
{user_requirements}

PROJECT CONTEXT:
- Branch: {branch}
- Project directory: {directory}

YOUR TASK:
Build a complete, detailed technical spec/prompt that a code-writing AI (Codex) will use
to implement this feature. The spec must be thorough enough that Codex can build it
without asking questions.

Your spec MUST include:
1. OVERVIEW: What is being built and why
2. REQUIREMENTS: Numbered list of every feature/behavior expected
3. TECHNICAL DESIGN:
   - File structure and where new files go
   - Database schema changes (if any)
   - API endpoints with request/response shapes (if any)
   - UI components and their behavior (if any)
   - Integration points with existing code
4. EDGE CASES: What should happen in error scenarios
5. TESTING REQUIREMENTS: What tests must be written
   - Unit tests for each function/endpoint
   - Integration tests for workflows
   - Edge case tests
6. ACCEPTANCE CRITERIA: How to verify the feature works correctly
7. OUT OF SCOPE: What this feature explicitly does NOT include

FORMAT:
Write the spec as a clean Markdown document. Be specific — include function names,
file paths, data shapes, and expected behaviors. Do not be vague.

RULES:
- Do NOT write any code. Spec only.
- Do NOT leave placeholder sections. Every section must have real content.
- If the user requirements are vague, make reasonable assumptions and document them.
- Think about security implications and include them in requirements.
- Think about performance implications for large datasets.

Write the complete spec now.
"""

PROMPT_REVIEW_PROMPT = """You are Codex, acting as a spec reviewer and gap analyst.

You have been given a technical spec that YOU will later need to implement.
Before you write any code, review the spec for completeness and flag any gaps.

THE SPEC TO REVIEW:
Read the file _review_spec.txt in the current directory. It contains the full spec.

ORIGINAL USER REQUIREMENTS (what was asked for):
{user_requirements}

YOUR TASK:
Review the spec critically. You are the one who has to build this — so flag anything
that would block you or leave you guessing during implementation.

Check for:
1. MISSING REQUIREMENTS: Things the user asked for that the spec doesn't cover
2. AMBIGUOUS SECTIONS: Parts where you wouldn't know what to build
3. MISSING TECHNICAL DETAILS: Undefined data shapes, unclear API contracts, missing schemas
4. MISSING ERROR HANDLING: What happens when things fail?
5. MISSING TEST CASES: Are the testing requirements specific enough?
6. DEPENDENCY GAPS: Does the spec assume libraries/services that aren't mentioned?
7. SECURITY GAPS: Auth, validation, injection risks not addressed
8. CONTRADICTIONS: Parts of the spec that conflict with each other

Output your review as JSON with this EXACT structure:

```json
{{
    "verdict": "approved" or "needs_revision",
    "completeness_pct": 85,
    "gaps": [
        {{
            "section": "Which part of the spec",
            "type": "missing" or "ambiguous" or "contradictory" or "incomplete",
            "description": "What is wrong or missing",
            "suggestion": "What should be added or clarified"
        }}
    ],
    "strengths": ["What the spec does well"],
    "summary": "Overall assessment"
}}
```

RULES:
- Only flag REAL gaps that would block or confuse implementation.
- Do NOT flag style or formatting preferences.
- If the spec is complete and implementable, return {{"verdict": "approved", "gaps": [], ...}}.
- Your response MUST contain a JSON code block.
- Do NOT modify any files. Review only.
"""

PROMPT_REVISION_PROMPT = """You are Claude, revising a technical spec based on Codex's feedback.

ORIGINAL SPEC:
Read the file _review_spec.txt in the current directory.

CODEX'S FEEDBACK (gaps found):
{gaps_json}

ORIGINAL USER REQUIREMENTS:
{user_requirements}

YOUR TASK:
1. Read the original spec and Codex's feedback carefully.
2. Address EVERY gap Codex identified.
3. Rewrite the spec with all gaps filled — do not just append notes.
4. Keep everything Codex said was strong.
5. Output the COMPLETE revised spec as a Markdown document.

RULES:
- Output ONLY the revised spec. No commentary before or after.
- Do NOT write any code. Spec only.
- Every gap must be resolved with specific, implementable content.
"""

REVIEW_PROMPT = """You are reviewing code changes on branch '{branch}' (diff from '{base}').

INSTRUCTIONS:
1. If the file _review_spec.txt exists in the current directory, read it first. It contains the original scope/prompt.
2. Read the file _review_diff.txt in the current directory. It contains the full git diff.
3. Use the current working tree to inspect the actual implementation files referenced by the diff when needed.
4. Analyze the changes carefully for:
   - Bugs, logic errors, incorrect implementations
   - Security vulnerabilities
   - Missing error handling
   - Type errors or incorrect annotations
   - Import errors or missing dependencies
   - Broken API contracts (request/response shapes)
   - React/Next.js anti-patterns (frontend code)
   - SQLAlchemy/FastAPI anti-patterns (backend code)
   - Missing or broken tests
   - Requested scope that is still missing or only partially implemented
   - Merge conflict artifacts (<<<<<<< ======= >>>>>>>)
5. Output your review as JSON with this EXACT structure:

```json
{{
    "verdict": "pass" or "needs_fixes",
    "scope_status": "covered" or "partial" or "missing",
    "issues": [
        {{
            "severity": "critical" or "major" or "minor",
            "file": "path/to/file",
            "line": 42,
            "description": "What is wrong",
            "suggestion": "How to fix it"
        }}
    ],
    "summary": "Brief overall assessment"
}}
```

RULES:
- Only flag REAL issues that cause bugs, crashes, or incorrect behavior.
- Do NOT flag style preferences, naming, or formatting.
- If a requested feature is absent, incomplete, or wired incorrectly, that is a REAL issue.
- Treat missing tests for new logic, endpoints, calculations, filters, exports, and UI interactions as REAL issues.
- If code is correct and functional, return {{"verdict": "pass", "issues": [], "summary": "..."}}.
- Your response MUST contain a JSON code block.
- Do NOT modify any files. Review only.
"""

FIX_PROMPT = """You are fixing code issues on branch '{branch}'.

CONTEXT:
1. Read the file _review_spec.txt in the current directory -- it contains the ORIGINAL SPEC (what was being built and why).
2. Read the file _review_diff.txt in the current directory -- it contains the CURRENT DIFF (code changes on this branch).
3. Read the file _review_issues.json in the current directory -- it contains the CODE REVIEW ISSUES to fix.

INSTRUCTIONS:
1. Read ALL THREE files above first to understand the full context.
2. Fix ONLY the issues listed in _review_issues.json. Do not refactor unrelated code.
3. For each issue, open the source file, find the problem, and apply the fix.
4. After fixing all issues, stage and commit with message:
   "fix: address review feedback for {branch}"
5. Do NOT push. Just commit locally.
6. If an issue is invalid (file doesn't exist, etc.), skip it.

Fix all issues now.
"""

CONFLICT_PROMPT = """You are resolving merge conflicts on branch '{base}'.

After merging '{branch}', these files have conflicts:
{conflict_files}

INSTRUCTIONS:
1. Open each conflicted file.
2. Resolve all conflict markers (<<<<<<< ======= >>>>>>>).
3. Keep changes from BOTH sides where possible.
4. If truly conflicting, prefer the feature branch changes.
5. Stage all resolved files with `git add`.
6. Commit with: "merge: resolve conflicts merging {branch}"
7. Do NOT push.

Resolve all conflicts now.
"""

SPEC_COMPLIANCE_PROMPT = """You are verifying that code changes on branch '{branch}' actually implement what was requested.

ORIGINAL SPEC / PROMPT (what was asked):
Read the file _review_spec.txt in the current directory. It contains the original prompt/spec.

ACTUAL IMPLEMENTATION (what was built):
Read the file _review_diff.txt in the current directory. It contains the git diff of all changes.

INSTRUCTIONS:
1. Read BOTH files carefully.
2. Use the current working tree to inspect the actual implementation files referenced by the diff when needed.
3. Compare the spec requirements against the actual implementation.
3. For each requirement in the spec, check:
   - Was it implemented at all?
   - Was it implemented correctly and completely?
   - Does it match the spec's expected behavior?
   - Are there missing pieces (endpoints, UI components, database fields, etc.)?
4. Treat required automated tests and manual verification steps from the spec as first-class requirements.
5. Output your verification as JSON with this EXACT structure:

```json
{{
    "compliance": "full" or "partial" or "minimal" or "none",
    "completion_pct": 85,
    "requirements": [
        {{
            "requirement": "Brief description of what was asked",
            "status": "implemented" or "partial" or "missing" or "incorrect",
            "details": "What was done or what's missing",
            "fix_needed": "What needs to be built/fixed (null if implemented)"
        }}
    ],
    "missing_items": [
        "List of specific things that were asked for but not built"
    ],
    "summary": "Overall assessment of spec compliance"
}}
```

RULES:
- Be thorough -- check EVERY requirement in the spec.
- "partial" means started but incomplete. "missing" means not attempted.
- "incorrect" means built but doesn't match what was asked.
- Missing tests for required logic count against compliance.
- Focus on FUNCTIONALITY, not code style.
- Do NOT modify any files. Verification only.
"""

TEST_FAILURE_PROMPT = """Tests failed on branch '{branch}'.

The following test failures were detected:
{failures_json}

INSTRUCTIONS:
1. Read each failure carefully -- look at the test file, test name, and error message.
2. Open the SOURCE files (not the test files) and fix the bugs causing the failures.
3. If a test itself is wrong (testing the wrong behavior), fix the test instead.
4. After fixing, stage and commit with message:
   "fix: resolve test failures for {branch}"
5. Do NOT push. Just commit locally.

Fix all test failures now.
"""

SPEC_FIX_PROMPT = """You are completing missing or incorrect implementations on branch '{branch}'.

The original spec asked for specific features. A compliance check found these gaps:

{gaps_json}

ORIGINAL SPEC (for reference):
Read the file _review_spec.txt in the current directory for the full original requirements.

INSTRUCTIONS:
1. Implement ONLY the missing/incomplete items listed above.
2. Follow the patterns already established in the codebase.
3. For each gap:
   - If status is "missing": build it from scratch per the spec.
   - If status is "partial": complete the missing pieces.
   - If status is "incorrect": fix it to match the spec.
4. After implementing everything, stage and commit with message:
   "feat: complete spec requirements for {branch}"
5. Do NOT push. Just commit locally.

Build the missing features now.
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Core phases
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def phase_build_prompt(
    branch_config: dict,
    config: dict | None = None,
) -> str:
    """Phase 0.5: Claude builds the technical spec from user requirements."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    user_requirements = branch_config.get("user_requirements", "")
    prompt_file = branch_config.get("prompt_file", "")

    if not user_requirements:
        if prompt_file and os.path.exists(prompt_file):
            log.info(f"  Prompt file already exists for '{branch}', skipping build")
            return prompt_file
        log.warning(f"  No user_requirements for '{branch}' and no existing prompt_file, skipping")
        return ""

    log.info(f"{'='*60}")
    log.info(f"PROMPT BUILD: {branch}  (builder=claude)")
    log.info(f"{'='*60}")
    log.info(f"  User requirements: {user_requirements[:200]}")

    prompt = PROMPT_BUILD_PROMPT.format(
        user_requirements=user_requirements,
        branch=branch,
        directory=directory,
    )

    build_timeout = scaled_timeout(300, len(user_requirements), max_timeout=900)
    output = run_claude(
        prompt,
        directory,
        timeout=build_timeout,
        idle_timeout=scaled_idle_timeout(build_timeout),
        log_label=f"claude prompt-build {branch}",
    )

    # Save the generated spec
    if not prompt_file:
        prompt_file = os.path.join(directory, "PROMPT.md")
        branch_config["prompt_file"] = prompt_file

    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(output)
    log.info(f"  Spec written to {prompt_file} ({len(output):,} chars)")

    # Save log
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"prompt_build_{branch.replace('/', '_')}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "branch": branch,
                "builder_model": "claude",
                "user_requirements": user_requirements,
                "spec_length": len(output),
                "prompt_file": prompt_file,
                "timestamp": ts,
            },
            f,
            indent=2,
        )

    return prompt_file


def phase_review_prompt(
    branch_config: dict,
    config: dict | None = None,
) -> dict:
    """Phase 0.6: Codex reviews Claude's spec for gaps before writing code."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    user_requirements = branch_config.get("user_requirements", "")
    prompt_file = branch_config.get("prompt_file", "")

    if not prompt_file or not os.path.exists(prompt_file):
        log.info(f"  No prompt_file for '{branch}', skipping prompt review")
        return {"verdict": "approved", "gaps": [], "summary": "No spec to review."}

    log.info(f"{'='*60}")
    log.info(f"PROMPT REVIEW: {branch}  (reviewer=codex)")
    log.info(f"{'='*60}")

    # Write spec for Codex to read
    with open(prompt_file, "r", encoding="utf-8") as f:
        spec_content = f.read()
    write_prompt_file(directory, "_review_spec.txt", spec_content)

    prompt = PROMPT_REVIEW_PROMPT.format(
        user_requirements=user_requirements or "(see spec file)",
    )

    review_timeout = scaled_timeout(300, len(spec_content), max_timeout=900)
    output = run_codex(
        prompt,
        directory,
        timeout=review_timeout,
        idle_timeout=scaled_idle_timeout(review_timeout),
        log_label=f"codex prompt-review {branch}",
    )

    cleanup_file(os.path.join(directory, "_review_spec.txt"))

    # Parse Codex's review
    result = {"verdict": "approved", "gaps": [], "summary": ""}
    for candidate in _structured_output_candidates(output, "verdict"):
        parsed = _parse_expected_json(candidate, "verdict")
        if parsed is not None:
            result = parsed
            break

    # Save log
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"prompt_review_{branch.replace('/', '_')}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "branch": branch,
                "reviewer_model": "codex",
                "result": result,
                "raw_excerpt": output[:2000],
                "timestamp": ts,
            },
            f,
            indent=2,
        )

    gaps = result.get("gaps", [])
    verdict = result.get("verdict", "unknown")
    log.info(f"  Verdict: {verdict}  |  Gaps: {len(gaps)}")
    for gap in gaps[:10]:
        log.info(f"    [{gap.get('type', '?')}] {gap.get('section', '?')}: {gap.get('description', '?')[:80]}")

    return result


def phase_revise_prompt(
    branch_config: dict,
    prompt_review: dict,
    config: dict | None = None,
) -> str:
    """Phase 0.7: Claude revises the spec based on Codex's gap feedback."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    user_requirements = branch_config.get("user_requirements", "")
    prompt_file = branch_config.get("prompt_file", "")

    gaps = prompt_review.get("gaps", [])
    if not gaps:
        log.info(f"  No gaps found for '{branch}', spec is approved")
        return prompt_file

    log.info(f"{'='*60}")
    log.info(f"PROMPT REVISION: {branch}  ({len(gaps)} gaps, reviser=claude)")
    log.info(f"{'='*60}")

    # Write current spec for Claude to read
    with open(prompt_file, "r", encoding="utf-8") as f:
        spec_content = f.read()
    write_prompt_file(directory, "_review_spec.txt", spec_content)

    gaps_json = json.dumps(gaps, indent=2)
    prompt = PROMPT_REVISION_PROMPT.format(
        gaps_json=gaps_json,
        user_requirements=user_requirements or "(see spec file)",
    )

    revision_timeout = scaled_timeout(300, len(spec_content) + len(gaps_json), max_timeout=900)
    output = run_claude(
        prompt,
        directory,
        timeout=revision_timeout,
        idle_timeout=scaled_idle_timeout(revision_timeout),
        log_label=f"claude prompt-revision {branch}",
    )

    cleanup_file(os.path.join(directory, "_review_spec.txt"))

    # Overwrite spec with revised version
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(output)
    log.info(f"  Revised spec written to {prompt_file} ({len(output):,} chars)")

    # Save log
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"prompt_revision_{branch.replace('/', '_')}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "branch": branch,
                "reviser_model": "claude",
                "gaps_addressed": len(gaps),
                "revised_spec_length": len(output),
                "timestamp": ts,
            },
            f,
            indent=2,
        )

    return prompt_file


def phase_spec_check(
    branch_config: dict,
    base: str,
    review_dir: str,
    config: dict | None = None,
) -> dict:
    """Verify that implementation matches the original spec/prompt."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    prompt_file = branch_config.get("prompt_file", "")
    author = branch_config["author_model"]
    reviewer = get_reviewer_model(branch_config, config)

    if not prompt_file or not os.path.exists(prompt_file):
        log.info(f"  No prompt_file for '{branch}', skipping spec check")
        return {"compliance": "skipped", "requirements": [], "summary": "No spec provided."}

    log.info(f"{'='*60}")
    log.info(f"SPEC CHECK: {branch}  (verifier={reviewer})")
    log.info(f"{'='*60}")

    git(f"checkout {branch}", cwd=directory)
    git(f"pull origin {branch}", cwd=directory, timeout=60)

    diff = git_diff(directory, base)
    with open(prompt_file, "r", encoding="utf-8") as f:
        spec = f.read()

    log.info(f"  Spec size: {len(spec):,} chars  |  Diff size: {len(diff):,} chars")

    write_prompt_file(directory, "_review_spec.txt", spec)
    write_prompt_file(directory, "_review_diff.txt", diff)

    prompt = SPEC_COMPLIANCE_PROMPT.format(branch=branch)
    spec_timeout = scaled_timeout(420, len(diff) + len(spec), max_timeout=1800)
    output = run_model(
        reviewer,
        prompt,
        directory,
        timeout=spec_timeout,
        idle_timeout=scaled_idle_timeout(spec_timeout),
        log_label=f"{reviewer} spec-check {branch}",
    )

    git("checkout -- .", cwd=directory)
    cleanup_file(os.path.join(directory, "_review_spec.txt"))
    cleanup_file(os.path.join(directory, "_review_diff.txt"))

    result = parse_spec_output(output)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"spec_{branch.replace('/', '_')}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "branch": branch,
                "verifier_model": reviewer,
                "result": result,
                "raw_excerpt": output[:2000],
                "timestamp": ts,
            },
            f,
            indent=2,
        )

    compliance = result.get("compliance", "unknown")
    pct = result.get("completion_pct", "?")
    missing = result.get("missing_items", [])
    log.info(f"  Compliance: {compliance}  |  Completion: {pct}%")
    if missing:
        log.info("  Missing items:")
        for item in missing[:10]:
            log.info(f"    - {item[:100]}")

    return result


def phase_spec_fix(branch_config: dict, spec_result: dict) -> bool:
    """Fix missing/incomplete spec items using the original model."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    author = branch_config["author_model"]
    prompt_file = branch_config.get("prompt_file", "")

    gaps = [
        r for r in spec_result.get("requirements", [])
        if r.get("status") in ("missing", "partial", "incorrect")
    ]
    if not gaps:
        gaps = [
            {
                "requirement": item,
                "status": "missing",
                "details": "Derived from spec_result.missing_items",
                "fix_needed": item,
            }
            for item in spec_result.get("missing_items", [])
        ]

    if not gaps:
        log.info(f"  No spec gaps for '{branch}'")
        return True

    log.info(f"{'='*60}")
    log.info(f"SPEC FIX: {branch}  ({len(gaps)} gaps, fixer={author})")
    log.info(f"{'='*60}")

    git(f"checkout {branch}", cwd=directory)

    if prompt_file and os.path.exists(prompt_file):
        import shutil as _shutil
        dest = os.path.join(directory, "_review_spec.txt")
        _shutil.copy2(prompt_file, dest)

    before = git_commit_count(directory)

    gaps_json = json.dumps(gaps, indent=2)
    prompt = SPEC_FIX_PROMPT.format(branch=branch, gaps_json=gaps_json)
    spec_fix_timeout = scaled_timeout(900, len(gaps_json), max_timeout=2400)
    output = run_model(
        author,
        prompt,
        directory,
        timeout=spec_fix_timeout,
        idle_timeout=scaled_idle_timeout(spec_fix_timeout),
        log_label=f"{author} spec-fix {branch}",
    )

    cleanup_file(os.path.join(directory, "_review_spec.txt"))

    after = git_commit_count(directory)
    new_commits = after - before

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"specfix_{branch.replace('/', '_')}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "branch": branch,
                "fixer_model": author,
                "gaps_sent": gaps,
                "new_commits": new_commits,
                "raw_excerpt": output[:2000],
                "timestamp": ts,
            },
            f,
            indent=2,
        )

    log.info(f"  Spec fix produced {new_commits} new commit(s)")
    return new_commits > 0


def phase_review(
    branch_config: dict,
    base: str,
    review_dir: str,
    config: dict | None = None,
) -> dict:
    """Review a single branch using the configured reviewer model."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    author = branch_config["author_model"]
    reviewer = get_reviewer_model(branch_config, config)

    log.info(f"{'='*60}")
    log.info(f"REVIEW: {branch}  (by {author}, reviewed by {reviewer})")
    log.info(f"{'='*60}")

    git(f"checkout {branch}", cwd=directory)
    git(f"pull origin {branch}", cwd=directory, timeout=60)

    diff = git_diff(directory, base)
    commits = git_log(directory, base)

    if not diff.strip() or "FULL DIFF:\n" == diff.strip()[-len("FULL DIFF:\n"):]:
        log.info(f"  No changes on '{branch}', skipping")
        return {"verdict": "pass", "issues": [], "summary": "No changes."}

    log.info(f"  Commits: {commits[:200]}")
    log.info(f"  Diff size: {len(diff):,} chars")

    write_prompt_file(directory, "_review_diff.txt", diff)
    prompt_file = branch_config.get("prompt_file", "")
    if prompt_file and os.path.exists(prompt_file):
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                write_prompt_file(directory, "_review_spec.txt", f.read())
        except OSError:
            pass

    prompt = REVIEW_PROMPT.format(branch=branch, base=base)

    review_timeout = scaled_timeout(300, len(diff), max_timeout=2400)
    output = run_model(
        reviewer,
        prompt,
        directory,
        timeout=review_timeout,
        idle_timeout=scaled_idle_timeout(review_timeout),
        log_label=f"{reviewer} review {branch}",
    )

    git("checkout -- .", cwd=directory)

    cleanup_file(os.path.join(directory, "_review_diff.txt"))
    cleanup_file(os.path.join(directory, "_review_spec.txt"))

    review = parse_review_output(output)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"review_{branch.replace('/', '_')}_{ts}.json"
    log_payload = {
        "branch": branch,
        "author_model": author,
        "reviewer_model": reviewer,
        "commits": commits,
        "review": review,
        "raw_output_length": len(output),
        "raw_excerpt": output[:2000],
        "timestamp": ts,
    }
    if review.get("verdict") == "parse_error":
        log_payload["raw_output_file"] = save_raw_review_output(branch, ts, output)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            log_payload,
            f,
            indent=2,
        )

    verdict = review.get("verdict", "unknown")
    issues = review.get("issues", [])
    log.info(f"  Verdict: {verdict}  |  Issues: {len(issues)}")
    for iss in issues:
        log.info(f"    [{iss.get('severity', '?')}] {iss.get('file', '?')}: {iss.get('description', '?')[:80]}")

    return review


def _auto_detect_test_commands(diff: str) -> list[str]:
    """Detect which test suites to run based on changed files in diff."""
    commands = []
    if "services/api/" in diff:
        commands.append("cd services/api && python3 -m pytest tests/ -x --tb=short -q")
    if "services/pipeline/" in diff:
        commands.append("cd services/pipeline && python3 -m pytest tests/ -x --tb=short -q")
    if "services/web/" in diff:
        commands.append("cd services/web && npm run test -- --run")
    return commands


def _parse_test_output(output: str) -> dict:
    """Parse test runner output for pass/fail counts and failure details."""
    failures = []
    passed = 0
    failed = 0

    m = re.search(r"(\d+) passed", output)
    if m:
        passed += int(m.group(1))
    m = re.search(r"(\d+) failed", output)
    if m:
        failed += int(m.group(1))

    m = re.search(r"Tests\s+(\d+)\s+passed", output)
    if m:
        passed += int(m.group(1))
    m = re.search(r"Tests\s+(\d+)\s+failed", output)
    if m:
        failed += int(m.group(1))

    for m in re.finditer(r"FAILED\s+(\S+)", output):
        failures.append(m.group(1))

    for m in re.finditer(r"((?:FAILED|ERROR)\s+\S+.*?)(?=\n(?:FAILED|ERROR|=|$))", output, re.DOTALL):
        desc = m.group(1).strip()[:500]
        if desc not in [f.get("description", "") for f in failures if isinstance(f, dict)]:
            failures.append({"test": desc.split()[1] if len(desc.split()) > 1 else desc[:80], "description": desc})

    normalized = []
    for f in failures:
        if isinstance(f, str):
            normalized.append({"test": f, "description": f})
        else:
            normalized.append(f)

    parsed_counts = passed > 0 or failed > 0
    return {
        "passed": passed,
        "failed": failed,
        "failures": normalized,
        "parsed_counts": parsed_counts,
        "all_passed": failed == 0 and not normalized and passed > 0,
    }


def _classify_unparsed_test_failure(output: str) -> str:
    """Best-effort classification for non-parseable failing test commands."""
    lower = output.lower()
    environment_markers = [
        "node_modules",
        "vitest is not installed",
        "vitest is not recognized",
        "cannot find module",
        "module not found",
        "no module named",
        "database",
        "connection refused",
        "could not connect",
        "econnrefused",
        "getaddrinfo",
        "service unavailable",
        "timed out after",
        "not implementederror",
        "not implemented",
        "localhost:5432",
    ]
    if any(marker in lower for marker in environment_markers):
        return "environment_failure"
    return "unknown_failure"


def phase_test_check(
    branch_config: dict,
    base: str,
) -> dict:
    """Run tests on a branch and return results."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    test_commands = branch_config.get("test_commands", [])

    log.info(f"{'='*60}")
    log.info(f"TEST CHECK: {branch}")
    log.info(f"{'='*60}")

    git(f"checkout {branch}", cwd=directory)

    if not test_commands:
        diff = git_diff(directory, base)
        test_commands = _auto_detect_test_commands(diff)
        if test_commands:
            log.info(f"  Auto-detected {len(test_commands)} test command(s)")
        else:
            log.info(f"  No test commands configured or detected, skipping")
            return {"passed": True, "summary": "No tests to run.", "failures": []}

    all_results = []
    overall_passed = True
    uncounted_passes = 0

    for cmd in test_commands:
        log.info(f"  Running: {cmd}")
        try:
            rc, stdout, stderr = run_cmd(cmd, cwd=directory, timeout=300, shell=True)
            output = (stdout or "") + (stderr or "")
            result = _parse_test_output(output)
            result["command"] = cmd
            result["returncode"] = rc
            result["status"] = "fail"

            if rc == 0 and result["failed"] == 0 and not result["failures"]:
                if result.get("parsed_counts"):
                    result["status"] = "pass"
                    result["all_passed"] = True
                    log.info(f"  PASSED: {cmd} ({result['passed']} tests)")
                else:
                    result["status"] = "pass_unknown_count"
                    result["all_passed"] = True
                    result["summary_note"] = "Command exited with rc=0 but emitted no parseable pass/fail counts."
                    uncounted_passes += 1
                    log.warning(f"  PASSED (uncounted): {cmd} (rc=0, counts not parsed)")
            else:
                overall_passed = False
                if rc != 0 and not result["failures"]:
                    excerpt = re.sub(r"\s+", " ", output.strip())[:500] or "No stdout/stderr captured."
                    result["failures"].append(
                        {
                            "test": "command_failed",
                            "failure_type": _classify_unparsed_test_failure(output),
                            "description": f"Command exited with rc={rc}. Output excerpt: {excerpt}",
                        }
                    )
                log.warning(f"  FAILED: {cmd} (rc={rc}, {result['failed']} failures)")
        except Exception as e:
            log.error(f"  ERROR running {cmd}: {e}")
            result = {
                "command": cmd,
                "returncode": -1,
                "all_passed": False,
                "status": "error",
                "passed": 0,
                "failed": 0,
                "failures": [{"test": "runner_error", "error": str(e)}],
            }
            overall_passed = False

        all_results.append(result)

    total_passed = sum(r["passed"] for r in all_results)
    total_failed = sum(r["failed"] for r in all_results)
    all_failures = []
    for r in all_results:
        all_failures.extend(r.get("failures", []))

    summary = f"{total_passed} passed, {total_failed} failed across {len(test_commands)} suite(s)"
    if uncounted_passes:
        summary += f"; {uncounted_passes} suite(s) passed with rc=0 but emitted no parseable counts"

    result = {
        "passed": overall_passed,
        "summary": summary,
        "failures": all_failures,
        "suites": all_results,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"tests_{branch.replace('/', '_')}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({"branch": branch, "result": result, "timestamp": ts}, f, indent=2)

    log.info(f"  Tests: {summary}")
    return result


def _truncate_for_file(content: str, budget: int, label: str) -> str:
    """Truncate content to fit within a character budget."""
    if len(content) <= budget:
        return content
    return content[:budget] + f"\n\n... {label} TRUNCATED (>{budget} chars) ..."


def phase_fix(branch_config: dict, review: dict, round_num: int, config: dict | None = None) -> bool:
    """Fix issues using the original (or escalated) model."""
    branch = branch_config["name"]
    directory = branch_config["directory"]
    author = branch_config["author_model"]
    prompt_file = branch_config.get("prompt_file", "")
    base = (config or {}).get("base_branch", "main")

    critical_major = [
        i for i in review.get("issues", [])
        if i.get("severity") in ("critical", "major")
    ]

    if not critical_major:
        log.info(f"  No critical/major issues on '{branch}', skipping fix")
        return True

    if round_num <= 1:
        fixer = author
    else:
        fixer = get_reviewer_model(branch_config, config)
        log.info(f"  ESCALATING: {fixer} will fix instead of {author}")

    log.info(f"{'='*60}")
    log.info(f"FIX (round {round_num}): {branch}  ({len(critical_major)} issues, fixer={fixer})")
    log.info(f"{'='*60}")

    git(f"checkout {branch}", cwd=directory)

    total_budget = 120_000

    spec_content = "(no spec provided)"
    spec_included = False
    if prompt_file and os.path.exists(prompt_file):
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                spec_content = f.read()
            spec_included = True
            log.info(f"  Loaded spec: {len(spec_content):,} chars from {prompt_file}")
        except Exception as e:
            log.warning(f"  Could not read spec file: {e}")

    spec_budget = int(total_budget * 0.4)
    spec_content = _truncate_for_file(spec_content, spec_budget, "SPEC")

    issues_json = json.dumps(critical_major, indent=2)
    issues_budget = int(total_budget * 0.2)
    issues_json = _truncate_for_file(issues_json, issues_budget, "ISSUES")

    diff_content = git_diff(directory, base)
    diff_budget = total_budget - len(spec_content) - len(issues_json)
    if diff_budget < 2000:
        diff_content = "(diff omitted -- spec and issues consumed the context budget)"
    else:
        diff_content = _truncate_for_file(diff_content, diff_budget, "DIFF")
    log.info(f"  Context sizes -- spec: {len(spec_content):,}  issues: {len(issues_json):,}  diff: {len(diff_content):,}")

    write_prompt_file(directory, "_review_spec.txt", spec_content)
    write_prompt_file(directory, "_review_diff.txt", diff_content)
    write_prompt_file(directory, "_review_issues.json", issues_json)

    prompt = FIX_PROMPT.format(branch=branch)

    before = git_commit_count(directory)

    fix_timeout = scaled_timeout(600, len(spec_content) + len(issues_json) + len(diff_content), max_timeout=2400)
    output = run_model(
        fixer,
        prompt,
        directory,
        timeout=fix_timeout,
        idle_timeout=scaled_idle_timeout(fix_timeout),
        log_label=f"{fixer} fix {branch}",
    )

    after = git_commit_count(directory)
    new_commits = after - before

    cleanup_file(os.path.join(directory, "_review_spec.txt"))
    cleanup_file(os.path.join(directory, "_review_diff.txt"))
    cleanup_file(os.path.join(directory, "_review_issues.json"))

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"fix_{branch.replace('/', '_')}_r{round_num}_{ts}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "branch": branch,
                "fixer_model": fixer,
                "round": round_num,
                "issues_sent": critical_major,
                "spec_included": spec_included,
                "diff_size": len(diff_content),
                "prompt_size": len(prompt),
                "new_commits": new_commits,
                "raw_excerpt": output[:2000],
                "timestamp": ts,
            },
            f,
            indent=2,
        )

    log.info(f"  Fix produced {new_commits} new commit(s)")
    return new_commits > 0


def phase_merge(config: dict) -> dict[str, str]:
    """Merge all reviewed branches into base."""
    base = config["base_branch"]
    merge_dir = config["merge_directory"]
    branches = config["branches"]

    log.info(f"\n{'='*60}")
    log.info(f"MERGE PHASE: {len(branches)} branches -> {base}")
    log.info(f"{'='*60}")

    git(f"checkout {base}", cwd=merge_dir)
    git(f"pull origin {base}", cwd=merge_dir, timeout=60)
    git("fetch --all", cwd=merge_dir, timeout=60)

    results: dict[str, str] = {}

    for bc in branches:
        branch = bc["name"]
        src_dir = bc["directory"]

        log.info(f"\n  Merging '{branch}'...")

        git(f"push origin {branch}", cwd=src_dir, timeout=60)
        git(f"fetch origin {branch}", cwd=merge_dir, timeout=60)

        rc, out = git(f"merge origin/{branch} --no-edit", cwd=merge_dir, timeout=60)

        if rc == 0:
            log.info(f"  OK  '{branch}' merged cleanly")
            results[branch] = "clean"
            continue

        conflicts = git_conflict_files(merge_dir)
        if not conflicts:
            log.error(f"  FAIL  '{branch}': {out[:200]}")
            git("merge --abort", cwd=merge_dir)
            results[branch] = f"error: {out[:200]}"
            continue

        log.warning(f"  CONFLICT  '{branch}': {conflicts}")

        prompt = CONFLICT_PROMPT.format(
            base=base, branch=branch, conflict_files=conflicts
        )
        run_claude(prompt, merge_dir, timeout=300)

        remaining = git_conflict_files(merge_dir)
        if remaining:
            log.error(f"  UNRESOLVED  Still conflicts in: {remaining}")
            git("merge --abort", cwd=merge_dir)
            results[branch] = f"unresolved: {remaining}"
        else:
            log.info(f"  OK  Conflicts resolved for '{branch}'")
            results[branch] = "resolved"

    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Report
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_report(
    config: dict,
    reviews: dict,
    fixes: dict,
    merge_results: dict,
    spec_results: dict | None = None,
    test_results: dict | None = None,
) -> str:
    lines = [
        "=" * 70,
        "  REVIEWER AGENT  --  SUMMARY REPORT",
        f"  {datetime.now():%Y-%m-%d %H:%M:%S}",
        "=" * 70,
        "",
    ]

    report_test_status: dict[str, str] = {}
    report_review_status: dict[str, str] = {}

    for bc in config["branches"]:
        branch = bc["name"]
        author = bc["author_model"]
        reviewer = opposite_model(author)

        lines.append(f"-- {branch}  (by {author}, reviewed by {reviewer})")

        if spec_results and branch in spec_results:
            spec = spec_results[branch]
            compliance = spec.get("compliance", "n/a")
            pct = spec.get("completion_pct", "?")
            lines.append(f"   Spec:    {compliance}  ({pct}% complete)")
            for gap in spec.get("missing_items", [])[:5]:
                lines.append(f"     MISSING: {gap[:80]}")

        if test_results and branch in test_results:
            tr = test_results[branch]
            passed = tr.get("passed", False)
            status = "PASS" if passed else "FAIL"
            report_test_status[branch] = "pass" if passed else "fail"
            lines.append(f"   Tests:   {status}  ({tr.get('summary', 'n/a')})")
            for fail in tr.get("failures", [])[:5]:
                test_name = fail.get("test", "?") if isinstance(fail, dict) else str(fail)
                lines.append(f"     FAIL: {test_name[:80]}")
        else:
            report_test_status[branch] = "no_tests"

        rev = reviews.get(branch, {})
        verdict = rev.get("verdict", "n/a")
        issues = rev.get("issues", [])
        summary = rev.get("summary", "")
        report_review_status[branch] = verdict

        lines.append(f"   Review:  {verdict}  ({len(issues)} issues)")
        for iss in issues:
            sev = iss.get("severity", "?")
            desc = iss.get("description", "?")[:80]
            f = iss.get("file", "?")
            lines.append(f"     [{sev}] {f}: {desc}")

        lines.append(f"   Fix:     {fixes.get(branch, 'n/a')}")
        lines.append(f"   Merge:   {merge_results.get(branch, 'n/a')}")
        lines.append(f"   Summary: {summary[:120]}")
        lines.append("")

    any_fail = any(s == "fail" for s in report_test_status.values())
    overall_test = "FAIL" if any_fail else "PASS"
    require_tests = config.get("require_tests_pass", False)
    lines.append(f"  test_status: {overall_test}  (require_tests_pass={require_tests})")
    for branch, ts in report_test_status.items():
        lines.append(f"    {branch}: {ts}")
    lines.append("")

    review_blockers = [b for b, verdict in report_review_status.items() if verdict not in ("pass", "n/a")]
    overall_review = "FAIL" if review_blockers else "PASS"
    lines.append(f"  review_status: {overall_review}")
    for branch, verdict in report_review_status.items():
        lines.append(f"    {branch}: {verdict}")
    if review_blockers:
        lines.append(f"  review_blockers: {', '.join(review_blockers)}")
    lines.append("")

    lines.append("=" * 70)

    merge_dir = config.get("merge_directory", "")
    if merge_dir:
        _, recent = git("log --oneline -10", cwd=merge_dir)
        lines.append("Recent commits (merge target):")
        lines.append(recent)

    lines.append("=" * 70)

    report = "\n".join(lines)

    report_path = LOG_DIR / f"report_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    log.info(f"Report saved: {report_path}")

    json_report_path = LOG_DIR / f"report_{datetime.now():%Y%m%d_%H%M%S}.json"
    structured = {
        "timestamp": datetime.now().isoformat(),
        "test_status": report_test_status,
        "overall_test_status": overall_test,
        "review_status": report_review_status,
        "overall_review_status": overall_review,
        "review_blockers": review_blockers,
        "require_tests_pass": require_tests,
        "reviews": report_review_status,
        "fixes": fixes,
        "merge_results": merge_results,
    }
    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)
    log.info(f"JSON report saved: {json_report_path}")

    return report


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pre-flight checks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def preflight_clean_worktree(directory: str) -> list[str]:
    """Check that the merge directory has no uncommitted changes."""
    issues = []
    rc, out = git("status --porcelain", cwd=directory)
    dirty = [line for line in (out or "").splitlines() if line.strip() and not line.startswith("??")]
    if dirty:
        issues.append(
            f"Merge directory '{directory}' has {len(dirty)} uncommitted change(s). "
            f"Commit or stash before running the reviewer. First 5: "
            + "; ".join(d.strip() for d in dirty[:5])
        )
    return issues


def preflight_alembic_revisions(directory: str) -> list[str]:
    """Scan alembic versions for duplicate revision IDs."""
    issues = []
    versions_dir = os.path.join(directory, "services", "api", "alembic", "versions")
    if not os.path.isdir(versions_dir):
        return issues

    revisions: dict[str, list[str]] = {}
    for fname in os.listdir(versions_dir):
        if not fname.endswith(".py") or fname.startswith("__"):
            continue
        fpath = os.path.join(versions_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("revision") and "=" in line:
                        rev_id = line.split("=", 1)[1].strip().strip('"').strip("'")
                        revisions.setdefault(rev_id, []).append(fname)
                        break
        except Exception:
            pass

    for rev_id, files in revisions.items():
        if len(files) > 1:
            issues.append(
                f"Duplicate Alembic revision '{rev_id}' in {len(files)} files: {', '.join(files)}"
            )
    return issues


def preflight_model_columns(directory: str) -> list[str]:
    """Scan SQLAlchemy models for duplicate column definitions."""
    issues = []
    entities_path = os.path.join(directory, "services", "api", "app", "models", "entities.py")
    if not os.path.isfile(entities_path):
        return issues

    current_class = None
    columns: dict[str, list[str]] = {}

    try:
        with open(entities_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                cls_match = re.match(r"^class\s+(\w+)\(", line)
                if cls_match:
                    current_class = cls_match.group(1)
                    columns[current_class] = []
                    continue

                if current_class and ": Mapped[" in line:
                    col_match = re.match(r"\s+(\w+)\s*:\s*Mapped\[", line)
                    if col_match:
                        col_name = col_match.group(1)
                        if col_name in columns[current_class]:
                            issues.append(
                                f"Duplicate column '{col_name}' in model '{current_class}' "
                                f"at line {line_num} of entities.py"
                            )
                        columns[current_class].append(col_name)
    except Exception:
        pass

    return issues


def phase_preflight(config: dict) -> list[str]:
    """Run all pre-flight checks, return list of issues."""
    log.info(f"\n{'#'*60}")
    log.info("PHASE 0: PRE-FLIGHT CHECKS")
    log.info(f"{'#'*60}")

    all_issues: list[str] = []
    merge_dir = config.get("merge_directory", config["branches"][0]["directory"])

    worktree_issues = preflight_clean_worktree(merge_dir)
    for issue in worktree_issues:
        log.warning(f"  [worktree] {issue}")
    all_issues.extend(worktree_issues)

    dirs_to_check = {merge_dir}
    for bc in config["branches"]:
        dirs_to_check.add(bc["directory"])
    for d in dirs_to_check:
        alembic_issues = preflight_alembic_revisions(d)
        for issue in alembic_issues:
            log.warning(f"  [alembic] {issue}")
        all_issues.extend(alembic_issues)

    for d in dirs_to_check:
        model_issues = preflight_model_columns(d)
        for issue in model_issues:
            log.warning(f"  [model] {issue}")
        all_issues.extend(model_issues)

    if all_issues:
        log.warning(f"  Pre-flight found {len(all_issues)} issue(s)")
    else:
        log.info("  All pre-flight checks passed")

    return all_issues


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Orchestrators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_full(config: dict) -> None:
    """Full pipeline: spec check -> review -> fix -> merge -> report."""
    base = config["base_branch"]
    max_rounds = config.get("max_rounds", 2)
    branches = config["branches"]
    review_dir = config.get("merge_directory", branches[0]["directory"])

    reviews: dict[str, dict] = {}
    spec_results: dict[str, dict] = {}
    fixes: dict[str, str] = {}
    max_test_rounds = config.get("max_test_rounds", max_rounds + 2)

    log.info(f"Starting full pipeline: {len(branches)} branches, max {max_rounds} review rounds, max {max_test_rounds} total rounds")
    log.info(f"Dispatch: Claude builds prompts -> Codex reviews prompts -> Codex writes code -> Claude reviews code")

    # Phase 0: Pre-flight checks
    preflight_issues = phase_preflight(config)
    worktree_blocked = any("[worktree]" in str(i) or "uncommitted" in str(i) for i in preflight_issues)
    if worktree_blocked:
        log.error("ABORTING: merge directory has uncommitted changes. Commit or stash first.")
        return

    # Phase 0.5: Claude builds prompts from user requirements
    has_requirements = any(bc.get("user_requirements") for bc in branches)
    if has_requirements:
        log.info(f"\n{'#'*60}")
        log.info("PHASE 0.5: PROMPT BUILD (Claude)")
        log.info(f"{'#'*60}")

        for bc in branches:
            branch = bc["name"]
            if bc.get("user_requirements"):
                prompt_file = phase_build_prompt(bc, config)

                if prompt_file:
                    # Phase 0.6: Codex reviews the prompt for gaps
                    log.info(f"\n{'#'*60}")
                    log.info("PHASE 0.6: PROMPT REVIEW (Codex)")
                    log.info(f"{'#'*60}")

                    prompt_review = phase_review_prompt(bc, config)

                    if prompt_review.get("verdict") == "needs_revision":
                        # Phase 0.7: Claude revises based on Codex's feedback
                        log.info(f"\n{'#'*60}")
                        log.info("PHASE 0.7: PROMPT REVISION (Claude)")
                        log.info(f"{'#'*60}")

                        phase_revise_prompt(bc, prompt_review, config)

                        # Re-review after revision (one round)
                        log.info(f"  Re-reviewing revised spec...")
                        second_review = phase_review_prompt(bc, config)
                        if second_review.get("verdict") == "needs_revision":
                            remaining_gaps = len(second_review.get("gaps", []))
                            log.warning(
                                f"  Spec still has {remaining_gaps} gap(s) after revision. "
                                f"Proceeding with current spec."
                            )
                        else:
                            log.info(f"  Revised spec approved by Codex")

    # Phase 1: Spec Compliance Check
    has_specs = any(bc.get("prompt_file") for bc in branches)
    if has_specs:
        log.info(f"\n{'#'*60}")
        log.info("PHASE 1: SPEC COMPLIANCE CHECK")
        log.info(f"{'#'*60}")

        for bc in branches:
            branch = bc["name"]
            result = phase_spec_check(bc, base, review_dir, config)
            spec_results[branch] = result

            compliance = result.get("compliance", "skipped")
            missing_items = result.get("missing_items", [])
            if compliance in ("partial", "minimal", "none") or missing_items:
                log.info(f"  Spec gaps found for '{branch}', dispatching fix...")
                success = phase_spec_fix(bc, result)
                if success:
                    git(f"push origin {branch}", cwd=bc["directory"], timeout=60)
                    new_result = phase_spec_check(bc, base, review_dir, config)
                    spec_results[branch] = new_result
                    new_compliance = new_result.get("compliance", "unknown")
                    log.info(f"  After fix: compliance={new_compliance}")

    # Phase 2: Code Quality Review
    log.info(f"\n{'#'*60}")
    log.info("PHASE 2: CODE QUALITY REVIEW")
    log.info(f"{'#'*60}")

    for bc in branches:
        branch = bc["name"]
        review = phase_review_with_retries(
            bc,
            base,
            review_dir,
            config,
            spec_missing_items=spec_results.get(branch, {}).get("missing_items", []),
            retry_label="Review",
        )
        reviews[branch] = review

        if review["verdict"] == "pass":
            fixes[branch] = "not needed"
        elif review["verdict"] == "needs_fixes":
            fixes[branch] = "issues pending"
        elif review["verdict"] == "parse_error":
            fixes[branch] = "review parse error"

    # Phase 2.5: Test Verification
    test_results: dict[str, dict] = {}
    log.info(f"\n{'#'*60}")
    log.info("PHASE 2.5: TEST VERIFICATION")
    log.info(f"{'#'*60}")

    for bc in branches:
        branch = bc["name"]
        t_result = phase_test_check(bc, base)
        test_results[branch] = t_result

        if not t_result["passed"]:
            injected_failures = 0
            skipped_failures = 0
            for failure in t_result.get("failures", []):
                failure_type = failure.get("failure_type", "code_failure")
                if failure_type in ("environment_failure", "unknown_failure"):
                    skipped_failures += 1
                    continue
                test_file = failure.get("test", "unknown")
                desc = failure.get("description", "Test failure")
                issue = {
                    "severity": "critical",
                    "file": test_file,
                    "description": f"TEST FAILURE: {desc}",
                    "suggestion": "Fix the code to make this test pass.",
                }
                if branch not in reviews:
                    reviews[branch] = {"verdict": "needs_fixes", "issues": [], "summary": ""}
                reviews[branch]["issues"].append(issue)
                reviews[branch]["verdict"] = "needs_fixes"
                injected_failures += 1
            if injected_failures:
                log.info(f"  Injected {injected_failures} test failure(s) as critical issues")
            if skipped_failures:
                log.warning(
                    f"  Skipped auto-fix injection for {skipped_failures} non-code test failure(s); "
                    f"branch will remain blocked until manually resolved or reclassified"
                )

    # Phase 3: Fix loop
    review_rounds_used: dict[str, int] = {}

    for round_num in range(1, max_test_rounds + 1):
        needs_fix = []
        for bc in branches:
            branch = bc["name"]
            review = reviews.get(branch, {})
            verdict = review.get("verdict")
            if verdict == "parse_error":
                fixes[branch] = "blocked: review parse error"
                continue
            if verdict != "needs_fixes":
                continue

            review_issues = [i for i in review.get("issues", []) if "TEST FAILURE" not in i.get("description", "")]
            test_issues = [i for i in review.get("issues", []) if "TEST FAILURE" in i.get("description", "")]

            has_review_issues = len(review_issues) > 0
            has_test_failures = len(test_issues) > 0
            branch_review_rounds = review_rounds_used.get(branch, 0)

            if has_review_issues and not has_test_failures and branch_review_rounds >= max_rounds:
                log.error(
                    f"  '{branch}': {len(review_issues)} review issue(s) remain after hitting the review round cap "
                    f"({max_rounds}); leaving branch blocked"
                )
                reviews[branch]["verdict"] = "needs_fixes"
                reviews[branch]["summary"] = (
                    reviews[branch].get("summary", "") + f" (blocked after hitting the {max_rounds}-round review cap)"
                ).strip()
                fixes[branch] = f"blocked after {max_rounds} review rounds"
                continue

            if has_review_issues:
                review_rounds_used[branch] = branch_review_rounds + 1

            needs_fix.append(bc)

        if not needs_fix:
            parse_blockers = [
                bc["name"]
                for bc in branches
                if reviews.get(bc["name"], {}).get("verdict") == "parse_error"
            ]
            if parse_blockers:
                log.error(
                    f"Stopping fix loop with unresolved review parse errors: {', '.join(parse_blockers)}"
                )
                for branch in parse_blockers:
                    fixes[branch] = "blocked: review parse error"
                break
            log.info("All branches passed. No more fixes needed.")
            break

        log.info(f"\n{'#'*60}")
        log.info(f"PHASE 3: FIX ROUND {round_num}/{max_test_rounds}")
        log.info(f"{'#'*60}")

        for bc in needs_fix:
            branch = bc["name"]
            success = phase_fix(bc, reviews[branch], round_num, config)
            fixes[branch] = f"round {round_num}: {'applied' if success else 'no changes'}"

            if success:
                git(f"push origin {branch}", cwd=bc["directory"], timeout=60)
                new_review = phase_review_with_retries(
                    bc,
                    base,
                    review_dir,
                    config,
                    spec_missing_items=spec_results.get(branch, {}).get("missing_items", []),
                    retry_label="Re-review",
                )
                reviews[branch] = new_review

                log.info(f"  Re-running tests after fix round {round_num} for '{branch}'...")
                new_test = phase_test_check(bc, base)
                test_results[branch] = new_test

                if not new_test["passed"]:
                    for failure in new_test.get("failures", []):
                        test_file = failure.get("test", "unknown")
                        desc = failure.get("description", "Test failure")
                        issue = {
                            "severity": "critical",
                            "file": test_file,
                            "description": f"TEST FAILURE: {desc}",
                            "suggestion": "Fix the code to make this test pass.",
                        }
                        reviews[branch].setdefault("issues", []).append(issue)
                        reviews[branch]["verdict"] = "needs_fixes"
                    log.warning(
                        f"  Tests still failing after fix round {round_num}: "
                        f"{new_test.get('summary', '?')}"
                    )

                review_ok = new_review.get("verdict") == "pass"
                tests_ok = new_test.get("passed", True)
                if review_ok and tests_ok:
                    fixes[branch] = f"fixed in round {round_num}"
                elif review_ok and not tests_ok:
                    fixes[branch] = f"round {round_num}: review passed but tests failing"

    # Phase 4: Merge
    merge_results: dict[str, str] = {}

    branch_test_status: dict[str, str] = {}
    for bc in branches:
        branch = bc["name"]
        tr = test_results.get(branch, {})
        if tr.get("passed"):
            branch_test_status[branch] = "pass"
        elif not tr:
            branch_test_status[branch] = "no_tests"
        else:
            branch_test_status[branch] = "fail"

    require_tests = config.get("require_tests_pass", False)

    if config.get("auto_merge", True):
        test_blockers = [
            b for b, s in branch_test_status.items() if s == "fail"
        ]
        review_blockers = [
            bc["name"]
            for bc in branches
            if reviews.get(bc["name"], {}).get("verdict") not in ("pass", "n/a")
        ]
        if review_blockers:
            log.error(
                f"MERGE BLOCKED: {len(review_blockers)} branch(es) still have unresolved review status: "
                f"{', '.join(review_blockers)}"
            )
            for b in review_blockers:
                merge_results[b] = f"blocked: review {reviews.get(b, {}).get('verdict', 'unknown')}"
        elif test_blockers and require_tests:
            log.error(
                f"MERGE BLOCKED: require_tests_pass=true and {len(test_blockers)} branch(es) "
                f"have failing tests: {', '.join(test_blockers)}"
            )
            for b in test_blockers:
                merge_results[b] = "blocked: tests failing"
        else:
            if test_blockers:
                log.warning(
                    f"WARNING: {len(test_blockers)} branch(es) have failing tests "
                    f"({', '.join(test_blockers)}), but require_tests_pass=false -- proceeding with merge. "
                    f"Tests may fail due to missing DB/env on build host."
                )

            dirty_check = preflight_clean_worktree(review_dir)
            if dirty_check:
                log.warning("Merge directory became dirty during review cycle, cleaning...")
                git("checkout -- .", cwd=review_dir)
                git("clean -fd", cwd=review_dir)
            log.info(f"\n{'#'*60}")
            log.info("PHASE 4: MERGE")
            log.info(f"{'#'*60}")
            merge_results = phase_merge(config)
    else:
        log.info("Auto-merge disabled, skipping.")

    # Phase 5: Report
    log.info(f"\n{'#'*60}")
    log.info("PHASE 5: REPORT")
    log.info(f"{'#'*60}")

    report = generate_report(
        config, reviews, fixes, merge_results,
        spec_results=spec_results or None,
        test_results=test_results or None,
    )
    print(report)

    all_clean = all(v in ("clean", "resolved") for v in merge_results.values())
    if all_clean and merge_results:
        merge_dir = config["merge_directory"]
        log.info(f"\nAll branches merged! To push:")
        log.info(f"  cd {merge_dir} && git push origin {base}")


def cmd_review(config: dict) -> None:
    """Review only."""
    base = config["base_branch"]
    branches = config["branches"]
    review_dir = config.get("merge_directory", branches[0]["directory"])

    reviews = {}
    for bc in branches:
        reviews[bc["name"]] = phase_review_with_retries(bc, base, review_dir, config)

    report = generate_report(config, reviews, {}, {})
    print(report)


def cmd_fix(config: dict) -> None:
    """Fix from previously saved review logs."""
    base = config["base_branch"]
    branches = config["branches"]
    review_dir = config.get("merge_directory", branches[0]["directory"])

    reviews = {}
    for bc in branches:
        branch = bc["name"]
        pattern = f"review_{branch.replace('/', '_')}_*.json"
        matching = sorted(LOG_DIR.glob(pattern), reverse=True)
        if matching:
            with open(matching[0]) as f:
                data = json.load(f)
                reviews[branch] = data.get("review", {})
                reviews[branch] = normalize_review_result(reviews[branch])
                log.info(f"  Loaded review for '{branch}' from {matching[0].name}")
        else:
            log.warning(f"  No saved review found for '{branch}', run 'review' first")
            reviews[branch] = {"verdict": "pass", "issues": []}

    fixes = {}
    for bc in branches:
        branch = bc["name"]
        if reviews[branch].get("verdict") == "parse_error":
            log.warning(f"  Latest saved review for '{branch}' is parse_error, re-running review before fix")
            reviews[branch] = phase_review_with_retries(bc, base, review_dir, config)
        if reviews[branch].get("verdict") == "needs_fixes":
            success = phase_fix(bc, reviews[branch], round_num=1, config=config)
            fixes[branch] = "applied" if success else "no changes"
        elif reviews[branch].get("verdict") == "parse_error":
            fixes[branch] = "blocked: review parse error"
        else:
            fixes[branch] = "not needed"

    for branch, status in fixes.items():
        log.info(f"  {branch}: {status}")


def cmd_prompt(config: dict) -> None:
    """Build and validate prompts only (Claude builds, Codex reviews)."""
    branches = config["branches"]

    for bc in branches:
        branch = bc["name"]
        if not bc.get("user_requirements"):
            log.warning(f"  No user_requirements for '{branch}', skipping")
            continue

        # Claude builds the spec
        prompt_file = phase_build_prompt(bc, config)
        if not prompt_file:
            continue

        # Codex reviews for gaps
        prompt_review = phase_review_prompt(bc, config)

        if prompt_review.get("verdict") == "needs_revision":
            # Claude revises
            phase_revise_prompt(bc, prompt_review, config)

            # Codex re-reviews
            second_review = phase_review_prompt(bc, config)
            if second_review.get("verdict") == "approved":
                log.info(f"  Spec APPROVED after revision for '{branch}'")
            else:
                remaining = len(second_review.get("gaps", []))
                log.warning(f"  Spec has {remaining} remaining gap(s) for '{branch}'")
        else:
            log.info(f"  Spec APPROVED on first pass for '{branch}'")

        log.info(f"  Final spec: {bc.get('prompt_file', 'N/A')}")


def cmd_merge(config: dict) -> None:
    """Merge only."""
    results = phase_merge(config)
    for branch, status in results.items():
        print(f"  {branch}: {status}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-Model Code Review & Fix Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=["execute-technical-review", "etr", "full", "prompt", "review", "fix", "merge"],
        help="Pipeline to run. 'execute-technical-review' (or 'etr') runs the full pipeline.",
    )
    parser.add_argument("--config", "-c", required=True, help="Config JSON path")
    parser.add_argument("--max-rounds", "-r", type=int, help="Override max rounds")
    parser.add_argument("--no-merge", action="store_true", help="Skip merge in full mode")

    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    if args.max_rounds is not None:
        config["max_rounds"] = args.max_rounds
    if args.no_merge:
        config["auto_merge"] = False

    # Validate executables
    log.info(f"Platform: {platform.system()} {platform.machine()}")
    log.info(f"Claude CLI: {CLAUDE_EXE}")
    log.info(f"Codex CLI: {CODEX_CMD}")
    log.info(f"Log directory: {LOG_DIR}")
    log.info(f"Loaded config: {len(config['branches'])} branches")

    commands = {
        "execute-technical-review": cmd_full,
        "etr": cmd_full,
        "full": cmd_full,
        "prompt": cmd_prompt,
        "review": cmd_review,
        "fix": cmd_fix,
        "merge": cmd_merge,
    }
    commands[args.command](config)


if __name__ == "__main__":
    main()

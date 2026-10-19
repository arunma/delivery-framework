#!/usr/bin/env python3
"""PreToolUse(Write|Edit|Bash): keep secrets out of the agent's hands.

- Write/Edit of a .env file (except .env.example) or of the owner's approval file: blocked.
- Bash that writes a .env file or the approval file: blocked.
- Bash that prints a .env file or a token variable: read_mode (ask by default; warn or block).
"""
import re
import sys

from common import block, config, decide, project_dir, read_input

ENV_NAME = re.compile(r"(^|/)\.env(\.(?!example\b)[\w.-]+)?$")
ENV_WORD = r"\S*\.env(\.(?!example\b)[\w.-]+)?(?=$|[\s;&|)'\"])"
WRITES_ENV = re.compile(r"(>>?|\btee(\s+-a)?|\b(cp|mv|ln)(\s+-\w+)*\s+\S+)\s*" + ENV_WORD)
READS_ENV = re.compile(r"\b(cat|less|more|head|tail|bat|nl|strings|xxd|od)\b[^;&|]*\s" + ENV_WORD)
PRINTS_TOKEN = re.compile(r"\b(echo|printf)\b[^;&|]*\$\{?\w*(TOKEN|SECRET|PASSWORD|API_KEY)\w*|"
                          r"^\s*(printenv|env|set)\s*($|[;&|])")


def main():
    data = read_input()
    root = project_dir(data)
    cfg = config(root, "secrets_guard")
    if not cfg:
        return 0
    tool, inp = data.get("tool_name"), data.get("tool_input") or {}
    approval = (config(root, "git_guard") or {}).get("approval_file", ".delivery/APPROVED")
    if tool in ("Write", "Edit"):
        path = inp.get("file_path", "")
        if ENV_NAME.search(path):
            block(f"delivery: writing {path} is blocked. Secrets files are the owner's; ask the owner "
                  "to edit it, or edit .env.example with placeholders.")
        if path.endswith(approval):
            block("delivery: only the owner creates the commit approval file.")
        return 0
    cmd = inp.get("command", "")
    if WRITES_ENV.search(cmd):
        block("delivery: writing a .env file from the shell is blocked. Ask the owner.")
    if approval.rsplit("/", 1)[-1] in cmd and re.search(r"\b(touch|cp|mv|ln|tee)\b|>", cmd):
        block("delivery: only the owner creates the commit approval file.")
    if READS_ENV.search(cmd) or PRINTS_TOKEN.search(cmd):
        decide(cfg["read_mode"], "delivery: this command may print secrets (a .env file or a token) "
               "into the transcript. Read single non-secret keys instead, e.g. grep '^JIRA_SITE=' .env.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

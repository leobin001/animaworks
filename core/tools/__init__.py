"""AnimaWorks external tools package."""
from __future__ import annotations
import sys

TOOL_MODULES = {
    "web_search": "core.tools.web_search",
    "x_search": "core.tools.x_search",
    "chatwork": "core.tools.chatwork",
    "slack": "core.tools.slack",
    "gmail": "core.tools.gmail",
    "local_llm": "core.tools.local_llm",
    "transcribe": "core.tools.transcribe",
    "aws_collector": "core.tools.aws_collector",
    "github": "core.tools.github",
}


def cli_dispatch():
    """Entry point for `animaworks-tool` CLI command."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        tools = ", ".join(sorted(TOOL_MODULES.keys()))
        print(f"Usage: animaworks-tool <tool_name> [args...]")
        print(f"Available tools: {tools}")
        sys.exit(0 if "--help" in sys.argv else 1)

    tool_name = sys.argv[1]
    if tool_name not in TOOL_MODULES:
        print(f"Unknown tool: {tool_name}")
        print(f"Available: {', '.join(sorted(TOOL_MODULES.keys()))}")
        sys.exit(1)

    import importlib
    mod = importlib.import_module(TOOL_MODULES[tool_name])
    if not hasattr(mod, "cli_main"):
        print(f"Tool '{tool_name}' has no CLI interface")
        sys.exit(1)

    mod.cli_main(sys.argv[2:])

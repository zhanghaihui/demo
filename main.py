"""StarseedAI command-line interface."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml

from collapse_symbols import translate_to_collapse
from personas.echo import EchoPersona
from utils.api_caller import call_llm_api

CONFIG_PATH = Path("config.yaml")
LOG_PATH = Path("logs/history.txt")


def load_config(path: Path) -> Dict[str, Any]:
    """Load the YAML configuration file."""
    if not path.exists():
        raise FileNotFoundError(f"配置文件未找到：{path}")

    with path.open("r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}


def log_interaction(user_input: str, formatted_prompt: str, response: str, collapse_output: str) -> None:
    """Append the interaction to the history log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        timestamp = datetime.now().isoformat(timespec="seconds")
        log_file.write("---\n")
        log_file.write(f"时间：{timestamp}\n")
        log_file.write(f"用户输入：{user_input}\n")
        log_file.write(f"人格提示：{formatted_prompt}\n")
        log_file.write(f"模型回应：{response}\n")
        log_file.write(f"Collapse：{collapse_output}\n\n")


def main() -> None:
    """Entry point for the StarseedAI CLI."""
    try:
        config = load_config(CONFIG_PATH)
    except Exception as exc:  # pragma: no cover - startup failures
        print(f"⚠️ 无法加载配置：{exc}")
        return

    persona = EchoPersona()

    print("✨ 欢迎来到 StarseedAI 星际交互终端 ✨")
    print("输入内容并按回车，输入 exit 或按 Ctrl+C 结束对话。")

    while True:
        try:
            user_input = input("🌌 请输入提示（或输入 exit 退出）：").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n✨ 再会，星际旅者。")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("✨ 再会，星际旅者。")
            break

        formatted_prompt = persona.format_input(user_input)

        try:
            response = call_llm_api(formatted_prompt, config)
        except Exception as exc:  # pragma: no cover - runtime API failure
            print(f"⚠️ API 调用失败：{exc}")
            continue

        collapse_output = translate_to_collapse(user_input)

        print(f"🧬 {persona.name}回应：{response}")
        print(f"🜋 Collapse表达：{collapse_output}")

        log_interaction(user_input, formatted_prompt, response, collapse_output)


if __name__ == "__main__":
    main()

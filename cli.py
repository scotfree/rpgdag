"""Command-line driver. See mvp_implement.md §9.

Only `render` exists so far; validate/new-game/answer/move/status/score are
tracked as GitHub issues.
"""

import argparse

from rpgdag.model import load_config
from rpgdag.render import write_views


def main() -> None:
    parser = argparse.ArgumentParser(prog="rpgdag")
    sub = parser.add_subparsers(dest="command", required=True)

    render = sub.add_parser("render", help="generate HTML views from a config")
    render.add_argument("--config", required=True, help="path to game_config.json")
    render.add_argument("--out", default="out", help="output directory (default: out/)")

    args = parser.parse_args()
    if args.command == "render":
        config = load_config(args.config)
        for path in write_views(config, args.out):
            print(f"wrote {path}")


if __name__ == "__main__":
    main()

import argparse
import os

import yaml

from .bullet import Bullet, Input, VerticalPrompt, colors

description = "Launches an interactive instruction to create and save a launch script for CoLLiE. If the configuration file is not found or not specified, a new one will be saved at the given path, default to ./collie_default.yml. The launch script will be saved at the given path, default to ./run.sh."


def gen_run_command_parser(subparsers=None):
    if subparsers is not None:
        parser = subparsers.add_parser("gen_run")
    else:
        parser = argparse.ArgumentParser("CoLLiE gen_run command")

    parser.usage = "collie gen_run [<args>]"

    parser.add_argument(
        "--config_file",
        "-c",
        default="./collie_default.yml",
        help="If `--config_file` is not specified, it will be set to `./collie_default.yml`. If the config file does not exist, it will be generated by `collie config`.",
        type=str,
    )

    parser.add_argument(
        "--run_file",
        "-r",
        default="./run.sh",
        help="If `--run_file` is specified, the run script will be generated at the given path. Otherwise, the script will be generated at `./run.sh`.",
        type=str,
    )

    if subparsers is not None:
        parser.set_defaults(entrypoint=gen_run_command_entry)
    return parser


_prompt_argname_map = {"Test": "test"}


def _parse(v):
    if v.isdigit():
        return int(v)
    elif v.replace(".", "", 1).isdigit():
        return float(v)
    elif v in ["Yes", "No"]:
        return v == "Yes"
    else:
        return v


def gen_run_command_entry(args):
    raise NotImplementedError

    word_color = colors.foreground["cyan"]

    if not os.path.exists(args.config_file):
        from .config import config_command_entry

        print(f"Can't find file {args.config_file}, generate a new one.")
        config_command_entry(args)

    gen_run_command_cli = VerticalPrompt(
        [
            Input("Test", default="1", word_color=word_color),
        ]
    )
    result = gen_run_command_cli.launch()
    parameters = {_prompt_argname_map[k]: _parse(v) for k, v in result}

    with open(args.run_file, "w") as f:
        # TODO: generate run script
        print(
            f"🎉 Script saved to {args.run_file}, use `sh {args.run_file}` to launch CoLLiE!"
        )
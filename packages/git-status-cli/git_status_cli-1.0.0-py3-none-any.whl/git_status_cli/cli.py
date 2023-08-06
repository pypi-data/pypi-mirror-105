import os
import shutil
import subprocess as sp
from importlib import resources
from pathlib import Path

import click
import yaml
from tabulate import tabulate


def load_user_config():
    app_dir = Path(click.get_app_dir("gitstatus"))

    try:
        with open(app_dir / "config.yaml") as config_file:
            return yaml.safe_load(config_file)

    except FileNotFoundError:
        os.makedirs(app_dir, mode=0o755, exist_ok=True)

        with resources.path("gitstatus", "config.yaml") as config_path:
            shutil.copy(config_path, app_dir)

        return load_user_config()


def clean(git):
    click.secho(str(git), fg="blue")
    sp.run(
        "git status".split(),
        cwd=git,
    )
    sp.run(click.prompt(click.style(f"{git}$ ", fg="blue")).split(), cwd=git)
    return get_status(git)


def get_status(git):

    status_lines = (
        sp.run(
            "git status --short --branch".split(),
            cwd=git,
            stdout=sp.PIPE,
            stderr=sp.DEVNULL,
        )
        .stdout.decode()
        .splitlines()
    )

    if (
        "ahead" in status_lines[0]
        or "behind" in status_lines[0]
        or len(status_lines) > 1
    ):
        return clean(git)

    return [
        click.style(str(git), fg="blue"),
        click.style("OK", fg="green"),
        status_lines[0][3:],
    ]


@click.command()
def main():
    """Get the status of all your gits in one command!"""
    config = load_user_config()

    try:
        assert config is not None

        gits = set()
        try:
            gits = {
                dir
                for dir in Path(config.get("gits_folder")).iterdir()
                if dir.is_dir()
            }
        except TypeError:
            pass

        gits |= {Path(dir) for dir in config.get("individual_gits", [])}

        assert gits != set()

        click.echo(
            tabulate(
                [get_status(git) for git in gits],
                headers=["Git", "Status", "Branch"],
            )
        )

    except AssertionError as error:
        click.echo(
            "Please edit your config file to include at least one git: "
            f"{Path(click.get_app_dir('gitstatus')) / 'config.yaml'}",
        )

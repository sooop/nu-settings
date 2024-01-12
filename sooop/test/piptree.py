import json
import re
import subprocess
from typing import Any

from rich import print
from rich.console import Console
from rich.tree import Tree

__CACHE__: dict[str, Tree | None] = {}
console = Console()


def get_packages(option: str = "top") -> Tree | None:
    assert option in ("top", "outdated")
    match option:
        case "top":
            option = "--not-required"
        case "outdated":
            option = "--outdated"
    with console.status(f"Getting package info..."):
        res = subprocess.run(
            f"pip list {option}".split(), capture_output=True, universal_newlines=True
        )
    lines = res.stdout.splitlines()[2:]
    packs = [line.split()[0] for line in lines]
    tree = Tree("Installed Packages")
    if packs:
        for pack in packs:
            branch = create_package_tree(pack)
            assert branch is not None
            tree.add(branch)

    return tree


def create_package_tree(name: str) -> Tree | None:
    if name in __CACHE__:
        return __CACHE__[name]
    with console.status(f"Getting package info: {name}"):
        res = subprocess.run(
            f"pip show {name}".split(), capture_output=True, universal_newlines=True
        )
    if res.returncode != 0:
        __CACHE__[name] = None
        print(res.stderr)
        return None

    line = [
        line for line in res.stdout.splitlines() if line.lower().startswith("requires:")
    ].pop()

    subpacks = re.split(r"[:,] ", line)[1:]
    tree = Tree(name, style="green")
    for pack in subpacks:
        if pack.strip():
            branch = create_package_tree(pack)
            if branch is not None:
                tree.add(branch)
    __CACHE__[name] = tree
    return tree


def build_package_tree(item: dict[str, Any]) -> Tree:
    if item["name"] in __CACHE__:
        return __CACHE__[item["name"]]
    tree = Tree(item["name"])
    for subpack in item["requires"]:
        branch = build_package_tree(subpack)
        tree.add(branch)
    __CACHE__[item["name"]] = tree
    return tree


def print_package_tree(info):
    tree = Tree("Installed Packages")
    for p in info:
        branch = build_package_tree(p)
        tree.add(branch)
    print(tree)


def main(filename: str = "packages.json"):
    tree = Tree("Installed Packages")
    with open("packages.json", "rb") as f:
        packs = json.load(f)
        print_package_tree(packs)


if __name__ == "__main__":
    main()

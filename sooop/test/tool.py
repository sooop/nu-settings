import json
import re
import subprocess
import sys
import time
from typing import Any

from rich.console import Console
from rich.prompt import Prompt
from rich.themes import DEFAULT
from rich.tree import Tree
from dicttool import traverse

CACHE: dict[str, dict[str, str | list[str]]] = {}
console = Console(theme=DEFAULT)


def make_tree(item, lv=1) -> Tree:
    if isinstance(item, str):
        return Tree(item, style="dim yellow")
    _style = ["yellow", "green", "blue", "magenta", "bright_red", "cyan"]
    tree = Tree(item["name"])
    for x in item["requires"]:
        branch = make_tree(x, lv + 1)
        tree.add(branch, style=_style[lv % len(_style)])
    return tree


def get_detail_info(name: str) -> dict[str, str | list[str]]:
    name = name.strip()
    # console.print(f"{name=}")
    if name in CACHE:
        console.log(f"[dim red] {name} is matched with cache")
        return CACHE[name]

    cmd = f"pip show {name}"
    with console.status(f"EXECUTING: {cmd}"):
        res = subprocess.run(cmd, universal_newlines=True, capture_output=True)
    if res.returncode > 0:
        raise ValueError("Invalid package name")
    lines = res.stdout.splitlines()
    # console.log(lines)
    info: dict[str, str | list[str]] = {}
    for line in lines:
        if re.match(r"^[A-Z][a-z0-9\-_]{2,}:", line) is None:
            console.log(f"[gray46]informal line - {line}")
            continue
        k, v = re.split(r":\s*", line, 1)
        k = k.lower().replace("-", "_")
        match k:
            case "requires" | "required_by":
                info[k] = [w.strip() for w in re.split(r",\s*", v) if w.strip()]
            case _:
                info[k] = v.strip()

    CACHE[name] = info
    return info


def __expand(item: str | dict[str, Any], parent: str = "") -> dict[str, Any]:
    if isinstance(item, str):
        item = get_detail_info(item)
    if "requires" not in item:
        item["requires"] = []
        CACHE[item["name"]] = item
        return item
    if parent and "required_by" not in item:
        item["required_by"] = [parent]
        CACHE[item["name"]] = item
    elif parent and parent not in item["required_by"]:
        item["required_by"].append(parent)
        CACHE[item["name"]] = item

    expanded = [__expand(subpack) for subpack in item["requires"]]
    return {**item, "requires": expanded}


def get_installed_packages():
    cmd = "pip list --not-required"
    res = subprocess.run(cmd, universal_newlines=True, capture_output=True)
    if res.returncode != 0:
        raise ValueError("Failed to process")
    lines = res.stdout.splitlines()[2:]
    return [line.split()[0] for line in lines]


def main() -> list[dict[str, Any]]:
    ps = get_installed_packages()
    ps = [__expand(get_detail_info(p)) for p in ps]
    with open("packages.json", "w") as f:
        json.dump(ps, f, indent=2)
    return ps


def load_file(filename: str) -> Any:
    try:
        with open(filename, "rb") as f:
            ps = json.load(f)
            return ps
    except FileNotFoundError:
        reply = Prompt.ask("File not found. Read all packages? [Y/n]")
        if reply:
            return main()


def demo(filename: str):
    ps = load_file(filename)
    tree = Tree("[b]Installed Packages", style="yellow", guide_style="dim yellow")
    for p in ps:
        branch = make_tree(__expand(p))
        tree.add(branch)
    console.print(tree)
    return tree


if __name__ == "__main__":
    # demo("packages.json" if len(sys.argv) == 1 else sys.argv[1])
    pn = "textual-dev"
    root = __expand(get_detail_info(pn))
    target = traverse(root, "requires")
    print([x["name"] for x in target])
    for p in target:
        print(f'{p["name"]}: {p["required_by"]}')

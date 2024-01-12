import subprocess
import re
import json
from piptree import build_package_tree

__CACHE__ = {}

def get_package_info(package_name: str, parent: str='') -> dict:
    if package_name in __CACHE__:
        item = __CACHE__[package_name]
        if package_name not in item['required_by']:
            item['required_by'].append(package_name)
        return item

    print(f"Getting package info: {package_name}")

    command = f"pip show {package_name}"
    res = subprocess.run(
            command.split(),
            capture_output=True,
            universal_newlines=True)
    if res.returncode > 0:
        __CACHE__[package_name] = None
        raise subprocess.CalledProcessError(
                res.returncode,
                command,
                res.stdout,
                res.stderr)
    info = {}
    for line in res.stdout.splitlines():
        k, *v = re.split(r":\s*", line, 1)
        if not v:
            info[k] = ""
            continue
        else:
            v = v[0]
        k = k.lower().replace('-', '_')
        match k:
            case 'requires' if v.strip() != '':
                info[k] = [get_package_info(cname.strip(), package_name) for cname in
                           re.split(r',\s*', v)
                           if cname.strip() != '']
            case 'requires' if v.strip() == '':
                info[k] = []
            case 'required_by':
                info[k] = [p.strip() for p in re.split(r',\s*', v)
                           if p.strip()]
                if parent and parent not in info[k]:
                    info[k].append(parent)
            case _:
                info[k] = v

    __CACHE__[package_name] = info
    return info


def get_package_list(option: str="top") -> list:
    assert option in ('top', 'outdated')
    match option:
        case 'top':
            option = '--not-required'
        case 'outdated':
            option = '--outdated'
        case _:
            option = ''
    res = subprocess.run(f"pip list {option}".split(),
                         capture_output=True,
                         universal_newlines=True)
    lines = res.stdout.splitlines()[2:]
    packs = [line.split()[0] for line in lines if line.strip()]
    return packs


def build_package_info(filename: str="packages.json"):
    tree = [get_package_info(p) for p in get_package_list()]
    with open(filename, 'w') as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)
    return tree




if __name__ == '__main__':
    packages = build_package_info()
    # from rich import print
    # print(get_package_info('webcolors'))
    from rich import print
    print(build_package_tree(packages))

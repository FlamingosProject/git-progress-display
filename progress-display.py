#!/usr/bin/python3
Bart Massey 2025

# Work with a Git "progress display". See this project's repo
# <https://github.com/FlamingosProject/git-progress-display>
# for information including licensing.

import argparse, os, re, subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("chapter", type=int, help="Starting chapter number")
args = ap.parse_args()

top = os.getcwd()

def run_command(command, silent=False):
    result = subprocess.run(
        command.split(),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if not silent:
            print("{command} failed", file=sys.stdout)
            print("{result.stderr}", file=sys.stdout)
        raise Exception("command failed")
    return str(result.stdout)

def get_branches():
    try:
        branch_list = run_command("git branch -a")
    except:
        exit(1)
    branch_re = re.compile("^  remotes/origin/(([0-9]+)-.+)$")
    branches = []
    for b in branch_list.splitlines():
        m = branch_re.match(b)
        if m:
            ch = int(m[2])
            if args.chapter < ch:
                branches.append((ch, m[1]))
    return branches

def submodule_update():
    os.chdir(top)
    run_command("git submodule update")

branches = get_branches()

for ch, name in branches:
    print(f"{ch:02}", name)

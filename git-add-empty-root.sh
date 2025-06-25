#!/bin/sh
# git-add-empty-root.sh: Bart Massey 2025
#
# Create an empty root commit at the root of an existing
# Git repo, without otherwise disturbing the repo.
#
# Note that the date of the root commit will be current
# rather than older. If that's a problem, see the link below
# for fancier solutions.
#
# `git filter-repo --force` is used here because `git-filter-repo`
# needs it even on a fresh repo. Nonetheless, *back up your repo*
# and perform this operation on a *fresh clone*. NO WARRANTY: I
# hacked up someone else's hack, and have no idea what this will
# actually do to your repo.
#
# Thanks to Aristotle Pagaltzis https://stackoverflow.com/a/647451
TREE=`git hash-object -wt tree --stdin < /dev/null`
COMMIT=`git commit-tree -m 'root commit' $TREE`
git branch root $COMMIT
ROOT=`git rev-list --max-parents=0 HEAD`
git replace $ROOT --graft root
git filter-repo --proceed --force

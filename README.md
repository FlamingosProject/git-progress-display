# git-progress-display: show progress in Git via branch submodules
Bart Massey and Philipp Oppermann 2025

This is a somewhat grotty implementation of a technique
developed by Philipp Oppermann to display various stages
of a work-in-progress project as part of a Git repo.

You can see a demo repo made using this technique on Github:
[FlamingosProject/git-progress-display-demo](https://github.com/FlamingosProject/git-progress-display-demo).

## Intent

The goal is to have a number of Git submodules of an
upstream repo, each pointing to a *viewpoint*: a successive
numbered branch in that repo displaying work-in-progress. A
viewpoint allows the reader to jump directly into a
directory corresponding to a particular point in
development. The top-level directory in the `main` branch is
decoupled from these branches, so it can be updated
separately without disturbing the force.

For example, here's what a `main` branch might look
like. (The README here is the top-level project README.)

    README.md
    01-starting-out/
    02-elaborating/
    03-improving/

Each of these numbered viewpoint directories corresponds to
a git submodule pointing at a branch of the same name
upstream: `03-improving` would be a Git submodule containing
the work-in-progress code at that branch. For example,
here's what that subdirectory might contain. (This README is
for the work-in-progress code, and disjoint from the
top-level README.)

    README.md
    hello.py

## Scripting

This sort of display is relatively easy to set up, and
wouldn't require any scripting on its own. However, it could
*conceivably* happen (LOL) that some retroactive change is
needed in an early branch. Once that change is made, it
needs to be "rolled forward" to subsequent branches to bring
the later code up to date. This can be accomplished with
`git merge` commits in subsequent branches, but accessing
the original branch commit — which has not yet been pushed —
is a little exciting, since the branch submodules only know
about upstream and their parents.

[One way to accomplish things easily would be to set the URL
for each submodule to `file://.` so that the submodules
track the downstream repo rather than upstream. Git actually
handles this case fine, but unfortunately Github has a bug
in how it generates display URLs that keeps the reader from
clicking into the submodules on Github. Thus we currently
don't use this approach.]

## Workflow

We are currently using the following workflow, which
takes advantage of the really nice `git worktree`
functionality.

### Initializing the repo

You really want an empty commit at the root of your Git repo
with both the top-level and project coming from that.

* When starting a new repo, getting a root commit is relatively easy.

  ```sh
  git init
  git commit --allow-empty -m 'my thing'
  git branch -m main root
  git branch main
  git branch 01-starting`
  git checkout main
  ```

* If you are working with an existing repo and want to
  convert it to progress-display form, you'll want to graft
  an empty commit onto the root so that you don't lose
  history and yet don't have the new `main` track the old
  state. You'll then have to make display branches for the
  intermediate steps you want to show off.

  Git hates this kind of thing. See
  [`git-add-empty-root.sh`](./git-add-empty-root.sh) in this
  repo for a sequence of commands that seems to work for this.
  You will definitely want to work on a fresh `--no-local`
  local clone of your repo, and only force-push upstream
  when you are super-confident the good thing has happened.

### Adding a viewpoint

The whole point of progress-display is to have viewpoints
representing the stages of project development.

*[TODO]*

### Updating the project

* Check out a git worktree at the branch b to be modified
  using `git worktree add work` with b.
  
* Change directory into `work`.

* For each subsequent branch b:
  * `git switch` to b in the worktree.
  * `git merge` branch b - 1, resolving any merge conflicts.
  * Commit the result.

* Change back to the main directory.

* `git commit -a` to ensure that all the branches are
  correctly updated in the actual repository.
  
* `git push --all` to send the changes upstream.

* `git submodule update --remote` to make the branch
  submodules correct.

* `git commit -a` to update `.gitmodules`.

* `git push` the updated `.gitmodules`.

* `git worktree remove -f work`

This is a pretty fragile and tedious workflow, but it does
work and flow. Automation seemed highly desirable here.

## Tool

*[TODO]*

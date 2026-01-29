# Git Commands Guide (DevOps-Oriented)

## 1. Installation and Setup

### Install Git

Download and install Git from:
[https://git-scm.com/](https://git-scm.com/)

Linux (Debian/Ubuntu):

```bash
sudo apt update && sudo apt install git -y
```

RHEL/CentOS:

```bash
sudo yum install git -y
```

macOS (Homebrew):

```bash
brew install git
```

### Verify Installation

```bash
git --version
```

### Configure User Identity

Git uses this information for commits:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Check configuration:

```bash
git config --list
```

Configuration scopes:

* `--system`: All users
* `--global`: Current user
* `--local`: Repository only

---

## 2. SSH Key Configuration

### Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

Start SSH agent and add key:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Use Custom SSH Key (Per Repository)

```bash
git config --local core.sshCommand "ssh -i <PATH_TO_SSH_KEY>"
```

Clone with custom SSH key:

```bash
git -c core.sshCommand="ssh -i <key-path>" clone git@host:repo.git
```

---

## 3. Initialize Repository

Create a new Git repository:

```bash
git init -b main
```

Existing repository:

```bash
git init
```

---

## 4. Basic Workflow

### Stage and Commit Changes

Stage all changes:

```bash
git add -A
```

Commit changes:

```bash
git commit -m "Initial commit"
```

### Connect Local Repository to Remote

```bash
git remote add origin <REPO_URL>
```

Verify:

```bash
git remote -v
```

### Push to Remote

First push:

```bash
git push -u origin main
```

Subsequent pushes:

```bash
git push
```

---

## 5. Repository Status and History

### Check Repository Status

```bash
git status
```

### View Commit History

```bash
git log
```

Common options:

```bash
git log --oneline
git log --graph --oneline --all
git log -p
git log -3
```

### View File Changes

Unstaged changes:

```bash
git diff
```

Staged changes:

```bash
git diff --staged
```

Compare branches:

```bash
git diff main..dev
```

---

## 6. File Operations

### Stage Specific Files

```bash
git add <file>
```

### Unstage Files

```bash
git reset <file>
```

### Discard Local Changes

```bash
git checkout -- <file>
```

Restore using modern command:

```bash
git restore <file>
```

### Rename File

```bash
git mv old-name new-name
```

### Remove File

```bash
git rm <file>
```

Remove but keep locally:

```bash
git rm --cached <file>
```

---

## 7. Branch Management

### Create and Switch Branch

```bash
git checkout -b <branch-name>
```

Modern alternative:

```bash
git switch -c <branch-name>
```

### List Branches

```bash
git branch
git branch -a
git branch -v
```

### Delete Branch

```bash
git branch -d <branch-name>
```

Force delete:

```bash
git branch -D <branch-name>
```

### Rename Branch

```bash
git branch -m old-name new-name
```

---

## 8. Merging and Rebasing

### Merge Branch

```bash
git merge <branch-name>
```

Merge types:

* Fast-forward
* Three-way merge (creates merge commit)

### Rebase (Linear History)

```bash
git rebase main
```

Abort rebase:

```bash
git rebase --abort
```

Continue rebase:

```bash
git rebase --continue
```

---

## 9. Remote Operations

### List Remotes

```bash
git remote
git remote -v
```

### Show Remote Details

```bash
git remote show origin
```

### Fetch Changes

```bash
git fetch
git fetch --all
```

### Pull Changes

Fetch + merge:

```bash
git pull
```

Rebase instead of merge:

```bash
git pull --rebase
```

---

## 10. Commit Management

### Amend Last Commit

```bash
git commit --amend
```

### Show Commit Details

```bash
git show <commit-id>
```

### Revert Commit (Safe for Shared Branches)

```bash
git revert <commit-id>
```

### Reset Commit (Use with Caution)

Soft reset:

```bash
git reset --soft HEAD~1
```

Mixed reset:

```bash
git reset HEAD~1
```

Hard reset:

```bash
git reset --hard HEAD~1
```

---

## 11. Stash (Temporary Changes)

Save work without committing:

```bash
git stash
```

List stashes:

```bash
git stash list
```

Apply stash:

```bash
git stash apply
```

Pop stash:

```bash
git stash pop
```

---

## 12. Tags (Releases)

Create tag:

```bash
git tag v1.0.0
```

Annotated tag:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
```

Push tags:

```bash
git push origin --tags
```

---

## 13. .gitignore

Create `.gitignore`:

```bash
touch .gitignore
```

Example:

```
.env
node_modules/
*.log
```

Apply after commit:

```bash
git rm -r --cached .
git add .
git commit -m "Apply gitignore"
```

---

## 14. Useful Configuration and Aliases

Change default editor:

```bash
git config --global core.editor "vim"
```

Create aliases:

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.cm commit
git config --global alias.br branch
```

---

## 15. Troubleshooting and Recovery

Undo last commit but keep changes:

```bash
git reset --soft HEAD~1
```

Recover deleted branch:

```bash
git reflog
git checkout -b <branch-name> <commit-id>
```

Fix detached HEAD:

```bash
git checkout main
```

---

## 16. Clone Repository

Clone via SSH:

```bash
git clone git@github.com:user/repo.git
```

Clone specific branch:

```bash
git clone -b <branch> <repo-url>
```


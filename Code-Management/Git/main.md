# Git Commands Guide

## 1. Installation and Setup

### Install Git
Download from [git-scm.com](https://git-scm.com/).

### Verify Installation
```bash
git --version
```

### Configure User Info
Set your name and email for commits:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 2. SSH Key Configuration

Use a custom SSH key:
```bash
git config --add --local core.sshCommand 'ssh -i <PATH_TO_SSH_KEY>'
```

Clone with custom key:
```bash
git -c core.sshCommand="ssh -i <key-path>" clone host:repo
```

## 3. Initialize Repository

Create a new Git repo:
```bash
git init -b main
```
- `-b main`: Sets default branch name to `main`.

## 4. Basic Workflow

### Stage and Commit
Stage all changes:
```bash
git add -A
```
Commit changes:
```bash
git commit -m "Initial Commit"
```

### Connect to Remote
Link local repo to remote:
```bash
git remote add origin <Repo-Link>
```

### Push to Remote
```bash
git push origin main
```

## 5. Repository Status and History

### Check Status
```bash
git status
```
Shows staged, unstaged, and untracked files.

### View History
```bash
git log
```
- `git log -p`: Shows diffs per commit.
- `git log -3`: Shows last 3 commits.
- `git log --graph`: Shows history as a graph.
- `git log --oneline`: Shows compact log.

### View Changes
```bash
git diff
```
Shows unstaged changes.

```bash
git diff --staged
```
Shows staged changes.

## 6. File Operations

### Stage Specific Files
```bash
git add <filename>
```

### Unstage Files
```bash
git reset <filename>
```

### Discard Changes
```bash
git checkout -- <filename>
```
Reverts file to last committed state.

### Rename File
```bash
git mv <old-name> <new-name>
```

### Remove File
```bash
git rm <filename>
```

## 7. Branch Management

### Create and Switch to Branch
```bash
git checkout -b <branch-name>
```

### List Branches
```bash
git branch
```
List with details:
```bash
git branch -v
```

### Delete Branch
```bash
git branch -d <branch-name>
```

### Switch Branch
```bash
git checkout <branch-name>
```

## 8. Merging

### Merge Branch
```bash
git merge <branch-name>
```

**Merge Types:**
- **Fast-forward:** No conflicts; branch is ahead of target.
- **Three-way:** Conflicts possible; creates new merge commit.

## 9. Remote Operations

### List Remotes
```bash
git remote
```

### Show Remote Info
```bash
git remote -v
```
```bash
git remote show origin
```

### Fetch Changes
```bash
git fetch
```
Get updates without merging.

```bash
git fetch --all
```
Fetch from all remotes.

## 10. Commit Management

### Edit Last Commit Message
```bash
git commit --amend
```

### Show Commit Changes
```bash
git show <commit-id>
```

### Revert Commit
```bash
git revert HEAD
```
Revert last commit.

```bash
git revert <commit-id>
```
Revert specific commit.

## 11. Miscellaneous

### Change Default Editor
```bash
git config --global core.editor "vim"
```

### Clone Repository
```bash
git clone <Repo-Link>
```

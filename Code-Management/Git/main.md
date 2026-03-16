# Git Commands Guide for DevOps Engineers

**Professional Reference Document**  
*Comprehensive Git workflow for development, CI/CD pipelines, and team collaboration*

---

## Table of Contents
1. [Installation and Setup](#1-installation-and-setup)
2. [SSH Key Configuration](#2-ssh-key-configuration)
3. [Repository Initialization](#3-repository-initialization)
4. [Basic Workflow](#4-basic-workflow)
5. [Status and History](#5-status-and-history)
6. [File Operations](#6-file-operations)
7. [Branch Management](#7-branch-management)
8. [Merging and Rebasing](#8-merging-and-rebasing)
9. [Remote Operations](#9-remote-operations)
10. [Commit Management](#10-commit-management)
11. [Removing Commits](#11-removing-commits)
12. [Stash Operations](#12-stash-operations)
13. [Tags and Releases](#13-tags-and-releases)
14. [.gitignore Management](#14-gitignore-management)
15. [Configuration and Aliases](#15-configuration-and-aliases)
16. [Troubleshooting and Recovery](#16-troubleshooting-and-recovery)
17. [Repository Cloning](#17-repository-cloning)

---

## 1. Installation and Setup

### **Install Git**
Download from official source: [git-scm.com](https://git-scm.com/)

**Linux Distributions:**
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install git -y

# RHEL/CentOS/Fedora
sudo yum install git -y    # or dnf install git -y
```

**macOS:**
```bash
brew install git
```

### **Verify Installation**
```bash
git --version
```
*Displays installed Git version*

### **Configure User Identity**
Git requires author information for every commit:
```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@company.com"
```

**Configuration Scopes:**
| Scope | Command Flag | Applies To | Persistence |
|-------|--------------|------------|-------------|
| System | `--system` | All users on machine | System-wide |
| Global | `--global` | Current user | User account |
| Local | `--local` | Specific repository | Repository only |

**Verify Configuration:**
```bash
git config --list
```

---

## 2. SSH Key Configuration

### **Generate SSH Key Pair**
```bash
ssh-keygen -t ed25519 -C "your.email@company.com"
```
- **`-t ed25519`**: Modern, secure key algorithm
- **`-C`**: Comment for key identification

### **SSH Agent Management**
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add private key to agent
ssh-add ~/.ssh/id_ed25519
```

### **Per-Repository SSH Key**
```bash
# Set custom key for specific repo
git config --local core.sshCommand "ssh -i /path/to/custom_key"

# Clone with specific key (one-time)
git -c core.sshCommand="ssh -i /path/to/key" clone git@host:repo.git
```

---

## 3. Repository Initialization

### **Create New Repository**
```bash
# Initialize with main branch
git init -b main

# Initialize with default branch
git init
```

**Key Concepts:**
- **Working Directory**: Files not yet tracked by Git
- **Staging Area (Index)**: Files prepared for commit
- **Repository**: Committed history and metadata

---

## 4. Basic Workflow

### **Stage Changes**
```bash
# Stage all changes (new, modified, deleted)
git add -A

# Stage specific files
git add <file1> <file2>

# Stage all modified files (not new files)
git add .
```

### **Commit Changes**
```bash
git commit -m "Descriptive commit message"
```

### **Connect to Remote**
```bash
git remote add origin <repository-url>
git remote -v    # Verify remote configuration
```

### **Push to Remote**
```bash
# First push (sets upstream tracking)
git push -u origin main

# Subsequent pushes
git push
```

---

## 5. Status and History

### **Repository Status**
```bash
git status
```
*Shows working directory and staging area state*

### **Commit History**
```bash
# One-line summary
git log --oneline

# Visual graph of all branches
git log --graph --oneline --all

# Last N commits with patch
git log -p -3

# Show specific commit details
git show <commit-hash>
```

### **Change Visualization**
```bash
# Unstaged changes (working directory)
git diff

# Staged changes (index vs HEAD)
git diff --staged

# Branch comparison
git diff main..develop
```

---

## 6. File Operations

| Operation | Command | Effect |
|-----------|---------|---------|
| Stage file | `git add <file>` | Moves file to staging area |
| Unstage | `git reset <file>` | Removes from staging, keeps changes |
| Discard changes | `git restore <file>` | Reverts to last committed version |
| Rename | `git mv old new` | Stages rename operation |
| Remove (tracked) | `git rm <file>` | Stages file deletion |
| Untrack | `git rm --cached <file>` | Removes from Git, keeps locally |

---

## 7. Branch Management

### **Branch Operations**
```bash
# Create and switch
git switch -c feature/new-api

# List branches
git branch -v          # Local branches with last commit
git branch -a          # All branches (local + remote)

# Delete branch
git branch -d feature  # Safe delete (merged)
git branch -D feature  # Force delete

# Rename branch
git branch -m old-name new-name
```

**Branch States:**
- **Local Branch**: Exists only in your repository
- **Remote Branch**: Exists on remote server (`origin/main`)
- **Tracking Branch**: Local branch linked to remote (`main -> origin/main`)

---

## 8. Merging and Rebasing

### **Merge (Preserves History)**
```bash
git checkout main
git merge feature/xyz
```

**Merge Types:**
| Type | Condition | Result |
|------|-----------|---------|
| Fast-forward | Target ahead, no divergence | Linear history |
| Three-way | Both branches have new commits | Merge commit created |

### **Rebase (Linear History)**
```bash
git checkout feature/xyz
git rebase main
```

**Rebase Controls:**
```bash
git rebase --abort     # Cancel rebase
git rebase --continue  # Resolve conflicts and continue
```

---

## 9. Remote Operations

### **Remote Management**
```bash
git remote -v              # List remotes
git remote show origin     # Detailed remote info
git fetch --all            # Fetch all remotes
```

### **Pull Strategies**
```bash
git pull                   # Fetch + merge
git pull --rebase          # Fetch + rebase (cleaner history)
```

---

## 10. Commit Management

### **Modify Last Commit**
```bash
git commit --amend         # Edit message/files
```

### **Safe Undo (Shared Branches)**
```bash
git revert <commit-hash>   # Creates reversing commit
```

### **Reset Types**
```bash
git reset --soft HEAD~1    # Keeps staging area
git reset HEAD~1           # Unstages, keeps files
git reset --hard HEAD~1    # Discards everything
```

---

## 11. Removing Commits

### **Remove Local (Unpushed) Commit**
```bash
# Soft reset (interactive rebase recommended)
git reset --soft HEAD~1

# Interactive rebase for multiple commits
git rebase -i HEAD~3
# Change 'pick' to 'drop' or delete line
```

### **Remove Pushed Commit from Remote**

**⚠️ DANGER: Rewrites shared history**

```bash
# 1. Reset locally
git reset --hard HEAD~1

# 2. Force push (collaborators must coordinate)
git push --force-with-lease origin main

# 3. Alternative: Safer revert
git revert HEAD    # Creates undoing commit
git push
```

**Team Coordination Required:**
```
1. Notify team before force push
2. Team runs: git fetch && git reset --hard origin/main
3. Use revert for shared production branches
```

### **Remove Specific Pushed Commit**
```bash
# Interactive rebase
git rebase -i <commit-before-target>~1

# Or create revert
git revert <specific-commit-hash>
```

---

## 12. Stash Operations

**Temporary Storage:**
```bash
git stash push -m "WIP: API changes"
git stash list
git stash apply stash@{0}    # Keep stash
git stash pop                # Apply and remove
```

---

## 13. Tags and Releases

### **Tag Management**
```bash
# Lightweight tag
git tag v1.2.3

# Annotated tag (recommended)
git tag -a v1.2.3 -m "Release v1.2.3"

# Push tags
git push origin --tags
```

---

## 14. .gitignore Management

**Create/Update:**
```bash
touch .gitignore
```

**Common Patterns:**
```
# Dependencies
node_modules/
vendor/

# Logs
*.log
logs/

# Environment
.env
*.env.local

# OS
.DS_Store
Thumbs.db
```

**Apply Existing .gitignore:**
```bash
git rm -r --cached .
git add . && git commit -m "Apply .gitignore"
```

---

## 15. Configuration and Aliases

### **Editor and Pager**
```bash
git config --global core.editor "code --wait"
```

### **Productivity Aliases**
```bash
git config --global alias.st "status"
git config --global alias.co "checkout"
git config --global alias.br "branch -v"
git config --global alias.cm "!f() { git add -A && git commit -m \"$@\"; }; f"
```

---

## 16. Troubleshooting and Recovery

### **Common Recovery**
```bash
# View all history (including resets)
git reflog

# Recover deleted branch
git checkout -b recovery-branch <commit-hash>

# Fix detached HEAD
git checkout main
```

---

## 17. Repository Cloning

```bash
# Standard clone
git clone <url>

# Specific branch
git clone -b develop <url>

# Shallow clone (history limited)
git clone --depth 1 <url>
```

---

## Key Git Concepts Explained

| Concept | Definition | Importance |
|---------|------------|-----------|
| **HEAD** | Current commit/branch pointer | Always points to active commit |
| **Index/Staging** | Intermediate area between working dir and repo | Prepares exact commit content |
| **Fast-forward** | Linear merge without merge commit | Clean history |
| **Detached HEAD** | HEAD points directly to commit | Use for inspection, create branch to save work |
| **Reflog** | Local history of HEAD movements | Recovery lifeline |
| **Force Push** | Overwrites remote history | Use only with team coordination |

**Document Version: 2.0**  
*Optimized for DevOps workflows, CI/CD integration, and team collaboration*
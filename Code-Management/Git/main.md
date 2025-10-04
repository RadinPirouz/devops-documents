# Git Commands Guide

## Getting Started with Git

### 1. Installing Git

Before you begin, ensure Git is installed on your machine. You can download it from [git-scm.com](https://git-scm.com/).

### 2. Check Git Installation

To verify that Git is installed, run:

```bash
git --version
```

### 3. Configure Git User Information

Set up your name and email address, which will be used for your commits:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Configuring Git to Use a Custom SSH Key

If you need to use a specific SSH key for your Git operations, you can configure Git as follows:

```bash
git config --add --local core.sshCommand 'ssh -i <PATH_TO_SSH_KEY>'
```

For Clone With Custom SSH Key Use:
```bash
git -c core.sshCommand="ssh -i <key-path>" clone host:repo 
```


*Replace `<PATH_TO_SSH_KEY>` with the actual path to your SSH key file.*

## Creating and Managing a Local Git Repository

### 1. Initialize a Git Repository

Start by creating a new Git repository in your local project directory:

```bash
git init -b main
```

*The `-b main` flag sets the default branch name to "main".*

### 2. Add Files and Commit Changes

Next, stage all your files and create your initial commit:

```bash
git add -A
git commit -m "Initial Commit"
```

*The `git add -A` command stages all changes, while the `git commit` command records those changes with a descriptive message.*

### 3. Connect to a Remote Repository

Now, link your local repository to a remote GitHub repository:

```bash
git remote add origin <Repo-Link>
```

*Replace `<Repo-Link>` with the URL of your GitHub repository.*

### 4. Push Changes to GitHub

Finally, push your initial commit to the remote repository:

```bash
git push origin main
```

## Common Git Commands for Beginners

### 1. Check the Status of Your Repository

To see which changes are staged, unstaged, or untracked:

```bash
git status
```

### 2. View Commit History

To view the commit history of your repository:

```bash
git log
```

*You can press `q` to exit the log view.*

### 3. Viewing Changes

To see changes made to files before staging them:

```bash
git diff
```

### 4. Staging Individual Files

If you want to stage specific files instead of all changes:

```bash
git add <filename>
```

*Replace `<filename>` with the name of the file you wish to stage.*

### 5. Undoing Changes

To unstage a file that you added by mistake:

```bash
git reset <filename>
```

To discard changes in a file and revert it to the last committed state:

```bash
git checkout -- <filename>
```

### 6. Cloning a Repository

If you want to create a copy of an existing remote repository:

```bash
git clone <Repo-Link>
```

*Replace `<Repo-Link>` with the URL of the repository you want to clone.*

### 7. Creating a New Branch

To create a new branch for development:

```bash
git checkout -b <branch-name>
```

*Replace `<branch-name>` with your desired branch name.*

### 8. Merging Branches

To merge changes from another branch into your current branch:

```bash
git merge <branch-name>
```

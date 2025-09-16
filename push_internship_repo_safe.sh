#!/bin/bash

# ------------------------------------------
# Internship Program Safe Push Script
# ------------------------------------------
# Uses SSH host github-manish
# main branch -> assignments only (solution.py backed up)
# solutions branch -> full repo with solutions
# Old backups >7 days are automatically deleted
# ------------------------------------------

cd "$(dirname "$0")" || exit
echo "Starting safe push process..."

# 1️⃣ Set remote to SSH host for manishdsingh
git remote set-url origin git@github-manish:manishdsingh/internshipProgram.git

# 2️⃣ Push full repo to solutions branch
if git show-ref --quiet refs/heads/solutions; then
    git checkout solutions
else
    git checkout -b solutions
fi

git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Add/update full internship program with solutions"
else
    echo "No changes to commit in solutions branch"
fi
git push -u origin solutions
echo "✅ Solutions branch pushed"

# 3️⃣ Push assignments only to main branch
if git show-ref --quiet refs/heads/main; then
    git checkout main
else
    git checkout -b main
fi

# Backup solution.py files before deleting
BACKUP_DIR="./solution_backup_$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"
find . -name "solution.py" -type f -exec cp --parents {} "$BACKUP_DIR" \;
echo "✅ solution.py files backed up to $BACKUP_DIR"

# Remove solution.py files for interns
find . -name "solution.py" -type f -delete

git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Add/update only assignment.md files for interns (solution.py backed up)"
else
    echo "No changes to commit in main branch"
fi
git push -u origin main
echo "✅ Main branch pushed (assignments only)"

# 4️⃣ Cleanup old backups older than 7 days
find . -maxdepth 1 -type d -name "solution_backup_*" -mtime +7 -exec rm -rf {} \;
echo "✅ Old backups older than 7 days cleaned up"

echo "🎉 Safe push process with backup and cleanup completed!"
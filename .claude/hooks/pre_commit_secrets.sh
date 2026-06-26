#!/bin/sh
# Pre-commit hook to check for secrets in files
echo "Checking for secrets in staged files..."

# Check for .env files
if git status --porcelain | grep -q ".env"; then
    echo "ERROR: You are trying to commit a .env file! Please remove it from staging."
    exit 1
fi

# Check for hardcoded secrets in staged files
STAGED_FILES=$(git diff --cached --name-only)
for FILE in $STAGED_FILES; do
    if [ -f "$FILE" ]; then
        if git show ":$FILE" | grep -iqE "(password|secret|token|api[_-]key)"; then
            echo "WARNING: Potential secret found in $FILE"
        fi
    fi
done

echo "Secret check complete!"

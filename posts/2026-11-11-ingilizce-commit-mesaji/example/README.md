# Example: a tiny commit message checker

```bash
node check-commit.mjs "Added new stuff."
node check-commit.mjs "Add search box to the post drawer"
```

Use it as a Git hook (optional): copy it to `.git/hooks/commit-msg`, make it executable, and Git will pass the message file path as the first argument. The script accepts either a message or a file path.

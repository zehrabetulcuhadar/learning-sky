# Example: mask before you paste

```bash
python mask.py sample.log            # mask a file
cat error.txt | python mask.py       # or pipe text in
```

`sample.log` contains fake data only. The script prints the masked text and a short summary of what it replaced.

It is a habit helper, not a guarantee: always read what you are about to share.

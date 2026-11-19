# Example: one post, three formats

- `post.json`, `post.yaml`, `post.xml`: the same data.
- `read_formats.py`: reads the JSON and XML with Python's standard library and checks they describe the same post.

```bash
python read_formats.py
```

YAML needs a third-party parser in Python (`pip install pyyaml`), so the script only prints a note about it. To see JavaScript's big-number issue:

```bash
node -e "console.log(JSON.parse('{\"id\": 9007199254740993}').id)"
# prints 9007199254740992: the last digit changed
```

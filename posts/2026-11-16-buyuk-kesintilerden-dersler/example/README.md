# Example: fail-fast vs last known good config

A simulation inspired by the Cloudflare outage of 18 November 2025. No packages needed.

```bash
node config-reload.mjs fragile     # crashes when the config grows past the limit
node config-reload.mjs resilient   # rejects the bad config and keeps the last good one
```

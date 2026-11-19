# Example: unit and integration tests with `node --test`

Needs Node.js 20+ (the test runner is built in).

```bash
node --test
```

- `cart.mjs`: the code under test (pure function + a service that uses a repository).
- `cart.test.mjs`: unit tests (Arrange-Act-Assert) and one small integration test with an in-memory repository.

Try it: change `>= 1000` to `> 1000` in `cart.mjs` and run the tests again. One test turns red. That is the safety net working.

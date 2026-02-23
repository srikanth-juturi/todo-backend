# Backend Testing v1

## Run test suite

```bash
pytest -q
```

## Run with fast-fail mode

```bash
pytest --maxfail=1 --disable-warnings -q
```

## Run with coverage summary

```bash
pytest --cov=app --cov-report=term-missing
```

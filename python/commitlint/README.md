# Commitlint

https://github.com/pre-commit/pre-commit
https://github.com/pre-commit/pre-commit-hooks

```bash
pip install pre-commit
```

https://github.com/compilerla/conventional-pre-commit

.pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: <git sha or tag>
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [] # optional: list of Conventional Commits types to allow e.g. [feat, fix, ci, chore, test]
```

```bash
pre-commit install --hook-type commit-msg
```
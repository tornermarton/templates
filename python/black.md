# Black

https://github.com/psf/black

## Install

```bash
pip install black
```

## Config

```toml
[tool.black]
line-length = 88
target-version = ['py39', 'py310']
```

## PyCharm

Plugin needed: File Watchers

Configure file watcher to allow same behaviour as eslint --fix on save
```
Preferences > Tools > File Watchers > +

Name: black

File type: Python
Scope: Project Files

Program: [project]/venv/bin/black
Arguments: $FilePath$
Output paths to refresh: $FilePath$
Working directory: $ProjectFileDir$

Advanced options > only check: Trigger the file watcher regardless of syntax errors
```
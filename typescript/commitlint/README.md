# Commitlint and lint-staged w/ Husky

https://commitlint.js.org/#/
https://github.com/lint-staged/lint-staged

## Install

Commitlint
```shell
# Install and configure if needed
npm install --save-dev @commitlint/{cli,config-conventional}
# For Windows:
npm install --save-dev @commitlint/config-conventional @commitlint/cli
```

lint-staged
```shell
npm install --save-dev lint-staged
```

## Commitlint configuration

https://commitlint.js.org/#/reference-rules

.commitlintrc.json
```json
{
  "extends": [
    "@commitlint/config-conventional"
  ]
}
```

OR

.commitlintrc.yml
```yaml
extends: 
  - "@commitlint/config-conventional"
```

OR

package.json
```json
{
  ...
  "commitlint": {
    "extends": ["@commitlint/config-conventional"]
  }
}
```

## lint-staged configuration

https://github.com/lint-staged/lint-staged/tree/master#configuration

.lintstagedrc.json
```json
{
  "**/*.ts": [
    "npx eslint --fix"
  ]
}
```

OR

.lintstagedrc.yml
```yaml
"**/*.ts":
  - "npx eslint --fix"
```

OR

package.json
```json
{
  ...
 "lint-staged": {
    "**/*.ts": [
      "npx eslint --fix"
    ]
  }
}
```

## Husky

```shell
# Install Husky
npm install --save-dev husky
# Activate hooks (sets hooks path to [project]/.husky)
# User can use own hooks by setting back hooks path and referring 
# to husky hook in own git hook
npx husky install
# Add simple commit-msg hook (validates commit message)
npx husky add .husky/commit-msg  'npx --no-install commitlint --edit $1'
# Add pre-commit hook (lints staged files)
npx husky add .husky/pre-commit 'npx lint-staged'
```

All required resources should be sourced in `~/.huskyrc` 
to allow git clients to use these hooks properly (since
they might not run in the same context as the terminal
commands).

```shell
# NVM installed with brew
export NVM_DIR=~/.nvm
. $(brew --prefix nvm)/nvm.sh
```

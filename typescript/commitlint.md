# Commitlint w/ Husky

https://commitlint.js.org/#/

## Install

```bash
# Install and configure if needed
npm install --save-dev @commitlint/{cli,config-conventional}
# For Windows:
npm install --save-dev @commitlint/config-conventional @commitlint/cli
```

## Minimal configuration

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
  "name": "testproject",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@commitlint/cli": "^17.2.0",
    "@commitlint/config-conventional": "^17.2.0",
    "husky": "^8.0.2"
  },
  "commitlint": {
    "extends": ["@commitlint/config-conventional"]
  }
}

```

## Husky

```bash
# Install Husky v6
npm install --save-dev husky
# Activate hooks (sets hooks path to [project]/.husky)
# User can use own hooks by setting back hooks path and referring 
# to husky hook in own git hook
npx husky install
# Add simple commit-msg hook (validates commit message)
npx husky add .husky/commit-msg  'npx --no -- commitlint --edit'
```

All required resources should be sourced in `~/.huskyrc` 
to allow git clients to use these hooks properly (since
they might not run in the same context as the terminal
commands).

```bash
# NVM installed with brew
export NVM_DIR=~/.nvm
. $(brew --prefix nvm)/nvm.sh
```

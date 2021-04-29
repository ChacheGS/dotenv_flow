# dotenv_flow

Loads different dotenv files based on the value of the `PY_ENV` variable.

Values in more specific files override previous values.

Files have 2 flavors:

- public (ex: .env.dev) that should be committed to version control
- private (ex: .env.dev.local) that has preference over the previous one if present, and should **NOT**

This is the python version of Node's [dotenv-flow](https://www.npmjs.com/package/dotenv-flow)

dotenv files are loaded with [python-dotenv](https://pypi.org/project/python-dotenv/)

This should be added to version control ignore file:
```
# local .env* files
.env.local
.env.*.local
```

# dotenv_flow

Hierarchically load different dotenv files based on the value of the `PY_ENV` variable. Dotenv files will be searched
by name, by decreasing order of priority (specificity) to the selected environment.

As dotenv files are loaded, the process' environment (os.environ) is enriched with the variables found in those files.
Environment values that already exist will be left untouched.

Files have 2 flavors:

- public (ex: .env.dev) that should be committed to version control
- private (ex: .env.dev.local) that has preference over the previous one if present, and should **NOT**

This is the python version of Node's [dotenv-flow](https://www.npmjs.com/package/dotenv-flow).

dotenv files are loaded with [python-dotenv](https://pypi.org/project/python-dotenv/)

This should be added to version control ignore file:
```
# local .env* files
.env.local
.env.*.local
```

It's probably a good idea to also ignore plain `.env` files, as most tools will warn you
that it's a potential security risk. 
Instead, including a `.env-example` seems to be a popular way to document the environment variables in use. 

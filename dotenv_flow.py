import os

import logging
import warnings
from pathlib import Path

from typing import Sequence, Optional

from dotenv import load_dotenv, find_dotenv


def dotenv_flow(
    env: Optional[str] = ...,
    base_path: Optional[os.PathLike] = None,
    override: bool = False,
    interpolate: bool = True,
    **kwargs: Optional[str],
) -> Sequence[str]:
    """
    Loads different dotenv files based on the value of the PY_ENV variable, if set.
    Values in more specific files override previous values.
    Files have 2 flavors:
        - public (ex: .env.dev) that should be committed to version control
        - private (ex: .env.dev.local) that has preference over the previous one, if present

    This package aims to be the python version of: https://www.npmjs.com/package/dotenv-flow

    dotenv files are loaded with python-dotenv

    This entry should be added to version control ignore file:
    # local .env* files
    .env.local
    .env.*.local
    :param env: can be set to None explicitly to stop the warning and run with defaults only
    :param base_path: If provided, the base path to load the files from. Otherwise, the current working directory is used.
    :param override: passed to python-dotenv
    :param interpolate: passed to python-dotenv
    :return: a list with the paths of the files loaded
    """

    use_cwd = False
    if base_path is None:
        use_cwd = True

    if env in (..., None):
        env = os.getenv("PY_ENV", "")

    defaults = [".env.defaults", ".env"]
    if env not in (..., None):
        defaults.append(f".env.{env}")
    elif env is not None:
        warnings.warn("no env selected, using defaults only")

    loaded = {}
    for dft in reversed(defaults):
        for el in (f"{dft}.local", dft):
            if not use_cwd:
                el = Path(base_path) / el

            dotenv_path = find_dotenv(el, usecwd=use_cwd)
            if dotenv_path:
                loaded[dotenv_path] = load_dotenv(
                    dotenv_path, override=override, interpolate=interpolate, **kwargs
                )
    return [e for e in loaded if loaded[e]]

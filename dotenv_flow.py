import os

import logging
import warnings

from typing import Sequence, Text, Optional

from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)


def dotenv_flow(
    env: Optional[Text] = ...,
    usecwd: bool = False,
    override: bool = False,
    interpolate: bool = True,
    **kwargs: Optional[str],
) -> Sequence[Text]:
    """
    Loads different dotenv files based on the value of the PY_ENV variable.
    Values in more specific files override previous values.
    Files have 2 flavors:
        - public (ex: .env.dev) that should be committed to version control
        - private (ex: .env.dev.local) that has preference over the previous one if present

    This is the python version of: https://www.npmjs.com/package/dotenv-flow

    dotenv files are loaded with python-dotenv

    This entry should be added to version control ignore file:
    # local .env* files
    .env.local
    .env.*.local
    :param env: can be set to None explicitly to stop the warning and run with defaults only
    :param usecwd: passed to python-dotenv
    :param override: passed to python-dotenv
    :param interpolate: passed to python-dotenv
    :return: a list with the paths of the files loaded
    """

    defaults = [".env.defaults", ".env"]
    if env not in (..., None):
        defaults.append(f".env.{env}")
    elif env is not None:
        warnings.warn("no env selected, using defaults only")

    loaded = {}
    logger.debug(f"env is {'default' if env in (..., None) else env}")
    for dft in reversed(defaults):
        for el in (f"{dft}.local", dft):
            dotenv_path = find_dotenv(el, usecwd=usecwd)
            if dotenv_path:
                logger.info(f"loading {dotenv_path}")
                loaded[dotenv_path] = load_dotenv(
                    dotenv_path, override=override, interpolate=interpolate, **kwargs
                )
    return [e for e in loaded if loaded[e]]


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    dotenv_flow("test_envs")
    for e in ["", "test", "pro", "dev"]:
        print(dotenv_flow(e))

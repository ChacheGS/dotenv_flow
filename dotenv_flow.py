import os

import logging
from StringIO import StringIO
from typing import Union, Optional

from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)


def dotenv_flow(raise_error_if_not_found: bool = False,
                usecwd: bool = False,
                stream: Union[StringIO, StringIO[str], None] = None,
                verbose: bool = False,
                override: bool = False,
                interpolate: bool = True,
                **kwargs: Optional[str]) -> bool:
    """
    Loads different dotenv files based on the value of the PY_ENV variable. Values in more specific files override previous values.
    Files have 2 versions:
        - public (ex: .env.dev) that should be committed to version control
        - private (ex: .env.dev.local) that has preference over the previous one if present

    This is the python version of: https://www.npmjs.com/package/dotenv-flow

    dotenv files are loaded with python-dotenv

    This entry should be added to version control ignore file:
    # local .env* files
    .env.local
    .env.*.local
    :param verbose:
    :param stream:
    :param usecwd:
    :param raise_error_if_not_found:
    :param override:
    :param interpolate:
    :return:
    """
    env = os.environ.get("PY_ENV")

    envs = [".env.defaults", ".env"]
    if env:
        envs.append(f".env.{env}")

    logger.debug(f"PY_ENV is {env}")
    for e in reversed(envs):
        for el in (f"{e}.local", e):
            dotenv_path = find_dotenv(el, raise_error_if_not_found=raise_error_if_not_found, usecwd=usecwd)
            if dotenv_path:
                logger.info(f"loading {dotenv_path}")
                load_dotenv(dotenv_path, stream=stream, verbose=verbose, override=override, interpolate=interpolate,
                            **kwargs)
    return True


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    dotenv_flow("test_envs")
    for e in ["", "test", "pro", "dev"]:
        os.environ["PY_ENV"] = e
        dotenv_flow(path="test_envs")

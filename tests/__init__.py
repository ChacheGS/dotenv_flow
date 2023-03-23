import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, MutableMapping, Optional

BASE_DIR = Path(__file__).parent


class EnvFilesManager:
    def __init__(self, base_dir: os.PathLike = BASE_DIR):
        self.files = set()
        self.base_dir = Path(base_dir)

    def new_file(self, name: Optional[str], local: bool):
        name = f".env.{name}" if name else ".env"
        suffix = ".local" if local else ""
        name = f"{name}{suffix}".lower()
        self.files.update([name])
        return self.base_dir / name

    def clear(self):
        for env in self.files:
            file = BASE_DIR / env
            if file.is_file() and file.stem.startswith(".env"):
                file.unlink()


class EnvironManager:
    def __init__(
        self,
        files: EnvFilesManager,
        name: Optional[str] = None,
    ):
        self.name = name
        self.files = files
        self._old_env: MutableMapping[str, str] = {}

        self.create_files()

    def create_files(self) -> None:
        """
        Create .env files for this env, both in public and private mode.
        """
        for private in (True, False):
            for env in (self.name, None):
                with self.files.new_file(env, private).open("w") as env_file:
                    value = var_value(env, private)
                    env_file.write(f"PRIVATE={value}\n")
                    if not private:  # add another var to public files only
                        value = var_value(env, False)
                        env_file.write(f"PUBLIC={value}\n")

    def __enter__(self):
        """
        Swap os.environ with a fresh dict, that is prepopulated with
        the environment selector variable.
        """
        self._old_env = os.environ

        if self.name not in (None, ...):
            os.environ = {"PY_ENV": self.name}
        else:
            os.environ = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Restore the original os.environ, for cleanliness.
        """
        os.environ = self._old_env


def var_value(env: Optional[str], private: Optional[bool]) -> str:
    """
    Compute the value we should give to the variable.

    :param env: the name of the environment
    :param private: whether it's the public or private file
    :return: the computed value for the variable
    """
    mode = "private" if private else "public"
    env = env if env not in [..., None] else "common"
    parts = [env, mode]

    with open("/tmp/wtf.log", "w") as f:
        f.write(f"{env} {mode}\n")

    return "_".join(parts).upper()


def expected_environ(env: Optional[str], private: Optional[bool]) -> Dict[str, str]:
    """
    Since all files are present for every test, when no
    env is selected the expected value is always the private one.

    Public files have one more variable called PUBLIC.

    :param env: the name of the environment
    :param private: whether it's the public or private file
    :return: the expected environment for this combination
    """

    exp = {
        "PUBLIC": var_value(env, False),
        "PRIVATE": var_value(env, private),
    }
    if env and env is not ...:
        exp["PY_ENV"] = env  # env selector

    # if private:
    # exp["PUBLIC"] = var_value(env, False)
    # exp.pop("PRIVATE")

    return exp

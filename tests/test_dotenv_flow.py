import os
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import TestCase

from parameterized import parameterized

from dotenv_flow import dotenv_flow

BASE_DIR = Path(__file__).parent.parent


def expectations(args):
    # assert len(args) == 4
    exp = []
    for a in args:
        for private in (True, False):
            args = (
                f"{a if a else 'empty'}_{'private' if private else 'public'}",
                a,
                private,
                f".env{f'.{a}' if a else ''}{'.local' if private else ''}",
            )
            exp.append(args)
    return exp


class Test(TestCase):
    __ENVS_NAMES = {
        "edge": [..., None],
        "regular": ["", "dev", "test", "pro"],
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls._envfiles = set()

    @classmethod
    def tearDownClass(cls) -> None:
        for env in cls._envfiles:
            file = BASE_DIR / env
            if file.is_file() and file.stem.startswith(".env"):
                file.unlink()

    def setUp(self) -> None:
        if os.getenv("VAR"):
            os.environ.pop("VAR")

    @contextmanager
    def environment(self, env: str, private: bool):
        if env:
            os.environ["PY_ENV"] = env

        name = f".env.{env}" if env else ".env"
        names = [name]

        if private:
            names.append(
                f"{name}.local"
            )

        for env in names:
            with (BASE_DIR / env).open("w") as f:
                print(f"VAR={env}", file=f)

        self._envfiles.update(names)

        yield

    @parameterized.expand(
        expectations(__ENVS_NAMES["regular"])
    )
    def test_dotenv_flow(self, name, env, private, expected):
        with self.environment(env, private):
            dotenv_flow(env)
            self.assertEqual(expected, os.getenv("VAR"))

    @parameterized.expand(
        expectations(__ENVS_NAMES["regular"])
    )
    def test_when_name_unset(self, name, env, private, expected):
        with self.environment(env, private):
            with self.assertWarns(Warning):
                dotenv_flow()
            self.assertEqual(expected, os.getenv("VAR"))

    @parameterized.expand(
        expectations(__ENVS_NAMES["regular"])
    )
    def test_when_name_is_none(self, name, env, private, expected):
        with self.environment(env, private):
            dotenv_flow(None)
            self.assertEqual(expected, os.getenv("VAR"))

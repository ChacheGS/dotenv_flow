import os
from typing import Iterable, Optional
from unittest import TestCase

from parameterized import parameterized

from dotenv_flow import dotenv_flow
from tests import EnvFilesManager, EnvironManager, expected_environ


def expectations(envs: Iterable[Optional[str]]):
    """
    Build the arguments for the test functions.
    """
    args_tuples = []
    for env in envs:
        # make the public and private versions of the expectations
        # since all files are present for all tests. expected env will always be the private one
        for private in (True, False):
            expected = expected_environ(env, True)

            mode = "private" if private else "public"

            args = (f"{env if env else 'empty'}_{mode}", env, expected)
            args_tuples.append(args)
    return args_tuples


class Test(TestCase):
    __ENVS_NAMES = ["dev", "test", "pro"]

    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = EnvFilesManager()

    def tearDown(self) -> None:
        """
        Remove the files that we created earlier.
        """
        self.manager.clear()

    @parameterized.expand(expectations(__ENVS_NAMES))
    def test_dotenv_flow(self, name, env, expected):
        with EnvironManager(self.manager, env):
            dotenv_flow(env, base_path=self.manager.base_dir)
            self.assertEqual(expected, os.environ)

    @parameterized.expand(expectations([...]))
    def test_when_name_unset(self, name, env, expected):
        with EnvironManager(self.manager, env):
            with self.assertWarns(Warning):
                dotenv_flow(base_path=self.manager.base_dir)
            self.assertEqual(expected, os.environ)

    @parameterized.expand(expectations([None]))
    def test_when_name_is_none(self, name, env, expected):
        with EnvironManager(self.manager, env):
            dotenv_flow(None, base_path=self.manager.base_dir)
            self.assertEqual(expected, os.environ)

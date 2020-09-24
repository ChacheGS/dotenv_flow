from unittest import TestCase

from parameterized import parameterized

from dotenv_flow import dotenv_flow


def expectations(args):
    # assert len(args) == 4
    exp = []
    for a in args:
        exp.append((a if a else "<empty>", a, 5 if a else 3))
    return exp


class Test(TestCase):
    @parameterized.expand(
        expectations(["", "test", "pro", "dev"])
    )
    def test_dotenv_flow(self, name, environment, expected):
        assert len(dotenv_flow(environment)) == expected

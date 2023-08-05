import unittest

from sacrerouge.common.testing.util import sacrerouge_command_exists


class TestDUC2007Subcommand(unittest.TestCase):
    def test_command_exists(self):
        assert sacrerouge_command_exists(['setup-dataset', 'duc2007'])

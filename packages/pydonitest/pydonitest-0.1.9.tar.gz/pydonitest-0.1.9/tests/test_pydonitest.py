#!/usr/bin/env python

"""Tests for `pydonitest` package."""


import unittest
from click.testing import CliRunner

from pydonitest import pydonitest
from pydonitest import cli


class TestPydonitest(unittest.TestCase):
    """Tests for `pydonitest` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'pydonitest.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_advanced_strip(self):
        runner = CliRunner()
        result = runner.invoke(pydonitest.advanced_strip, ['  test  '])
        assert result.exit_code == 0
        assert result.output == 'test'

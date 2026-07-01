"""Tests for interfaces.cli.commands — args parsing and execution."""

import pytest

from mechlab.interfaces.cli.commands import build_parser, run_beam_command


def test_parser_requires_two_supports():
    parser = build_parser()
    args = parser.parse_args([
        "beam", "--length", "4.0", "--E", "200e9", "--yield", "250e6",
        "--I", "9.19e-6", "--area", "2.3e-3", "--c", "0.076",
        "--support", "0.0",  # only one support
    ])
    with pytest.raises(SystemExit):
        run_beam_command(args)


def test_run_beam_command_produces_report_text():
    parser = build_parser()
    args = parser.parse_args([
        "beam", "--length", "4.0", "--E", "200e9", "--yield", "250e6",
        "--I", "9.19e-6", "--area", "2.3e-3", "--c", "0.076",
        "--support", "0.0", "--support", "4.0",
        "--point-load", "2.0", "5000",
    ])
    output = run_beam_command(args)
    assert "Beam Analysis Report" in output
    assert "Reactions" in output

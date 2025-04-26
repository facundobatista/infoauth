# Copyright 2018-2025 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://github.com/facundobatista/infoauth

"""Tests for infrastructure stuff."""

import io
import os
import subprocess

import docutils.core
import pytest
import rst2html5_


def _get_python_filepaths(self, roots):
    """Helper to retrieve paths of Python files."""
    python_paths = []
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if filename.endswith(".py"):
                    python_paths.append(os.path.join(dirpath, filename))
    return python_paths


def test_ruff():
    cmd = [
        "ruff",
        "--quiet",  # avoid messages if all went ok
        "check",
        "--preview",  # some rules are only enabled in preview mode
        # generic settings
        "--line-length=99",
        "--select=E,W,F,C,N",
        # paths
        "infoauth",
        "tests",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stdout:
        pytest.fail("There are issues!\n" + proc.stdout)


def test_readme_sanity(mocker):
    fake_stdout = io.StringIO()  # just to ignore the output
    mocker.patch('sys.stdout', fake_stdout)
    fake_stderr = io.StringIO()  # will have content if there are problems
    mocker.patch('sys.stderr', fake_stderr)

    with open('README.rst', 'rt', encoding='utf8') as fh:
        docutils.core.publish_file(source=fh, writer=rst2html5_.HTML5Writer())

    errors = fake_stderr.getvalue()
    if errors:
        pytest.fail("There are issues!\n" + errors)

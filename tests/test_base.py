# Copyright 2018 Facundo Batista
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
import random
import string
import tempfile
import unittest
from textwrap import dedent
from unittest.mock import patch

from infoauth import _create, _show, dump, load


def get_temp_file(testcase):
    """Provide a temporary file."""
    descriptor, filepath = tempfile.mkstemp(prefix="test-temp-file")
    os.close(descriptor)
    testcase.addCleanup(lambda: os.path.exists(filepath) and os.remove(filepath))
    return filepath


class CmdLineTestCase(unittest.TestCase):

    def test_show_ok_one_string(self):
        # create a sample file
        tempfile = get_temp_file(self)
        data = {'foo': 'bar'}
        dump(data, tempfile)

        # show it and check
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show(tempfile)

        result = fake_stdout.getvalue()
        self.assertEqual(result, dedent("""\
            foo: 'bar'
        """))

    def test_show_ok_one_other_data_type(self):
        # create a sample file
        tempfile = get_temp_file(self)
        data = {'foo': 55}
        dump(data, tempfile)

        # show it and check
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show(tempfile)

        result = fake_stdout.getvalue()
        self.assertEqual(result, dedent("""\
            foo: 55
        """))

    def test_show_ok_several(self):
        # create a sample file
        tempfile = get_temp_file(self)
        data = {'foo': 55, 'bar': 'bleh', 'another': 88}
        dump(data, tempfile)

        # show it and check
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show(tempfile)

        result = fake_stdout.getvalue()
        self.assertEqual(result, dedent("""\
            another: 88
            bar: 'bleh'
            foo: 55
        """))

    def test_show_missing_file(self):
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show('test-missing')

        result = fake_stdout.getvalue()
        self.assertEqual(result, dedent("""\
            ERROR: [Errno 2] No such file or directory: 'test-missing'
        """))

    def test_create_ok_simple(self):
        tempfile = get_temp_file(self)
        _create(tempfile, ['foo=57'])

        # check
        saved = load(tempfile)
        self.assertEqual(saved, {'foo': '57'})

    def test_create_ok_several(self):
        tempfile = get_temp_file(self)
        _create(tempfile, ['foo=57', 'bar=bleh'])

        # check
        saved = load(tempfile)
        self.assertEqual(saved, {'foo': '57', 'bar': 'bleh'})

    def test_create_bad_option_no_equal(self):
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _create('nomatterpath', ['foo57', 'bar=bleh'])

        result = fake_stdout.getvalue()
        self.assertEqual(result, dedent("""\
            ERROR: bad option 'foo57'
        """))

    def test_create_weird_equals(self):
        tempfile = get_temp_file(self)
        _create(tempfile, ['foo=', '=bleh', 'a=b=c'])

        # check
        saved = load(tempfile)
        self.assertEqual(saved, {'foo': '', '': 'bleh', 'a': 'b=c'})


class AsModuleTestCase(unittest.TestCase):

    def test_sanity_sequence(self):
        tempfile = get_temp_file(self)

        # dump random stuff
        numbers = [random.randint(-3, 200) for _ in range(len(string.ascii_letters))]
        original_data = dict(zip(string.ascii_letters, numbers))
        dump(original_data, tempfile)

        # load and compare
        retrieved_data = load(tempfile)
        self.assertEqual(original_data, retrieved_data)

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
import random
import string
from textwrap import dedent
from unittest.mock import patch

import pytest

from infoauth import _create, _show, dump, load


class TestCmdLine:

    def test_show_ok_one_string(self, tmp_path):
        # create a sample file
        tempfile = tmp_path / "tempfile"
        data = {'foo': 'bar'}
        dump(data, tempfile)

        # show it and check
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show(tempfile)

        result = fake_stdout.getvalue()
        assert result == dedent("""\
            foo: 'bar'
        """)

    def test_show_ok_one_other_data_type(self, tmp_path):
        # create a sample file
        tempfile = tmp_path / "tempfile"
        data = {'foo': 55}
        dump(data, tempfile)

        # show it and check
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show(tempfile)

        result = fake_stdout.getvalue()
        assert result == dedent("""\
            foo: 55
        """)

    def test_show_ok_several(self, tmp_path):
        # create a sample file
        tempfile = tmp_path / "tempfile"
        data = {'foo': 55, 'bar': 'bleh', 'another': 88}
        dump(data, tempfile)

        # show it and check
        fake_stdout = io.StringIO()
        with patch('sys.stdout', fake_stdout):
            _show(tempfile)

        result = fake_stdout.getvalue()
        assert result == dedent("""\
            another: 88
            bar: 'bleh'
            foo: 55
        """)

    def test_show_missing_file(self):
        with pytest.raises(OSError) as exc:
            _show('test-missing')
        assert str(exc.value) == "[Errno 2] No such file or directory: 'test-missing'"

    def test_create_ok_simple(self, tmp_path):
        tempfile = tmp_path / "tempfile"
        _create(tempfile, ['foo=57'])

        # check
        saved = load(tempfile)
        assert saved == {'foo': '57'}

    def test_create_ok_several(self, tmp_path):
        tempfile = tmp_path / "tempfile"
        _create(tempfile, ['foo=57', 'bar=bleh'])

        # check
        saved = load(tempfile)
        assert saved == {'foo': '57', 'bar': 'bleh'}

    def test_create_bad_option_no_equal(self):
        with pytest.raises(ValueError) as exc:
            _create('nomatterpath', ['foo57', 'bar=bleh'])
        assert str(exc.value) == "ERROR: bad option 'foo57'"

    def test_create_weird_equals(self, tmp_path):
        tempfile = tmp_path / "tempfile"
        _create(tempfile, ['foo=', '=bleh', 'a=b=c'])

        # check
        saved = load(tempfile)
        assert saved == {'foo': '', '': 'bleh', 'a': 'b=c'}

    def test_create_repeated(self, tmp_path):
        tempfile = tmp_path / "tempfile"
        _create(tempfile, ['foo=57'])
        _create(tempfile, ['foo=59'])

        # check
        saved = load(tempfile)
        assert saved == {'foo': '59'}


class TestAsModule:

    def test_sanity_sequence(self, tmp_path):
        tempfile = tmp_path / "tempfile"

        # dump random stuff
        numbers = [random.randint(-3, 200) for _ in range(len(string.ascii_letters))]
        original_data = dict(zip(string.ascii_letters, numbers))
        dump(original_data, tempfile)

        # load and compare
        retrieved_data = load(tempfile)
        assert original_data == retrieved_data

    def test_permissions_after_saving(self, tmp_path):
        tempfile = tmp_path / "tempfile"
        tempfile.touch()
        assert (os.stat(tempfile).st_mode & 0o777) != 0o400

        # dump some stuff and check permission
        dump({'foo': 2}, tempfile)
        assert (os.stat(tempfile).st_mode & 0o777) == 0o400

    def test_create_repeated(self, tmp_path):
        tempfile = tmp_path / "tempfile"
        dump({'foo': 2}, tempfile)
        dump({'foo': 3}, tempfile)

        # check
        saved = load(tempfile)
        assert saved == {'foo': 3}

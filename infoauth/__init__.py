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

"""Main code."""

import os
import pickle
import zlib


def load(filepath):
    """Load slightly scrambled data from filepath."""
    with open(filepath, 'rb') as fh:
        compressed = fh.read()
    pickled = zlib.decompress(compressed)
    data = pickle.loads(pickled)
    return data


def dump(data, filepath):
    """Dump data to filepath slightly scrambled."""
    pickled = pickle.dumps(data)
    compressed = zlib.compress(pickled)
    if os.path.exists(filepath):
        os.chmod(filepath, 0o600)  # allow writing to be able to dump, will go back to RO
    with open(filepath, 'wb') as fh:
        fh.write(compressed)
    os.chmod(filepath, 0o400)  # read only for owner alone


def _show(filepath):
    """Show the content of the file to stdout."""
    data = load(filepath)
    for key, value in sorted(data.items()):
        print("{}: {!r}".format(key, value))


def _create(filepath, data_as_pair_kv):
    """Create the file with the data information."""
    data_as_dict = {}
    for k_eq_v in data_as_pair_kv:
        try:
            k, v = map(str.strip, k_eq_v.split("=", maxsplit=1))
        except ValueError:
            raise ValueError("ERROR: bad option " + repr(k_eq_v))
        data_as_dict[k] = v

    # save!
    dump(data_as_dict, filepath)

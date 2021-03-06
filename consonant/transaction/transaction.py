# Copyright (C) 2013 Codethink Limited.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Classes for representing transactions."""


class Transaction(object):

    """Class to represent a transaction."""

    def __init__(self, actions):
        self.actions = actions

    def begin(self):
        """Return the begin action of the transaction."""

        return self.actions[0]

    def commit(self):
        """Return the commit action of the transaction."""

        return self.actions[-1]

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        else:
            return self.actions == other.actions

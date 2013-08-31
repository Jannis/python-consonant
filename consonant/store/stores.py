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


"""Classes and interfaces to implement local and remote stores."""


import os
import urlparse


class Store(object):  # pragma: no cover

    """Abstract base class for store implementations."""

    def refs(self):
        """Return a set of Ref objects for all Git refs in the store."""
        raise NotImplementedError

    def ref(self, name):
        """Return the Ref object for the Git ref with the given name."""
        raise NotImplementedError

    def commit(self, sha1):
        """Return the Commit object for the Git commit with the given SHA1."""
        raise NotImplementedError

    def uuid(self, commit):
        """Return the store UUUID for the given commit."""
        raise NotImplementedError

    def schema(self, commit):
        """Return the schema UUID for the given commit."""
        raise NotImplementedError

    def services(self, commit):
        """Return service aliases for the given commit."""
        raise NotImplementedError

    def classes(self, commit):
        """Return object classes for the given commit."""
        raise NotImplementedError

    def klass(self, commit, name):
        """Return the object classes for the given commit and class name."""
        raise NotImplementedError

    def objects(self, commit, klass=None):
        """Return all objects in the given commit and, optionally, class."""
        raise NotImplementedError

    def object(self, commit, uuid):
        """Return the object with the given UUID in the given commit."""
        raise NotImplementedError

    def create_ref(self, type, commit, author, committer, message):
        """Create a new Git ref in the store."""
        raise NotImplementedError

    def create_commit(self, transaction, ref=None, parent=None):
        """Create a new commit in the store from a transaction."""
        raise NotImplementedError

    def sync(self):
        """Sync any changes made to the store back to its real repository."""
        raise NotImplementedError

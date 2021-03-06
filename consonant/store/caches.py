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


"""Caching mechanisms for improving object and raw property loading."""


import pylibmc


class ObjectCache(object):  # pragma: no cover

    """Base class for object cache implementations."""

    def read_properties(self, uuid, sha1):
        """Look up the object properties for a given SHA1.

        Returns an object properties dictionary if the UUID1 and SHA1 tuple
        is found in the cache. Otherwise returns None.

        """

        raise NotImplementedError

    def write_properties(self, uuid, sha1, properties):
        """Store an object properties dictionary for a given UUID and SHA1."""

        raise NotImplementedError

    def read_raw_property_data(self, sha1):
        """Look up the raw property data for a given SHA1.

        Returns the data in exactly the way it was stored if the SHA1
        is found in the cache. Otherwise returns None.

        """

        raise NotImplementedError

    def write_raw_property_data(self, sha1, data):
        """Store raw property data for a given SHA1."""

        raise NotImplementedError


class MemcachedObjectCache(ObjectCache):  # pragma: no cover

    """Object cache implementation for Memcached."""

    def __init__(self, servers):
        ObjectCache.__init__(self)

        self.mc = pylibmc.Client(servers)
        self.mc_pool = pylibmc.ThreadMappedPool(self.mc)

    def read_properties(self, uuid, sha1):
        """Look up the object properties for a given SHA1.

        Returns an object properties dictionary if the UUID1 and SHA1 tuple
        is found in the cache. Otherwise returns None.

        """

        with self.mc_pool.reserve() as mc:
            return mc.get('%s,%s' % (uuid, sha1))

    def write_properties(self, uuid, sha1, properties):
        """Store an object properties dictionary for a given UUID and SHA1."""

        with self.mc_pool.reserve() as mc:
            mc.set('%s,%s' % (uuid, sha1), properties)

    def read_raw_property_data(self, sha1):
        """Look up the raw property data for a given SHA1.

        Returns the data in exactly the way it was stored if the SHA1
        is found in the cache. Otherwise returns None.

        """

        with self.mc_pool.reserve() as mc:
            return mc.get(sha1)

    def write_raw_property_data(self, sha1, data):
        """Store raw property data for a given SHA1."""

        with self.mc_pool.reserve() as mc:
            mc.set(sha1, data)

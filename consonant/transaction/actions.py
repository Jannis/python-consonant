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


"""Classes for representing actions in transactions."""


class Action(object):

    """Class to represent an action of a transaction."""

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        raise NotImplementedError


class BeginAction(Action):

    """Class to represent the begin action of a transaction."""

    def __init__(self, id, source):
        Action.__init__(self, id)
        self.source = source

    def __eq__(self, other):
        if not isinstance(other, BeginAction):
            return False
        else:
            return self.id == other.id and self.source == other.source


class CommitAction(Action):

    """Class to represent the commit action of a transaction."""

    def __init__(self, id, target, author, author_date,
                 committer, committer_date, message):
        Action.__init__(self, id)
        self.target = target
        self.author = author
        self.author_date = author_date
        self.committer = committer
        self.committer_date = committer_date
        self.message = message

    def __eq__(self, other):
        if not isinstance(other, CommitAction):
            return False
        else:
            return self.id == other.id \
                and self.target == other.target \
                and self.author == other.author \
                and self.author_date == other.author_date \
                and self.committer == other.committer \
                and self.committer_date == other.committer_date \
                and self.message == other.message


class CreateAction(Action):

    """Class to represent create actions in transactions."""

    def __init__(self, id, klass, properties):
        Action.__init__(self, id)
        self.klass = klass
        self.properties = dict((p.name, p) for p in properties)

    def __eq__(self, other):
        if not isinstance(other, CreateAction):
            return False
        else:
            return self.id == other.id \
                and self.klass == other.klass \
                and self.properties == other.properties


class DeleteAction(Action):

    """Class to represent delete actions in transactions."""

    def __init__(self, id, uuid):
        Action.__init__(self, id)
        self.uuid = uuid

    def __eq__(self, other):
        if not isinstance(other, DeleteAction):
            return False
        else:
            return self.id == other.id and self.uuid == other.uuid


class UpdateAction(Action):

    """Class to represent update actions in transactions."""

    def __init__(self, id, uuid, properties):
        Action.__init__(self, id)
        self.uuid = uuid
        self.properties = dict((p.name, p) for p in properties)

    def __eq__(self, other):
        if not isinstance(other, UpdateAction):
            return False
        else:
            return self.id == other.id \
                and self.uuid == other.uuid \
                and self.properties == other.properties


class UpdateRawPropertyAction(Action):

    """Class to represent update-raw-property actions in transactions."""

    def __init__(self, id, uuid, property, content_type, data):
        Action.__init__(self, id)
        self.uuid = uuid
        self.property = property
        self.content_type = content_type
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, UpdateRawPropertyAction):
            return False
        else:
            return self.id == other.id \
                and self.uuid == other.uuid \
                and self.property == other.property \
                and self.content_type == other.content_type \
                and self.data == other.data


class UnsetRawPropertyAction(Action):

    """Class to represent unset-raw-property actions in transactions."""

    def __init__(self, id, uuid, property):
        Action.__init__(self, id)
        self.uuid = uuid
        self.property = property

    def __eq__(self, other):
        if not isinstance(other, UnsetRawPropertyAction):
            return False
        else:
            return self.id == other.id \
                and self.uuid == other.uuid \
                and self.property == other.property
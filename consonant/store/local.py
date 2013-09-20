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


"""Classes to load from and write to local services."""


import pygit2
import urllib2
import yaml

from consonant import schema
from consonant.service import services
from consonant.store import git, objects, properties, references, timestamps


class LocalStore(services.Service):

    """Store implementation for local services."""

    def __init__(self, url, register):
        services.Service.__init__(self)
        self.register = register
        self.repo = pygit2.Repository(url)
        self.cache = None

    def refs(self):
        """Return a set of Ref objects for all Git refs in the store."""

        refs = {}
        for ref in self._list_refs():
            commit = ref.get_object()
            head = self._parse_commit(commit)

            if ref.name.startswith('refs/tags'):
                refs[ref.name] = git.Ref('tag', ref.name, head)
            else:
                refs[ref.name] = git.Ref('branch', ref.name, head)
        return refs

    def ref(self, name):
        """Return the Ref object for a specific Git ref in the store."""

        refs = self.refs()
        if name in refs:
            return refs[name]
        else:
            for ref in refs.itervalues():
                if name in ref.aliases:
                    return ref
            names = set(refs.keys())
            for ref in refs.itervalues():
                names.update(ref.aliases)
            raise services.RefNotFoundError(name, names)

    def commit(self, sha1):
        """Return the Commit object for a specific commit in the store."""

        try:
            commit = self.repo[sha1]
        except:
            raise services.CommitNotFoundError(sha1)
        return self._parse_commit(commit)

    def name(self, commit):
        """Return the name the store has in the given commit."""

        data = self._load_metadata(commit)
        return data['name']

    def schema(self, commit):
        """Return the schema name the store uses in the given commit."""

        data = self._load_metadata(commit)
        name = data['schema']
        url = self.register.schema_url(name)
        stream = urllib2.urlopen(url)
        return schema.parsers.SchemaParser().parse(stream)

    def services(self, commit):
        """Return the service aliases used in the store at the given commit."""

        data = self._load_metadata(commit)
        return data.get('services', {})

    def classes(self, commit):
        """Return the classes present in the given commit of the store."""

        commit_object = self.repo[commit.sha1]
        classes = {}
        for class_entry in commit_object.tree:
            if class_entry.name == 'consonant.yaml':
                continue
            object_references = self._class_object_references(class_entry)
            klass = objects.ObjectClass(class_entry.name, object_references)
            classes[class_entry.name] = klass
        return classes

    def klass(self, commit, name):
        """Return the class for the given name and commit of the store."""

        commit_object = self.repo[commit.sha1]
        if name != 'consonant.yaml' and name in commit_object.tree:
            class_entry = commit_object.tree[name]
            object_references = self._class_object_references(class_entry)
            return objects.ObjectClass(class_entry.name, object_references)
        else:
            raise services.ClassNotFoundError(commit, name)

    def objects(self, commit, klass=None):
        """Return the objects present in the given commit of the store."""

        if klass:
            return sorted(self._class_objects(commit, klass))
        else:
            classes = self.classes(commit)
            objects = {}
            for klass in classes.itervalues():
                objects[klass.name] = sorted(
                    self._class_objects(commit, klass))
            return objects

    def object(self, commit, uuid, klass=None):
        """Return the object with the given UUID from a commit of the store."""

        if klass:
            object = self._class_object(commit, uuid, klass)
            if object:
                return object
            else:
                raise services.ObjectNotFoundError(commit, uuid, klass)
        else:
            classes = self.classes(commit)
            for klass in classes.itervalues():
                object = self._class_object(commit, uuid, klass)
                if object:
                    return object
            raise services.ObjectNotFoundError(commit, uuid)

    def _class_object(self, commit, uuid, klass):
        objects = [x for x in klass.objects if x.uuid == uuid]
        if objects:
            commit_object = self.repo[commit.sha1]
            class_entry = commit_object.tree[klass.name]
            class_tree = self.repo[class_entry.oid]
            object_entry = class_tree[uuid]
            return self._load_object(commit, klass, object_entry)
        else:
            return None

    def _class_object_references(self, class_entry):
        """Return references to all objects of a class in a commit."""

        object_references = set()
        object_entries = self.repo[class_entry.oid]
        for object_entry in object_entries:
            reference = references.Reference(object_entry.name, None, None)
            object_references.add(reference)
        return object_references

    def _class_objects(self, commit, klass):
        """Return the objects of a class in the given commit of the store."""

        commit_object = self.repo[commit.sha1]
        class_tree_entry = commit_object.tree[klass.name]
        class_tree = self.repo[class_tree_entry.oid]
        objects = set()
        for object_entry in class_tree:
            object = self._load_object(commit, klass, object_entry)
            objects.add(object)
        return objects

    def _list_refs(self):
        head = self.repo.lookup_reference('HEAD')
        yield head
        for name in self.repo.listall_references():
            if not name.startswith('refs/remotes'):
                ref = self.repo.lookup_reference(name)
                yield ref

    def _parse_commit(self, commit):
        return git.Commit(
            commit.oid.hex,
            str('%s <%s>' % (
                commit.author.name, commit.author.email)),
            timestamps.Timestamp(commit.author.time,
                                 commit.author.offset),
            str('%s <%s>' % (
                commit.committer.name, commit.committer.email)),
            timestamps.Timestamp(commit.committer.time,
                                 commit.committer.offset),
            str(commit.message),
            [x.oid.hex for x in commit.parents])

    def _load_metadata(self, commit):
        commit_object = self.repo[commit.sha1]
        entry = commit_object.tree['consonant.yaml']
        blob = self.repo[entry.oid]
        return yaml.load(blob.data)

    def _load_object(self, commit, klass, object_entry):
        object_tree = self.repo[object_entry.oid]
        properties_entry = object_tree['properties.yaml']
        properties_sha1 = properties_entry.oid.hex
        object = None
        if self.cache:
            object = self.cache.read_object(object_entry.name, properties_sha1)
        if not object:
            object = self._parse_object(
                commit, klass, object_entry, properties_entry)
        if self.cache:
            self.cache.write_object(object_entry.name, properties_sha1, object)
        return object

    def _parse_object(self, commit, klass, object_entry, properties_entry):
        blob = self.repo[properties_entry.oid]
        properties_data = yaml.load(blob.data)
        return objects.Object(
            object_entry.name, klass,
            [properties.Property(k, v)
             for (k, v) in properties_data.iteritems()])

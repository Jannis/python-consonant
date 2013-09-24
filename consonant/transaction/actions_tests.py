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


"""Unit tests for classes representing actions in transactions."""


import unittest

from consonant.store import properties
from consonant.transaction import actions


class ActionTests(unittest.TestCase):

    """Unit tests for the Action class."""

    def test_constructor_sets_action_id(self):
        """Verify that the constructor sets the action id."""

        action = actions.Action('1')
        self.assertEqual(action.id, '1')

        action = actions.Action('foo')
        self.assertEqual(action.id, 'foo')


class BeginActionTests(unittest.TestCase):

    """Unit tests for the BeginAction class."""

    def test_constructor_sets_action_id_and_source_sha1(self):
        """Verify that the constructor sets the action id and source."""

        action = actions.BeginAction(
            '1', 'b5f538a424ef18782dfe11fe5be764275394a14a')
        self.assertEqual(action.id, '1')
        self.assertEqual(
            action.source, 'b5f538a424ef18782dfe11fe5be764275394a14a')

        action = actions.BeginAction(
            '2', 'b5f538a424ef18782dfe11fe5be764275394a14a')
        self.assertEqual(action.id, '2')
        self.assertEqual(
            action.source, 'b5f538a424ef18782dfe11fe5be764275394a14a')

        action = actions.BeginAction(
            '2', '4a723c3748b984962f58dfcfc274995f4a7e75db')
        self.assertEqual(action.id, '2')
        self.assertEqual(
            action.source, '4a723c3748b984962f58dfcfc274995f4a7e75db')


class CommitActionTests(unittest.TestCase):

    """Unit tests for the CommitAction class."""

    def test_constructor_sets_action_id_and_other_fields(self):
        """Verify that the constructor sets the action id and other fields."""

        action = actions.CommitAction(
            'foo', 'refs/heads/master',
            'Jannis Pohlmann <jannis.pohlmann@codethink.co.uk>',
            '1379947345 +0100',
            'Jannis Pohlmann <jannis.pohlmann@codethink.co.uk>',
            '1380614011 +0100',
            'This is a commit message')

        self.assertEqual(action.id, 'foo')
        self.assertEqual(action.target, 'refs/heads/master')
        self.assertEqual(action.author,
                         'Jannis Pohlmann <jannis.pohlmann@codethink.co.uk>')
        self.assertEqual(action.author_date, '1379947345 +0100')
        self.assertEqual(action.committer,
                         'Jannis Pohlmann <jannis.pohlmann@codethink.co.uk>')
        self.assertEqual(action.committer_date, '1380614011 +0100')
        self.assertEqual(action.message, 'This is a commit message')

        action = actions.CommitAction(
            'bar', 'refs/heads/user/branch',
            'Aidan Wilkins <aidan@yourproject.org>',
            '1376405234 +0100',
            'Jeff Arnold <jeff@yourproject.org>',
            '1374782771 +0100',
            'This is a different commit message')

        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.target, 'refs/heads/user/branch')
        self.assertEqual(action.author,
                         'Aidan Wilkins <aidan@yourproject.org>')
        self.assertEqual(action.author_date, '1376405234 +0100')
        self.assertEqual(action.committer,
                         'Jeff Arnold <jeff@yourproject.org>')
        self.assertEqual(action.committer_date, '1374782771 +0100')
        self.assertEqual(action.message, 'This is a different commit message')


class CreateActionTests(unittest.TestCase):

    """Unit tests for the CreateAction class."""

    def test_constructor_sets_action_id_class_and_properties(self):
        """Verify that the constructor sets the action id, class and props."""

        action = actions.CreateAction('foo', 'card', [
            properties.TextProperty('title', 'New title'),
            properties.ReferenceProperty(
                'lane', {'uuid': 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39'}),
            ])
        self.assertEqual(action.id, 'foo')
        self.assertEqual(action.klass, 'card')
        self.assertEqual(action.properties, {
            'title': properties.TextProperty('title', 'New title'),
            'lane': properties.ReferenceProperty(
                'lane', {'uuid': 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39'}),
            })

        action = actions.CreateAction('bar', 'lane', [
            properties.TextProperty('title', 'A new title'),
            properties.ListProperty(
                'cards', [
                    properties.ReferenceProperty(
                        'cards',
                        {'uuid': '3d745cc5-cff4-4676-aa78-ff48b9da0ed0'}),
                    ])
            ])
        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.klass, 'lane')
        self.assertEqual(action.properties, {
            'title': properties.TextProperty('title', 'A new title'),
            'cards': properties.ListProperty(
                'cards', [
                    properties.ReferenceProperty(
                        'cards',
                        {'uuid': '3d745cc5-cff4-4676-aa78-ff48b9da0ed0'}),
                    ]),
            })


class DeleteActionTests(unittest.TestCase):

    """Unit tests for the DeleteAction class."""

    def test_constructor_sets_action_id_and_object_uuid(self):
        """Verify that the constructor sets the action id and object uuid."""

        action = actions.DeleteAction(
            'foo', 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39')
        self.assertEqual(action.id, 'foo')
        self.assertEqual(action.uuid, 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39')

        action = actions.DeleteAction(
            'bar', 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39')
        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.uuid, 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39')

        action = actions.DeleteAction(
            'bar', 'b4f4de38-1fa1-45ce-ab7a-8c749954538c')
        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.uuid, 'b4f4de38-1fa1-45ce-ab7a-8c749954538c')


class UpdateActionTests(unittest.TestCase):

    """Unit tests for the UpdateAction class."""

    def test_constructor_sets_action_id_uuid_and_properties(self):
        """Verify that the constructor sets the action id, uuid and props."""

        action = actions.UpdateAction(
            'foo',
            '37982fe0-467f-4f02-b6a0-f010ceb8ad63',
            [
                properties.TextProperty('title', 'New title'),
                properties.ReferenceProperty(
                    'lane', {'uuid': 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39'}),
                ])
        self.assertEqual(action.id, 'foo')
        self.assertEqual(action.uuid, '37982fe0-467f-4f02-b6a0-f010ceb8ad63')
        self.assertEqual(action.properties, {
            'title': properties.TextProperty('title', 'New title'),
            'lane': properties.ReferenceProperty(
                'lane', {'uuid': 'cfdaa6e9-eb13-49a3-b43c-51b40a005d39'}),
            })

        action = actions.UpdateAction(
            'bar',
            'e0fac940-e60a-4f55-aa95-bae774b72870',
            [
                properties.TextProperty('title', 'A new title'),
                properties.ListProperty(
                    'cards', [
                        properties.ReferenceProperty(
                            'cards',
                            {'uuid': '3d745cc5-cff4-4676-aa78-ff48b9da0ed0'})
                        ])
                ])
        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.uuid, 'e0fac940-e60a-4f55-aa95-bae774b72870')
        self.assertEqual(action.properties, {
            'title': properties.TextProperty('title', 'A new title'),
            'cards': properties.ListProperty(
                'cards', [
                    properties.ReferenceProperty(
                        'cards',
                        {'uuid': '3d745cc5-cff4-4676-aa78-ff48b9da0ed0'}),
                    ])
            })


class UpdateRawPropertyActionTests(unittest.TestCase):

    """Unit tests for the UpdateRawPropertyAction class."""

    def test_constructor_sets_action_id_uuid_property_etc(self):
        """Verify that the constructor sets the action id, uuid etc."""

        action = actions.UpdateRawPropertyAction(
            'foo', '7b6b8292-7b01-4cea-87c9-6ad3b771314c',
            'avatar', 'image/png', 'image data')
        self.assertEqual(action.id, 'foo')
        self.assertEqual(action.uuid, '7b6b8292-7b01-4cea-87c9-6ad3b771314c')
        self.assertEqual(action.property, 'avatar')
        self.assertEqual(action.content_type, 'image/png')
        self.assertEqual(action.data, 'image data')

        action = actions.UpdateRawPropertyAction(
            'bar', 'e17de337-73ab-411a-9e1d-5b84e8d101f0',
            'patch', 'text/plain', 'patch content')
        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.uuid, 'e17de337-73ab-411a-9e1d-5b84e8d101f0')
        self.assertEqual(action.property, 'patch')
        self.assertEqual(action.content_type, 'text/plain')
        self.assertEqual(action.data, 'patch content')


class UnsetRawPropertyActionTests(unittest.TestCase):

    """Unit tests for the UnsetRawPropertyAction class."""

    def test_constructor_sets_action_id_uuid_and_property(self):
        """Verify that the constructor sets the action id, uuid, property."""

        action = actions.UnsetRawPropertyAction(
            'foo', '7b6b8292-7b01-4cea-87c9-6ad3b771314c', 'avatar')
        self.assertEqual(action.id, 'foo')
        self.assertEqual(action.uuid, '7b6b8292-7b01-4cea-87c9-6ad3b771314c')
        self.assertEqual(action.property, 'avatar')

        action = actions.UnsetRawPropertyAction(
            'bar', 'e17de337-73ab-411a-9e1d-5b84e8d101f0', 'patch')
        self.assertEqual(action.id, 'bar')
        self.assertEqual(action.uuid, 'e17de337-73ab-411a-9e1d-5b84e8d101f0')
        self.assertEqual(action.property, 'patch')

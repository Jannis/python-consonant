# Copyright (C) 2013-2014 Codethink Limited.
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


"""Unit tests for property definition classes."""


import itertools
import json
import re
import unittest
import yaml

from consonant.schema import definitions
from consonant.util.converters import JSONObjectEncoder


class PropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the PropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.PropertyDefinition('name1', False)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.PropertyDefinition('name2', False)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.PropertyDefinition('name1', False)
        self.assertEqual(prop.optional, False)

        prop = definitions.PropertyDefinition('name1', True)
        self.assertEqual(prop.optional, True)

    def test_property_definitions_are_not_equal_if_types_differ(self):
        """Verify that property definitions are not equal if types differe."""

        props = [
            definitions.IntPropertyDefinition('name', False),
            definitions.BooleanPropertyDefinition('name', False),
            definitions.FloatPropertyDefinition('name', False),
            definitions.TimestampPropertyDefinition('name', False),
            definitions.TextPropertyDefinition('name', False, []),
            definitions.RawPropertyDefinition('name', False, []),
            definitions.ReferencePropertyDefinition(
                'name', False, 'class', None, False),
            definitions.ListPropertyDefinition(
                'name', False,
                definitions.IntPropertyDefinition('name', False)),
            ]

        for prop1, prop2 in itertools.permutations(props, 2):
            self.assertFalse(prop1 == prop2)

    def test_properties_with_same_type_name_and_optional_are_equal(self):
        """Verify that prop defs with same type, name, optional are equal."""

        props = [
            (definitions.IntPropertyDefinition, 'name', False),
            (definitions.BooleanPropertyDefinition, 'name', False),
            (definitions.FloatPropertyDefinition, 'name', False),
            (definitions.TimestampPropertyDefinition, 'name', False),
            (definitions.TextPropertyDefinition, 'name', False, []),
            (definitions.RawPropertyDefinition, 'name', False, []),
            (definitions.ReferencePropertyDefinition,
                'name', False, 'class', None, False),
            (definitions.ListPropertyDefinition,
                'name', False,
                definitions.IntPropertyDefinition('name', False)),
            ]

        for data in props:
            klass, params = data[0], data[1:]
            prop1 = klass(*params)
            prop2 = klass(*params)
            self.assertEqual(prop1, prop2)


class BooleanPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the BooleanPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.BooleanPropertyDefinition('name1', False)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.BooleanPropertyDefinition('name2', False)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.BooleanPropertyDefinition('name1', False)
        self.assertEqual(prop.optional, False)

        prop = definitions.BooleanPropertyDefinition('name1', True)
        self.assertEqual(prop.optional, True)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of bool prop defs is ok."""

        prop = definitions.BooleanPropertyDefinition('name1', False)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'boolean')
        self.assertFalse('optional' in yaml_data)

        prop = definitions.BooleanPropertyDefinition('name2', True)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'boolean')
        self.assertTrue(yaml_data['optional'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of bool prop defs is ok."""

        prop = definitions.BooleanPropertyDefinition('name1', False)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'boolean')
        self.assertFalse('optional' in json_data)

        prop = definitions.BooleanPropertyDefinition('name2', True)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'boolean')
        self.assertTrue(json_data['optional'])


class IntPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the IntPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.IntPropertyDefinition('name1', False)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.IntPropertyDefinition('name2', False)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.IntPropertyDefinition('name1', False)
        self.assertEqual(prop.optional, False)

        prop = definitions.IntPropertyDefinition('name1', True)
        self.assertEqual(prop.optional, True)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of int prop defs is ok."""

        prop = definitions.IntPropertyDefinition('name1', False)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'int')
        self.assertFalse('optional' in yaml_data)

        prop = definitions.IntPropertyDefinition('name2', True)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'int')
        self.assertTrue(yaml_data['optional'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of int prop defs is ok."""

        prop = definitions.IntPropertyDefinition('name1', False)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'int')
        self.assertFalse('optional' in json_data)

        prop = definitions.IntPropertyDefinition('name2', True)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'int')
        self.assertTrue(json_data['optional'])


class FloatPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the FloatPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.FloatPropertyDefinition('name1', False)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.FloatPropertyDefinition('name2', False)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.FloatPropertyDefinition('name1', False)
        self.assertEqual(prop.optional, False)

        prop = definitions.FloatPropertyDefinition('name1', True)
        self.assertEqual(prop.optional, True)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of float prop defs is ok."""

        prop = definitions.FloatPropertyDefinition('name1', False)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'float')
        self.assertFalse('optional' in yaml_data)

        prop = definitions.FloatPropertyDefinition('name2', True)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'float')
        self.assertTrue(yaml_data['optional'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of float prop defs is ok."""

        prop = definitions.FloatPropertyDefinition('name1', False)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'float')
        self.assertFalse('optional' in json_data)

        prop = definitions.FloatPropertyDefinition('name2', True)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'float')
        self.assertTrue(json_data['optional'])


class TimestampPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the TimestampPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.TimestampPropertyDefinition('name1', False)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.TimestampPropertyDefinition('name2', False)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.TimestampPropertyDefinition('name1', False)
        self.assertEqual(prop.optional, False)

        prop = definitions.TimestampPropertyDefinition('name1', True)
        self.assertEqual(prop.optional, True)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of timestamp prop defs is ok."""

        prop = definitions.TimestampPropertyDefinition('name1', False)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'timestamp')
        self.assertFalse('optional' in yaml_data)

        prop = definitions.TimestampPropertyDefinition('name2', True)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'timestamp')
        self.assertTrue(yaml_data['optional'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of timestamp prop defs is ok."""

        prop = definitions.TimestampPropertyDefinition('name1', False)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'timestamp')
        self.assertFalse('optional' in json_data)

        prop = definitions.TimestampPropertyDefinition('name2', True)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'timestamp')
        self.assertTrue(json_data['optional'])


class TextPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the TextPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.TextPropertyDefinition('name1', False, [])
        self.assertEqual(prop.name, 'name1')

        prop = definitions.TextPropertyDefinition('name2', False, [])
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.TextPropertyDefinition('name1', False, [])
        self.assertEqual(prop.optional, False)

        prop = definitions.TextPropertyDefinition('name1', True, [])
        self.assertEqual(prop.optional, True)

    def test_constructor_sets_regular_expressions(self):
        """Verify that the constructor sets the regular expressions field."""

        prop = definitions.TextPropertyDefinition('name', False, [])
        self.assertEqual(prop.expressions, [])

        prop = definitions.TextPropertyDefinition(
            'name1', False, ['^foo(bar|baz)$'])
        self.assertEqual(prop.expressions,
                         [re.compile('^foo(bar|baz)$')])

        prop = definitions.TextPropertyDefinition(
            'name2', True, ['^foo', '^[0-9abcdef]{40}$', '.*\.pyc?$'])
        self.assertEqual(prop.expressions,
                         [re.compile('^foo'),
                          re.compile('^[0-9abcdef]{40}$'),
                          re.compile('.*\.pyc?$')])

    def test_definitions_with_the_same_expressions_are_equal(self):
        """Verify that text prop defs with the same expressions are equal."""

        prop1 = definitions.TextPropertyDefinition('name', False, [])
        prop2 = definitions.TextPropertyDefinition('name', False, [])
        self.assertEqual(prop1, prop2)

        prop1 = definitions.TextPropertyDefinition(
            'name', False, ['^foo', '[0-9]+'])
        prop2 = definitions.TextPropertyDefinition(
            'name', False, ['^foo', '[0-9]+'])
        self.assertEqual(prop1, prop2)

    def test_definitions_with_different_expressions_are_not_equal(self):
        """Verify that text prop defs with different exprs are not equal."""

        prop1 = definitions.TextPropertyDefinition(
            'name', False, ['^foo', '[0123456789]+'])
        prop2 = definitions.TextPropertyDefinition(
            'name', False, ['^foo', '[0-9]+'])
        self.assertFalse(prop1 == prop2)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of text prop defs is ok."""

        prop = definitions.TextPropertyDefinition('name1', False, [])
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'text')
        self.assertFalse('optional' in yaml_data)

        prop = definitions.TextPropertyDefinition('name2', True, ['^foo$'])
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'text')
        self.assertTrue(yaml_data['optional'])
        self.assertTrue('^foo$' in yaml_data['regex'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of text prop defs is ok."""

        prop = definitions.TextPropertyDefinition('name1', False, [])
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'text')
        self.assertFalse('optional' in json_data)

        prop = definitions.TextPropertyDefinition('name2', True, ['^foo$'])
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'text')
        self.assertTrue(json_data['optional'])
        self.assertTrue('^foo$' in json_data['regex'])


class RawPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the RawPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.RawPropertyDefinition('name1', False, [])
        self.assertEqual(prop.name, 'name1')

        prop = definitions.RawPropertyDefinition('name2', False, [])
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.RawPropertyDefinition('name1', False, [])
        self.assertEqual(prop.optional, False)

        prop = definitions.RawPropertyDefinition('name1', True, [])
        self.assertEqual(prop.optional, True)

    def test_constructor_sets_regular_expressions(self):
        """Verify that the constructor sets the regular expressions field."""

        prop = definitions.RawPropertyDefinition('name', False, [])
        self.assertEqual(prop.expressions, [])

        prop = definitions.RawPropertyDefinition(
            'name1', False, ['^foo(bar|baz)$'])
        self.assertEqual(prop.expressions,
                         [re.compile('^foo(bar|baz)$')])

        prop = definitions.RawPropertyDefinition(
            'name2', True, ['^foo', '^[0-9abcdef]{40}$', '.*\.pyc?$'])
        self.assertEqual([x.pattern for x in prop.expressions],
                         ['^foo', '^[0-9abcdef]{40}$', '.*\.pyc?$'])

    def test_definitions_with_the_same_expressions_are_equal(self):
        """Verify that raw prop defs with the same expressions are equal."""

        prop1 = definitions.RawPropertyDefinition('name', False, [])
        prop2 = definitions.RawPropertyDefinition('name', False, [])
        self.assertEqual(prop1, prop2)

        prop1 = definitions.RawPropertyDefinition(
            'name', False, ['^foo', '[0-9]+'])
        prop2 = definitions.RawPropertyDefinition(
            'name', False, ['^foo', '[0-9]+'])
        self.assertEqual(prop1, prop2)

    def test_definitions_with_different_expressions_are_not_equal(self):
        """Verify that raw prop defs with different exprs are not equal."""

        prop1 = definitions.RawPropertyDefinition(
            'name', False, ['^foo', '[0123456789]+'])
        prop2 = definitions.RawPropertyDefinition(
            'name', False, ['^foo', '[0-9]+'])
        self.assertFalse(prop1 == prop2)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of raw prop defs is ok."""

        prop = definitions.RawPropertyDefinition('name1', False, [])
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'raw')
        self.assertFalse('optional' in yaml_data)

        prop = definitions.RawPropertyDefinition('name2', True, ['^bar$'])
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'raw')
        self.assertTrue(yaml_data['optional'])
        self.assertTrue('^bar$' in yaml_data['content-type-regex'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of raw prop defs is ok."""

        prop = definitions.RawPropertyDefinition('name1', False, [])
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'raw')
        self.assertFalse('optional' in json_data)

        prop = definitions.RawPropertyDefinition('name2', True, ['^bar$'])
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'raw')
        self.assertTrue(json_data['optional'])
        self.assertTrue('^bar$' in json_data['content-type-regex'])


class ReferencePropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the ReferencePropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', None, False)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.ReferencePropertyDefinition(
            'name2', False, 'lane', None, False)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', None, False)
        self.assertEqual(prop.optional, False)

        prop = definitions.ReferencePropertyDefinition(
            'name1', True, 'lane', None, False)
        self.assertEqual(prop.optional, True)

    def test_constructor_sets_the_class_name(self):
        """Verify that the constructor sets the target class."""

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', None, False)
        self.assertEqual(prop.klass, 'lane')

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'card', None, False)
        self.assertEqual(prop.klass, 'card')

    def test_constructor_sets_the_schema(self):
        """Verify that the constructor sets the target schema."""

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', None, False)
        self.assertEqual(prop.schema, None)

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', 'schema1', False)
        self.assertEqual(prop.schema, 'schema1')

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', 'schema2', False)
        self.assertEqual(prop.schema, 'schema2')

    def test_constructor_sets_the_bidirectional_hint(self):
        """Verify that the constructor sets the bidirectional hint."""

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', None, False)
        self.assertEqual(prop.bidirectional, False)

        prop = definitions.ReferencePropertyDefinition(
            'name1', False, 'lane', None, True)
        self.assertEqual(prop.bidirectional, True)

    def test_definitions_with_same_target_attributes_are_equal(self):
        """Verify that ref prop defs with same target attributes are equal."""

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', None, False)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', None, False)
        self.assertEqual(prop1, prop2)

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', False)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', False)
        self.assertEqual(prop1, prop2)

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', False)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', False)
        self.assertEqual(prop1, prop2)

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', True)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', True)
        self.assertEqual(prop1, prop2)

    def test_definitions_with_different_target_class_are_not_equal(self):
        """Verify that ref prop defs with different classes are not equal."""

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', None, False)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'card', None, False)
        self.assertFalse(prop1 == prop2)

    def test_definitions_with_different_schema_are_not_equal(self):
        """Verify that ref prop defs with different schemas are not equal."""

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', False)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.2', False)
        self.assertFalse(prop1 == prop2)

    def test_bidirectional_and_non_bidirectional_defs_are_not_equal(self):
        """Verify that bi-/non-bidirectional ref prop defs are not equal."""

        prop1 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', False)
        prop2 = definitions.ReferencePropertyDefinition(
            'name', False, 'lane', 'schema.1', True)
        self.assertFalse(prop1 == prop2)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of reference prop defs is ok."""

        prop = definitions.ReferencePropertyDefinition(
            'cards', False, 'card', None, None)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'reference')
        self.assertFalse('optional' in yaml_data)
        self.assertEqual(yaml_data['class'], 'card')
        self.assertFalse('schema' in yaml_data)
        self.assertFalse('bidirectional' in yaml_data)

        prop = definitions.ReferencePropertyDefinition(
            'lane', True, 'lane', 'schema.2', None)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'reference')
        self.assertTrue(yaml_data['optional'])
        self.assertEqual(yaml_data['class'], 'lane')
        self.assertEqual(yaml_data['schema'], 'schema.2')
        self.assertFalse('bidirectional' in yaml_data)

        prop = definitions.ReferencePropertyDefinition(
            'lane', True, 'lane', 'schema.2', 'cards')
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'reference')
        self.assertTrue(yaml_data['optional'])
        self.assertEqual(yaml_data['class'], 'lane')
        self.assertEqual(yaml_data['schema'], 'schema.2')
        self.assertEqual(yaml_data['bidirectional'], 'cards')

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of reference prop defs is ok."""

        prop = definitions.ReferencePropertyDefinition(
            'cards', False, 'card', None, None)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'reference')
        self.assertFalse('optional' in json_data)
        self.assertEqual(json_data['class'], 'card')
        self.assertFalse('schema' in json_data)
        self.assertFalse('bidirectional' in json_data)

        prop = definitions.ReferencePropertyDefinition(
            'lane', True, 'lane', 'schema.2', None)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'reference')
        self.assertTrue(json_data['optional'])
        self.assertEqual(json_data['class'], 'lane')
        self.assertEqual(json_data['schema'], 'schema.2')
        self.assertFalse('bidirectional' in json_data)

        prop = definitions.ReferencePropertyDefinition(
            'lane', True, 'lane', 'schema.2', 'cards')
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'reference')
        self.assertTrue(json_data['optional'])
        self.assertEqual(json_data['class'], 'lane')
        self.assertEqual(json_data['schema'], 'schema.2')
        self.assertEqual(json_data['bidirectional'], 'cards')


class ListPropertyDefinitionTests(unittest.TestCase):

    """Unit tests for the ListPropertyDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the property name."""

        prop = definitions.ListPropertyDefinition('name1', False, None)
        self.assertEqual(prop.name, 'name1')

        prop = definitions.ListPropertyDefinition('name2', False, None)
        self.assertEqual(prop.name, 'name2')

    def test_constructor_sets_optional_hint(self):
        """Verify that the constructor sets the optional hint."""

        prop = definitions.ListPropertyDefinition('name1', False, None)
        self.assertEqual(prop.optional, False)

        prop = definitions.ListPropertyDefinition('name1', True, None)
        self.assertEqual(prop.optional, True)

    def test_constructor_sets_element_definition(self):
        """Verify that the constructor sets the element definition."""

        prop = definitions.ListPropertyDefinition('name1', False, None)
        self.assertEqual(prop.elements, None)

        elements = definitions.IntPropertyDefinition('name1', False)
        prop = definitions.ListPropertyDefinition('name1', False, elements)
        self.assertEqual(prop.elements, elements)

        elements = definitions.FloatPropertyDefinition('name1', False)
        prop = definitions.ListPropertyDefinition('name1', False, elements)
        self.assertEqual(prop.elements, elements)

    def test_definitions_with_same_elements_are_equal(self):
        """Verify that list prop defs with the same element type are equal."""

        prop1 = definitions.ListPropertyDefinition(
            'name', False, definitions.IntPropertyDefinition('name', False))
        prop2 = definitions.ListPropertyDefinition(
            'name', False, definitions.IntPropertyDefinition('name', False))
        self.assertEqual(prop1, prop2)

    def test_definitions_with_different_elements_are_not_equal(self):
        """Verify that list prop defs with different elements are not equal."""

        prop1 = definitions.ListPropertyDefinition(
            'name', False, definitions.FloatPropertyDefinition('name', False))
        prop2 = definitions.ListPropertyDefinition(
            'name', False, definitions.IntPropertyDefinition('name', False))
        self.assertFalse(prop1 == prop2)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of list prop defs is ok."""

        elements = definitions.IntPropertyDefinition('name', False)
        prop = definitions.ListPropertyDefinition('numbers', False, elements)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'list')
        self.assertFalse('optional' in yaml_data)
        self.assertTrue(isinstance(yaml_data['elements'], dict))
        self.assertEqual(yaml_data['elements']['type'], 'int')
        self.assertFalse('optional' in yaml_data['elements'])

        elements = definitions.FloatPropertyDefinition('name', False)
        prop = definitions.ListPropertyDefinition('numbers', True, elements)
        string = yaml.dump(prop)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['type'], 'list')
        self.assertTrue(yaml_data['optional'])
        self.assertTrue(isinstance(yaml_data['elements'], dict))
        self.assertEqual(yaml_data['elements']['type'], 'float')
        self.assertFalse('optional' in yaml_data['elements'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of list prop defs is ok."""

        elements = definitions.IntPropertyDefinition('name', False)
        prop = definitions.ListPropertyDefinition('numbers', False, elements)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'list')
        self.assertFalse('optional' in json_data)
        self.assertTrue(isinstance(json_data['elements'], dict))
        self.assertEqual(json_data['elements']['type'], 'int')
        self.assertFalse('optional' in json_data['elements'])

        elements = definitions.FloatPropertyDefinition('name', False)
        prop = definitions.ListPropertyDefinition('numbers', True, elements)
        string = json.dumps(prop, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['type'], 'list')
        self.assertTrue(json_data['optional'])
        self.assertTrue(isinstance(json_data['elements'], dict))
        self.assertEqual(json_data['elements']['type'], 'float')
        self.assertFalse('optional' in json_data['elements'])


class ClassDefinition(unittest.TestCase):

    """Unit tests for the ClassDefinition class."""

    def test_constructor_sets_name(self):
        """Verify that the constructor sets the class name."""

        klass = definitions.ClassDefinition('name1', [])
        self.assertEqual(klass.name, 'name1')

        klass = definitions.ClassDefinition('name2', [])
        self.assertEqual(klass.name, 'name2')

    def test_constructor_sets_property_definitions(self):
        """Verify that the constructor sets the property definitions."""

        klass = definitions.ClassDefinition('name1', [])
        self.assertEqual(klass.properties, {})

        properties = [
            definitions.IntPropertyDefinition('prop1', False),
            definitions.BooleanPropertyDefinition('prop2', False)
            ]
        klass = definitions.ClassDefinition('name1', properties)

        self.assertEqual(len(klass.properties), len(properties))
        for prop in properties:
            self.assertTrue(prop.name in klass.properties)
            self.assertEqual(klass.properties[prop.name], prop)

    def test_classes_and_non_classes_are_not_equal(self):
        """Verify that class definitions and non-classes are not equal."""

        self.assertFalse(definitions.ClassDefinition('name', []) == 'name')

    def test_classes_with_same_name_and_properties_are_equal(self):
        """Verify that classes with the same name and properties are equal."""

        klass1 = definitions.ClassDefinition('name', [
            definitions.IntPropertyDefinition('prop1', False),
            definitions.BooleanPropertyDefinition('prop2', False)
            ])
        klass2 = definitions.ClassDefinition('name', [
            definitions.IntPropertyDefinition('prop1', False),
            definitions.BooleanPropertyDefinition('prop2', False)
            ])

        self.assertEqual(klass1, klass2)

    def test_classes_with_different_names_are_not_equal(self):
        """Verify that classes with different names are not equal."""

        klass1 = definitions.ClassDefinition('name1', [
            definitions.IntPropertyDefinition('prop1', False),
            definitions.BooleanPropertyDefinition('prop2', False)
            ])
        klass2 = definitions.ClassDefinition('name2', [
            definitions.IntPropertyDefinition('prop1', False),
            definitions.BooleanPropertyDefinition('prop2', False)
            ])

        self.assertFalse(klass1 == klass2)

    def test_classes_with_different_properties_are_not_equal(self):
        """Verify that classes with different properties are not equal."""

        klass1 = definitions.ClassDefinition('name', [
            definitions.IntPropertyDefinition('prop1', False),
            ])
        klass2 = definitions.ClassDefinition('name', [
            definitions.BooleanPropertyDefinition('prop1', False),
            ])

        self.assertFalse(klass1 == klass2)

    def test_yaml_representation_has_all_expected_fields(self):
        """Verify that the YAML representation of class definitions is ok."""

        props = [
            definitions.TextPropertyDefinition('title', False, []),
            definitions.IntPropertyDefinition('number', True),
            ]
        klass = definitions.ClassDefinition('card', props)

        string = yaml.dump(klass)
        yaml_data = yaml.load(string)

        self.assertTrue(isinstance(yaml_data, dict))
        self.assertEqual(yaml_data['name'], 'card')
        self.assertEqual(len(yaml_data['properties']), 2)
        self.assertTrue('title' in yaml_data['properties'])
        self.assertTrue('number' in yaml_data['properties'])
        self.assertEqual(yaml_data['properties']['title']['type'], 'text')
        self.assertFalse('optional' in yaml_data['properties']['title'])
        self.assertEqual(yaml_data['properties']['number']['type'], 'int')
        self.assertTrue(yaml_data['properties']['number']['optional'])

    def test_json_representation_has_all_expected_fields(self):
        """Verify that the JSON representation of class definitions is ok."""

        props = [
            definitions.TextPropertyDefinition('title', False, []),
            definitions.IntPropertyDefinition('number', True),
            ]
        klass = definitions.ClassDefinition('card', props)

        string = json.dumps(klass, cls=JSONObjectEncoder)
        json_data = json.loads(string)

        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data['name'], 'card')
        self.assertEqual(len(json_data['properties']), 2)
        self.assertTrue('title' in json_data['properties'])
        self.assertTrue('number' in json_data['properties'])
        self.assertEqual(json_data['properties']['title']['type'], 'text')
        self.assertFalse('optional' in json_data['properties']['title'])
        self.assertEqual(json_data['properties']['number']['type'], 'int')
        self.assertTrue(json_data['properties']['number']['optional'])

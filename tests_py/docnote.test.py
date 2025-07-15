from typing import get_type_hints

import pytest

from docnote import DOCNOTE_CONFIG_ATTR
from docnote import ClcNote
from docnote import DocnoteConfig
from docnote import DocnoteConfigParams
from docnote import DocnoteGroup
from docnote import MarkupLang
from docnote import Note
from docnote import docnote


class TestDocnote:
    def test_clc_note(self):
        """ClcNote instances must be constructable as expected.
        This is about as close to a gimme as you can get.
        """
        note = ClcNote('Some doc note here')
        assert note.config is not None
        assert note.config.markup_lang is MarkupLang.CLEANCOPY

    def test_plain_note(self):
        """Note instances must be constructable as expected.
        """
        note = Note('Some doc note here')
        assert note.config is None

    def test_decorator(self):
        """The @docnote decorator must return the original
        decoree with the DOCNOTE_CONFIG_ATTR added.
        """
        class TestClass:
            pass

        assert not hasattr(TestClass, DOCNOTE_CONFIG_ATTR)

        config = DocnoteConfig()
        retval = docnote(config)(TestClass)
        assert retval is TestClass
        assert hasattr(TestClass, DOCNOTE_CONFIG_ATTR)
        assert getattr(TestClass, DOCNOTE_CONFIG_ATTR) is config

    def test_docnote_group(self):
        """Docnote groups must be creatable, assignable within a
        config, and ordered within that group.
        """
        group1 = DocnoteGroup('group1')
        group2 = DocnoteGroup('group2')
        group3 = DocnoteGroup('group3')
        group4 = DocnoteGroup('group4')

        config = DocnoteConfig(child_groups=[group1, group2, group3, group4])
        assert config.child_groups is not None
        assert tuple(config.child_groups) == (group1, group2, group3, group4)

    @pytest.mark.parametrize(
        'before,expected_retval',
        [
            (
                DocnoteConfig(enforce_known_lang=True),
                {'enforce_known_lang': True}),
            (
                DocnoteConfig(
                    enforce_known_lang=False,
                    markup_lang='foo',),
                {'enforce_known_lang': False, 'markup_lang': 'foo'}),
            (
                DocnoteConfig(),
                {}),
            (
                DocnoteConfig(parent_group_name='foo'),
                {}),
            (
                DocnoteConfig(
                    enforce_known_lang=True,
                    parent_group_name='foo'),
                {'enforce_known_lang': True}),])
    def test_get_stackables(self, before: DocnoteConfig, expected_retval):
        assert before.get_stackables() == expected_retval

    def test_config_params_matches_config(self):
        """The DocnoteConfigParams typeddict must match the
        DocnoteConfig.
        """
        params_hints = get_type_hints(DocnoteConfigParams)
        config_hints = get_type_hints(DocnoteConfig)

        assert set(params_hints) == set(config_hints)

        for key, param_hint_value in params_hints.items():
            config_hint_value = config_hints[key]

            assert (param_hint_value | None) == config_hint_value

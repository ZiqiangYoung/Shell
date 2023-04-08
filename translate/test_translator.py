from unittest import TestCase
from parameterized import parameterized

from translate import Translator, create_translator
from util.reflection import scanAllImpl4Parameterized

translate_en2zh_data_pos = [("one", "一"),
                            ("six", "六"),
                            ("apple", "苹果"),
                            ("banana", "香蕉"), ]

translate_en2zh_data_neg = [("two", "一"),
                            ("six", "十"),
                            ("orange", "苹果"),
                            ("banana", "黄瓜"), ]


class TestTranslator(TestCase):
    @parameterized.expand(scanAllImpl4Parameterized(Translator))
    def test_translate(self, impl: Translator):
        for en, zh in translate_en2zh_data_pos:
            self.assertEqual(zh, impl.translate(en))
        for en, zh in translate_en2zh_data_neg:
            self.assertNotEqual(zh, impl.translate(en))

    @parameterized.expand(translate_en2zh_data_pos)
    def test_create_translator_pos(self, inp, expect):
        with create_translator() as t:
            self.assertEqual(expect, t.translate(inp))

    @parameterized.expand(translate_en2zh_data_neg)
    def test_create_translator_neg(self, inp, expect):
        with create_translator() as t:
            self.assertNotEqual(expect, t.translate(inp))

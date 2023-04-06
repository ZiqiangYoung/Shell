from unittest import TestCase

from parameterized import parameterized

from translate.translator import Translator
from util.reflection import scan_all_impl_class


class TestTranslator(TestCase):
    @parameterized.expand(scan_all_impl_class(Translator))
    def test_function_1(self, impl: Translator):
        self.assertEqual(impl.translate("one"), "一")
        self.assertEqual(impl.translate("six"), "六")
        self.assertEqual(impl.translate("apple"), "苹果")

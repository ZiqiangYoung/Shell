from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

from conf import settings
from util.reflection import dynamic_load_impl


class Translator(metaclass=ABCMeta):

    @abstractmethod
    def translate(self, query: str, from_lang: str = 'en', to_lang: str = 'zh') -> str:
        pass

    @staticmethod
    def __spilt_text(text: str, limit_length: int, priority_delimiters: tuple) -> list[str]:
        if len(text) <= limit_length:
            return [text]

        result = []

        start: int = 0
        while True:
            if start + limit_length >= len(text):
                result.append(text[start:])
                return result

            rfind = -1
            for d in priority_delimiters:
                rfind = text.rfind(d, start, start + limit_length)
                if rfind > 0:
                    break
            if rfind < 0:
                raise ValueError(
                    "待翻译的文本以下分隔符出现较少导致异常： " + str(
                        priority_delimiters) + " 请考虑文本格式或分句规则有误。text: " + text)

            result.append(text[start:rfind + 1])
            start = rfind + 1

    @staticmethod
    def spilt_english_text(english_text: str, limit_length: int) -> list[str]:
        return Translator.__spilt_text(english_text, limit_length, ('.', '!', '?',
                                                                    ':', ';',
                                                                    ']', ')', '}', '>',
                                                                    '*', '%', ',', ' '))

    @staticmethod
    def spilt_chinese_text(chinese_text: str, limit_length: int) -> list[str]:
        return Translator.__spilt_text(chinese_text, limit_length, ('。', '！', '？',
                                                                    '：', '；',
                                                                    '】', '）', '}', '》',
                                                                    '*', '%', '，', ' '))


@contextmanager
def create_translator(translator_name: str = None, translator: Translator = None, *args, **kwargs):
    """
    管理 Translator 实例的 Context Manager
    :param translator_name: 希望实例化的 translator 类名
    :param translator: 希望实例化的 translator 类 (type==class)
    :param args: 实例化目标类所需的参数
    :param kwargs: 实例化目标类所需的参数
    :return: None
    """
    if translator is None and translator_name is None:
        if settings.translator.engine.active is not None:
            translator_name = settings.translator.engine.active
        elif settings.translator.engine.alternative is not None:
            for name in settings.translator.engine.alternative:
                if name is not None:
                    translator_name = name
                    break
        else:
            raise ValueError(
                "No valid configuration found for input as argument (settings.translator.engine). "
                "The function must take a translator behavior name or instance as an argument.")
    try:
        if translator is None:
            translator = dynamic_load_impl(Translator, translator_name, *args, **kwargs)

        yield translator
    finally:
        # close resource
        pass


class TranslatorContextManager:
    """
    @deprecated
    equals to translate.translator.create_translator
    """

    def __init__(self, translater_name: str = None, translator: Translator = None, *args, **kwargs):
        self.translator: Translator or None = None
        self.translator_name: str or None = None
        self.args = args
        self.kwargs = kwargs

        if translator is not None:
            self.translator = translator

        elif translater_name is not None:
            self.translator_name = translater_name

        elif settings.translator.engine.active is not None:
            self.translator_name = settings.translator.engine.active

        elif settings.translator.engine.alternative is not None:
            for name in settings.translator.engine.alternative:
                if name is not None:
                    self.translator_name = name
                    break

        else:
            raise ValueError(
                "No valid configuration found for input as argument (settings.translator.engine). "
                "The function must take a translator behavior name or instance as an argument.")

    def __enter__(self) -> Translator:
        if self.translator is None:
            assert self.translator_name is not None
            self.translator = dynamic_load_impl(Translator, self.translator_name, *self.args, **self.kwargs)

        return self.translator

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.translator
        del self.translator_name

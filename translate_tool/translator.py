from abc import ABCMeta, abstractmethod


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

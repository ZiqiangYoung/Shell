import random
import requests

from config import settings
from hashlib import md5
from translate_tool.translator import Translator


class BaiduTranslator(Translator):
    # Set your own appid/app_key.
    __id = settings.baidu.translation.id
    __key = settings.baidu.translation.key
    __url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    # noinspection HttpUrlsUsage
    __headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    __text_limit = 4000

    @staticmethod
    def __make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def translate(self, query: str, from_lang: str = 'en', to_lang: str = 'zh') -> str:
        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`

        # spilt query
        translated: str = ""
        spilt = Translator.spilt_english_text(query, self.__text_limit)
        for s in spilt:
            # Generate salt and sign
            salt = random.randint(32768, 65536)
            sign = self.__make_md5(str(self.__id) + s + str(salt) + self.__key)

            # Build request
            payload = {'appid': self.__id, 'q': s, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

            # Send request
            r = requests.post(self.__url, data=payload, headers=self.__headers).json()
            translated += r["trans_result"][0]["dst"]
        return translated

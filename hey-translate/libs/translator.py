import concurrent.futures
from logging import Logger
from deepl import DeepLClient, Language
from typing import Dict, Tuple

class Translator:
    def __init__(self, logger: Logger, auth_key: str):
        self.logger = logger
        
        self.auth_key = auth_key
        try:
            self.deepl_client = DeepLClient(auth_key, send_platform_info=False)
        except Exception as ex:
            self.logger.error(f"Translator DeepLClient 초기화 오류: {ex}")
    
    def set_auth_key(self, auth_key: str):
        self.deepl_client.close()
        
        self.auth_key = auth_key
        try:
            self.deepl_client = DeepLClient(auth_key, send_platform_info=False)
        except Exception as ex:
            self.logger.error(f"Translator DeepLClient 초기화 오류: {ex}")

    def get_target_langs(self) -> list[Language]:
        return self.deepl_client.get_target_languages()

    def batch_translate(self, target_langs: list[str], text: str) -> Dict[str, str]:
        result = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            for lang in target_langs:
                futures.append(executor.submit(self.translate, lang, text))

            for future in concurrent.futures.as_completed(futures):
                (lang, text) = future.result()
                result[lang] = text

        return result
    
    def translate(self, target_lang: str, text: str) -> Tuple[str, str]:
        try:
            return (target_lang, self.deepl_client.translate_text(text, target_lang=target_lang).text) # type: ignore
        except Exception as ex:
            self.logger.error(f"Translator API 요청 오류: {ex}")
            return (target_lang, text)

def test_benchmark():
    import os
    import time

    for i in range(1, 5):
        start = time.time()
        tr = Translator(os.getenv("DEEPL_AUTH_KEY")) # type: ignore
        result = tr.batch_translate(["en-us", "ja", "zh", "de"], "안녕하세요? MBC 뉴스 김형진 기자입니다.") # 오늘 날씨는 매우 맑겠습니다.
        end = time.time()
        print("결과:", result)
        print("걸린 시간: %0.3f초" % (end - start))

if __name__ == "__main__":
    test_benchmark()

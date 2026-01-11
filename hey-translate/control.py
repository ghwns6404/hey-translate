from deepl import Language
from libs.settings import Settings
from libs.sound_input import SoundInput
from libs.stt import STT
from libs.translator import Translator
from logging import Logger
import sounddevice as sd
from typing import Callable, Dict

class Control:
    def __init__(
        self,
        logger: Logger,
        on_stt_complete: Callable[[Dict[str, str]], None],
        on_stt_realtime: Callable[[Dict[str, str]], None],
        on_output_languages_change: Callable[[list[str]], None],
    ):
        self.logger = logger
        self.stt_complete = on_stt_complete
        self.stt_realtime = on_stt_realtime
        self.on_output_languages_change = on_output_languages_change

    def start(self):
        self.settings = Settings()

        self.stt = STT(self.logger, self.on_stt_complete, self.on_stt_realtime)
        self.sound_input = SoundInput(self.logger, self.stt.on_sound_callback)
        self.translator = Translator(self.logger, self.settings.get_deepl_auth_key())

        self.logger.info("Control이 시작되었습니다.")
    
    def exit(self):
        self.record_stop()
        self.settings.exit()

        self.logger.info("Control이 종료되었습니다.")

    def record_start(self, microphone: str | None = None):
        self.logger.info(f"녹음(mic: {microphone}) 시작 중...")

        if not microphone:
            microphone_idx = None
        else:
            microphone_idx = self.get_microphone_idx(microphone)

        self.stt.start_model()

        self.sound_input.input_start(microphone_idx)

        self.logger.info("녹음을 시작했습니다.")

    def record_stop(self):
        self.logger.info("녹음 종료 중...")

        self.sound_input.input_exit()
        self.stt.stop_model()

        self.logger.info("녹음을 종료했습니다.")

    def get_microphones(self, refresh: bool = False) -> Dict[str, int]:
        microphones = {}

        # 파이썬 오디오 모듈의 한계: https://github.com/spatialaudio/python-sounddevice/issues/125
        if refresh:
            sd._terminate()
            sd._initialize()

        for device in sd.query_devices():
            if device["max_input_channels"] > 0: # type: ignore
                microphones[device["name"]] = int(device["index"]) # type: ignore

        return microphones
    
    def get_microphones_i_s(self, refresh: bool = False) -> Dict[int, str]:
        microphones = {}

        # 파이썬 오디오 모듈의 한계: https://github.com/spatialaudio/python-sounddevice/issues/125
        if refresh:
            sd._terminate()
            sd._initialize()

        for device in sd.query_devices():
            if device["max_input_channels"] > 0: # type: ignore
                microphones[int(device["index"])] = device["name"] # type: ignore

        return microphones

    def get_microphone_idx(self, microphone: str) -> int:
        microphones = self.get_microphones()
        if not microphone in microphones.keys():
            raise Exception(f"마이크({microphone})를 인덱스에서 찾을 수 없습니다.")
        
        return microphones[microphone]
    
    def get_microphone_names(self, refresh: bool = False) -> list[str]:
        return [name for name in self.get_microphones(refresh).keys()]
    
    def get_current_input_device_idx(self) -> int:
        return self.sound_input.get_current_input_device_idx()

    def on_stt_complete(self, text: str):
        self.logger.debug(f"Control.on_stt_complete: {text}")

        # 원본만 미리 콜백.
        if "origin" in self.get_output_lang_codes():
            origin_result = {}
            origin_result["origin"] = text
            self.stt_complete(origin_result)

        result = self.translator.batch_translate([code for code in self.get_output_lang_codes() if code != "origin"], text)
        
        self.stt_complete(result)
    
    def on_stt_realtime(self, text: str):
        self.logger.debug(f"Control.on_stt_realtime: {text}")

        # 원본만 미리 콜백.
        if "origin" in self.get_output_lang_codes():
            origin_result = {}
            origin_result["origin"] = text
            self.stt_realtime(origin_result)

        result = self.translator.batch_translate([code for code in self.get_output_lang_codes() if code != "origin"], text)
        
        self.stt_realtime(result)

    def get_output_lang_codes(self) -> list[str]:
        return self.settings.get_output_languages()
    
    def set_output_lang_codes(self, lang_codes: list[str]):
        self.settings.set_output_languages(lang_codes)
        self.on_output_languages_change(lang_codes)
        self.settings.save()
    
    def get_target_langs(self) -> list[Language]:
        return self.translator.get_target_langs()

    def get_target_lang_codes(self) -> list[str]:
        return [lang.code for lang in self.get_target_langs()]

    def set_deepl_auth_key(self, auth_key: str):
        self.translator.set_auth_key(auth_key)

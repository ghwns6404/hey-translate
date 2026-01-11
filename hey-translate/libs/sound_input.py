from logging import Logger
import numpy as np
import sounddevice as sd
from typing import Callable

class SoundInput:
    def __init__(self, logger: Logger, sound_callback: Callable[[int, np.ndarray], None]):
        self.logger = logger
        self.__sound_callback = sound_callback
        self.__stream = None

    def __audio_callback(self, indata, frames, time, status):
        """Audio callback function that gets called when audio data is available"""
        if isinstance(status, list):  # status가 리스트일 경우, 함수처럼 호출하지 않도록 처리    
            self.logger.debug(f"Status is a list: {status}")
        else:
            self.__sound_callback(self.get_sample_rate(), indata)
         
    def input_start(self, idx=None):
        self.__stream = sd.InputStream(
            dtype="int16",
            blocksize=1024,
            callback=self.__audio_callback,
            device=idx,
            channels=1,
            latency='high'
        )
        self.sample_rate = self.__stream.samplerate

        self.__stream.start()

        self.logger.debug(f"SoundInput을 시작했습니다. sample_rate: {self.sample_rate}")

    def input_exit(self):
        if not self.__stream:
            self.logger.debug("Stream not initialized.")
            return
        
        self.__stream.stop()
        self.__stream.close()

        self.logger.debug("SoundInput을 종료했습니다.")

    def get_current_input_device_idx(self) -> int:
        if not self.__stream:
            return 0
        
        input_dev = self.__stream.device
        return input_dev # type: ignore
    
    def get_sample_rate(self) -> int:
        return int(self.sample_rate)

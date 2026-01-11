from logging import Logger
import numpy as np
import os
from RealtimeSTT import AudioToTextRecorder as ATTR
from scipy.signal import resample
from threading import Thread
from typing import Callable

TARGET_SAMPLE_RATE = 16000

class STT:
    def __init__(
        self,
        logger: Logger,
        complete_callback: Callable[[str], None],
        realtime_callback: Callable[[str], None]
    ):
        self.logger = logger
        self.complete_callback = complete_callback
        self.realtime_callback = realtime_callback
        self.model_has_been_started = False

    def start_model(self, input_device_index: int = 0):
        self.model = ATTR(
            model= "deepdml/faster-whisper-large-v3-turbo-ct2",
            input_device_index=input_device_index,
            use_microphone=False,

            enable_realtime_transcription=True,
            on_realtime_transcription_stabilized=self.realtime_callback,
            realtime_model_type="small",
            realtime_processing_pause=0.5,

            post_speech_silence_duration=0.1,

            silero_sensitivity=0.05,
            webrtc_sensitivity=1,

            spinner=True if os.getenv("APP_DEBUG") else False,

            no_log_file=False if os.getenv("APP_DEBUG") else True,
        )

        self.model_has_been_started = True
        self.model_thread = Thread(target=self.process_model, daemon=True)
        self.model_thread.start()
    
    def stop_model(self):
        if not self.model_has_been_started:
            return
        
        # 모델 강제 종료
        try:
            self.model.abort()
            self.model.stop()
            self.model.shutdown()
            del self.model
        except AttributeError:
            pass

    def process_model(self):
        try:
            while True:
                self.model.text(self.complete_callback)
        except AttributeError:
            # 강제 종료시 발생.
            pass
    
    def on_sound_callback(self, sample_rate: int, sounddata: np.ndarray):
        self.model.feed_audio(self.decode_and_resample(sounddata, sample_rate, TARGET_SAMPLE_RATE))

    def decode_and_resample(self, audio_data, original_sample_rate: int, target_sample_rate: int):
        try:
            num_original_samples = len(audio_data)
            num_target_samples = int(num_original_samples * target_sample_rate / original_sample_rate)
            resampled_audio = resample(audio_data, num_target_samples)
            return resampled_audio.astype(np.int16).tobytes() # type: ignore
        except Exception as e:
            self.logger.error(f"Error in resampling: {e}")
            return audio_data

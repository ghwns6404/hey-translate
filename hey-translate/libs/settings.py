from configparser import ConfigParser
import os.path
import platformdirs
from typing import Literal

type AppTheme = Literal["system", "light", "dark"]

class Settings:
    def __init__(self):
        self.config = ConfigParser()
        if not os.path.exists(self.get_settings_path()):
            # 기본값
            self.config["appearance"] = {}
            self.config.set("appearance", "theme", "system")
            self.config.set("appearance", "scaling", "100")
            self.config["output"] = {}
            self.config.set("output", "languages", "origin,en-us")
            self.config["deepl"] = {}
            self.config.set("deepl", "auth_key", "-")
            self.save()

        self.config.read(self.get_settings_path())

    def exit(self):
        self.save()

    def get_data_dir(self) -> str:
        return platformdirs.user_data_dir("HeyTranslate", "Bit41", roaming=True, ensure_exists=True)

    def get_settings_path(self) -> str:
        return os.path.join(self.get_data_dir(), "settings.ini")
    
    def get_appearance_theme(self) -> str:
        return self.config.get("appearance", "theme")
    
    def set_appearance_theme(self, theme: AppTheme):
        self.config.set("appearance", "theme", theme)
    
    def get_appearance_scaling(self) -> int:
        scaling = self.config.getint("appearance", "scaling")
        if not scaling:
            raise Exception("설정(appearance.scaling) 오류")
          
        return scaling
    
    def set_appearance_scaling(self, scaling: int):
        self.config.set("appearance", "scaling", str(scaling))
    
    def get_deepl_auth_key(self) -> str:
        return self.config.get("deepl", "auth_key")
    
    def set_deepl_auth_key(self, auth_key: str):
        self.config.set("deepl", "auth_key", auth_key)
    
    def get_output_languages(self) -> list[str]:
        return self.config.get("output", "languages").split(",")
    
    def set_output_languages(self, lang_codes: list[str]):
        self.config.set("output", "languages", ",".join(lang_codes))
    
    def save(self):
        with open(self.get_settings_path(), "w") as f:
            self.config.write(f)

from control import Control
import customtkinter as ctk
from logging import Logger
import os.path
import pathlib
from PIL import Image, ImageTk
from typing import Dict
import ui.constant as constant
from ui.frames.body.help_frame import HelpFrame
from ui.frames.body.settings_frame import SettingsFrame
from ui.frames.body.translate_frame import TranslateFrame
from ui.frames.nav_frame import NavFrame

class App(ctk.CTk):
    def __init__(self, logger: Logger):
        super().__init__()

        self.logger = logger
        self.control = Control(self.logger, self.on_stt_complete, self.on_stt_realtime, self.on_output_languages_change)
        self.control.start()

        logger.debug("현재 마이크 정보:")
        logger.debug(self.control.get_microphones())

        self.title(constant.APP_NAME)
        self.geometry(f"{constant.WINDOW_WIDTH}x{constant.WINDOW_HEIGHT}")
        self.minsize(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.load_resources()

        self.wm_iconbitmap()
        self.iconphoto(False, self.img_logo_t_photo) # type: ignore
        
        # Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Nav
        self.nav_frame = NavFrame(self, self.change_body)

        # Body Frame
        self.menu_current = "번역"
        self.bodies: Dict[str, ctk.CTkFrame | ctk.CTkScrollableFrame] = {
            "번역": TranslateFrame(self),
            "설정": SettingsFrame(self, self.logger),
            "도움말": HelpFrame(self)
        }
        self.change_body(self.menu_current)

    def exit(self):
        self.control.exit()
        self.destroy()

        self.logger.info("App이 종료되었습니다.")

    def load_resources(self):
        res_path = os.path.join(pathlib.Path.cwd(), "resources")
        img_path = os.path.join(res_path, "images")

        self.img_logo_t = ctk.CTkImage(Image.open(os.path.join(img_path, "logos", "hey_translate_t.png")), size=(70, 70))
        self.img_logo_t_photo = ImageTk.PhotoImage(file=os.path.join(img_path, "logos", "hey_translate_t.png"))

        self.img_logo = ctk.CTkImage(Image.open(os.path.join(img_path, "logos", "hey_translate.png")), size=(450 // 2, 250 // 2))

        # 아이콘 불러오기
        self.icons: Dict[str, ctk.CTkImage] = {}
        for icon_name in constant.RES_IMG_ICONS:
            img_light = Image.open(os.path.join(img_path, "icons", f"{icon_name}-light.png"))
            img_dark = Image.open(os.path.join(img_path, "icons", f"{icon_name}-dark.png"))
            self.icons[icon_name] = ctk.CTkImage(img_light, img_dark, (30, 30))
    
    def on_closing(self):
        self.exit()
    
    def on_stt_complete(self, result: Dict[str, str]):
        if isinstance(self.bodies["번역"], TranslateFrame):
            self.bodies["번역"].on_stt_complete(result)

    def on_stt_realtime(self, result: Dict[str, str]):
        if isinstance(self.bodies["번역"], TranslateFrame):
            self.bodies["번역"].on_stt_realtime(result)
    
    def on_output_languages_change(self, lang_codes: list[str]):
        if isinstance(self.bodies["번역"], TranslateFrame):
            self.bodies["번역"].on_output_languages_change(lang_codes)

    def change_body(self, name: str):
        self.bodies[self.menu_current].grid_forget()
        self.nav_frame.menu_items[self.menu_current].configure(fg_color="transparent")

        self.menu_current = name
        self.bodies[name].grid(row=0, column=1, sticky="nsew")
        self.nav_frame.menu_items[name].configure(fg_color=constant.BTN_BG_COLOR)

        self.logger.debug(f"App.Body({name})로 변경되었습니다.")

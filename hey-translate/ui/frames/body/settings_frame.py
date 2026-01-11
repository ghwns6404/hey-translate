import customtkinter as ctk
from logging import Logger
import ui.constant as constant

from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from ui.app import App

class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master: "App", logger: Logger, **kwargs):
        super().__init__(master, **kwargs)

        self.logger = logger
        self.control = master.control
        self.settings = master.control.settings

        self.configure(corner_radius=0, fg_color=constant.BG_COLOR)

        self.grid_columnconfigure(0, weight=1)

        self.init_ui(master)
    
    def init_ui(self, master: "App"):
        # 제목
        self.title = ctk.CTkLabel(
            self, 
            text="설정", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 테마
        self.title_appearance_theme = ctk.CTkLabel(
            self, 
            text="테마", 
            font=ctk.CTkFont(size=24)
        )
        self.title_appearance_theme.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        font_settings = ctk.CTkFont(size=20)
        self.appearance_theme_var = ctk.StringVar(value=self.settings.get_appearance_theme())
        ctk.set_appearance_mode(self.appearance_theme_var.get())
        self.appearance_theme_btns = [
            ctk.CTkRadioButton(self, text="시스템", variable=self.appearance_theme_var, value="system", font=font_settings, fg_color=constant.PRIMARY_COLOR, hover_color=constant.PRIMARY_COLOR, command=self.on_appearance_theme_change).grid(row=3, sticky="w", padx=30, pady=10),
            ctk.CTkRadioButton(self, text="밝은 색", variable=self.appearance_theme_var, value="light", font=font_settings, fg_color=constant.PRIMARY_COLOR, hover_color=constant.PRIMARY_COLOR, command=self.on_appearance_theme_change).grid(row=4, sticky="w", padx=30, pady=10),
            ctk.CTkRadioButton(self, text="어두운 색", variable=self.appearance_theme_var, value="dark", font=font_settings, fg_color=constant.PRIMARY_COLOR, hover_color=constant.PRIMARY_COLOR, command=self.on_appearance_theme_change).grid(row=5, sticky="w", padx=30, pady=10)
        ]

        # 배율
        self.title_appearance_scaling = ctk.CTkLabel(
            self, 
            text="배율", 
            font=ctk.CTkFont(size=24)
        )
        self.title_appearance_scaling.grid(row=6, column=0, padx=20, pady=(30, 10), sticky="w")

        scaling = self.settings.get_appearance_scaling()
        ctk.set_widget_scaling(scaling / 100)
        self.appearance_scaling_options = ctk.CTkOptionMenu(self, values=[f"{scale}%" for scale in range(50, 260, 10)], font=font_settings, fg_color=constant.BTN_BG_COLOR, button_color=constant.PRIMARY_COLOR, button_hover_color=constant.PRIMARY_COLOR, command=self.on_appearance_scaling_change)
        self.appearance_scaling_options.set(f"{scaling}%")
        self.appearance_scaling_options.grid(row=7, column=0, padx=20, pady=20, sticky="w")


        # 언어 선택
        self.title_output_languages = ctk.CTkLabel(
            self,
            text="출력 언어",
            font=ctk.CTkFont(size=24)
        )
        self.title_output_languages.grid(row=8, column=0, padx=20, pady=(30, 10), sticky="w")

        self.output_lang_frame = ctk.CTkScrollableFrame(self, height=300)
        self.output_lang_frame.grid(row=9, column=0, padx=20, pady=20, sticky="ew")
        self.output_lang_frame.columnconfigure(0, weight=1)

        self.init_output_languages(True)


        # DeepL Auth Key
        self.title_appearance_scaling = ctk.CTkLabel(
            self, 
            text="DeepL 인증키",
            font=ctk.CTkFont(size=24)
        )
        self.title_appearance_scaling.grid(row=10, column=0, padx=20, pady=(30, 10), sticky="w")

        self.deepl_auth_key_entry = ctk.CTkEntry(self, placeholder_text="DeepL 인증키", height=50, font=font_settings)
        self.deepl_auth_key_entry.grid(row=11, column=0, padx=20, pady=20, sticky="ew")
        self.deepl_auth_key_entry.insert(0, self.settings.get_deepl_auth_key())
        self.deepl_auth_key_entry.bind("<KeyRelease>", self.on_deepl_auth_key_change)

    def init_output_languages(self, is_first: bool):
        if not is_first:
            for lang in self.output_langs.values():
                lang.grid_forget()

        self.output_langs: Dict[str, ctk.CTkCheckBox] = {}
        for (row, (lang_code, lang_name)) in enumerate(constant.LANGS.items()):
            self.output_langs[lang_code] = ctk.CTkCheckBox(
                self.output_lang_frame, text=lang_name, font=ctk.CTkFont(size=20),
                fg_color=constant.PRIMARY_COLOR, hover_color=constant.BTN_HOVER_COLOR,
                checkmark_color="GRAY30", command=self.on_lang_change
            )
            self.output_langs[lang_code].grid(row=row, column=0, padx=10, pady=10, sticky="w")
        
        self.set_selected_languages(self.control.get_output_lang_codes())

    def on_appearance_theme_change(self):
        theme = self.appearance_theme_var.get()

        ctk.set_appearance_mode(theme)
        self.settings.set_appearance_theme(theme) # type: ignore
        self.settings.save()
    
    def on_appearance_scaling_change(self, scale: str):
        scale_value = int(scale.replace("%", ""))

        ctk.set_widget_scaling(scale_value / 100)
        self.settings.set_appearance_scaling(scale_value)
        self.settings.save()
    
    def on_lang_change(self):
        output_langs = self.get_selected_languages()
        if len(output_langs) < 1:
            self.init_output_languages(False)
            return
        
        self.logger.debug(f"Settings.output_langs({output_langs})로 변경되었습니다.")
        
        self.control.set_output_lang_codes(output_langs)

    def on_deepl_auth_key_change(self, event):
        auth_key = self.deepl_auth_key_entry.get()
        if not auth_key:
            return
        
        self.control.set_deepl_auth_key(auth_key)
        self.settings.set_deepl_auth_key(auth_key)
        self.settings.save()
    
    def get_selected_languages(self):
        return [lang_code for lang_code, checkbox in self.output_langs.items() if checkbox.get() == 1]
    
    def set_selected_languages(self, lang_codes: list[str]):
        for lang_code in lang_codes:
            self.output_langs[lang_code].select()

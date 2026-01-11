import customtkinter as ctk
import ui.constant as constant
from ui.libs.CTkScrollableDropdown.ctk_scrollable_dropdown import CTkScrollableDropdown
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ui.app import App

class TranslateFrame(ctk.CTkFrame):
    def __init__(self, master: "App", **kwargs):
        super().__init__(master, **kwargs)

        self.icons = master.icons
        self.control = master.control

        self.configure(corner_radius=0, fg_color=constant.BG_COLOR)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_ui(master)
    
    def init_ui(self, master: "App"):
        # Toolbar
        self.toolbar = ctk.CTkFrame(self, height=60, corner_radius=20, border_color=constant.BG_COLOR, border_width=8)
        self.toolbar.grid(row=0, column=0, sticky="nsew")
        self.toolbar.grid_columnconfigure(0, weight=1)

        toolbar_font = ctk.CTkFont(size=18)

        self.toolbar_btn_record_state = False
        self.toolbar_btn_record = ctk.CTkButton(self.toolbar, text="녹음 시작", image=master.icons["play"], font=toolbar_font, fg_color="RED", text_color=constant.BTN_TEXT_COLOR, hover_color="DARKGREEN", width=70, command=self.on_toolbar_btn_record_click)
        self.toolbar_btn_record.grid(column=1, row=0, sticky="e", padx=5, pady=15)

        #self.toolbar_btn_save = ctk.CTkButton(self.toolbar, text="저장", image=master.icons["save"], font=toolbar_font, fg_color=constant.BTN_BG_COLOR, text_color=constant.BTN_TEXT_COLOR, hover_color=constant.BTN_HOVER_COLOR, width=60)
        #self.toolbar_btn_save.grid(column=2, row=0, sticky="e", padx=(5, 20))

        self.toolbar_optionmenu_mic = ctk.CTkOptionMenu(self.toolbar, values=self.control.get_microphone_names(), font=toolbar_font, width=300, fg_color=constant.BTN_BG_COLOR, button_color=constant.PRIMARY_COLOR, button_hover_color=constant.PRIMARY_COLOR)
        self.toolbar_optionmenu_mic.grid(column=3, row=0, sticky="e", padx=(5, 20))

        self.after(1000, self.refresh_mics)


        # Output
        self.outputs = ctk.CTkScrollableFrame(self, fg_color=constant.BG_COLOR)
        self.outputs.grid_columnconfigure(0, weight=1)
        self.outputs.grid(row=1, sticky="nsew")

        self.init_outputs(True)
    
    def init_outputs(self, first_time: bool):
        if not first_time:
            for (lang_code, frame) in self.output_items.items():
                frame.grid_forget()

        self.output_items: Dict[str, TranslateOutputFrame] = {}
        for idx, lang_code in enumerate(self.control.get_output_lang_codes()):
            self.output_items[lang_code] = TranslateOutputFrame(self.outputs, idx, lang_code, constant.LANGS[lang_code])
    
    def refresh_mics(self):
        # 마이크 목록 갱신은 녹음 상태일 때 하면 안 돼요.
        if self.toolbar_btn_record_state:
            device_idx = self.control.get_current_input_device_idx()
            if device_idx:
                self.toolbar_optionmenu_mic.set(self.control.get_microphones_i_s()[device_idx])

            self.after(1000, self.refresh_mics)
            return
        
        self.toolbar_optionmenu_mic.configure(values=self.control.get_microphone_names(True))

        self.after(1000, self.refresh_mics)
    
    def on_toolbar_btn_record_click(self):
        self.toolbar_btn_record_state = not self.toolbar_btn_record_state

        btn = self.toolbar_btn_record
        if self.toolbar_btn_record_state:
            btn.configure(fg_color="ORANGE", text="녹음 시작 중...", state="disabled")
            btn.update()
            self.control.record_start(self.toolbar_optionmenu_mic.get())

            btn.configure(fg_color="GREEN", hover_color="DARKRED", text="녹음 중지", image=self.icons["pause"], state="normal")
        else:
            btn.configure(fg_color="ORANGE", text="녹음 중지 중...", state="disabled")
            btn.update()
            self.control.record_stop()

            btn.configure(fg_color="RED", hover_color="DARKGREEN", text="녹음 시작", image=self.icons["play"], state="normal")

    def on_stt_complete(self, result: Dict[str, str]):
        for lang_code, text in result.items():
            self.output_items[lang_code].on_stt_complete(text)
    
    def on_stt_realtime(self, result: Dict[str, str]):
        for lang_code, text in result.items():
            self.output_items[lang_code].on_stt_realtime(text)
    
    def on_output_languages_change(self, lang_codes: list[str]):
        self.init_outputs(False)

class TranslateOutputFrame(ctk.CTkFrame):
    def __init__(self, master, row: int, lang_code: str, lang_name: str, **kwargs):
        super().__init__(master, **kwargs)

        self.lang_code = lang_code
        self.lang_name = lang_name

        self.grid(row=row, padx=10, pady=10, sticky="ew")

        self.grid_columnconfigure(0, weight=1)

        self.init_ui(master)
    
    def init_ui(self, master: "App"):
        self.title = ctk.CTkLabel(self, text=self.lang_name, font=ctk.CTkFont(size=24))
        self.title.grid(row=0, padx=10, pady=5, sticky="w")

        self.output = ctk.CTkTextbox(self, height=200, font=ctk.CTkFont(size=20), state="disabled")
        self.output.tag_config("REALTIME", foreground="gray50")
        self.output.grid(row=1, padx=10, pady=(0, 10), sticky="ew")
    
    def on_stt_realtime(self, text: str):
        self.output.configure(state="normal")
        self.output.delete("end-1c linestart", "end-1c")
        self.output.insert("end", text)
        self.output.tag_add("REALTIME", "end-1c linestart", "end-1c")
        self.output.configure(state="disabled")

        self.output.see("end")

    def on_stt_complete(self, text: str):
        self.output.configure(state="normal")
        self.output.delete("end-1c linestart", "end-1c")
        self.output.insert("end", text)
        self.output.tag_remove("REALTIME", "end-1c linestart", "end-1c")
        self.output.insert("end", "\n")
        self.output.configure(state="disabled")

        self.output.see("end")

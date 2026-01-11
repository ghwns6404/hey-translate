import customtkinter as ctk
from typing import Callable, Dict
import ui.constant as constant
from ui.libs.CTkScrollableDropdown import CTkScrollableDropdown

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.app import App

class NavFrame(ctk.CTkFrame):
    def __init__(self, master: "App", on_change_body: Callable[[str], None], **kwargs):
        super().__init__(master, **kwargs)

        self.on_change_body = on_change_body

        self.configure(corner_radius=0)

        self.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_ui(master)
    
    def init_ui(self, master: "App"):
        # Nav Logo
        self.nav_frame_logo = ctk.CTkLabel(self, image=master.img_logo, text="")
        self.nav_frame_logo.grid(row=0, column=0, padx=25, pady=20, sticky="ew")

        # Nav Menu
        self.nav_font_btn = ctk.CTkFont(size=20)
        self.menus = [
            {
                "name": "번역",
                "icon": master.icons["audio-lines"],
            },
            {
                "name": "설정",
                "icon": master.icons["settings"],
            },
            {
                "name": "도움말",
                "icon":  master.icons["circle-help"],
            }
        ]
        self.menu_items: Dict[str, ctk.CTkButton] = {}

        for row, menu in enumerate(self.menus, start=1):
            self.add_nav_menu(row, menu["name"], menu["icon"])
    
    def add_nav_menu(self, row: int, text: str, icon: ctk.CTkImage):
        self.menu_items[text] = ctk.CTkButton(
            self, corner_radius=10, border_spacing=10, text=text, image=icon,
            fg_color="transparent", text_color=constant.BTN_TEXT_COLOR, hover_color=constant.BTN_HOVER_COLOR,
            anchor="w", font=self.nav_font_btn, command=lambda: self.on_nav_menu_click(text)
        )
        self.menu_items[text].grid(row=row, column=0, padx=20, pady=5, sticky="ew")
    
    def on_nav_menu_click(self, text: str):
        self.on_change_body(text)

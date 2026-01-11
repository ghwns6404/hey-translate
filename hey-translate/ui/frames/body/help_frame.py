import customtkinter as ctk
import ui.constant as constant

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.app import App

class HelpFrame(ctk.CTkFrame):
    def __init__(self, master: "App", **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=0, fg_color=constant.BG_COLOR)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.set_ui()
        
    def set_ui(self):
        # 제목
        self.title_label = ctk.CTkLabel(
            self, 
            text="도움말", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="w")
        
        # 스크롤 가능한 프레임
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Hey! 번역 사용 가이드", label_font=ctk.CTkFont(size=24, weight="bold"))
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # 도움말 내용
        help_content = [
            ("음성 녹음 기능", 
             "• '녹음 시작' 버튼을 클릭하여 음성 녹음을 시작할 수 있습니다.\n"
             "• 녹음된 음성은 자동으로 텍스트로 변환됩니다.\n"
             "• 마이크 권한이 필요합니다."),
            
            ("번역 기능",
             "• 영어 텍스트를 입력하면 중국어와 일본어로 번역됩니다.\n"
             "• 실시간 번역을 지원합니다.\n"
             "• API 키 설정이 필요합니다."),
            
            ("저장 기능",
             "• 번역 결과를 텍스트 파일로 저장할 수 있습니다.\n"
             "• 음성 파일도 함께 저장 가능합니다.\n"
             "• 저장 위치를 선택할 수 있습니다."),
            
            ("마이크 설정",
             "• 마이크 버튼을 통해 음성 입력 장치를 선택할 수 있습니다.\n"
             "• 음성 인식 품질을 조정할 수 있습니다.\n"
             "• 노이즈 제거 기능을 제공합니다."),
            
            ("설정",
             "• 테마 설정: Light, Dark, System 모드를 선택할 수 있습니다.\n"
             "• UI 크기: 80%~120% 사이에서 인터페이스 크기를 조정할 수 있습니다.\n"
             "• API 키: API 인증 키를 설정하여 번역 서비스를 이용할 수 있습니다."),
            
            ("언어 선택",
             "• 번역할 언어를 선택할 수 있습니다.\n"
             "• 여러 언어를 동시에 선택 가능합니다.\n"
             "• 자주 사용하는 언어를 즐겨찾기로 등록할 수 있습니다."),
            
            ("문제 해결",
             "• 마이크가 인식되지 않는 경우: 시스템 설정에서 마이크 권한을 확인하세요.\n"
             "• 번역이 되지 않는 경우: API 키가 올바르게 설정되었는지 확인하세요.\n"
             "• 프로그램이 느린 경우: UI 크기를 90% 이하로 설정해보세요."),
            
            ("지원",
             "• 버전: Hey! 번역 v1.0\n"
             "• 문의: support@heytranslate.com\n"
             "• 업데이트 확인: 설정 메뉴에서 확인 가능합니다.")
        ]
        
        # 도움말 항목들을 추가
        for i, (title, content) in enumerate(help_content):
            # 제목 라벨
            title_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=title,
                font=ctk.CTkFont(size=20, weight="bold"),
                anchor="w"
            )
            title_label.grid(row=i*2, column=0, padx=10, pady=(15, 5), sticky="ew")
            
            # 내용 라벨
            content_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=content,
                font=ctk.CTkFont(size=16),
                anchor="nw",
                justify="left",
                wraplength=600
            )
            content_label.grid(row=i*2+1, column=0, padx=20, pady=(0, 10), sticky="ew")

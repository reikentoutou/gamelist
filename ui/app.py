"""Main application class — composes all view mixins."""

import customtkinter as ctk

from config import FONT_FAMILY, ACCENT, ACCENT_HOVER
from data import load_data, migrate_old_data
from i18n import I18N
from ui.views import QueryMixin, SubmitMixin, ManageMixin
from ui.windows import AvailableWindowMixin, PendingWindowMixin


class GameQueryApp(
    QueryMixin,
    SubmitMixin,
    ManageMixin,
    AvailableWindowMixin,
    PendingWindowMixin,
):
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.resizable(False, False)
        self.lang = "zh"
        self.data = load_data()
        migrate_old_data(self.data)
        self._build_ui()
        self._center_window()

    # ── i18n ──────────────────────────────────────────────────

    def t(self, key, **kwargs):
        text = I18N[self.lang][key]
        return text.format(**kwargs) if kwargs else text

    def _set_lang(self, lang):
        self.lang = lang
        for child in self.root.winfo_children():
            child.destroy()
        self._build_ui()
        self._center_window()

    # ── Layout ────────────────────────────────────────────────

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def _build_ui(self):
        self.root.title(self.t("title"))
        self._build_lang_bar()
        self._build_query_section()
        self._build_submit_section()
        self._build_manage_section()

    def _build_lang_bar(self):
        bar = ctk.CTkFrame(self.root, fg_color="transparent")
        bar.pack(padx=16, pady=(12, 0), anchor="e")
        for code, label in [("zh", "中文"), ("en", "EN"), ("ja", "日本語")]:
            ctk.CTkButton(
                bar, text=label, width=60, height=28,
                corner_radius=14,
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                fg_color=ACCENT if code == self.lang else "transparent",
                text_color="white" if code == self.lang else None,
                border_width=1,
                border_color=ACCENT,
                hover_color=ACCENT_HOVER,
                command=lambda c=code: self._set_lang(c),
            ).pack(side="left", padx=3)

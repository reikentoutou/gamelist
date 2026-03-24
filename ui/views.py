"""Main window sections: query, submit, manage buttons."""

import sys
from tkinter import filedialog, messagebox

import customtkinter as ctk

from config import (
    FONT_FAMILY, ACCENT, ACCENT_HOVER, SUCCESS_FG, MISS_FG,
    IMPORT_BTN, IMPORT_BTN_HOVER,
)
from data import (
    load_data, save_data,
    read_import_file, parse_import_rows, import_games,
    game_display_name, game_all_names, search_games,
)


class QueryMixin:
    """Query section on the main page."""

    def _build_query_section(self):
        frame = ctk.CTkFrame(self.root, corner_radius=12)
        frame.pack(padx=16, pady=(8, 6), fill="x")

        ctk.CTkLabel(
            frame, text=self.t("query_frame"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(12, 4))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 4))

        ctk.CTkLabel(row, text=self.t("game_name"),
                      font=ctk.CTkFont(family=FONT_FAMILY, size=13)).pack(side="left")
        self.query_entry = ctk.CTkEntry(
            row, width=300, height=36,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            placeholder_text="Cyberpunk 2077 ...",
        )
        self.query_entry.pack(side="left", padx=(6, 8))
        self.query_entry.bind("<Return>", lambda e: self._do_query())
        ctk.CTkButton(
            row, text=self.t("btn_query"), width=100, height=36,
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            command=self._do_query,
        ).pack(side="left")

        self.result_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.result_frame.pack(fill="x", padx=16, pady=(0, 12))

        self.query_result = ctk.CTkTextbox(
            self.result_frame, height=1, width=520,
            wrap="word", state="disabled",
            fg_color="transparent", border_width=0,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
        )

    def _do_query(self):
        keyword = self.query_entry.get().strip()
        if not keyword:
            messagebox.showwarning(self.t("dlg_tip"), self.t("warn_empty"))
            return

        self.data = load_data()
        matches = search_games(self.data, keyword)

        self.query_result.pack_forget()
        self.query_result.configure(state="normal")
        self.query_result.delete("1.0", "end")

        if matches:
            lines = []
            for key, info in matches.items():
                display = game_display_name(info, self.lang)
                names = game_all_names(info)
                lines.append(
                    f"{self.t('downloaded')} {display}\n"
                    f"  {names}\n"
                    f"  {self.t('system_prefix')}{info['system']}"
                    f"　{self.t('launch_prefix')}{info['launch']}"
                )
            self.query_result.insert("1.0", "\n".join(lines))
            self.query_result.configure(
                text_color=SUCCESS_FG,
                height=min(len(matches) * 55, 250),
            )
        else:
            self.query_result.insert("1.0", self.t("not_downloaded"))
            self.query_result.configure(text_color=MISS_FG, height=30)

        self.query_result.configure(state="disabled")
        self.query_result.pack(fill="x", pady=(4, 0))


class SubmitMixin:
    """Submit game request section on the main page."""

    def _build_submit_section(self):
        frame = ctk.CTkFrame(self.root, corner_radius=12)
        frame.pack(padx=16, pady=6, fill="x")

        ctk.CTkLabel(
            frame, text=self.t("submit_frame"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(12, 4))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkLabel(row, text=self.t("game_name"),
                      font=ctk.CTkFont(family=FONT_FAMILY, size=13)).pack(side="left")
        self.submit_entry = ctk.CTkEntry(
            row, width=300, height=36,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            placeholder_text="Game name ...",
        )
        self.submit_entry.pack(side="left", padx=(6, 8))
        self.submit_entry.bind("<Return>", lambda e: self._do_submit())
        ctk.CTkButton(
            row, text=self.t("btn_submit"), width=100, height=36,
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            command=self._do_submit,
        ).pack(side="left")

    def _do_submit(self):
        name = self.submit_entry.get().strip()
        if not name:
            messagebox.showwarning(self.t("dlg_tip"), self.t("warn_empty"))
            return

        self.data = load_data()

        if name in self.data["available"]:
            messagebox.showinfo(self.t("dlg_tip"), self.t("info_exists"))
            return
        if name in self.data["pending"]:
            messagebox.showinfo(self.t("dlg_tip"), self.t("info_pending"))
            return

        self.data["pending"].append(name)
        save_data(self.data)
        self.submit_entry.delete(0, "end")
        messagebox.showinfo(self.t("dlg_success"), self.t("info_submitted", name=name))


class ManageMixin:
    """Manage buttons and bulk-import on the main page."""

    def _build_manage_section(self):
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(padx=16, pady=(6, 16), fill="x")

        ctk.CTkButton(
            frame, text=self.t("btn_view_all"), height=40,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self._open_available_window,
        ).pack(fill="x", pady=(0, 8))
        ctk.CTkButton(
            frame, text=self.t("btn_manage"), height=40,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self._open_manage_window,
        ).pack(fill="x", pady=(0, 8))
        ctk.CTkButton(
            frame, text=self.t("btn_import"), height=40,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            fg_color=IMPORT_BTN, hover_color=IMPORT_BTN_HOVER,
            command=self._do_bulk_import,
        ).pack(fill="x")

    def _do_bulk_import(self):
        if sys.platform == "win32":
            csv_txt_glob = "*.csv;*.txt"
        else:
            csv_txt_glob = "*.csv *.txt"
        filepath = filedialog.askopenfilename(
            title=self.t("import_title"),
            filetypes=[
                ("CSV / TXT", csv_txt_glob),
                ("CSV", "*.csv"),
                ("TXT", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        if not filepath:
            return

        content = read_import_file(filepath)
        if content is None:
            messagebox.showerror(self.t("dlg_tip"), self.t("import_read_err"))
            return

        rows = parse_import_rows(content)
        self.data = load_data()
        added, skipped, error_line = import_games(self.data, rows)

        if error_line:
            messagebox.showwarning(self.t("dlg_tip"), self.t("import_format_err", line=error_line))
            return

        if added == 0 and skipped == 0:
            messagebox.showinfo(self.t("dlg_tip"), self.t("import_empty"))
            return

        save_data(self.data)
        msg = self.t("import_success", count=added)
        if skipped:
            msg += self.t("import_skip", skip=skipped)
        messagebox.showinfo(self.t("dlg_success"), msg)

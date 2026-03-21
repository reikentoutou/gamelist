import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

from data import (
    load_data, save_data, migrate_old_data,
    read_import_file, parse_import_rows, import_games,
    game_display_name, game_all_names, search_games,
    build_game_record,
)
from i18n import I18N

ACCENT = "#1E90FF"
ACCENT_HOVER = "#1C86EE"
DANGER = "#E74C3C"
DANGER_HOVER = "#C0392B"
SUCCESS_FG = "#2ECC71"
MISS_FG = "#E74C3C"


class GameQueryApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.resizable(False, False)
        self.lang = "zh"
        self.data = load_data()
        migrate_old_data(self.data)
        self._build_ui()
        self._center_window()

    # ── i18n helper ───────────────────────────────────────────

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
                fg_color=ACCENT if code == self.lang else "transparent",
                text_color="white" if code == self.lang else None,
                border_width=1,
                border_color=ACCENT,
                hover_color=ACCENT_HOVER,
                command=lambda c=code: self._set_lang(c),
            ).pack(side="left", padx=3)

    # ── Query section ─────────────────────────────────────────

    def _build_query_section(self):
        frame = ctk.CTkFrame(self.root, corner_radius=12)
        frame.pack(padx=16, pady=(8, 6), fill="x")

        ctk.CTkLabel(frame, text=self.t("query_frame"),
                      font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=16, pady=(12, 4))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 4))

        ctk.CTkLabel(row, text=self.t("game_name")).pack(side="left")
        self.query_entry = ctk.CTkEntry(row, width=240, placeholder_text="Cyberpunk 2077 ...")
        self.query_entry.pack(side="left", padx=(6, 8))
        self.query_entry.bind("<Return>", lambda e: self._do_query())
        ctk.CTkButton(row, text=self.t("btn_query"), width=80,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       command=self._do_query).pack(side="left")

        self.result_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.result_frame.pack(fill="x", padx=16, pady=(0, 12))

        self.query_result = ctk.CTkTextbox(
            self.result_frame, height=1, width=460,
            wrap="word", state="disabled",
            fg_color="transparent", border_width=0,
            font=ctk.CTkFont(size=13),
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
            text = "\n".join(lines)
            self.query_result.insert("1.0", text)
            self.query_result.configure(
                text_color=SUCCESS_FG,
                height=min(len(matches) * 55, 250),
            )
        else:
            self.query_result.insert("1.0", self.t("not_downloaded"))
            self.query_result.configure(text_color=MISS_FG, height=30)

        self.query_result.configure(state="disabled")
        self.query_result.pack(fill="x", pady=(4, 0))

    # ── Submit section ────────────────────────────────────────

    def _build_submit_section(self):
        frame = ctk.CTkFrame(self.root, corner_radius=12)
        frame.pack(padx=16, pady=6, fill="x")

        ctk.CTkLabel(frame, text=self.t("submit_frame"),
                      font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=16, pady=(12, 4))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkLabel(row, text=self.t("game_name")).pack(side="left")
        self.submit_entry = ctk.CTkEntry(row, width=240, placeholder_text="Game name ...")
        self.submit_entry.pack(side="left", padx=(6, 8))
        self.submit_entry.bind("<Return>", lambda e: self._do_submit())
        ctk.CTkButton(row, text=self.t("btn_submit"), width=80,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       command=self._do_submit).pack(side="left")

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

    # ── Manage / import section ───────────────────────────────

    def _build_manage_section(self):
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(padx=16, pady=(6, 16), fill="x")

        ctk.CTkButton(
            frame, text=self.t("btn_view_all"), height=36,
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self._open_available_window,
        ).pack(fill="x", pady=(0, 6))
        ctk.CTkButton(
            frame, text=self.t("btn_manage"), height=36,
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self._open_manage_window,
        ).pack(fill="x", pady=(0, 6))
        ctk.CTkButton(
            frame, text=self.t("btn_import"), height=36,
            fg_color="#6C63FF", hover_color="#5A52D5",
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

    # ── Available games window ────────────────────────────────

    def _style_treeview(self, win):
        """Apply dark-theme styling to ttk.Treeview inside the given window."""
        style = ttk.Style(win)
        is_dark = ctk.get_appearance_mode() == "Dark"
        if is_dark:
            bg, fg, sel_bg = "#2b2b2b", "#dcdcdc", "#1E90FF"
            heading_bg, heading_fg = "#3a3a3a", "#ffffff"
            stripe = "#323232"
        else:
            bg, fg, sel_bg = "#ffffff", "#1a1a1a", "#1E90FF"
            heading_bg, heading_fg = "#e8e8e8", "#1a1a1a"
            stripe = "#f5f5f5"

        style.theme_use("default")
        style.configure("Game.Treeview",
                         background=bg, foreground=fg, fieldbackground=bg,
                         rowheight=28, font=("", 12), borderwidth=0)
        style.configure("Game.Treeview.Heading",
                         background=heading_bg, foreground=heading_fg,
                         font=("", 13, "bold"), borderwidth=0, relief="flat")
        style.map("Game.Treeview",
                   background=[("selected", sel_bg)],
                   foreground=[("selected", "#ffffff")])
        style.map("Game.Treeview.Heading",
                   background=[("active", heading_bg)])

        return stripe

    def _open_available_window(self):
        self.data = load_data()
        win = ctk.CTkToplevel(self.root)
        win.title(self.t("win_available"))
        win.resizable(True, True)
        win.geometry("820x540")
        win.after(50, lambda: self._center_toplevel(win, 820, 540))

        if not self.data["available"]:
            ctk.CTkLabel(win, text=self.t("no_available"),
                          font=ctk.CTkFont(size=14)).pack(padx=40, pady=40)
            return

        stripe_color = self._style_treeview(win)

        col_ids = ("name_zh", "name_en", "name_ja", "system", "launch")
        col_headers = [
            self.t("col_game_zh"), self.t("col_game_en"),
            self.t("col_game_ja"), self.t("col_system"),
            self.t("col_launch"),
        ]
        col_widths = (140, 190, 160, 120, 120)

        container = ctk.CTkFrame(win, corner_radius=0, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        tree = ttk.Treeview(container, columns=col_ids, show="headings",
                             style="Game.Treeview")
        for cid, heading, width in zip(col_ids, col_headers, col_widths):
            tree.heading(cid, text=heading, anchor="w")
            tree.column(cid, width=width, minwidth=60, anchor="w")

        tree.tag_configure("stripe", background=stripe_color)

        for idx, (key, info) in enumerate(self.data["available"].items()):
            vals = (
                info.get("name_zh", key), info.get("name_en", ""),
                info.get("name_ja", ""), info.get("system", ""),
                info.get("launch", ""),
            )
            tag = ("stripe",) if idx % 2 == 1 else ()
            tree.insert("", "end", values=vals, tags=tag)

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    # ── Manage pending window ─────────────────────────────────

    def _open_manage_window(self):
        self.data = load_data()
        win = ctk.CTkToplevel(self.root)
        win.title(self.t("win_manage"))
        win.resizable(False, False)
        self._populate_manage_window(win)
        win.after(50, lambda: self._center_toplevel(win))

    def _populate_manage_window(self, win):
        for child in win.winfo_children():
            child.destroy()

        if not self.data["pending"]:
            ctk.CTkLabel(win, text=self.t("no_pending"),
                          font=ctk.CTkFont(size=14)).pack(padx=40, pady=30)
            return

        outer = ctk.CTkFrame(win, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=12, pady=12)

        col_defs = [
            ("col_game_zh", 120), ("col_game_en", 120),
            ("col_game_ja", 120), ("col_system", 100),
            ("col_launch", 100), ("col_action", 140),
        ]
        header = ctk.CTkFrame(outer, corner_radius=8, fg_color=("gray85", "gray25"))
        header.pack(fill="x", pady=(0, 4))
        for i, (key, w) in enumerate(col_defs):
            ctk.CTkLabel(header, text=self.t(key), width=w,
                          anchor="w", font=ctk.CTkFont(size=13, weight="bold"),
                          ).grid(row=0, column=i, padx=6, pady=6)

        container = ctk.CTkFrame(outer, fg_color="transparent")
        container.pack(fill="both", expand=True)

        for idx, game_name in enumerate(self.data["pending"]):
            bg = ("gray92", "gray18") if idx % 2 == 0 else ("gray97", "gray22")
            row_frame = ctk.CTkFrame(container, fg_color=bg, corner_radius=4)
            row_frame.pack(fill="x", pady=1)

            ctk.CTkLabel(row_frame, text=game_name, width=120, anchor="w",
                          font=ctk.CTkFont(size=12)).grid(
                row=0, column=0, padx=6, pady=4)

            en_entry = ctk.CTkEntry(row_frame, width=120, placeholder_text="English")
            en_entry.grid(row=0, column=1, padx=4, pady=4)

            ja_entry = ctk.CTkEntry(row_frame, width=120, placeholder_text="日本語")
            ja_entry.grid(row=0, column=2, padx=4, pady=4)

            system_entry = ctk.CTkEntry(row_frame, width=100, placeholder_text="System")
            system_entry.grid(row=0, column=3, padx=4, pady=4)

            launch_entry = ctk.CTkEntry(row_frame, width=100, placeholder_text="Launch")
            launch_entry.grid(row=0, column=4, padx=4, pady=4)

            btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=5, padx=4, pady=4)

            ctk.CTkButton(
                btn_frame, text=self.t("btn_added"), width=56, height=28,
                corner_radius=6, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                command=lambda n=game_name, ee=en_entry, je=ja_entry, se=system_entry, le=launch_entry: self._confirm_add(n, ee, je, se, le, win),
            ).pack(side="left", padx=(0, 4))

            ctk.CTkButton(
                btn_frame, text=self.t("btn_delete"), width=56, height=28,
                corner_radius=6, fg_color=DANGER, hover_color=DANGER_HOVER,
                command=lambda n=game_name: self._delete_pending(n, win),
            ).pack(side="left")

    def _delete_pending(self, game_name, win):
        if not messagebox.askyesno(self.t("dlg_confirm"), self.t("confirm_delete", name=game_name), parent=win):
            return
        self.data = load_data()
        if game_name in self.data["pending"]:
            self.data["pending"].remove(game_name)
        save_data(self.data)
        self._populate_manage_window(win)

    def _confirm_add(self, game_name, en_entry, ja_entry, system_entry, launch_entry, win):
        system_val = system_entry.get().strip()
        launch_val = launch_entry.get().strip()
        en_val = en_entry.get().strip()
        ja_val = ja_entry.get().strip()

        if not system_val or not launch_val:
            messagebox.showwarning(self.t("dlg_tip"), self.t("warn_fill"), parent=win)
            return

        self.data = load_data()
        if game_name in self.data["pending"]:
            self.data["pending"].remove(game_name)
        self.data["available"][game_name] = build_game_record(game_name, en_val, ja_val, system_val, launch_val)
        save_data(self.data)
        messagebox.showinfo(self.t("dlg_success"), self.t("info_added", name=game_name), parent=win)
        self._populate_manage_window(win)

    # ── Helpers ───────────────────────────────────────────────

    @staticmethod
    def _center_toplevel(win, w=None, h=None):
        win.update_idletasks()
        if w is None:
            w = win.winfo_width()
        if h is None:
            h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

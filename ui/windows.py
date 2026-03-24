"""Popup windows: available games list, pending games management."""

from tkinter import messagebox, ttk

import customtkinter as ctk

from config import FONT_FAMILY, ACCENT, ACCENT_HOVER, DANGER, DANGER_HOVER
from data import load_data, save_data, build_game_record
from ui.theme import style_treeview, center_toplevel, labeled_entry


class AvailableWindowMixin:
    """'View all available games' popup window."""

    def _open_available_window(self):
        self.data = load_data()
        win = ctk.CTkToplevel(self.root)
        win.title(self.t("win_available"))
        win.resizable(True, True)
        win.geometry("900x600")
        win.after(50, lambda: center_toplevel(win, 900, 600))

        if not self.data["available"]:
            ctk.CTkLabel(win, text=self.t("no_available"),
                          font=ctk.CTkFont(family=FONT_FAMILY, size=14)).pack(padx=40, pady=40)
            return

        stripe_color = style_treeview(win)

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


class PendingWindowMixin:
    """'Manage pending games' popup window."""

    def _open_manage_window(self):
        self.data = load_data()
        win = ctk.CTkToplevel(self.root)
        win.title(self.t("win_manage"))
        win.resizable(True, True)
        win.geometry("1000x600")
        self._populate_manage_window(win)
        win.after(50, lambda: center_toplevel(win, 1000, 600))

    def _populate_manage_window(self, win):
        for child in win.winfo_children():
            child.destroy()

        if not self.data["pending"]:
            ctk.CTkLabel(win, text=self.t("no_pending"),
                          font=ctk.CTkFont(family=FONT_FAMILY, size=15)).pack(padx=40, pady=40)
            return

        outer = ctk.CTkFrame(win, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        scroll = ctk.CTkScrollableFrame(outer, corner_radius=8)
        scroll.pack(fill="both", expand=True)

        for idx, game_name in enumerate(self.data["pending"]):
            bg = ("gray92", "gray18") if idx % 2 == 0 else ("gray97", "gray22")
            card = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=8)
            card.pack(fill="x", pady=4, padx=4)

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=12, pady=(10, 4))

            ctk.CTkLabel(top_row, text=game_name,
                          font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
                          anchor="w").pack(side="left")

            btn_frame = ctk.CTkFrame(top_row, fg_color="transparent")
            btn_frame.pack(side="right")

            fields_row = ctk.CTkFrame(card, fg_color="transparent")
            fields_row.pack(fill="x", padx=12, pady=(0, 10))

            en_entry = labeled_entry(fields_row, self.t("col_game_en"), "English", 180)
            ja_entry = labeled_entry(fields_row, self.t("col_game_ja"), "日本語", 180)
            system_entry = labeled_entry(fields_row, self.t("col_system"), "System", 150)
            launch_entry = labeled_entry(fields_row, self.t("col_launch"), "Launch", 150)

            ctk.CTkButton(
                btn_frame, text=self.t("btn_added"), width=72, height=32,
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                corner_radius=6, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                command=lambda n=game_name, ee=en_entry, je=ja_entry, se=system_entry, le=launch_entry: self._confirm_add(n, ee, je, se, le, win),
            ).pack(side="left", padx=(0, 6))

            ctk.CTkButton(
                btn_frame, text=self.t("btn_delete"), width=72, height=32,
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
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

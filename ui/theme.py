"""Shared UI helpers: Treeview styling, window centering, labeled entry."""

from tkinter import ttk

import customtkinter as ctk

from config import FONT_FAMILY


def style_treeview(win):
    """Apply dark/light themed styling to ttk.Treeview. Returns stripe color."""
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
                     rowheight=32, font=(FONT_FAMILY, 12), borderwidth=0)
    style.configure("Game.Treeview.Heading",
                     background=heading_bg, foreground=heading_fg,
                     font=(FONT_FAMILY, 13, "bold"), borderwidth=0, relief="flat")
    style.map("Game.Treeview",
               background=[("selected", sel_bg)],
               foreground=[("selected", "#ffffff")])
    style.map("Game.Treeview.Heading",
               background=[("active", heading_bg)])
    return stripe


def center_toplevel(win, w=None, h=None):
    """Center a Toplevel window on screen."""
    win.update_idletasks()
    if w is None:
        w = win.winfo_width()
    if h is None:
        h = win.winfo_height()
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


def labeled_entry(parent, label_text, placeholder, width):
    """Create a label + entry pair packed side by side. Returns the entry widget."""
    group = ctk.CTkFrame(parent, fg_color="transparent")
    group.pack(side="left", padx=(0, 16))
    ctk.CTkLabel(group, text=label_text,
                  font=ctk.CTkFont(family=FONT_FAMILY, size=13)).pack(anchor="w")
    entry = ctk.CTkEntry(group, width=width, height=36,
                          placeholder_text=placeholder,
                          font=ctk.CTkFont(family=FONT_FAMILY, size=13))
    entry.pack(anchor="w")
    return entry

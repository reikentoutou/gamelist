import sys
import ctypes

import customtkinter as ctk

from ui import GameQueryApp

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    root = ctk.CTk()
    GameQueryApp(root)
    root.mainloop()

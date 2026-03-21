import customtkinter as ctk

from app import GameQueryApp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    root = ctk.CTk()
    GameQueryApp(root)
    root.mainloop()

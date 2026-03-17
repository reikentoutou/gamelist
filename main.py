import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_data.json")

DEFAULT_DATA = {"available": {}, "pending": []}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class GameQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESPORTS CAFE PHOENIX - 游戏查询系统")
        self.root.resizable(False, False)
        self.data = load_data()
        self._build_ui()
        self._center_window()

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

    # ── 查询模块 ──────────────────────────────────────────────

    def _build_ui(self):
        self._build_query_section()
        self._build_submit_section()
        self._build_manage_section()

    def _build_query_section(self):
        frame = tk.LabelFrame(self.root, text="游戏状态查询", padx=12, pady=8)
        frame.pack(padx=12, pady=(12, 4), fill="x")

        row = tk.Frame(frame)
        row.pack(fill="x")

        tk.Label(row, text="游戏名：").pack(side="left")
        self.query_entry = tk.Entry(row, width=30)
        self.query_entry.pack(side="left", padx=(0, 8))
        self.query_entry.bind("<Return>", lambda e: self._do_query())
        tk.Button(row, text="查询", command=self._do_query).pack(side="left")

        self.query_result = tk.Label(frame, text="", justify="left", anchor="w")
        self.query_result.pack(fill="x", pady=(6, 0))

    def _do_query(self):
        name = self.query_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入游戏名称")
            return

        self.data = load_data()
        if name in self.data["available"]:
            info = self.data["available"][name]
            text = (
                f"【已下载】\n"
                f"游戏名：{name}\n"
                f"启动系统：{info['system']}\n"
                f"启动方式：{info['launch']}"
            )
            self.query_result.config(text=text, fg="green")
        else:
            self.query_result.config(text="未下载", fg="red")

    # ── 提交需求模块 ──────────────────────────────────────────

    def _build_submit_section(self):
        frame = tk.LabelFrame(self.root, text="提交待添加游戏", padx=12, pady=8)
        frame.pack(padx=12, pady=4, fill="x")

        row = tk.Frame(frame)
        row.pack(fill="x")

        tk.Label(row, text="游戏名：").pack(side="left")
        self.submit_entry = tk.Entry(row, width=30)
        self.submit_entry.pack(side="left", padx=(0, 8))
        self.submit_entry.bind("<Return>", lambda e: self._do_submit())
        tk.Button(row, text="提交需求", command=self._do_submit).pack(side="left")

    def _do_submit(self):
        name = self.submit_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入游戏名称")
            return

        self.data = load_data()

        if name in self.data["available"]:
            messagebox.showinfo("提示", "该游戏已在网吧机器中")
            return
        if name in self.data["pending"]:
            messagebox.showinfo("提示", "该游戏已在待添加列表中")
            return

        self.data["pending"].append(name)
        save_data(self.data)
        self.submit_entry.delete(0, tk.END)
        messagebox.showinfo("成功", f"已将「{name}」加入待添加列表")

    # ── 管理入口 ──────────────────────────────────────────────

    def _build_manage_section(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=12, pady=(4, 12), fill="x")
        tk.Button(
            frame,
            text="查看 / 处理待添加游戏列表",
            command=self._open_manage_window,
        ).pack(fill="x")

    def _open_manage_window(self):
        self.data = load_data()
        win = tk.Toplevel(self.root)
        win.title("待添加游戏管理")
        win.resizable(False, False)
        self._populate_manage_window(win)

        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"+{x}+{y}")

    def _populate_manage_window(self, win):
        for child in win.winfo_children():
            child.destroy()

        if not self.data["pending"]:
            tk.Label(win, text="暂无待添加游戏", padx=40, pady=20).pack()
            return

        header = tk.Frame(win, padx=8, pady=4)
        header.pack(fill="x")
        tk.Label(header, text="游戏名", width=18, anchor="w", font=("", 0, "bold")).grid(row=0, column=0, padx=4)
        tk.Label(header, text="启动系统", width=12, font=("", 0, "bold")).grid(row=0, column=1, padx=4)
        tk.Label(header, text="启动方式", width=12, font=("", 0, "bold")).grid(row=0, column=2, padx=4)
        tk.Label(header, text="操作", width=8, font=("", 0, "bold")).grid(row=0, column=3, padx=4)

        container = tk.Frame(win, padx=8, pady=4)
        container.pack(fill="both", expand=True)

        for idx, game_name in enumerate(self.data["pending"]):
            tk.Label(container, text=game_name, width=18, anchor="w").grid(row=idx, column=0, padx=4, pady=2)

            system_entry = tk.Entry(container, width=14)
            system_entry.grid(row=idx, column=1, padx=4, pady=2)

            launch_entry = tk.Entry(container, width=14)
            launch_entry.grid(row=idx, column=2, padx=4, pady=2)

            btn = tk.Button(
                container,
                text="已添加",
                command=lambda n=game_name, se=system_entry, le=launch_entry: self._confirm_add(
                    n, se, le, win
                ),
            )
            btn.grid(row=idx, column=3, padx=4, pady=2)

    def _confirm_add(self, game_name, system_entry, launch_entry, win):
        system_val = system_entry.get().strip()
        launch_val = launch_entry.get().strip()

        if not system_val or not launch_val:
            messagebox.showwarning("提示", "请填写启动系统和启动方式", parent=win)
            return

        self.data = load_data()
        if game_name in self.data["pending"]:
            self.data["pending"].remove(game_name)
        self.data["available"][game_name] = {
            "system": system_val,
            "launch": launch_val,
        }
        save_data(self.data)
        messagebox.showinfo("成功", f"已将「{game_name}」添加至已下载列表", parent=win)
        self._populate_manage_window(win)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameQueryApp(root)
    root.mainloop()

import csv
import io
import json
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# Always store game_data.json next to the running executable/script.
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "game_data.json")

DEFAULT_DATA = {"available": {}, "pending": []}

I18N = {
    "zh": {
        "title": "ESPORTS CAFE PHOENIX - 游戏查询系统",
        "query_frame": "游戏状态查询",
        "game_name": "游戏名：",
        "btn_query": "查询",
        "submit_frame": "提交待添加游戏",
        "btn_submit": "提交需求",
        "btn_view_all": "查看所有已添加游戏",
        "btn_manage": "查看 / 处理待添加游戏列表",
        "col_game": "游戏名",
        "col_system": "启动系统",
        "col_launch": "启动方式",
        "col_action": "操作",
        "btn_added": "已添加",
        "btn_delete": "删除",
        "downloaded": "【已下载】",
        "not_downloaded": "未下载",
        "system_prefix": "启动系统：",
        "launch_prefix": "启动方式：",
        "no_pending": "暂无待添加游戏",
        "no_available": "暂无已添加游戏",
        "win_manage": "待添加游戏管理",
        "win_available": "所有已添加游戏",
        "warn_empty": "请输入游戏名称",
        "warn_fill": "请填写启动系统和启动方式",
        "info_exists": "该游戏已在网吧机器中",
        "info_pending": "该游戏已在待添加列表中",
        "info_submitted": "已将「{name}」加入待添加列表",
        "info_added": "已将「{name}」添加至已下载列表",
        "confirm_delete": "确定要删除「{name}」吗？",
        "btn_import": "批量导入（从 CSV/TXT 文件）",
        "import_title": "选择导入文件",
        "import_success": "成功导入 {count} 款游戏",
        "import_skip": "（跳过 {skip} 款已存在的游戏）",
        "import_empty": "文件中没有有效数据",
        "import_format_err": "第 {line} 行格式错误，需要3列（游戏名,启动系统,启动方式）",
        "dlg_tip": "提示",
        "dlg_success": "成功",
        "dlg_confirm": "确认",
    },
    "en": {
        "title": "ESPORTS CAFE PHOENIX - Game Query System",
        "query_frame": "Game Status Query",
        "game_name": "Game: ",
        "btn_query": "Search",
        "submit_frame": "Submit Game Request",
        "btn_submit": "Submit",
        "btn_view_all": "View All Available Games",
        "btn_manage": "View / Manage Pending Games",
        "col_game": "Game",
        "col_system": "System",
        "col_launch": "Launch",
        "col_action": "Action",
        "btn_added": "Done",
        "btn_delete": "Delete",
        "downloaded": "[Downloaded]",
        "not_downloaded": "Not Downloaded",
        "system_prefix": "System: ",
        "launch_prefix": "Launch: ",
        "no_pending": "No pending games",
        "no_available": "No available games",
        "win_manage": "Pending Games",
        "win_available": "All Available Games",
        "warn_empty": "Please enter a game name",
        "warn_fill": "Please fill in system and launch method",
        "info_exists": "This game is already available",
        "info_pending": "This game is already in the pending list",
        "info_submitted": '"{name}" has been added to the pending list',
        "info_added": '"{name}" has been added to available games',
        "confirm_delete": 'Delete "{name}"?',
        "btn_import": "Bulk Import (from CSV/TXT)",
        "import_title": "Select import file",
        "import_success": "Successfully imported {count} game(s)",
        "import_skip": " (skipped {skip} existing game(s))",
        "import_empty": "No valid data found in the file",
        "import_format_err": "Line {line}: format error, need 3 columns (game,system,launch)",
        "dlg_tip": "Info",
        "dlg_success": "Success",
        "dlg_confirm": "Confirm",
    },
    "ja": {
        "title": "ESPORTS CAFE PHOENIX - ゲーム検索システム",
        "query_frame": "ゲーム状態検索",
        "game_name": "ゲーム名：",
        "btn_query": "検索",
        "submit_frame": "追加リクエスト",
        "btn_submit": "リクエスト送信",
        "btn_view_all": "追加済みゲーム一覧",
        "btn_manage": "追加待ちゲームの管理",
        "col_game": "ゲーム名",
        "col_system": "起動システム",
        "col_launch": "起動方法",
        "col_action": "操作",
        "btn_added": "追加済み",
        "btn_delete": "削除",
        "downloaded": "【ダウンロード済み】",
        "not_downloaded": "未ダウンロード",
        "system_prefix": "起動システム：",
        "launch_prefix": "起動方法：",
        "no_pending": "追加待ちゲームはありません",
        "no_available": "追加済みゲームはありません",
        "win_manage": "追加待ちゲーム管理",
        "win_available": "追加済みゲーム一覧",
        "warn_empty": "ゲーム名を入力してください",
        "warn_fill": "起動システムと起動方法を入力してください",
        "info_exists": "このゲームは既にインストール済みです",
        "info_pending": "このゲームは既に追加待ちリストにあります",
        "info_submitted": "「{name}」を追加待ちリストに登録しました",
        "info_added": "「{name}」を追加済みリストに登録しました",
        "confirm_delete": "「{name}」を削除しますか？",
        "btn_import": "一括インポート（CSV/TXTファイル）",
        "import_title": "インポートファイルを選択",
        "import_success": "{count} 本のゲームをインポートしました",
        "import_skip": "（{skip} 本の既存ゲームをスキップ）",
        "import_empty": "ファイルに有効なデータがありません",
        "import_format_err": "{line}行目：フォーマットエラー、3列必要（ゲーム名,システム,起動方法）",
        "dlg_tip": "情報",
        "dlg_success": "完了",
        "dlg_confirm": "確認",
    },
}


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
        self.root.resizable(False, False)
        self.lang = "zh"
        self.data = load_data()
        self._build_ui()
        self._center_window()

    def t(self, key, **kwargs):
        text = I18N[self.lang][key]
        return text.format(**kwargs) if kwargs else text

    def _set_lang(self, lang):
        self.lang = lang
        for child in self.root.winfo_children():
            child.destroy()
        self._build_ui()
        self._center_window()

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
        bar = tk.Frame(self.root)
        bar.pack(padx=12, pady=(8, 0), anchor="e")
        for code, label in [("zh", "中文"), ("en", "EN"), ("ja", "日本語")]:
            tk.Button(
                bar, text=label, width=6,
                relief="sunken" if code == self.lang else "raised",
                command=lambda c=code: self._set_lang(c),
            ).pack(side="left", padx=2)

    # ── 查询模块 ──────────────────────────────────────────────

    def _build_query_section(self):
        frame = tk.LabelFrame(self.root, text=self.t("query_frame"), padx=12, pady=8)
        frame.pack(padx=12, pady=(4, 4), fill="x")

        row = tk.Frame(frame)
        row.pack(fill="x")

        tk.Label(row, text=self.t("game_name")).pack(side="left")
        self.query_entry = tk.Entry(row, width=30)
        self.query_entry.pack(side="left", padx=(0, 8))
        self.query_entry.bind("<Return>", lambda e: self._do_query())
        tk.Button(row, text=self.t("btn_query"), command=self._do_query).pack(side="left")

        self.query_result = tk.Text(
            frame, height=2, width=48, state="disabled",
            wrap="word", bd=0, bg=frame.cget("bg"),
        )
        self.query_result.pack(fill="x", pady=(6, 0))
        self.query_result.tag_config("hit", foreground="green")
        self.query_result.tag_config("miss", foreground="red")

    def _do_query(self):
        keyword = self.query_entry.get().strip()
        if not keyword:
            messagebox.showwarning(self.t("dlg_tip"), self.t("warn_empty"))
            return

        self.data = load_data()
        keyword_lower = keyword.lower()
        matches = {
            name: info
            for name, info in self.data["available"].items()
            if keyword_lower in name.lower()
        }

        self.query_result.config(state="normal")
        self.query_result.delete("1.0", "end")

        if matches:
            lines = []
            for name, info in matches.items():
                lines.append(
                    f"{self.t('downloaded')} {name}\n"
                    f"  {self.t('system_prefix')}{info['system']}"
                    f"　{self.t('launch_prefix')}{info['launch']}"
                )
            self.query_result.insert("1.0", "\n".join(lines), "hit")
            self.query_result.config(height=min(len(matches) * 2 + 1, 12))
        else:
            self.query_result.insert("1.0", self.t("not_downloaded"), "miss")
            self.query_result.config(height=2)

        self.query_result.config(state="disabled")

    # ── 提交需求模块 ──────────────────────────────────────────

    def _build_submit_section(self):
        frame = tk.LabelFrame(self.root, text=self.t("submit_frame"), padx=12, pady=8)
        frame.pack(padx=12, pady=4, fill="x")

        row = tk.Frame(frame)
        row.pack(fill="x")

        tk.Label(row, text=self.t("game_name")).pack(side="left")
        self.submit_entry = tk.Entry(row, width=30)
        self.submit_entry.pack(side="left", padx=(0, 8))
        self.submit_entry.bind("<Return>", lambda e: self._do_submit())
        tk.Button(row, text=self.t("btn_submit"), command=self._do_submit).pack(side="left")

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
        self.submit_entry.delete(0, tk.END)
        messagebox.showinfo(self.t("dlg_success"), self.t("info_submitted", name=name))

    # ── 管理入口 ──────────────────────────────────────────────

    def _build_manage_section(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=12, pady=(4, 12), fill="x")
        tk.Button(
            frame, text=self.t("btn_view_all"),
            command=self._open_available_window,
        ).pack(fill="x", pady=(0, 4))
        tk.Button(
            frame, text=self.t("btn_manage"),
            command=self._open_manage_window,
        ).pack(fill="x", pady=(0, 4))
        tk.Button(
            frame, text=self.t("btn_import"),
            command=self._do_bulk_import,
        ).pack(fill="x")

    def _do_bulk_import(self):
        filepath = filedialog.askopenfilename(
            title=self.t("import_title"),
            filetypes=[("CSV / TXT", "*.csv *.txt"), ("All files", "*.*")],
        )
        if not filepath:
            return

        with open(filepath, "r", encoding="utf-8-sig") as f:
            content = f.read()

        reader = csv.reader(io.StringIO(content))
        self.data = load_data()
        added = 0
        skipped = 0
        for line_num, row in enumerate(reader, start=1):
            if not row or all(c.strip() == "" for c in row):
                continue
            if len(row) < 3:
                messagebox.showwarning(self.t("dlg_tip"), self.t("import_format_err", line=line_num))
                return
            name, system, launch = row[0].strip(), row[1].strip(), row[2].strip()
            if not name:
                continue
            if name in self.data["available"]:
                skipped += 1
                continue
            self.data["available"][name] = {"system": system, "launch": launch}
            if name in self.data["pending"]:
                self.data["pending"].remove(name)
            added += 1

        if added == 0 and skipped == 0:
            messagebox.showinfo(self.t("dlg_tip"), self.t("import_empty"))
            return

        save_data(self.data)
        msg = self.t("import_success", count=added)
        if skipped:
            msg += self.t("import_skip", skip=skipped)
        messagebox.showinfo(self.t("dlg_success"), msg)

    def _open_available_window(self):
        self.data = load_data()
        win = tk.Toplevel(self.root)
        win.title(self.t("win_available"))
        win.resizable(False, False)

        if not self.data["available"]:
            tk.Label(win, text=self.t("no_available"), padx=40, pady=20).pack()
        else:
            header = tk.Frame(win, padx=8, pady=4)
            header.pack(fill="x")
            tk.Label(header, text=self.t("col_game"), width=20, anchor="w", font=("", 0, "bold")).grid(row=0, column=0, padx=4)
            tk.Label(header, text=self.t("col_system"), width=12, font=("", 0, "bold")).grid(row=0, column=1, padx=4)
            tk.Label(header, text=self.t("col_launch"), width=12, font=("", 0, "bold")).grid(row=0, column=2, padx=4)

            container = tk.Frame(win, padx=8, pady=4)
            container.pack(fill="both", expand=True)
            for idx, (name, info) in enumerate(self.data["available"].items()):
                tk.Label(container, text=name, width=20, anchor="w").grid(row=idx, column=0, padx=4, pady=2)
                tk.Label(container, text=info["system"], width=12).grid(row=idx, column=1, padx=4, pady=2)
                tk.Label(container, text=info["launch"], width=12).grid(row=idx, column=2, padx=4, pady=2)

        win.update_idletasks()
        x = (win.winfo_screenwidth() - win.winfo_width()) // 2
        y = (win.winfo_screenheight() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    def _open_manage_window(self):
        self.data = load_data()
        win = tk.Toplevel(self.root)
        win.title(self.t("win_manage"))
        win.resizable(False, False)
        self._populate_manage_window(win)

        win.update_idletasks()
        x = (win.winfo_screenwidth() - win.winfo_width()) // 2
        y = (win.winfo_screenheight() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    def _populate_manage_window(self, win):
        for child in win.winfo_children():
            child.destroy()

        if not self.data["pending"]:
            tk.Label(win, text=self.t("no_pending"), padx=40, pady=20).pack()
            return

        header = tk.Frame(win, padx=8, pady=4)
        header.pack(fill="x")
        tk.Label(header, text=self.t("col_game"), width=18, anchor="w", font=("", 0, "bold")).grid(row=0, column=0, padx=4)
        tk.Label(header, text=self.t("col_system"), width=12, font=("", 0, "bold")).grid(row=0, column=1, padx=4)
        tk.Label(header, text=self.t("col_launch"), width=12, font=("", 0, "bold")).grid(row=0, column=2, padx=4)
        tk.Label(header, text=self.t("col_action"), width=16, font=("", 0, "bold")).grid(row=0, column=3, padx=4)

        container = tk.Frame(win, padx=8, pady=4)
        container.pack(fill="both", expand=True)

        for idx, game_name in enumerate(self.data["pending"]):
            tk.Label(container, text=game_name, width=18, anchor="w").grid(row=idx, column=0, padx=4, pady=2)

            system_entry = tk.Entry(container, width=14)
            system_entry.grid(row=idx, column=1, padx=4, pady=2)

            launch_entry = tk.Entry(container, width=14)
            launch_entry.grid(row=idx, column=2, padx=4, pady=2)

            btn_frame = tk.Frame(container)
            btn_frame.grid(row=idx, column=3, padx=4, pady=2)

            tk.Button(
                btn_frame, text=self.t("btn_added"),
                command=lambda n=game_name, se=system_entry, le=launch_entry: self._confirm_add(n, se, le, win),
            ).pack(side="left", padx=(0, 4))

            tk.Button(
                btn_frame, text=self.t("btn_delete"), fg="red",
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

    def _confirm_add(self, game_name, system_entry, launch_entry, win):
        system_val = system_entry.get().strip()
        launch_val = launch_entry.get().strip()

        if not system_val or not launch_val:
            messagebox.showwarning(self.t("dlg_tip"), self.t("warn_fill"), parent=win)
            return

        self.data = load_data()
        if game_name in self.data["pending"]:
            self.data["pending"].remove(game_name)
        self.data["available"][game_name] = {
            "system": system_val,
            "launch": launch_val,
        }
        save_data(self.data)
        messagebox.showinfo(self.t("dlg_success"), self.t("info_added", name=game_name), parent=win)
        self._populate_manage_window(win)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameQueryApp(root)
    root.mainloop()

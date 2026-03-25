# ESPORTS CAFE PHOENIX 游戏查询系统

网吧门店游戏资源查询与需求收集的轻量级桌面应用。

---

## 下载使用

**无需安装任何环境，下载即用：**

[>>> 点击下载 GameQuery.exe <<<](https://github.com/reikentoutou/gamelist/releases/latest/download/GameQuery.exe)
[>>> 点击下载 GameQuery.zip <<<](https://github.com/reikentoutou/gamelist/releases/latest/download/GameQuery.zip)

下载后双击运行即可，首次运行会自动在同目录下生成 `game_data.json` 数据文件。

---

## 功能

- **游戏状态查询** — 支持模糊搜索，输入关键词即可匹配所有包含该关键词的已下载游戏
- **多语言游戏名存储** — 每款游戏存储中文名、英文名、日文名，查询时自动匹配三语
- **提交待添加游戏** — 顾客/店员提交想玩的游戏，自动查重
- **查看所有已添加游戏** — 高性能 Treeview 表格，支持上千条数据秒开
- **待添加游戏管理** — 卡片式布局，补充三语名称和启停信息后一键入库
- **批量导入** — 从 CSV/TXT 文件一次性导入大量已有游戏，自动跳过重复项
- **多语言界面** — 中文 / English / 日本語 一键切换
- **Windows 11 适配** — 高 DPI 感知、微软雅黑 UI 字体、Fluent Design 主题色

## 技术栈

- **Python 3** + **CustomTkinter**（现代暗色主题 GUI）
- 本地 JSON 数据存储，无需数据库
- Windows 11 高 DPI 适配（`SetProcessDpiAwareness`）

## 项目结构

```
gamelist/
├── main.py              # 入口：DPI 适配 + 主题设置
├── config.py            # 全局常量：路径、主题色、字体
├── i18n.py              # 翻译字典（中/英/日）
├── data/                # 数据层（纯 Python，无 UI 依赖）
│   ├── storage.py       # load / save / migrate
│   ├── game.py          # search / display_name / match / build_record
│   └── importer.py      # read_file / parse_rows / import_games
├── ui/                  # UI 层（所有 CustomTkinter 代码）
│   ├── app.py           # 主类：初始化、语言切换
│   ├── views.py         # 主页面（查询 / 提交 / 管理按钮）
│   ├── windows.py       # 弹出窗口（游戏列表 / 待添加管理）
│   └── theme.py         # 样式工具（Treeview 主题 / 居中 / 输入框）
├── requirements.txt
└── README.md
```

改 UI 只动 `ui/`，改算法只动 `data/`，改翻译只动 `i18n.py`，改主题只动 `config.py`。

## 批量导入格式

准备一个 `.csv` 或 `.txt` 文件，支持两种格式：

**3 列（名称 + 系统 + 启动方式）：**
```
游戏名,启动系统,启动方式
```

**5 列（三语名称 + 系统 + 启动方式）：**
```
中文名,英文名,日文名,启动系统,启动方式
```

支持逗号或 Tab 分隔，自动检测编码（UTF-8 / GBK）。

## 开发者信息

如需从源码运行或二次开发：

```bash
# 创建虚拟环境并安装依赖
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 运行
python main.py

# 打包为 .exe（Windows 环境下执行）
pip install pyinstaller
pyinstaller --onefile --windowed --name "GameQuery" main.py
```

## 数据存储

数据保存在程序同目录下的 `game_data.json`，首次运行自动创建。

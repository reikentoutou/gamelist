# ESPORTS CAFE PHOENIX 游戏查询系统

网吧门店游戏资源查询与需求收集的轻量级桌面应用。

---

## 下载使用

**无需安装任何环境，下载即用：**

[>>> 点击下载 GameQuery.exe <<<](https://github.com/reikentoutou/gamelist/raw/main/dist/GameQuery.exe)

下载后双击运行即可，首次运行会自动在同目录下生成 `game_data.json` 数据文件。

---

## 功能

- **游戏状态查询** — 支持模糊搜索，输入关键词即可匹配所有包含该关键词的已下载游戏
- **多语言游戏名存储** — 每款游戏存储中文名、英文名、日文名，查询时自动匹配三语
- **提交待添加游戏** — 顾客/店员提交想玩的游戏，自动查重
- **查看所有已添加游戏** — 一键查看网吧全部已下载游戏列表（高性能表格，支持上千条数据）
- **待添加游戏管理** — 补充英文名、日文名、启动系统和启动方式后一键入库，支持删除误提交的条目
- **批量导入** — 从 CSV/TXT 文件一次性导入大量已有游戏，自动跳过重复项
- **多语言界面** — 中文 / English / 日本語 一键切换

## 技术栈

- **Python 3** + **CustomTkinter**（现代暗色主题 GUI）
- 本地 JSON 数据存储，无需数据库
- 模块化架构：`data.py`（数据层）/ `i18n.py`（国际化）/ `app.py`（UI）/ `main.py`（入口）

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

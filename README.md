# ESPORTS CAFE PHOENIX — 游戏查询系统

> 网吧门店游戏资源查询与需求收集的轻量级桌面应用。

---

## 下载使用

**无需安装任何环境，下载即用：**

[>>> 点击下载 GameQuery.exe <<<](https://github.com/reikentoutou/gamelist/releases/latest/download/GameQuery.exe)

下载后双击运行即可，首次运行会自动在同目录下生成 `game_data.json` 数据文件。

---

## 功能

| 功能 | 说明 |
|------|------|
| **游戏状态查询** | 支持模糊搜索，输入关键词即可匹配所有包含该关键词的已下载游戏 |
| **多语言游戏名** | 每款游戏存储中文名、英文名、日文名，查询时自动匹配三语 |
| **提交待添加游戏** | 顾客 / 店员提交想玩的游戏，自动查重 |
| **查看所有游戏** | 一键查看全部已下载游戏列表（高性能表格，支持上千条数据） |
| **待添加管理** | 补充英文名、日文名、启动系统和启动方式后一键入库；支持删除误提交条目 |
| **批量导入** | 从 CSV / TXT 文件一次性导入大量游戏，自动跳过重复项 |
| **多语言界面** | 中文 / English / 日本語 一键切换 |

---

## 项目结构

```
gamelist/
├── main.py            # 程序入口
├── app.py             # UI 层（CustomTkinter）
├── data.py            # 数据层（JSON 读写、导入、搜索）
├── i18n.py            # 国际化（中 / 英 / 日）
├── list.txt           # 游戏列表文本（参考）
├── requirements.txt   # Python 依赖
└── game_data.json     # 运行时自动生成的数据文件
```

## 技术栈

- **Python 3.12+** + **CustomTkinter 5.x**（现代暗色主题 GUI）
- 本地 JSON 数据存储，无需数据库
- 模块化架构：数据层 / 国际化 / UI / 入口分离

---

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

---

## 开发者指南

### 环境准备

```bash
# 克隆仓库
git clone https://github.com/reikentoutou/gamelist.git
cd gamelist

# 创建虚拟环境并安装依赖
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 运行
python main.py
```

### 打包为可执行文件

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "GameQuery" --add-data "<customtkinter_path>;customtkinter/" main.py
```

> `<customtkinter_path>` 可通过 `python -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))"` 获取。

生成的 `GameQuery.exe` 位于 `dist/` 目录。

---

## 数据存储

数据保存在程序同目录下的 `game_data.json`，首次运行自动创建。结构如下：

```json
{
  "available": {
    "游戏名": {
      "name_zh": "中文名",
      "name_en": "English Name",
      "name_ja": "日本語名",
      "system": "启动系统",
      "launch": "启动方式"
    }
  },
  "pending": ["待添加游戏名"]
}
```

---

## License

MIT

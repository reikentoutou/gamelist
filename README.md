# ESPORTS CAFE PHOENIX 游戏查询系统

网吧门店游戏资源查询与需求收集的轻量级桌面应用。采用 CustomTkinter 现代暗色主题 UI。

---

## 下载使用

**无需安装任何环境，下载即用：**

[>>> 点击下载 GameQuery.exe <<<](https://github.com/reikentoutou/gamelist/raw/main/dist/GameQuery.exe)

下载后双击运行即可，首次运行会自动在同目录下生成 `game_data.json` 数据文件。

---

## 功能

- **游戏状态查询** — 支持模糊搜索，输入关键词即可匹配中文/英文/日文名称
- **提交待添加游戏** — 顾客/店员提交想玩的游戏，自动查重
- **查看所有已添加游戏** — 高性能表格展示，百款游戏秒开
- **待添加游戏管理** — 补充启动系统、启动方式及多语言名称后一键入库，支持删除
- **批量导入** — 从 CSV/TXT 文件一次性导入大量已有游戏，自动跳过重复项
- **多语言支持** — 界面支持中文 / English / 日本語 一键切换
- **多语言游戏名** — 每款游戏存储中文、英文、日文三语名称

## 批量导入格式

准备一个 `.csv` 或 `.txt` 文件，支持两种格式：

**3 列（游戏名 + 系统 + 启动方式）：**

```
Cyberpunk 2077,中文系统,Steam
PUBG,日文系统,Steam
```

**5 列（中文名 + 英文名 + 日文名 + 系统 + 启动方式）：**

```
赛博朋克2077,Cyberpunk 2077,サイバーパンク2077,中文系统,Steam
绝地求生,PUBG,PUBG,中文系统,Steam
```

支持逗号或 Tab 分隔，支持 UTF-8 / GBK 编码。

## 项目结构

```
main.py          # 程序入口
app.py           # UI 界面（CustomTkinter）
data.py          # 数据加载/保存/查询/导入逻辑
i18n.py          # 多语言翻译字典
game_data.json   # 数据文件（运行时自动生成）
```

## 开发者信息

如需从源码运行或二次开发：

```bash
# 创建虚拟环境并安装依赖
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 运行
python main.py

# 打包为 .exe（Windows）
pyinstaller --onefile --windowed --name "GameQuery" --hidden-import customtkinter main.py
```

## 数据存储

数据保存在程序同目录下的 `game_data.json`，首次运行自动创建。
旧版数据会在启动时自动迁移至新格式（添加多语言名称字段）。

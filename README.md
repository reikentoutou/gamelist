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
- **提交待添加游戏** — 顾客/店员提交想玩的游戏，自动查重
- **查看所有已添加游戏** — 一键查看网吧全部已下载游戏列表
- **待添加游戏管理** — 补充启动系统和启动方式后一键入库，支持删除误提交的条目
- **批量导入** — 从 CSV/TXT 文件一次性导入大量已有游戏，自动跳过重复项
- **多语言支持** — 界面支持中文 / English / 日本語 一键切换

## 批量导入格式

准备一个 `.csv` 或 `.txt` 文件，每行三列，用逗号分隔：

```
游戏名,启动系统,启动方式
Cyberpunk 2077,中文,Steam
PUBG,日文,Steam
Valorant,英文,Riot Client
```

在程序中点击「批量导入」按钮选择文件即可。

## 开发者信息

如需从源码运行或二次开发：

```bash
# 运行
python main.py

# 打包为 .exe
pip install pyinstaller
pyinstaller --onefile --windowed --name "GameQuery" main.py
```

需要 Python 3，Tkinter 为 Python 内置，无额外依赖。

## 数据存储

数据保存在程序同目录下的 `game_data.json`，首次运行自动创建。

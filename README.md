# ESPORTS CAFE PHOENIX 游戏查询系统

网吧门店游戏资源查询与需求收集的轻量级桌面应用。

## 功能

- **游戏状态查询** — 输入游戏名，查看是否已下载及启动信息
- **提交待添加游戏** — 顾客/店员提交想玩的游戏，自动查重
- **待添加游戏管理** — 补充启动系统和启动方式后一键入库

## 运行

```bash
python main.py
```

需要 Python 3，无额外依赖（Tkinter 为 Python 内置）。

## 打包为 .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

生成的可执行文件位于 `dist/` 目录。

## 数据存储

数据保存在程序同目录下的 `game_data.json`，首次运行自动创建。

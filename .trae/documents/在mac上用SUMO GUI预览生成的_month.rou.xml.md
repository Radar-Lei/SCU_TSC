## 你现在看到的现象/问题
- `_month.rou.xml` 里的 `depart` 是“从仿真开始算的绝对秒数”，30 天会到 ~2,592,000s。
- 直接用 SUMO GUI 打开整个月的 `.rou.xml`，往往会非常慢（解析巨大 XML），就算你只想看某一个小时也得先把全文件读进来。

## 目标
- 在你的 mac 上能“肉眼查看”某一天/某个小时的车流效果：高峰更密、平峰更稀、周末曲线不同。
- 启动方式参考 `mcp_sumo_fastapi_llm`：核心就是 `sumo-gui -c xxx.sumocfg --start`（它那边是通过 TraCI 调起）。

## 方案概览
### A. 最快可用（不改代码，手动预览）
1. 确保本机装了 SUMO GUI，并且能执行 `sumo-gui`（或设置 `SUMO_HOME`）。
2. 在 `sumo_simulation/environments/arterial4x4_1/` 新建一个临时 `*.sumocfg`：
   - `net-file=arterial4x4.net.xml`
   - `route-files=arterial4x4_1.rou_month.rou.xml`
   - `begin=<你要看的起始秒>`，`end=begin+3600`
3. 用命令启动：`sumo-gui -c 这个新sumocfg --start`

限制：即便设置 begin/end，SUMO 仍可能需要解析完整月度 `.rou.xml`，文件很大时依旧慢。

### B. 推荐（实现“切片”工具，让GUI秒开）
新增一个“预览切片”脚本：从月度 `.rou.xml` 中抽取某个时间窗口（例如某一天 7:00–9:00），生成一个很小的 `.rou.xml` 供 GUI 快速打开。
- 输入：月度 `.rou.xml`、窗口起止（秒）或日期+小时
- 输出：`*_slice.rou.xml`（只包含窗口内车辆），并把 `depart` 平移到从 0 开始
- 再自动生成一个对应的 `*_slice.sumocfg`（`begin=0 end=窗口长度`）

### C. 提供一个一键启动器（可选）
新增一个 `preview_sumo_gui.py`：
- 参数：`--net` `--rou` `--begin` `--duration`（内部自动做切片+写 sumocfg）
- 最后用 `subprocess` 或仿照 mcp 的 TraCI 启动 `sumo-gui`。

## 将要新增的文件（如果你确认）
- `sumo_simulation/tools/rou_slice_for_gui.py`：大文件流式解析（iterparse），过滤车辆，输出切片 `.rou.xml`。
- `sumo_simulation/tools/preview_sumo_gui.py`：生成切片 + 生成 `.sumocfg` + 启动 `sumo-gui`。

## 验证方式
- 本机对 `arterial4x4_1.rou_month.rou.xml` 切 2 个窗口：工作日早高峰 vs 夜间低谷；输出车辆数差异明显。
- 用 GUI 打开切片文件，确认视觉上车流密度差异明显。

如果你确认这个方案，我就按 B（切片工具）+ 可选 C（一键启动）落地实现，确保在 mac 上可以直接 `python3 ...` 弹出 GUI。
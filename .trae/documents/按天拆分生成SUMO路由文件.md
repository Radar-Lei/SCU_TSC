## 现状定位
- 目前月度文件由 [rou_month_generator.py](file:///Users/leida/Cline/SCU_TSC/sumo_simulation/tools/rou_month_generator.py) 的 [generate_month](file:///Users/leida/Cline/SCU_TSC/sumo_simulation/tools/rou_month_generator.py#L196-L326) 一次性写出单个 `*_month.rou.xml`：`depart` 为从仿真开始算的绝对秒（跨 30 天会到 ~2,592,000s），导致文件巨大、SUMO GUI 解析慢。

## 目标
- 程序一次运行仍按“一个月”的统计规律生成，但输出改为“每天一个 `.rou.xml`”，每个文件仅覆盖当天 24 小时（`depart` 0–86400），显著减小单文件体积、提升加载速度。
- 保持向后兼容：不加新参数时仍生成单个 `_month.rou.xml`。

## 方案设计
### 1) 抽取共享的“事件生成”逻辑
- 将 `generate_month` 内部的模板解析、`template_events` 构造、`daily_factors` 生成等，整理为可复用的准备步骤（仍在同一文件内，避免引入新依赖）。
- 小时内事件仍按当前逻辑（`profile * day_factor` 决定倍数，支持小数倍随机采样 + `jitter_seconds` 抖动）。

### 2) 新增“按天输出”函数
- 新增 `generate_daily_files(...)`：循环 `days`，每次写一个当日文件：
  - 文件包含同样的 `<routes ...>` 根属性与静态子节点（`<vType>`、`<route>` 等）。
  - 车辆 `depart` 写入“当天秒数”（0–`hour_seconds*24`），不再叠加 `day_index*24*hour_seconds`。
  - 车辆 `id` 保持唯一性（建议：`gen_{date}_{hour}_{seq}`，`seq` 可按天重置或全月累增；我会选“按天重置”便于阅读）。

### 3) 扩展 CLI 参数（保持兼容）
- 在 [build_arg_parser](file:///Users/leida/Cline/SCU_TSC/sumo_simulation/tools/rou_month_generator.py#L328-L344) 增加：
  - `--split-by-day`：开启按天拆分输出。
  - `--output-dir`：按天输出目录（默认：输入文件同目录下 `<stem>_daily/`）。
- 行为：
  - 未传 `--split-by-day`：沿用当前 `--output`（默认 `_month.rou.xml`）。
  - 传了 `--split-by-day`：在 `output-dir` 下生成 `stem_YYYY-MM-DD.rou.xml` 共 `days` 个文件。

### 4) 校验与统计输出
- 复用 [validate_rou](file:///Users/leida/Cline/SCU_TSC/sumo_simulation/tools/rou_month_generator.py#L135-L194)：
  - 单月模式：维持 `expect_hours=days*24`。
  - 拆分模式：对每个日文件使用 `expect_hours=24`（若用户开启 `--validate`）。
- 输出摘要：打印每天车辆总数与首日/末日的小时计数片段，便于确认“高峰更密、周末不同”。

## 文件改动范围
- 只修改一个文件：`sumo_simulation/tools/rou_month_generator.py`（新增函数 + CLI 参数 + 入口逻辑分支；不新增额外脚本）。

## 验证方式（我会在实现后执行）
- 用 `arterial4x4_1.rou.xml` 作为模板，生成 2–3 天的 daily 文件：
  - 确认输出文件数量、命名、大小明显下降。
  - 开启 `--validate`，确保 `depart` 单调、hour index 不越界。
  - 抽查对比工作日 vs 周末的每天总量与某些小时计数差异。

## 使用示例（实现后）
- 生成 30 天、按天拆分：
  - ```python3 sumo_simulation/tools/rou_month_generator.py \
  --input sumo_simulation/environments/arterial4x4_1/arterial4x4_1.rou.xml \
  --start-date 2026-01-01 --days 30 \
  --split-by-day \
  --output-dir sumo_simulation/environments/arterial4x4_1/arterial4x4_1_daily \
  --validate```
- 仍生成单个大文件（原行为）：
  - `python3 sumo_simulation/tools/rou_month_generator.py --input .../arterial4x4_1.rou.xml --days 30`

确认后我会开始落地实现与本地验证。
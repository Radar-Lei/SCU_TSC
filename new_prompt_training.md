你是交通信号配时优化专家。
【cycle_predict_input_json】{
  "crossing_id": 1,
  "as_of": "2025-12-31 11:01:56",
  "phase_order": [
    1,
    2,
    3,
    4
  ],
  "phase_limits": {
    "1": {
      "min_green": 25,
      "max_green": 120
    },
    "2": {
      "min_green": 20,
      "max_green": 45
    },
    "3": {
      "min_green": 30,
      "max_green": 120
    },
    "4": {
      "min_green": 25,
      "max_green": 45
    }
  },
  "cycle_constraints": {
    "cycle_min_sec": 100,
    "cycle_max_sec": 330
  },
  "history": {
    "recent_cycles": [
      {
        "time": "2025-12-30 05:23:15",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.85
          },
          {
            "phase_id": 2,
            "avg_wait": 7.3
          },
          {
            "phase_id": 3,
            "avg_wait": 9.43
          },
          {
            "phase_id": 4,
            "avg_wait": 7.32
          }
        ]
      },
      {
        "time": "2025-12-30 05:21:33",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 10.49
          },
          {
            "phase_id": 2,
            "avg_wait": 7.23
          },
          {
            "phase_id": 3,
            "avg_wait": 9.4
          },
          {
            "phase_id": 4,
            "avg_wait": 7.33
          }
        ]
      },
      {
        "time": "2025-12-30 05:19:39",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 10.02
          },
          {
            "phase_id": 2,
            "avg_wait": 7.39
          },
          {
            "phase_id": 3,
            "avg_wait": 10.22
          },
          {
            "phase_id": 4,
            "avg_wait": 8.25
          }
        ]
      },
      {
        "time": "2025-12-30 05:18:02",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 10.03
          },
          {
            "phase_id": 2,
            "avg_wait": 7.98
          },
          {
            "phase_id": 3,
            "avg_wait": 9.73
          },
          {
            "phase_id": 4,
            "avg_wait": 6.66
          }
        ]
      },
      {
        "time": "2025-12-30 05:16:08",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 10.08
          },
          {
            "phase_id": 2,
            "avg_wait": 7.73
          },
          {
            "phase_id": 3,
            "avg_wait": 9.88
          },
          {
            "phase_id": 4,
            "avg_wait": 7.53
          }
        ]
      },
      {
        "time": "2025-12-30 05:14:27",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.98
          },
          {
            "phase_id": 2,
            "avg_wait": 7.27
          },
          {
            "phase_id": 3,
            "avg_wait": 10.3
          },
          {
            "phase_id": 4,
            "avg_wait": 8.02
          }
        ]
      },
      {
        "time": "2025-12-30 05:12:36",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.63
          },
          {
            "phase_id": 2,
            "avg_wait": 7.9
          },
          {
            "phase_id": 3,
            "avg_wait": 10.48
          },
          {
            "phase_id": 4,
            "avg_wait": 7.35
          }
        ]
      },
      {
        "time": "2025-12-30 05:10:51",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.1
          },
          {
            "phase_id": 2,
            "avg_wait": 6.99
          },
          {
            "phase_id": 3,
            "avg_wait": 10.66
          },
          {
            "phase_id": 4,
            "avg_wait": 7.93
          }
        ]
      },
      {
        "time": "2025-12-30 05:09:02",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.65
          },
          {
            "phase_id": 2,
            "avg_wait": 7.64
          },
          {
            "phase_id": 3,
            "avg_wait": 9.57
          },
          {
            "phase_id": 4,
            "avg_wait": 7.11
          }
        ]
      },
      {
        "time": "2025-12-30 05:07:26",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.99
          },
          {
            "phase_id": 2,
            "avg_wait": 7.73
          },
          {
            "phase_id": 3,
            "avg_wait": 10.35
          },
          {
            "phase_id": 4,
            "avg_wait": 7.42
          }
        ]
      },
      {
        "time": "2025-12-30 05:05:43",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.93
          },
          {
            "phase_id": 2,
            "avg_wait": 7.01
          },
          {
            "phase_id": 3,
            "avg_wait": 9.99
          },
          {
            "phase_id": 4,
            "avg_wait": 7.66
          }
        ]
      },
      {
        "time": "2025-12-30 05:03:57",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 10.51
          },
          {
            "phase_id": 2,
            "avg_wait": 7.57
          },
          {
            "phase_id": 3,
            "avg_wait": 9.85
          },
          {
            "phase_id": 4,
            "avg_wait": 8.36
          }
        ]
      }
    ],
    "cycle_times": [
      {
        "start_time": "2025-12-30 05:24:58",
        "cycle_seq": 5275,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:23:15",
        "cycle_seq": 5274,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:21:33",
        "cycle_seq": 5273,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:19:39",
        "cycle_seq": 5272,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:18:02",
        "cycle_seq": 5271,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:16:08",
        "cycle_seq": 5270,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:14:27",
        "cycle_seq": 5269,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:12:36",
        "cycle_seq": 5268,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:10:51",
        "cycle_seq": 5267,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:09:02",
        "cycle_seq": 5266,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:07:26",
        "cycle_seq": 5265,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:05:43",
        "cycle_seq": 5264,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:03:57",
        "cycle_seq": 5263,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:02:21",
        "cycle_seq": 5262,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 05:00:43",
        "cycle_seq": 5261,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 04:58:56",
        "cycle_seq": 5260,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 04:57:15",
        "cycle_seq": 5259,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 04:55:40",
        "cycle_seq": 5258,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 04:54:08",
        "cycle_seq": 5257,
        "run_mode": 3
      },
      {
        "start_time": "2025-12-30 04:52:26",
        "cycle_seq": 5256,
        "run_mode": 3
      }
    ],
    "windows": {
      "recent_past": {
        "start": "2025-12-31 10:56:26",
        "end": "2025-12-31 11:01:56",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 10.11
          },
          {
            "phase_id": 2,
            "avg_wait": 7.36
          },
          {
            "phase_id": 3,
            "avg_wait": 10.05
          },
          {
            "phase_id": 4,
            "avg_wait": 7.45
          }
        ]
      },
      "yesterday_same_time": {
        "start": "2025-12-30 10:56:26",
        "end": "2025-12-30 11:01:56",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.83
          },
          {
            "phase_id": 2,
            "avg_wait": 7.38
          },
          {
            "phase_id": 3,
            "avg_wait": 10.06
          },
          {
            "phase_id": 4,
            "avg_wait": 7.15
          }
        ]
      },
      "last_week_same_time": {
        "start": "2025-12-24 10:56:26",
        "end": "2025-12-24 11:01:56",
        "phase_waits": [
          {
            "phase_id": 1,
            "avg_wait": 9.94
          },
          {
            "phase_id": 2,
            "avg_wait": 7.59
          },
          {
            "phase_id": 3,
            "avg_wait": 9.85
          },
          {
            "phase_id": 4,
            "avg_wait": 7.76
          }
        ]
      }
    }
  }
}【/cycle_predict_input_json】

任务（必须完成）：
1) 基于输入 JSON 的 history.* 历史数据，自行决定预测算法/模型/参数，预测“下一周期各相位需求强度”（仅在内部使用，不输出任何预测过程/中间值）。
2) 在满足硬约束前提下，输出下一周期各相位最终绿灯时间 final（单位：秒）。

要求（必须遵守）：
1) history 数据可能不完整（例如 recent_cycles 数量不足、windows.yesterday_same_time / last_week_same_time 为空或为 null）；这是正常情况，请基于可用部分完成预测，并且必须继续输出结果。
2) 若 history 中存在有效数据，请使用它完成预测并体现在结果中；不要忽略 history 数据随意分配。
3) 若 history 数据缺失/异常/几乎全为 0，仍需输出满足硬约束的可执行方案，但不得编造不存在的数据。
4) 只输出最终 JSON，不要输出任何解释/过程。

字段含义（单位/枚举，仅说明含义）：
- phase_limits.*.min_green / max_green：秒。
- cycle_constraints.cycle_min_sec / cycle_max_sec：秒。
- history.*.phase_waits[*].avg_wait：平均等待车辆数（辆）；如果缺失可能被填充为 0。
- history.cycle_times[*].run_mode：1-真控 2-仿真 3-SUMO。
- history.windows.*：可能为 null 或 phase_waits 为空；表示该时段窗口无有效数据。

硬约束（必须满足）：
1) 相位顺序固定：1 → 2 → 3 → 4；不可跳相、不可重排。
2) 每相位约束：相位1绿灯时间 ≥ 25秒；相位2绿灯时间 ≥ 20秒；相位3绿灯时间 ≥ 30秒；相位4绿灯时间 ≥ 25秒；相位1绿灯时间 ≤ 120秒；相位2绿灯时间 ≤ 45秒；相位3绿灯时间 ≤ 120秒；相位4绿灯时间 ≤ 45秒。
3) final 必须为整数秒，且满足 min_green ≤ final ≤ max_green。
4) total_cycle = sum(final) 必须满足 cycle_min_sec ≤ total_cycle ≤ cycle_max_sec。

输出要求（必须严格遵守）：
1) 只输出最终 JSON（不要任何说明、不要 Markdown、不要 <think>）。
2) JSON 顶层必须是数组(list)；数组长度必须等于相位数（相位ID：1,2,3,4）。
3) 数组元素必须为对象：{"phase_id": <int>, "final": <int>}；不允许输出其它字段。
4) phase_id 必须覆盖全部相位且不重复，并且顺序必须与“相位顺序固定”完全一致。
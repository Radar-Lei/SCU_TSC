
[completion_log] step=5, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 8}
[1] (extend_decision):{'extend': '是', 'extend_sec': 8}
[2] (extend_decision):{'extend': '否', 'extend_sec': 15}
[reward_diag] steps 0..10 invalid_rate=0.456 (73/160)
[reward_diag]  - extend_decision: invalid_rate=0.830 (73/88) top=extend_decision_extend_sec_exceeds_max_soft:52, extend_decision_extend_sec_nonzero_when_no_soft:21
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a
[reward_diag] KL spike at step=10 kl=5.1961 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "是", "extend_sec": 16}', '{"extend": "否", "extend_sec": 15}', '{"extend": "是", "extend_sec": 17}'], 'sample_reasons': ['extend_decision_extend_sec_exceeds_max_soft', 'extend_decision_extend_sec_nonzero_when_no_soft', 'extend_decision_extend_sec_exceeds_max_soft'], 'sample_rewards': [-0.4, -0.3, -0.45], 'task_types': ['extend_decision'], 'invalid_count': 0}

[completion_log] step=10, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 12}
[8] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=15, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 14}
[2] (extend_decision):{'extend': '是', 'extend_sec': 18}
[0] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 10..20 invalid_rate=0.581 (93/160)
[reward_diag]  - extend_decision: invalid_rate=0.830 (93/112) top=extend_decision_extend_sec_exceeds_max_soft:58, extend_decision_extend_sec_nonzero_when_no_soft:34, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a
[reward_diag] KL spike at step=20 kl=10.1908 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"next_phase_id": 3, "green_sec": 30}', '{"next_phase_id": 3, "green_sec": 46}', '{"next_phase_id": 5, "green_sec": 25}'], 'sample_reasons': ['ok', 'ok', 'ok'], 'sample_rewards': [0.0, 0.0, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=20, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 20}
[3] (extend_decision):{'extend': '是', 'extend_sec': 12}
[1] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=25, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 11}
[11] (extend_decision):{'extend': '是', 'extend_sec': 10}
[9] (extend_decision):{'extend': '否', 'extend_sec': 14}
[reward_diag] steps 20..30 invalid_rate=0.588 (94/160)
[reward_diag]  - extend_decision: invalid_rate=0.870 (94/108) top=extend_decision_extend_sec_exceeds_max_soft:73, extend_decision_extend_sec_nonzero_when_no_soft:21
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a
[reward_diag] KL spike at step=30 kl=8.7258 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "是", "extend_sec": 19}', '{"extend": "是", "extend_sec": 23}', '{"extend": "是", "extend_sec": 18}'], 'sample_reasons': ['extend_decision_extend_sec_exceeds_max_soft', 'extend_decision_extend_sec_exceeds_max_soft', 'extend_decision_extend_sec_exceeds_max_soft'], 'sample_rewards': [-0.5, -0.5, -0.5], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=30, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 23}
[1] (extend_decision):{'extend': '是', 'extend_sec': 11}
[11] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=35, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 17}
[5] (extend_decision):{'extend': '是', 'extend_sec': 12}
[15] (extend_decision):{'extend': '否', 'extend_sec': 6}
[reward_diag] steps 30..40 invalid_rate=0.456 (73/160)
[reward_diag]  - extend_decision: invalid_rate=0.830 (73/88) top=extend_decision_extend_sec_exceeds_max_soft:53, extend_decision_extend_sec_nonzero_when_no_soft:20
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=40, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 12}
[1] (extend_decision):{'extend': '是', 'extend_sec': 10}
[2] (extend_decision):{'extend': '否', 'extend_sec': 12}

[completion_log] step=45, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 15}
[2] (extend_decision):{'extend': '是', 'extend_sec': 13}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 40..50 invalid_rate=0.444 (71/160)
[reward_diag]  - extend_decision: invalid_rate=0.807 (71/88) top=extend_decision_extend_sec_exceeds_max_soft:49, extend_decision_extend_sec_nonzero_when_no_soft:21, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a
[reward_diag] KL spike at step=50 kl=6.2696 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "否", "extend_sec": 13}', '{"extend": "是", "extend_sec": 12}', '{"extend": "否", "extend_sec": 20}'], 'sample_reasons': ['extend_decision_extend_sec_nonzero_when_no_soft', 'extend_decision_extend_sec_exceeds_max_soft', 'extend_decision_extend_sec_nonzero_when_no_soft'], 'sample_rewards': [-0.3, -0.2, -0.3], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=50, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 8}
[2] (extend_decision):{'extend': '是', 'extend_sec': 17}
[0] (extend_decision):{'extend': '否', 'extend_sec': 16}

[completion_log] step=55, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 26}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 32}
  [2] (signal_step): {"next_phase_id": 5, "green_sec": 11}
[reward_diag] steps 50..60 invalid_rate=0.463 (74/160)
[reward_diag]  - extend_decision: invalid_rate=0.804 (74/92) top=extend_decision_extend_sec_exceeds_max_soft:55, extend_decision_extend_sec_nonzero_when_no_soft:19
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a
[reward_diag] KL spike at step=60 kl=8.8767 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "是", "extend_sec": 4}', '{"extend": "是", "extend_sec": 6}', '{"extend": "否", "extend_sec": 0}'], 'sample_reasons': ['ok', 'ok', 'ok'], 'sample_rewards': [0.0, 0.0, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=60, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 16}
[6] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 6}

[completion_log] step=65, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 12}
[9] (extend_decision):{'extend': '是', 'extend_sec': 8}
[reward_diag] steps 60..70 invalid_rate=0.431 (69/160)
[reward_diag]  - extend_decision: invalid_rate=0.863 (69/80) top=extend_decision_extend_sec_exceeds_max_soft:36, extend_decision_extend_sec_nonzero_when_no_soft:32, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a
[reward_diag] KL spike at step=70 kl=7.8477 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "是", "extend_sec": 18}', '{"extend": "否", "extend_sec": 13}', '{"extend": "是", "extend_sec": 6}'], 'sample_reasons': ['extend_decision_extend_sec_exceeds_max_soft', 'extend_decision_extend_sec_nonzero_when_no_soft', 'ok'], 'sample_rewards': [-0.5, -0.3, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=70, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 18}
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 16}

[completion_log] step=75, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 17}
[5] (extend_decision):{'extend': '是', 'extend_sec': 20}
[6] (extend_decision):{'extend': '否', 'extend_sec': 16}
[reward_diag] steps 70..80 invalid_rate=0.537 (86/160)
[reward_diag]  - extend_decision: invalid_rate=0.796 (86/108) top=extend_decision_extend_sec_exceeds_max_soft:43, extend_decision_extend_sec_nonzero_when_no_soft:40, extend_decision_extend_when_at_max_green:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=80, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 5}
[1] (extend_decision):{'extend': '是', 'extend_sec': 13}
[3] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=85, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 13}
[2] (extend_decision):{'extend': '是', 'extend_sec': 19}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 80..90 invalid_rate=0.519 (83/160)
[reward_diag]  - extend_decision: invalid_rate=0.798 (83/104) top=extend_decision_extend_sec_exceeds_max_soft:45, extend_decision_extend_sec_nonzero_when_no_soft:35, extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=90, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 17}
[3] (extend_decision):{'extend': '是', 'extend_sec': 22}
[0] (extend_decision):{'extend': '否', 'extend_sec': 12}

[completion_log] step=95, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 5}
[5] (extend_decision):{'extend': '是', 'extend_sec': 8}
[1] (extend_decision):{'extend': '否', 'extend_sec': 20}
[reward_diag] steps 90..100 invalid_rate=0.456 (73/160)
[reward_diag]  - extend_decision: invalid_rate=0.830 (73/88) top=extend_decision_extend_sec_nonzero_when_no_soft:38, extend_decision_extend_sec_exceeds_max_soft:35
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=100, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 17}
[1] (extend_decision):{'extend': '是', 'extend_sec': 16}
[2] (extend_decision):{'extend': '否', 'extend_sec': 13}

[completion_log] step=105, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 14}
[0] (extend_decision):{'extend': '否', 'extend_sec': 5}
[reward_diag] steps 100..110 invalid_rate=0.613 (98/160)
[reward_diag]  - extend_decision: invalid_rate=0.907 (98/108) top=extend_decision_extend_sec_nonzero_when_no_soft:49, extend_decision_extend_sec_exceeds_max_soft:48, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=110, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 17}
[10] (extend_decision):{'extend': '是', 'extend_sec': 12}
[9] (extend_decision):{'extend': '否', 'extend_sec': 6}

[completion_log] step=115, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '是', 'extend_sec': 20}
[2] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 110..120 invalid_rate=0.456 (73/160)
[reward_diag]  - extend_decision: invalid_rate=0.830 (73/88) top=extend_decision_extend_sec_nonzero_when_no_soft:39, extend_decision_extend_sec_exceeds_max_soft:34
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=120, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 9}
[5] (extend_decision):{'extend': '是', 'extend_sec': 16}
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=125, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 12}
[reward_diag] steps 120..130 invalid_rate=0.487 (78/160)
[reward_diag]  - extend_decision: invalid_rate=0.886 (78/88) top=extend_decision_extend_sec_nonzero_when_no_soft:59, extend_decision_extend_sec_exceeds_max_soft:19
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=130, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 17}
[4] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 9}

[completion_log] step=135, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 19}
[12] (extend_decision):{'extend': '否', 'extend_sec': 5}
[reward_diag] steps 130..140 invalid_rate=0.525 (84/160)
[reward_diag]  - extend_decision: invalid_rate=0.840 (84/100) top=extend_decision_extend_sec_nonzero_when_no_soft:52, extend_decision_extend_sec_exceeds_max_soft:28, extend_decision_extend_when_at_max_green:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=140, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 13}
[14] (extend_decision):{'extend': '是', 'extend_sec': 6}
[8] (extend_decision):{'extend': '否', 'extend_sec': 6}

[completion_log] step=145, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 14}
[15] (extend_decision):{'extend': '是', 'extend_sec': 20}
[4] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 140..150 invalid_rate=0.444 (71/160)
[reward_diag]  - extend_decision: invalid_rate=0.845 (71/84) top=extend_decision_extend_sec_nonzero_when_no_soft:52, extend_decision_extend_sec_exceeds_max_soft:19
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=150, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 14}

[completion_log] step=155, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 19}
[6] (extend_decision):{'extend': '是', 'extend_sec': 18}
[5] (extend_decision):{'extend': '否', 'extend_sec': 15}
[reward_diag] steps 150..160 invalid_rate=0.500 (80/160)
[reward_diag]  - extend_decision: invalid_rate=0.952 (80/84) top=extend_decision_extend_sec_nonzero_when_no_soft:58, extend_decision_extend_sec_exceeds_max_soft:22
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=160, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 19}
[8] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=165, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 22}
[2] (extend_decision):{'extend': '是', 'extend_sec': 19}
[1] (extend_decision):{'extend': '否', 'extend_sec': 8}
[reward_diag] steps 160..170 invalid_rate=0.500 (80/160)
[reward_diag]  - extend_decision: invalid_rate=0.952 (80/84) top=extend_decision_extend_sec_nonzero_when_no_soft:55, extend_decision_extend_sec_exceeds_max_soft:24, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=170, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 6}
[2] (extend_decision):{'extend': '是', 'extend_sec': 16}
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=175, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 16}
[15] (extend_decision):{'extend': '是', 'extend_sec': 12}
[4] (extend_decision):{'extend': '否', 'extend_sec': 16}
[reward_diag] steps 170..180 invalid_rate=0.569 (91/160)
[reward_diag]  - extend_decision: invalid_rate=0.948 (91/96) top=extend_decision_extend_sec_nonzero_when_no_soft:70, extend_decision_extend_sec_exceeds_max_soft:21
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=180, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 20}
[13] (extend_decision):{'extend': '是', 'extend_sec': 20}
[1] (extend_decision):{'extend': '否', 'extend_sec': 12}

[completion_log] step=185, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 16}
[8] (extend_decision):{'extend': '是', 'extend_sec': 19}
[4] (extend_decision):{'extend': '否', 'extend_sec': 11}
[reward_diag] steps 180..190 invalid_rate=0.600 (96/160)
[reward_diag]  - extend_decision: invalid_rate=0.960 (96/100) top=extend_decision_extend_sec_nonzero_when_no_soft:85, extend_decision_extend_sec_exceeds_max_soft:11
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=190, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 11}
[11] (extend_decision):{'extend': '是', 'extend_sec': 12}
[8] (extend_decision):{'extend': '否', 'extend_sec': 13}

[completion_log] step=195, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 10}
[1] (extend_decision):{'extend': '否', 'extend_sec': 20}
[reward_diag] steps 190..200 invalid_rate=0.569 (91/160)
[reward_diag]  - extend_decision: invalid_rate=0.989 (91/92) top=extend_decision_extend_sec_nonzero_when_no_soft:78, extend_decision_extend_sec_exceeds_max_soft:13
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=200, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=205, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 20}
[8] (extend_decision):{'extend': '否', 'extend_sec': 6}
[reward_diag] steps 200..210 invalid_rate=0.544 (87/160)
[reward_diag]  - extend_decision: invalid_rate=0.989 (87/88) top=extend_decision_extend_sec_nonzero_when_no_soft:82, extend_decision_extend_sec_exceeds_max_soft:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=210, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 9}
[13] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=215, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 12}
[reward_diag] steps 210..220 invalid_rate=0.688 (110/160)
[reward_diag]  - extend_decision: invalid_rate=0.982 (110/112) top=extend_decision_extend_sec_nonzero_when_no_soft:109, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=220, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 10}
[9] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=225, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 15}
[reward_diag] steps 220..230 invalid_rate=0.575 (92/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (92/92) top=extend_decision_extend_sec_nonzero_when_no_soft:91, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=230, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 11}

[completion_log] step=235, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}
[reward_diag] steps 230..240 invalid_rate=0.550 (88/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (88/88) top=extend_decision_extend_sec_nonzero_when_no_soft:88
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=240, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 13}

[completion_log] step=245, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 30}
[reward_diag] steps 240..250 invalid_rate=0.575 (92/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (92/92) top=extend_decision_extend_sec_nonzero_when_no_soft:88, extend_decision_extend_when_at_max_green:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=250, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=255, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 250..260 invalid_rate=0.600 (96/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (96/96) top=extend_decision_extend_sec_nonzero_when_no_soft:94, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=260, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 11}

[completion_log] step=265, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 6}
[reward_diag] steps 260..270 invalid_rate=0.600 (96/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (96/96) top=extend_decision_extend_sec_nonzero_when_no_soft:95, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=270, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 15}
[0] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=275, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 17}
[reward_diag] steps 270..280 invalid_rate=0.700 (112/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (112/112) top=extend_decision_extend_sec_nonzero_when_no_soft:111, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=280, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 14}
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=285, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 5}
[reward_diag] steps 280..290 invalid_rate=0.675 (108/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (108/108) top=extend_decision_extend_sec_nonzero_when_no_soft:105, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=290, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 14}
[0] (extend_decision):{'extend': '否', 'extend_sec': 16}

[completion_log] step=295, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 5}
[reward_diag] steps 290..300 invalid_rate=0.875 (140/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (140/140) top=extend_decision_extend_sec_nonzero_when_no_soft:138, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/20) top=n/a

[completion_log] step=300, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 17}

[completion_log] step=305, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 16}
[reward_diag] steps 300..310 invalid_rate=0.650 (104/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (104/104) top=extend_decision_extend_sec_nonzero_when_no_soft:104
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=310, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 11}

[completion_log] step=315, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 3}
[reward_diag] steps 310..320 invalid_rate=0.650 (104/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (104/104) top=extend_decision_extend_sec_nonzero_when_no_soft:104
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=320, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 30}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 1, "green_sec": 29}

[completion_log] step=325, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 320..330 invalid_rate=0.444 (71/160)
[reward_diag]  - extend_decision: invalid_rate=0.986 (71/72) top=extend_decision_extend_sec_nonzero_when_no_soft:66, extend_decision_extend_when_at_max_green:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=330, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=335, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 8}
[reward_diag] steps 330..340 invalid_rate=0.575 (92/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (92/92) top=extend_decision_extend_sec_nonzero_when_no_soft:91, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=340, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 7}

[completion_log] step=345, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 6}
[reward_diag] steps 340..350 invalid_rate=0.644 (103/160)
[reward_diag]  - extend_decision: invalid_rate=0.990 (103/104) top=extend_decision_extend_sec_nonzero_when_no_soft:103
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=350, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 16}

[completion_log] step=355, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 14}
[reward_diag] steps 350..360 invalid_rate=0.525 (84/160)
[reward_diag]  - extend_decision: invalid_rate=1.000 (84/84) top=extend_decision_extend_sec_nonzero_when_no_soft:84
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=360, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 12}

[completion_log] step=365, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 13}
[reward_diag] steps 360..370 invalid_rate=0.550 (88/160)
[reward_diag]  - extend_decision: invalid_rate=0.957 (88/92) top=extend_decision_extend_sec_nonzero_when_no_soft:88
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=370, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=375, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 370..380 invalid_rate=0.581 (93/160)
[reward_diag]  - extend_decision: invalid_rate=0.969 (93/96) top=extend_decision_extend_sec_nonzero_when_no_soft:92, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=380, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 10}
[8] (extend_decision):{'extend': '是', 'extend_sec': 4}
[1] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=385, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}
[reward_diag] steps 380..390 invalid_rate=0.544 (87/160)
[reward_diag]  - extend_decision: invalid_rate=0.989 (87/88) top=extend_decision_extend_sec_nonzero_when_no_soft:85, extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=390, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 15}
[8] (extend_decision):{'extend': '是', 'extend_sec': 19}
[0] (extend_decision):{'extend': '否', 'extend_sec': 17}

[completion_log] step=395, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 5}
[reward_diag] steps 390..400 invalid_rate=0.438 (70/160)
[reward_diag]  - extend_decision: invalid_rate=0.972 (70/72) top=extend_decision_extend_sec_nonzero_when_no_soft:68, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=400, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 16}

[completion_log] step=405, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 400..410 invalid_rate=0.519 (83/160)
[reward_diag]  - extend_decision: invalid_rate=0.988 (83/84) top=extend_decision_extend_sec_nonzero_when_no_soft:82, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=410, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 15}

[completion_log] step=415, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 10}
[3] (extend_decision):{'extend': '是', 'extend_sec': 10}
[1] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 410..420 invalid_rate=0.594 (95/160)
[reward_diag]  - extend_decision: invalid_rate=0.990 (95/96) top=extend_decision_extend_sec_nonzero_when_no_soft:92, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=420, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=425, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 18}
[reward_diag] steps 420..430 invalid_rate=0.600 (96/160)
[reward_diag]  - extend_decision: invalid_rate=0.960 (96/100) top=extend_decision_extend_sec_nonzero_when_no_soft:94, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=430, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=435, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 20}
[8] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 430..440 invalid_rate=0.506 (81/160)
[reward_diag]  - extend_decision: invalid_rate=0.964 (81/84) top=extend_decision_extend_sec_nonzero_when_no_soft:79, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=440, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 17}
[0] (extend_decision):{'extend': '否', 'extend_sec': 20}

[completion_log] step=445, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 440..450 invalid_rate=0.637 (102/160)
[reward_diag]  - extend_decision: invalid_rate=0.911 (102/112) top=extend_decision_extend_sec_nonzero_when_no_soft:100, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=450, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=455, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 7}
[reward_diag] steps 450..460 invalid_rate=0.450 (72/160)
[reward_diag]  - extend_decision: invalid_rate=0.857 (72/84) top=extend_decision_extend_sec_nonzero_when_no_soft:71, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a
[reward_diag] KL spike at step=460 kl=61.1183 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "否", "extend_sec": 0}', '{"extend": "否", "extend_sec": 15}', '{"extend": "否", "extend_sec": 13}'], 'sample_reasons': ['ok', 'extend_decision_extend_sec_nonzero_when_no_soft', 'extend_decision_extend_sec_nonzero_when_no_soft'], 'sample_rewards': [0.0, -0.3, -0.3], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=460, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[7] (extend_decision):{'extend': '是', 'extend_sec': 15}
[1] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=465, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 460..470 invalid_rate=0.406 (65/160)
[reward_diag]  - extend_decision: invalid_rate=0.739 (65/88) top=extend_decision_extend_sec_nonzero_when_no_soft:60, extend_decision_extend_sec_exceeds_max_soft:4, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=470, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 7}
[13] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=475, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 17}
[reward_diag] steps 470..480 invalid_rate=0.256 (41/160)
[reward_diag]  - extend_decision: invalid_rate=0.512 (41/80) top=extend_decision_extend_sec_nonzero_when_no_soft:39, extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=480, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 16}

[completion_log] step=485, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 8}
[6] (extend_decision):{'extend': '是', 'extend_sec': 12}
[1] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 480..490 invalid_rate=0.263 (42/160)
[reward_diag]  - extend_decision: invalid_rate=0.457 (42/92) top=extend_decision_extend_sec_nonzero_when_no_soft:37, extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=490, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=495, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 15}
[8] (extend_decision):{'extend': '是', 'extend_sec': 8}
[1] (extend_decision):{'extend': '否', 'extend_sec': 5}
[reward_diag] steps 490..500 invalid_rate=0.231 (37/160)
[reward_diag]  - extend_decision: invalid_rate=0.463 (37/80) top=extend_decision_extend_sec_nonzero_when_no_soft:34, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=500, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 8}
[12] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=505, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 9}
[15] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 500..510 invalid_rate=0.212 (34/160)
[reward_diag]  - extend_decision: invalid_rate=0.386 (34/88) top=extend_decision_extend_sec_nonzero_when_no_soft:29, extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_extend_when_at_max_green:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=510, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 9}
[1] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=515, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 510..520 invalid_rate=0.244 (39/160)
[reward_diag]  - extend_decision: invalid_rate=0.464 (39/84) top=extend_decision_extend_sec_nonzero_when_no_soft:31, extend_decision_extend_sec_exceeds_max_soft:6, extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=520, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 14}
  [1] (signal_step): {"next_phase_id": 1, "green_sec": 27}
  [2] (signal_step): {"next_phase_id": 6, "green_sec": 28}

[completion_log] step=525, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 520..530 invalid_rate=0.269 (43/160)
[reward_diag]  - extend_decision: invalid_rate=0.448 (43/96) top=extend_decision_extend_sec_nonzero_when_no_soft:40, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=530, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 50}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 40}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 21}

[completion_log] step=535, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 10}
[5] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 530..540 invalid_rate=0.188 (30/160)
[reward_diag]  - extend_decision: invalid_rate=0.288 (30/104) top=extend_decision_extend_sec_nonzero_when_no_soft:22, extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=540, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 12}
[14] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 5}

[completion_log] step=545, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[14] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 540..550 invalid_rate=0.206 (33/160)
[reward_diag]  - extend_decision: invalid_rate=0.344 (33/96) top=extend_decision_extend_sec_nonzero_when_no_soft:23, extend_decision_extend_sec_exceeds_max_soft:6, extend_decision_final_green_out_of_bounds:3, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=550, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=555, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 550..560 invalid_rate=0.225 (36/160)
[reward_diag]  - extend_decision: invalid_rate=0.310 (36/116) top=extend_decision_extend_sec_nonzero_when_no_soft:30, extend_decision_extend_when_at_max_green:3, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=560, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 15}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=565, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 15}
[reward_diag] steps 560..570 invalid_rate=0.181 (29/160)
[reward_diag]  - extend_decision: invalid_rate=0.315 (29/92) top=extend_decision_extend_sec_nonzero_when_no_soft:28, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=570, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 5}
[3] (extend_decision):{'extend': '是', 'extend_sec': 8}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=575, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 37}
  [1] (signal_step): {"next_phase_id": 1, "green_sec": 49}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 38}
[reward_diag] steps 570..580 invalid_rate=0.156 (25/160)
[reward_diag]  - extend_decision: invalid_rate=0.312 (25/80) top=extend_decision_extend_sec_nonzero_when_no_soft:20, extend_decision_extend_sec_exceeds_max_soft:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=580, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=585, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 580..590 invalid_rate=0.237 (38/160)
[reward_diag]  - extend_decision: invalid_rate=0.432 (38/88) top=extend_decision_extend_sec_nonzero_when_no_soft:37, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=590, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=595, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 590..600 invalid_rate=0.181 (29/160)
[reward_diag]  - extend_decision: invalid_rate=0.345 (29/84) top=extend_decision_extend_sec_nonzero_when_no_soft:19, extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=600, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=605, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 5}
[8] (extend_decision):{'extend': '是', 'extend_sec': 15}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 600..610 invalid_rate=0.156 (25/160)
[reward_diag]  - extend_decision: invalid_rate=0.240 (25/104) top=extend_decision_extend_sec_nonzero_when_no_soft:17, extend_decision_extend_sec_exceeds_max_soft:5, extend_decision_final_green_out_of_bounds:2, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=610, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=615, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 17}
[reward_diag] steps 610..620 invalid_rate=0.175 (28/160)
[reward_diag]  - extend_decision: invalid_rate=0.269 (28/104) top=extend_decision_extend_sec_nonzero_when_no_soft:21, extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=620, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 5}
[6] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=625, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[11] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 620..630 invalid_rate=0.212 (34/160)
[reward_diag]  - extend_decision: invalid_rate=0.386 (34/88) top=extend_decision_extend_sec_nonzero_when_no_soft:27, extend_decision_final_green_out_of_bounds:6, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=630, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 9}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=635, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 630..640 invalid_rate=0.106 (17/160)
[reward_diag]  - extend_decision: invalid_rate=0.163 (17/104) top=extend_decision_extend_sec_nonzero_when_no_soft:11, extend_decision_extend_sec_exceeds_max_soft:5, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=640, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=645, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 640..650 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (10/100) top=extend_decision_extend_sec_nonzero_when_no_soft:9, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=650, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=655, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 6}
[11] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 650..660 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.114 (10/88) top=extend_decision_extend_sec_nonzero_when_no_soft:7, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a
[reward_diag] KL spike at step=660 kl=43.2556 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "否", "extend_sec": 0}', '{"extend": "否", "extend_sec": 0}', '{"extend": "否", "extend_sec": 3}\n{"extend": "是", "extend_sec": 8}'], 'sample_reasons': ['ok', 'ok', 'ok'], 'sample_rewards': [0.0, 0.0, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=660, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=665, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 660..670 invalid_rate=0.125 (20/160)
[reward_diag]  - extend_decision: invalid_rate=0.200 (20/100) top=extend_decision_extend_sec_nonzero_when_no_soft:15, extend_decision_extend_sec_exceeds_max_soft:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=670, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=675, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 670..680 invalid_rate=0.119 (19/160)
[reward_diag]  - extend_decision: invalid_rate=0.226 (19/84) top=extend_decision_extend_sec_nonzero_when_no_soft:12, extend_decision_final_green_out_of_bounds:6, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=680, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=685, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 680..690 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.120 (12/100) top=extend_decision_extend_sec_nonzero_when_no_soft:5, extend_decision_final_green_out_of_bounds:4, extend_decision_extend_when_at_max_green:2, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=690, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 13}
[7] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=695, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 690..700 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (6/96) top=extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_extend_sec_nonzero_when_no_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=700, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=705, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 700..710 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.152 (14/92) top=extend_decision_final_green_out_of_bounds:10, extend_decision_extend_sec_nonzero_when_no_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=710, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=715, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 9}
[3] (extend_decision):{'extend': '是', 'extend_sec': 11}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 710..720 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.152 (14/92) top=extend_decision_extend_sec_nonzero_when_no_soft:11, extend_decision_extend_sec_exceeds_max_soft:2, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=720, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 6}
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 10}

[completion_log] step=725, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 13}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 720..730 invalid_rate=0.138 (22/160)
[reward_diag]  - extend_decision: invalid_rate=0.190 (22/116) top=extend_decision_extend_sec_nonzero_when_no_soft:17, extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=730, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[2] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=735, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 730..740 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.110 (11/100) top=extend_decision_extend_sec_nonzero_when_no_soft:9, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=740, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=745, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 9}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 740..750 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (10/100) top=extend_decision_extend_sec_nonzero_when_no_soft:4, extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=750, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=755, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 750..760 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.094 (9/96) top=extend_decision_extend_sec_nonzero_when_no_soft:8, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=760, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 31}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 16}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 35}

[completion_log] step=765, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 760..770 invalid_rate=0.094 (15/160)
[reward_diag]  - extend_decision: invalid_rate=0.179 (15/84) top=extend_decision_extend_sec_nonzero_when_no_soft:7, extend_decision_final_green_out_of_bounds:7, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=770, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=775, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 770..780 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_extend_sec_nonzero_when_no_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=780, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=785, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 780..790 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.158 (12/76) top=extend_decision_extend_sec_nonzero_when_no_soft:7, extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=790, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=795, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 790..800 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.093 (10/108) top=extend_decision_extend_sec_nonzero_when_no_soft:6, extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=800, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=805, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 800..810 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (3/88) top=extend_decision_extend_sec_nonzero_when_no_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=810, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=815, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 810..820 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (10/80) top=extend_decision_extend_sec_nonzero_when_no_soft:10
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=820, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 6}
[2] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=825, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 820..830 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (10/100) top=extend_decision_extend_sec_nonzero_when_no_soft:9, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=830, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=835, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 830..840 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=840, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=845, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 840..850 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_extend_sec_nonzero_when_no_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=850, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=855, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 850..860 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.069 (5/72) top=extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_nonzero_when_no_soft:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=860, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=865, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 860..870 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_extend_sec_nonzero_when_no_soft:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=870, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[2] (extend_decision):{'extend': '是', 'extend_sec': 4}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=875, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 870..880 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.068 (6/88) top=extend_decision_extend_sec_nonzero_when_no_soft:5, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=880, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=885, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 880..890 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:3, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=890, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=895, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 890..900 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (9/104) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=900, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 5}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=905, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 40}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 42}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 22}
[reward_diag] steps 900..910 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=910, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=915, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 910..920 invalid_rate=0.113 (18/160)
[reward_diag]  - extend_decision: invalid_rate=0.196 (18/92) top=extend_decision_final_green_out_of_bounds:14, extend_decision_extend_sec_nonzero_when_no_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=925, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 16}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 920..930 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.073 (7/96) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2, extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=930, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=935, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 930..940 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.176 (12/68) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=940, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 940..950 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=950, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=955, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 950..960 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=960, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 960..970 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=970, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=975, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 970..980 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=980, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=985, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 980..990 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=990, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=995, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 8}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 990..1000 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.110 (11/100) top=extend_decision_final_green_out_of_bounds:7, extend_decision_extend_sec_nonzero_when_no_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=1000, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1005, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1000..1010 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (6/108) top=extend_decision_extend_sec_nonzero_when_no_soft:5, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1010, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1015, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1010..1020 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1020, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1025, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1020..1030 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1030, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1035, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1030..1040 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1040, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1045, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1040..1050 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/68) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=1050, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1055, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1050..1060 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.136 (12/88) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1060, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1065, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1060..1070 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=1070, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1075, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1070..1080 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.143 (12/84) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1080, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1085, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1080..1090 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.068 (6/88) top=extend_decision_final_green_out_of_bounds:5, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1090, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[12] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1095, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1090..1100 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1100, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1105, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1100..1110 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.095 (8/84) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1110, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1115, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1110..1120 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a
[reward_diag] KL spike at step=1120 kl=6.1985 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"next_phase_id": 5, "green_sec": 20}', '{"next_phase_id": 9, "green_sec": 20}', '{"next_phase_id": 6, "green_sec": 50}'], 'sample_reasons': ['ok', 'ok', 'ok'], 'sample_rewards': [0.0, 0.0, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=1120, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1125, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1120..1130 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1130, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1135, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1130..1140 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1140, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1145, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1140..1150 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1150, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1155, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1150..1160 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.024 (2/84) top=extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1160, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1165, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1160..1170 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1170, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1175, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1170..1180 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1180, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 10}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1185, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1180..1190 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1190, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 5}
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1195, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 56}
  [2] (signal_step): {"next_phase_id": 5, "green_sec": 22}
[reward_diag] steps 1190..1200 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.031 (3/96) top=extend_decision_extend_sec_exceeds_max_soft:2, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=1200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1205, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1200..1210 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (4/112) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=1210, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1215, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1210..1220 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1220, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1225, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1220..1230 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1230, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1235, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1230..1240 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1240, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1245, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 30}
[reward_diag] steps 1240..1250 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1250, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1255, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1250..1260 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1260, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1265, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 16}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 20}
[reward_diag] steps 1260..1270 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1270, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1275, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 50}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 20}
[reward_diag] steps 1270..1280 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1280, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1285, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1280..1290 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1290, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1295, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1290..1300 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1300, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1305, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1300..1310 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=1310, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1315, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1310..1320 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=1320, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1325, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1320..1330 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1330, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1335, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1330..1340 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1340, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[2] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1345, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 6}
[11] (extend_decision):{'extend': '是', 'extend_sec': 6}
[9] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1340..1350 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.067 (7/104) top=extend_decision_final_green_out_of_bounds:6, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1350, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1355, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1350..1360 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1360, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1365, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1360..1370 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1370, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1375, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1370..1380 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1380, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1385, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1380..1390 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/116) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=1390, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1395, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1390..1400 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=1400, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1405, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1400..1410 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=1410, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1415, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1410..1420 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1420, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1425, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1420..1430 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.069 (8/116) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=1430, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1435, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1430..1440 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (8/112) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=1440, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1445, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1440..1450 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=1450, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1455, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1450..1460 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/64) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/96) top=n/a

[completion_log] step=1460, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1465, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1460..1470 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1470, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1475, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[13] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1470..1480 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.075 (9/120) top=extend_decision_final_green_out_of_bounds:9
[reward_diag]  - signal_step: invalid_rate=0.000 (0/40) top=n/a

[completion_log] step=1480, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1485, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1480..1490 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1490, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1495, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1490..1500 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=1500, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1505, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1500..1510 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.095 (8/84) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1510, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1515, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1510..1520 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1520, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1525, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 19}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 27}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 18}
[reward_diag] steps 1520..1530 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=1530, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1535, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1530..1540 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (4/116) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=1540, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1545, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1540..1550 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.074 (8/108) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1550, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1555, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1550..1560 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1560, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1565, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1560..1570 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1570, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1575, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1570..1580 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1580, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1585, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1580..1590 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1590, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1595, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 5}
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1590..1600 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.054 (3/56) top=extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/104) top=n/a

[completion_log] step=1600, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 27}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 31}

[completion_log] step=1605, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1600..1610 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.017 (1/60) top=extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/100) top=n/a

[completion_log] step=1610, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1615, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1610..1620 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (8/112) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=1620, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1625, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1620..1630 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1630, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1635, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1630..1640 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=1640, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1645, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1640..1650 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (4/116) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=1650, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 17}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 28}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 17}

[completion_log] step=1655, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1650..1660 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/64) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/96) top=n/a

[completion_log] step=1660, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1665, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1660..1670 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1670, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1675, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1670..1680 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=1680, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 15}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 50}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 16}

[completion_log] step=1685, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1680..1690 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1690, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1695, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1690..1700 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=1700, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1705, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1700..1710 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1710, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1715, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1710..1720 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1720, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1725, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1720..1730 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=1730, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1735, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1730..1740 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1740, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1745, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1740..1750 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=1750, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1755, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1750..1760 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1760, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1765, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1760..1770 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1770, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1775, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1770..1780 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.095 (8/84) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1780, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1785, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 4}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1780..1790 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=1790, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1795, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1790..1800 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1800, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1805, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1800..1810 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=1810, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 5}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1815, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1810..1820 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1820, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1825, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1820..1830 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1830, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1835, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1830..1840 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=1840, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1845, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1840..1850 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.019 (2/104) top=extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1850, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '是', 'extend_sec': 5}
[2] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1855, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1850..1860 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.163 (13/80) top=extend_decision_final_green_out_of_bounds:12, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=1860, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1865, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1860..1870 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.090 (9/100) top=extend_decision_final_green_out_of_bounds:9
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=1870, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1875, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1870..1880 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1880, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1885, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[3] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1880..1890 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=1890, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1895, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1890..1900 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=1900, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1905, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1900..1910 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (5/100) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=1910, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1915, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1910..1920 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.013 (1/76) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=1920, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1925, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1920..1930 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=1930, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 7}
[7] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1935, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1930..1940 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=1940, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1940..1950 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=1950, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1955, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1950..1960 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.054 (6/112) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_when_at_max_green:1, extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=1960, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1960..1970 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (6/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1970, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1975, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1970..1980 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.024 (2/84) top=extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1980, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1985, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1980..1990 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=1990, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=1995, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 1990..2000 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.075 (6/80) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2000, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 4}
[10] (extend_decision):{'extend': '是', 'extend_sec': 5}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2005, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2000..2010 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (3/88) top=extend_decision_extend_sec_nonzero_when_no_soft:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=2010, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 6}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2015, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 10}
[reward_diag] steps 2010..2020 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.140 (14/100) top=extend_decision_extend_sec_nonzero_when_no_soft:7, extend_decision_final_green_out_of_bounds:6, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2020, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2025, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2020..2030 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=2030, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2035, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2030..2040 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (5/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2040, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 6}
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2045, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2040..2050 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=2050, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[9] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2055, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2050..2060 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.037 (3/80) top=signal_step_parse_failed:3

[completion_log] step=2060, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2065, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 5}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 11}
[reward_diag] steps 2060..2070 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=2070, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2075, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2070..2080 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=2080, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2085, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2080..2090 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2090, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2095, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2090..2100 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2100, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2105, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2100..2110 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=2110, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2115, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2110..2120 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=2120, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2125, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2120..2130 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (5/100) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=2130, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2135, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2130..2140 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2140, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2145, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2140..2150 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=2150, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2155, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2150..2160 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2160, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2165, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2160..2170 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2170, num_completions=16
  [0] (signal_step): {"next_phase_id": 5, "green_sec": 30}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 6, "green_sec": 10}

[completion_log] step=2175, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2170..2180 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=2180, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2185, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2180..2190 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.078 (5/64) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/96) top=n/a

[completion_log] step=2190, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2195, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 6}
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2190..2200 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.031 (3/96) top=extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=2200, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2205, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2200..2210 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=2210, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2215, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2210..2220 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2220, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2225, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2220..2230 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.095 (8/84) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=2230, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 18}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2235, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 5}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2230..2240 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_extend_sec_exceeds_max_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2240, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[10] (extend_decision):{'extend': '是', 'extend_sec': 4}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2245, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2240..2250 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (6/108) top=extend_decision_extend_sec_exceeds_max_soft:6
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=2250, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 10}
[7] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2255, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2250..2260 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.075 (6/80) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2260, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2265, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2260..2270 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2270, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2275, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2270..2280 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2280, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2285, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2280..2290 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2290, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2295, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2290..2300 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (4/112) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=2300, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2305, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 16}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 12}
[reward_diag] steps 2300..2310 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/60) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/100) top=n/a

[completion_log] step=2310, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2315, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2310..2320 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2320, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2325, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2320..2330 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2330, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2335, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2330..2340 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2340, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2345, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2340..2350 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2350, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2355, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2350..2360 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=2360, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2365, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2360..2370 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2370, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2375, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2370..2380 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2380, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2385, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2380..2390 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=2390, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2395, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2390..2400 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2400, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2405, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2400..2410 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.009 (1/112) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=2410, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2415, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2410..2420 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2420, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2425, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2420..2430 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=2430, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2435, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2430..2440 invalid_rate=0.100 (16/160)
[reward_diag]  - extend_decision: invalid_rate=0.143 (16/112) top=extend_decision_final_green_out_of_bounds:16
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=2440, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2445, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2440..2450 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=2450, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2455, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2450..2460 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=2460, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2465, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2460..2470 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2470, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2475, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2470..2480 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (5/116) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=2480, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2485, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2480..2490 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=2490, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2495, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2490..2500 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2500, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2505, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2500..2510 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2510, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2515, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2510..2520 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (5/112) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=2520, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2525, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2520..2530 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2530, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2535, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2530..2540 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2540, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2545, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2540..2550 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/64) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/96) top=n/a

[completion_log] step=2550, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2555, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2550..2560 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2560, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2565, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2560..2570 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2570, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2575, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2570..2580 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2580, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2585, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2580..2590 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2590, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2595, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 19}
  [2] (signal_step): {"next_phase_id": 5, "green_sec": 20}
[reward_diag] steps 2590..2600 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=2600, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2605, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2600..2610 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/108) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=2610, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2615, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2610..2620 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=2620, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2625, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2620..2630 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=2630, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2635, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 30}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 40}
  [2] (signal_step): {"next_phase_id": 6, "green_sec": 18}
[reward_diag] steps 2630..2640 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=2640, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2645, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2640..2650 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=2650, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 16}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 21}

[completion_log] step=2655, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2650..2660 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.111 (8/72) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=2660, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 5}
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2665, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2660..2670 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=2670, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2675, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2670..2680 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_phase_id_invalid:1

[completion_log] step=2680, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 5}
[7] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2685, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2680..2690 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.011 (1/88) top=signal_step_parse_failed:1

[completion_log] step=2690, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2695, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2690..2700 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.115 (11/96) top=extend_decision_final_green_out_of_bounds:10, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=2700, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[3] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2705, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2700..2710 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=2710, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2715, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[3] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2710..2720 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=2720, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2725, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2720..2730 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (4/116) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_parse_failed:1

[completion_log] step=2730, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2735, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2730..2740 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=2740, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2745, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2740..2750 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.027 (3/112) top=extend_decision_extend_when_at_max_green:1, extend_decision_final_green_out_of_bounds:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=2750, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2755, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2750..2760 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2760, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2765, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2760..2770 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=2770, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2775, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 5}
[5] (extend_decision):{'extend': '是', 'extend_sec': 4}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2770..2780 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.065 (7/108) top=extend_decision_final_green_out_of_bounds:7
[reward_diag]  - signal_step: invalid_rate=0.038 (2/52) top=signal_step_parse_failed:2

[completion_log] step=2780, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2785, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 6}
[9] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2780..2790 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (4/116) top=extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_parse_failed:1

[completion_log] step=2790, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2795, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2790..2800 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/124) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (1/36) top=signal_step_parse_failed:1

[completion_log] step=2800, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2805, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2800..2810 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (5/80) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2810, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[10] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2815, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2810..2820 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2820, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2825, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[15] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2820..2830 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=2830, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2835, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2830..2840 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.104 (10/96) top=extend_decision_final_green_out_of_bounds:9, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=2840, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 23}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 32}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 22}

[completion_log] step=2845, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2840..2850 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.013 (1/80) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=2850, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2855, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2850..2860 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=2860, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2865, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2860..2870 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2870, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2875, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2870..2880 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=2880, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2885, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2880..2890 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=2890, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2895, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2890..2900 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=2900, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2905, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2900..2910 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=2910, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2915, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2910..2920 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=2920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2925, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2920..2930 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.074 (8/108) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=2930, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2935, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2930..2940 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=2940, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2940..2950 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=2950, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2955, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2950..2960 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.054 (5/92) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.044 (3/68) top=signal_step_parse_failed:3

[completion_log] step=2960, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2960..2970 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=2970, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2975, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2970..2980 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.059 (4/68) top=signal_step_parse_failed:4
[reward_diag] KL spike at step=2980 kl=14.6578 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"next_phase_id": 7, "green_sec": 10}', '{"next_phase_id": 6, "green_sec": 5}', '{"next_phase_id": 9, "green_sec": 17}'], 'sample_reasons': ['ok', 'ok', 'ok'], 'sample_rewards': [0.0, 0.0, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=2980, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2985, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2980..2990 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.056 (4/72) top=signal_step_parse_failed:4

[completion_log] step=2990, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=2995, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 2990..3000 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/68) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.022 (2/92) top=signal_step_parse_failed:2

[completion_log] step=3000, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3005, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3000..3010 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (5/104) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=3010, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3015, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3010..3020 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=3020, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3025, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3020..3030 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=3030, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3035, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 6}
[6] (extend_decision):{'extend': '是', 'extend_sec': 11}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3030..3040 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.015 (1/68) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.033 (3/92) top=signal_step_parse_failed:3

[completion_log] step=3040, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3045, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3040..3050 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=3050, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3055, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3050..3060 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=3060, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 6}
[14] (extend_decision):{'extend': '是', 'extend_sec': 8}
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3065, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3060..3070 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.053 (4/76) top=signal_step_parse_failed:4

[completion_log] step=3070, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3075, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3070..3080 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=3080, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3085, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3080..3090 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=3090, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3095, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3090..3100 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=3100, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3105, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3100..3110 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=3110, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3115, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3110..3120 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.074 (8/108) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=3120, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3125, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3120..3130 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/116) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.136 (6/44) top=signal_step_parse_failed:6

[completion_log] step=3130, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3135, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3130..3140 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (8/112) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=3140, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3145, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3140..3150 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=3150, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 50}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 30}

[completion_log] step=3155, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3150..3160 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.013 (1/80) top=signal_step_parse_failed:1

[completion_log] step=3160, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3165, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3160..3170 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=3170, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3175, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3170..3180 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=3180, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3185, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3180..3190 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=3190, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3195, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3190..3200 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=3200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3205, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3200..3210 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=3210, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3215, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3210..3220 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=3220, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3225, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3220..3230 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/112) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.021 (1/48) top=signal_step_parse_failed:1

[completion_log] step=3230, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3235, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '是', 'extend_sec': 5}
[6] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3230..3240 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.069 (5/72) top=signal_step_parse_failed:5

[completion_log] step=3240, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3245, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3240..3250 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=3250, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 6}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3255, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3250..3260 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.056 (4/72) top=signal_step_parse_failed:4

[completion_log] step=3260, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3265, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3260..3270 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_parse_failed:1

[completion_log] step=3270, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3275, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3270..3280 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=3280, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3285, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3280..3290 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.058 (6/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=3290, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3295, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3290..3300 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.017 (2/116) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=3300, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3305, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3300..3310 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=3310, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3315, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3310..3320 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=3320, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3325, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3320..3330 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.104 (10/96) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=3330, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3335, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3330..3340 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/112) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.021 (1/48) top=signal_step_parse_failed:1

[completion_log] step=3340, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3345, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3340..3350 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.008 (1/124) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.028 (1/36) top=signal_step_parse_failed:1

[completion_log] step=3350, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3355, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3350..3360 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.071 (4/56) top=signal_step_parse_failed:4

[completion_log] step=3360, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 3}
[7] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3365, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3360..3370 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_parse_failed:1

[completion_log] step=3370, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3375, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3370..3380 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=3380, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3385, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3380..3390 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.030 (3/100) top=extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.133 (8/60) top=signal_step_parse_failed:8

[completion_log] step=3390, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3395, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3390..3400 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (12/96) top=extend_decision_final_green_out_of_bounds:10, extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=3400, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3405, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3400..3410 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=3410, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3415, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3410..3420 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=3420, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3425, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3420..3430 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=3430, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3435, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3430..3440 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=3440, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3445, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3440..3450 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.067 (4/60) top=signal_step_parse_failed:4

[completion_log] step=3450, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3455, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3450..3460 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.024 (2/84) top=extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=3460, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3465, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3460..3470 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=3470, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3475, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3470..3480 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=3480, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 60}
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[13] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3485, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3480..3490 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (10/80) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=3490, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3495, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3490..3500 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (3/84) top=extend_decision_extend_sec_exceeds_max_soft:2, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.079 (6/76) top=signal_step_parse_failed:6

[completion_log] step=3500, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 6}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3505, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3500..3510 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.039 (3/76) top=extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_parse_failed:1

[completion_log] step=3510, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3515, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3510..3520 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (4/116) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=3520, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3525, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3520..3530 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=3530, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 10}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3535, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3530..3540 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.065 (7/108) top=extend_decision_extend_sec_exceeds_max_soft:5, extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=3540, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 6}
[15] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3545, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 60}
[12] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3540..3550 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.086 (10/116) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.045 (2/44) top=signal_step_parse_failed:2

[completion_log] step=3550, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3555, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3550..3560 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.066 (5/76) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=3560, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3565, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3560..3570 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=3570, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3575, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3570..3580 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=3580, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3585, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3580..3590 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (9/104) top=extend_decision_final_green_out_of_bounds:9
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_phase_id_invalid:1

[completion_log] step=3590, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3595, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3590..3600 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.094 (6/64) top=signal_step_parse_failed:6

[completion_log] step=3600, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3605, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3600..3610 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/60) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.060 (6/100) top=signal_step_parse_failed:6

[completion_log] step=3610, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 0.0}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 10}
  [2] (signal_step): {"next_phase_id": 6, "green_sec": 35}

[completion_log] step=3615, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 30}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 5, "green_sec": 5.0}
[reward_diag] steps 3610..3620 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.050 (4/80) top=signal_step_parse_failed:4

[completion_log] step=3620, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3625, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3620..3630 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=3630, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3635, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3630..3640 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=3640, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3645, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3640..3650 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.107 (6/56) top=signal_step_parse_failed:6

[completion_log] step=3650, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3655, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3650..3660 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=3660, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3665, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3660..3670 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/112) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.083 (4/48) top=signal_step_parse_failed:4
[reward_diag] KL spike at step=3670 kl=6.5630 batch={'num_completions': 16, 'num_generations': 1, 'sample_completions': ['{"extend": "否", "extend_sec": 0}', '{"extend": "否", "extend_sec": 0}', '{"extend": "否", "extend_sec": 0}'], 'sample_reasons': ['ok', 'ok', 'ok'], 'sample_rewards': [0.0, 0.0, 0.0], 'task_types': ['extend_decision', 'signal_step'], 'invalid_count': 0}

[completion_log] step=3670, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3675, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3670..3680 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.024 (2/84) top=signal_step_parse_failed:2

[completion_log] step=3680, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3685, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3680..3690 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.054 (3/56) top=signal_step_parse_failed:3

[completion_log] step=3690, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3695, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3690..3700 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.062 (4/64) top=signal_step_parse_failed:4

[completion_log] step=3700, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3705, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3700..3710 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=3710, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3715, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 14}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 14}
  [2] (signal_step): {"next_phase_id": 1, "green_sec": 17}
[reward_diag] steps 3710..3720 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=3720, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3725, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3720..3730 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/108) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=3730, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3735, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3730..3740 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.024 (2/84) top=signal_step_parse_failed:2

[completion_log] step=3740, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3745, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3740..3750 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.074 (5/68) top=signal_step_parse_failed:5

[completion_log] step=3750, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3755, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3750..3760 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=3760, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3765, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3760..3770 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=3770, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3775, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3770..3780 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=3780, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3785, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3780..3790 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_parse_failed:1

[completion_log] step=3790, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3795, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3790..3800 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=3800, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 5}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3805, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 6}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3800..3810 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.033 (3/92) top=extend_decision_final_green_out_of_bounds:2, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.044 (3/68) top=signal_step_parse_failed:3

[completion_log] step=3810, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 60}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3815, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3810..3820 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=3820, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3825, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 5}
[15] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3820..3830 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.022 (2/92) top=extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=3830, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3835, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3830..3840 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=3840, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3845, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3840..3850 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=3850, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3855, num_completions=16
[9] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3850..3860 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.130 (12/92) top=extend_decision_parse_failed:8, extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=3860, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3865, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3860..3870 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.100 (6/60) top=signal_step_parse_failed:6

[completion_log] step=3870, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3875, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3870..3880 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=3880, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3885, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 3}
[5] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3880..3890 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.077 (8/104) top=extend_decision_extend_sec_exceeds_max_soft:6, extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=3890, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3895, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3890..3900 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.014 (1/72) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.045 (4/88) top=signal_step_parse_failed:4

[completion_log] step=3900, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3905, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3900..3910 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=3910, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3915, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3910..3920 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=3920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3925, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3920..3930 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (8/112) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=3930, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3935, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3930..3940 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=3940, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3940..3950 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=3950, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3955, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3950..3960 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=3960, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3960..3970 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/108) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=3970, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3975, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3970..3980 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=3980, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3985, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3980..3990 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=3990, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=3995, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 3990..4000 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=4000, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4005, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4000..4010 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.079 (6/76) top=signal_step_parse_failed:6

[completion_log] step=4010, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[12] (extend_decision):{'extend': '是', 'extend_sec': 5}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4015, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 33}
[reward_diag] steps 4010..4020 invalid_rate=0.119 (19/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.184 (14/76) top=signal_step_parse_failed:14

[completion_log] step=4020, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4025, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4020..4030 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (5/116) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.045 (2/44) top=signal_step_parse_failed:2

[completion_log] step=4030, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 15}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 10}

[completion_log] step=4035, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4030..4040 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.090 (9/100) top=extend_decision_final_green_out_of_bounds:7, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.050 (3/60) top=signal_step_parse_failed:3

[completion_log] step=4040, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4045, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4040..4050 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (12/96) top=extend_decision_final_green_out_of_bounds:10, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=4050, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 60}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4055, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4050..4060 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=4060, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 8}
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4065, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4060..4070 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:5, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=4070, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4075, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4070..4080 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (5/112) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=4080, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4085, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4080..4090 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (3/72) top=extend_decision_final_green_out_of_bounds:2, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.057 (5/88) top=signal_step_parse_failed:5

[completion_log] step=4090, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4095, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4090..4100 invalid_rate=0.094 (15/160)
[reward_diag]  - extend_decision: invalid_rate=0.110 (11/100) top=extend_decision_final_green_out_of_bounds:11
[reward_diag]  - signal_step: invalid_rate=0.067 (4/60) top=signal_step_parse_failed:4

[completion_log] step=4100, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4105, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4100..4110 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_parse_failed:4
[reward_diag]  - signal_step: invalid_rate=0.054 (3/56) top=signal_step_parse_failed:3

[completion_log] step=4110, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4115, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4110..4120 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.031 (3/96) top=extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=4120, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 6}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4125, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4120..4130 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.077 (4/52) top=extend_decision_extend_sec_exceeds_max_soft:2, extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.046 (5/108) top=signal_step_parse_failed:5

[completion_log] step=4130, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4135, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4130..4140 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (6/96) top=extend_decision_final_green_out_of_bounds:5, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=4140, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4145, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4140..4150 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.068 (6/88) top=extend_decision_final_green_out_of_bounds:5, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=4150, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4155, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4150..4160 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=4160, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4165, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4160..4170 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=4170, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4175, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[6] (extend_decision):{'extend': '是', 'extend_sec': 10}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4170..4180 invalid_rate=0.138 (22/160)
[reward_diag]  - extend_decision: invalid_rate=0.155 (18/116) top=extend_decision_final_green_out_of_bounds:12, extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_extend_when_at_max_green:2, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.091 (4/44) top=signal_step_parse_failed:4

[completion_log] step=4180, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4185, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4180..4190 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4190, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4195, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4190..4200 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=4200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4205, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4200..4210 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=4210, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4215, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4210..4220 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.054 (5/92) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.044 (3/68) top=signal_step_parse_failed:3

[completion_log] step=4220, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4225, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4220..4230 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.015 (1/68) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=4230, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4235, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4230..4240 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (5/100) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=4240, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4245, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4240..4250 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=4250, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4255, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4250..4260 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.019 (2/104) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=4260, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4265, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4260..4270 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.067 (7/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=4270, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4275, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 10}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4270..4280 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.094 (9/96) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=4280, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4285, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4280..4290 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=4290, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4295, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4290..4300 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=4300, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4305, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4300..4310 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (4/116) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=4310, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4315, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4310..4320 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=4320, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4325, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4320..4330 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_extend_sec_exceeds_max_soft:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=4330, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[6] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4335, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4330..4340 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (6/96) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=4340, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 6}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 6}

[completion_log] step=4345, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 15}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 4}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 3}
[reward_diag] steps 4340..4350 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=4350, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4355, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4350..4360 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/112) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=4360, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4365, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4360..4370 invalid_rate=0.094 (15/160)
[reward_diag]  - extend_decision: invalid_rate=0.135 (14/104) top=extend_decision_final_green_out_of_bounds:12, extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=4370, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4375, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 5}
[14] (extend_decision):{'extend': '是', 'extend_sec': 10}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4370..4380 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_extend_sec_exceeds_max_soft:4, extend_decision_final_green_out_of_bounds:2, extend_decision_parse_failed:1, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.059 (4/68) top=signal_step_parse_failed:4

[completion_log] step=4380, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[12] (extend_decision):{'extend': '是', 'extend_sec': 6}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4385, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4380..4390 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=4390, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4395, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4390..4400 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (6/96) top=extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_phase_id_invalid:1

[completion_log] step=4400, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4405, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 5}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4400..4410 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4410, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[14] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4415, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4410..4420 invalid_rate=0.094 (15/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (9/72) top=extend_decision_final_green_out_of_bounds:7, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.068 (6/88) top=signal_step_parse_failed:6

[completion_log] step=4420, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4425, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4420..4430 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (5/80) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.037 (3/80) top=signal_step_parse_failed:3

[completion_log] step=4430, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 6}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4435, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4430..4440 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.020 (2/100) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=4440, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4445, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 7}
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4440..4450 invalid_rate=0.106 (17/160)
[reward_diag]  - extend_decision: invalid_rate=0.116 (13/112) top=extend_decision_final_green_out_of_bounds:12, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.083 (4/48) top=signal_step_parse_failed:4

[completion_log] step=4450, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4455, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4450..4460 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.066 (5/76) top=signal_step_parse_failed:5

[completion_log] step=4460, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4465, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4460..4470 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.069 (5/72) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.080 (7/88) top=signal_step_parse_failed:7

[completion_log] step=4470, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 60}
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[6] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4475, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4470..4480 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4480, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4485, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4480..4490 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.046 (5/108) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.038 (2/52) top=signal_step_parse_failed:2

[completion_log] step=4490, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4495, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4490..4500 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.075 (6/80) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.013 (1/80) top=signal_step_parse_failed:1

[completion_log] step=4500, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[5] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4505, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4500..4510 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=4510, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4515, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4510..4520 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=4520, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 15}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 25}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 10}

[completion_log] step=4525, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4520..4530 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.062 (4/64) top=signal_step_parse_failed:4

[completion_log] step=4530, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4535, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 6}
[12] (extend_decision):{'extend': '是', 'extend_sec': 8}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4530..4540 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=4540, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 13}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 23}

[completion_log] step=4545, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4540..4550 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=4550, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4555, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 3}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4550..4560 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4560, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4565, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4560..4570 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.107 (9/84) top=extend_decision_final_green_out_of_bounds:9
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=4570, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 5}
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4575, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4570..4580 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.017 (1/60) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.070 (7/100) top=signal_step_parse_failed:7

[completion_log] step=4580, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 3}
[10] (extend_decision):{'extend': '是', 'extend_sec': 5}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4585, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4580..4590 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (3/84) top=extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=4590, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[14] (extend_decision):{'extend': '是', 'extend_sec': 6}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4595, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4590..4600 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.050 (4/80) top=signal_step_parse_failed:4

[completion_log] step=4600, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4605, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4600..4610 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=4610, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4615, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4610..4620 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.105 (8/76) top=signal_step_parse_failed:8

[completion_log] step=4620, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4625, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4620..4630 invalid_rate=0.100 (16/160)
[reward_diag]  - extend_decision: invalid_rate=0.150 (12/80) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.050 (4/80) top=signal_step_parse_failed:4

[completion_log] step=4630, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4635, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4630..4640 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.025 (2/80) top=extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.037 (3/80) top=signal_step_parse_failed:3

[completion_log] step=4640, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4645, num_completions=16
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4640..4650 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (3/88) top=extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=4650, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4655, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4650..4660 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.023 (2/88) top=signal_step_parse_failed:2

[completion_log] step=4660, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4665, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4660..4670 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=4670, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4675, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4670..4680 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (3/84) top=extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=4680, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[3] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4685, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 5}
[2] (extend_decision):{'extend': '是', 'extend_sec': 3}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4680..4690 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.028 (2/72) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.011 (1/88) top=signal_step_parse_failed:1

[completion_log] step=4690, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4695, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 12}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 27}
[reward_diag] steps 4690..4700 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=4700, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4705, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 3}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4700..4710 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (5/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=4710, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4715, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4710..4720 invalid_rate=0.106 (17/160)
[reward_diag]  - extend_decision: invalid_rate=0.066 (5/76) top=extend_decision_parse_failed:5
[reward_diag]  - signal_step: invalid_rate=0.143 (12/84) top=signal_step_parse_failed:12

[completion_log] step=4720, num_completions=16
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4725, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4720..4730 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_parse_failed:4
[reward_diag]  - signal_step: invalid_rate=0.069 (5/72) top=signal_step_parse_failed:5

[completion_log] step=4730, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4735, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4730..4740 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.095 (8/84) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4740, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4745, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4740..4750 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=4750, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4755, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4750..4760 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.095 (8/84) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4760, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4765, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4760..4770 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=4770, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4775, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4770..4780 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.031 (3/96) top=extend_decision_final_green_out_of_bounds:3
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=4780, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4785, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4780..4790 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=4790, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4795, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4790..4800 invalid_rate=0.106 (17/160)
[reward_diag]  - extend_decision: invalid_rate=0.167 (12/72) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.057 (5/88) top=signal_step_parse_failed:4, signal_step_phase_id_invalid:1

[completion_log] step=4800, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[3] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4805, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 8}
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4800..4810 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (5/100) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.050 (3/60) top=signal_step_parse_failed:3

[completion_log] step=4810, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4815, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4810..4820 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.045 (4/88) top=signal_step_parse_failed:4

[completion_log] step=4820, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 3}
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4825, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 10}
[6] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4820..4830 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.104 (10/96) top=extend_decision_final_green_out_of_bounds:5, extend_decision_extend_sec_exceeds_max_soft:5
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=4830, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4835, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 10}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4830..4840 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (6/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=4840, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4845, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4840..4850 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.103 (7/68) top=signal_step_parse_failed:7

[completion_log] step=4850, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4855, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4850..4860 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.044 (3/68) top=signal_step_parse_failed:3

[completion_log] step=4860, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4865, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4860..4870 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.048 (4/84) top=signal_step_phase_id_invalid:2, signal_step_parse_failed:2

[completion_log] step=4870, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4875, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4870..4880 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.020 (2/100) top=extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.083 (5/60) top=signal_step_parse_failed:5

[completion_log] step=4880, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4885, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4880..4890 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=4890, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4895, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4890..4900 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.024 (2/84) top=signal_step_parse_failed:2

[completion_log] step=4900, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4905, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4900..4910 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.057 (5/88) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=4910, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4915, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4910..4920 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=4920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4925, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4920..4930 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=4930, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4935, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4930..4940 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_phase_id_invalid:1

[completion_log] step=4940, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4945, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4940..4950 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=4950, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4955, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4950..4960 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (10/100) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=4960, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4965, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4960..4970 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.071 (4/56) top=signal_step_parse_failed:4

[completion_log] step=4970, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4975, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4970..4980 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=4980, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4985, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4980..4990 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=4990, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=4995, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 4990..5000 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.058 (6/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_phase_id_invalid:1, signal_step_parse_failed:1

[completion_log] step=5000, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5005, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5000..5010 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.090 (9/100) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=5010, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5015, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 5}
[10] (extend_decision):{'extend': '是', 'extend_sec': 4}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5010..5020 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=5020, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5025, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5020..5030 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=5030, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5035, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5030..5040 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.050 (3/60) top=signal_step_parse_failed:3

[completion_log] step=5040, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5045, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5040..5050 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=5050, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5055, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5050..5060 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.023 (2/88) top=signal_step_phase_id_invalid:1, signal_step_parse_failed:1

[completion_log] step=5060, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 3}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5065, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5060..5070 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=5070, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5075, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5070..5080 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=5080, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5085, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5080..5090 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/108) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=5090, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5095, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5090..5100 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (14/112) top=extend_decision_final_green_out_of_bounds:13, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=5100, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5105, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5100..5110 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=5110, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5115, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5110..5120 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.105 (8/76) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_parse_failed:1

[completion_log] step=5120, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5125, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5120..5130 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=5130, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5135, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5130..5140 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=5140, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5145, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5140..5150 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=5150, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5155, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5150..5160 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.046 (5/108) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=5160, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5165, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5160..5170 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5170, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5175, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5170..5180 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/116) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_parse_failed:1

[completion_log] step=5180, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 5}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 4}

[completion_log] step=5185, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5180..5190 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5190, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5195, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5190..5200 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=5200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5205, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5200..5210 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.074 (8/108) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.038 (2/52) top=signal_step_parse_failed:2

[completion_log] step=5210, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5215, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 60}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5210..5220 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.014 (1/72) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.023 (2/88) top=signal_step_parse_failed:2

[completion_log] step=5220, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5225, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5220..5230 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=5230, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5235, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5230..5240 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5240, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5245, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5240..5250 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=5250, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5255, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5250..5260 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=5260, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 3}
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5265, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5260..5270 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=5270, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5275, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5270..5280 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.067 (4/60) top=signal_step_parse_failed:4

[completion_log] step=5280, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5285, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5280..5290 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=5290, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5295, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5290..5300 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=5300, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5305, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5300..5310 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=5310, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5315, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5310..5320 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=5320, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5325, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5320..5330 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.059 (4/68) top=signal_step_parse_failed:4

[completion_log] step=5330, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5335, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5330..5340 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5340, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5345, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5340..5350 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=5350, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5355, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5350..5360 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.074 (8/108) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.038 (2/52) top=signal_step_parse_failed:2

[completion_log] step=5360, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5365, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5360..5370 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=5370, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5375, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5370..5380 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/72) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.023 (2/88) top=signal_step_parse_failed:2

[completion_log] step=5380, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5385, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5380..5390 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=5390, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5395, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5390..5400 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=5400, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5405, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5400..5410 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.011 (1/88) top=signal_step_parse_failed:1

[completion_log] step=5410, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5415, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[14] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5410..5420 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.057 (5/88) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.056 (4/72) top=signal_step_parse_failed:4

[completion_log] step=5420, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5425, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5420..5430 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (5/100) top=extend_decision_final_green_out_of_bounds:5
[reward_diag]  - signal_step: invalid_rate=0.083 (5/60) top=signal_step_parse_failed:5

[completion_log] step=5430, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5435, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5430..5440 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/64) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (3/96) top=signal_step_parse_failed:3

[completion_log] step=5440, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5445, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5440..5450 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (4/56) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (2/104) top=signal_step_parse_failed:1, signal_step_phase_id_invalid:1

[completion_log] step=5450, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5455, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5450..5460 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=5460, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5465, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5460..5470 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5470, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5475, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5470..5480 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.087 (7/80) top=signal_step_parse_failed:7

[completion_log] step=5480, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5485, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 60}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5480..5490 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.054 (5/92) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.118 (8/68) top=signal_step_parse_failed:8

[completion_log] step=5490, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5495, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5490..5500 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.067 (4/60) top=signal_step_parse_failed:3, signal_step_phase_id_invalid:1

[completion_log] step=5500, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5505, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5500..5510 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.066 (5/76) top=signal_step_parse_failed:4, signal_step_phase_id_invalid:1

[completion_log] step=5510, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5515, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5510..5520 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=5520, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5525, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5520..5530 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_phase_id_invalid:1

[completion_log] step=5530, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5535, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5530..5540 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=5540, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5545, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5540..5550 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=5550, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5555, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5550..5560 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=5560, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5565, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5560..5570 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:3, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.107 (6/56) top=signal_step_parse_failed:6

[completion_log] step=5570, num_completions=16
[7] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5575, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5570..5580 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5580, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5585, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5580..5590 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/112) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.083 (4/48) top=signal_step_parse_failed:4

[completion_log] step=5590, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5595, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5590..5600 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=5600, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5605, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5600..5610 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=5610, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5615, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5610..5620 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.059 (4/68) top=signal_step_parse_failed:4

[completion_log] step=5620, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 60}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 14}

[completion_log] step=5625, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5620..5630 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5630, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5635, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5630..5640 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=5640, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5645, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5640..5650 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.052 (5/96) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5650, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5655, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5650..5660 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.076 (7/92) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=5660, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5665, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5660..5670 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.021 (2/96) top=extend_decision_parse_failed:1, extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5670, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 3}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5675, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5670..5680 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.104 (10/96) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:3, extend_decision_extend_sec_nonzero_when_no_soft:3
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5680, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5685, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5680..5690 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.020 (2/100) top=extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.083 (5/60) top=signal_step_parse_failed:5

[completion_log] step=5690, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5695, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5690..5700 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=5700, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5705, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5700..5710 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=5710, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5715, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5710..5720 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5720, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5725, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5720..5730 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5730, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5735, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5730..5740 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.097 (7/72) top=signal_step_parse_failed:7

[completion_log] step=5740, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5745, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5740..5750 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=5750, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5755, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 3}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5750..5760 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.013 (1/80) top=signal_step_parse_failed:1

[completion_log] step=5760, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5765, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5760..5770 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.070 (7/100) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_phase_id_invalid:1

[completion_log] step=5770, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5775, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5770..5780 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (4/112) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=5780, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5785, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5780..5790 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=5790, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5795, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5790..5800 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=5800, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5805, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5800..5810 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=5810, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5815, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5810..5820 invalid_rate=0.106 (17/160)
[reward_diag]  - extend_decision: invalid_rate=0.159 (14/88) top=extend_decision_final_green_out_of_bounds:11, extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=5820, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5825, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5820..5830 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.091 (8/88) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=5830, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5835, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5830..5840 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.039 (3/76) top=extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.036 (3/84) top=signal_step_parse_failed:3

[completion_log] step=5840, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5845, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5840..5850 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5850, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5855, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5850..5860 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5860, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5865, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5860..5870 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.019 (2/104) top=extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=5870, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 13}
  [1] (signal_step): {"next_phase_id": 5, "green_sec": 16}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 20}

[completion_log] step=5875, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5870..5880 invalid_rate=0.094 (15/160)
[reward_diag]  - extend_decision: invalid_rate=0.118 (9/76) top=extend_decision_final_green_out_of_bounds:8, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.071 (6/84) top=signal_step_parse_failed:6

[completion_log] step=5880, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5885, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5880..5890 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=5890, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5895, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5890..5900 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=5900, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5905, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5900..5910 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/116) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/44) top=n/a

[completion_log] step=5910, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5915, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5910..5920 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=5920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5925, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5920..5930 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=5930, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 30}

[completion_log] step=5935, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5930..5940 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/68) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.065 (6/92) top=signal_step_parse_failed:5, signal_step_phase_id_invalid:1

[completion_log] step=5940, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5940..5950 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=5950, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5955, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5950..5960 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=5960, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5960..5970 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=5970, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5975, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5970..5980 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=5980, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5985, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5980..5990 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=5990, num_completions=16
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=5995, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 5990..6000 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.046 (5/108) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=6000, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6005, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6000..6010 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6010, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6015, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6010..6020 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=6020, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6025, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 3}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6020..6030 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=6030, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6035, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6030..6040 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6040, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6045, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6040..6050 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:7, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=6050, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[15] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6055, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6050..6060 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.046 (5/108) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.058 (3/52) top=signal_step_parse_failed:3

[completion_log] step=6060, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6065, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6060..6070 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=6070, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6075, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6070..6080 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.065 (6/92) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=6080, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 3}
[3] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6085, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 3}
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6080..6090 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.062 (4/64) top=signal_step_parse_failed:4

[completion_log] step=6090, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6095, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6090..6100 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/112) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=6100, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6105, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6100..6110 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=6110, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6115, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6110..6120 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.013 (1/80) top=signal_step_parse_failed:1

[completion_log] step=6120, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6125, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6120..6130 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_green_out_of_range:1

[completion_log] step=6130, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6135, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6130..6140 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=6140, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6145, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6140..6150 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.043 (4/92) top=signal_step_parse_failed:4

[completion_log] step=6150, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6155, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6150..6160 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=6160, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6165, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6160..6170 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=6170, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6175, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6170..6180 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.022 (2/92) top=extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=6180, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6185, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6180..6190 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=6190, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6195, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6190..6200 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=6200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6205, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6200..6210 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=6210, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6215, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6210..6220 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=6220, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6225, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 7}
[9] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6220..6230 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=6230, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6235, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[13] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6230..6240 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=6240, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6245, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 3}
[9] (extend_decision):{'extend': '是', 'extend_sec': 3}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6240..6250 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=6250, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6255, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 3}
[2] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6250..6260 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=6260, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[2] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6265, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 6}
[10] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6260..6270 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.107 (12/112) top=extend_decision_final_green_out_of_bounds:10, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.021 (1/48) top=signal_step_phase_id_invalid:1

[completion_log] step=6270, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6275, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 3}
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6270..6280 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (7/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:3
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=6280, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6285, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6280..6290 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.141 (9/64) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.010 (1/96) top=signal_step_parse_failed:1

[completion_log] step=6290, num_completions=16
[2] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6295, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6290..6300 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=6300, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6305, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6300..6310 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=6310, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6315, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6310..6320 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_extend_when_at_max_green:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=6320, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6325, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6320..6330 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.058 (3/52) top=signal_step_parse_failed:3

[completion_log] step=6330, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 60}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6335, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6330..6340 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=6340, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6345, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6340..6350 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=6350, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6355, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6350..6360 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=6360, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6365, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6360..6370 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=6370, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6375, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6370..6380 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=6380, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6385, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6380..6390 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (7/88) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=6390, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 15}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 10}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 20}

[completion_log] step=6395, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6390..6400 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.068 (6/88) top=extend_decision_parse_failed:6
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=6400, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6405, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6400..6410 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=6410, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6415, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 60}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 14}
[reward_diag] steps 6410..6420 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=6420, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 60}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6425, num_completions=16
[8] (extend_decision):{'extend': '是', 'extend_sec': 3}
[10] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6420..6430 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.070 (9/128) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/32) top=n/a

[completion_log] step=6430, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6435, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6430..6440 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/108) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=6440, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6445, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6440..6450 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.057 (5/88) top=signal_step_parse_failed:5

[completion_log] step=6450, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6455, num_completions=16
[3] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6450..6460 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.034 (3/88) top=extend_decision_final_green_out_of_bounds:2, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=6460, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 3}
[12] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6465, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6460..6470 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=6470, num_completions=16
[11] (extend_decision):{'extend': '是', 'extend_sec': 7}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6475, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6470..6480 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.062 (4/64) top=signal_step_parse_failed:4

[completion_log] step=6480, num_completions=16
[6] (extend_decision):{'extend': '是', 'extend_sec': 3}
[15] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6485, num_completions=16
[5] (extend_decision):{'extend': '是', 'extend_sec': 7}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6480..6490 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.091 (8/88) top=extend_decision_parse_failed:3, extend_decision_extend_sec_exceeds_max_soft:3, extend_decision_final_green_out_of_bounds:2
[reward_diag]  - signal_step: invalid_rate=0.056 (4/72) top=signal_step_parse_failed:4

[completion_log] step=6490, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6495, num_completions=16
[0] (extend_decision):{'extend': '是', 'extend_sec': 7}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6490..6500 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (5/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=6500, num_completions=16
[4] (extend_decision):{'extend': '是', 'extend_sec': 7}
[9] (extend_decision):{'extend': '是', 'extend_sec': 3}
[5] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6505, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6500..6510 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=6510, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6515, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6510..6520 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.056 (4/72) top=signal_step_parse_failed:4

[completion_log] step=6520, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 3}
[8] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6525, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6520..6530 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.058 (6/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_exceeds_max_soft:2
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=6530, num_completions=16
[1] (extend_decision):{'extend': '是', 'extend_sec': 7}
[9] (extend_decision):{'extend': '是', 'extend_sec': 3}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6535, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6530..6540 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=6540, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6545, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6540..6550 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6550, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6555, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6550..6560 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.017 (2/116) top=extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_parse_failed:1

[completion_log] step=6560, num_completions=16
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6565, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6560..6570 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=6570, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6575, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6570..6580 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.060 (5/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=6580, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6585, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6580..6590 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6590, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6595, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6590..6600 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.091 (8/88) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:3, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=6600, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6605, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6600..6610 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=6610, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6615, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6610..6620 invalid_rate=0.100 (16/160)
[reward_diag]  - extend_decision: invalid_rate=0.163 (13/80) top=extend_decision_final_green_out_of_bounds:12, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.037 (3/80) top=signal_step_parse_failed:3

[completion_log] step=6620, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6625, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6620..6630 invalid_rate=0.087 (14/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (8/112) top=extend_decision_parse_failed:8
[reward_diag]  - signal_step: invalid_rate=0.125 (6/48) top=signal_step_parse_failed:6

[completion_log] step=6630, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6635, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6630..6640 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/104) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=6640, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6645, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6640..6650 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=6650, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6655, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6650..6660 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=6660, num_completions=16
  [0] (signal_step): {"next_phase_id": 5, "green_sec": 6}
  [1] (signal_step): {"next_phase_id": 9, "green_sec": 20}
  [2] (signal_step): {"next_phase_id": 5, "green_sec": 10}

[completion_log] step=6665, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6660..6670 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6670, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6675, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 10}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 5}
[reward_diag] steps 6670..6680 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.078 (5/64) top=extend_decision_final_green_out_of_bounds:3, extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/96) top=n/a

[completion_log] step=6680, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6685, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6680..6690 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6690, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6695, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6690..6700 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.078 (9/116) top=extend_decision_parse_failed:8, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.091 (4/44) top=signal_step_parse_failed:4

[completion_log] step=6700, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6705, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6700..6710 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=6710, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6715, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6710..6720 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (7/84) top=extend_decision_final_green_out_of_bounds:5, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.039 (3/76) top=signal_step_parse_failed:3

[completion_log] step=6720, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6725, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6720..6730 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=6730, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6735, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6730..6740 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (8/112) top=extend_decision_final_green_out_of_bounds:7, extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.062 (3/48) top=signal_step_parse_failed:3

[completion_log] step=6740, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6745, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6740..6750 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.020 (2/100) top=extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=6750, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6755, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6750..6760 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=6760, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6765, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6760..6770 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_parse_failed:2, extend_decision_extend_sec_nonzero_when_no_soft:1, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=6770, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6775, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6770..6780 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=6780, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6785, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 25}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 10}
  [2] (signal_step): {"next_phase_id": 6, "green_sec": 20}
[reward_diag] steps 6780..6790 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=6790, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6795, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6790..6800 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=6800, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6805, num_completions=16
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6800..6810 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.029 (3/104) top=extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=6810, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6815, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6810..6820 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.100 (6/60) top=signal_step_parse_failed:6

[completion_log] step=6820, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6825, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6820..6830 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.009 (1/108) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.096 (5/52) top=signal_step_parse_failed:5

[completion_log] step=6830, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6835, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6830..6840 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.050 (3/60) top=signal_step_parse_failed:3

[completion_log] step=6840, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6845, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6840..6850 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.053 (4/76) top=signal_step_parse_failed:4

[completion_log] step=6850, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6855, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6850..6860 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.067 (4/60) top=signal_step_parse_failed:4

[completion_log] step=6860, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6865, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6860..6870 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.024 (2/84) top=extend_decision_extend_sec_exceeds_max_soft:1, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=6870, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6875, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 16}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 16}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 10}
[reward_diag] steps 6870..6880 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/60) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.020 (2/100) top=signal_step_parse_failed:2

[completion_log] step=6880, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6885, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6880..6890 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=6890, num_completions=16
[14] (extend_decision):{'extend': '是', 'extend_sec': 8}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6895, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6890..6900 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=6900, num_completions=16
[15] (extend_decision):{'extend': '是', 'extend_sec': 6}
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6905, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6900..6910 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (4/100) top=extend_decision_parse_failed:3, extend_decision_final_green_out_of_bounds:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=6910, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6915, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6910..6920 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.077 (8/104) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=6920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6925, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6920..6930 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=6930, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6935, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6930..6940 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.013 (1/76) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=6940, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6940..6950 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (4/64) top=extend_decision_parse_failed:4
[reward_diag]  - signal_step: invalid_rate=0.062 (6/96) top=signal_step_parse_failed:6

[completion_log] step=6950, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6955, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6950..6960 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.059 (4/68) top=signal_step_parse_failed:4

[completion_log] step=6960, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6960..6970 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=6970, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6975, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 5}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6970..6980 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.024 (2/84) top=signal_step_phase_id_invalid:1, signal_step_parse_failed:1

[completion_log] step=6980, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6985, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6980..6990 invalid_rate=0.069 (11/160)
[reward_diag]  - extend_decision: invalid_rate=0.081 (10/124) top=extend_decision_final_green_out_of_bounds:8, extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.028 (1/36) top=signal_step_parse_failed:1

[completion_log] step=6990, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=6995, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 6990..7000 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.029 (3/104) top=extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=7000, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7005, num_completions=16
[1] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7000..7010 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_parse_failed:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=7010, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7015, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7010..7020 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=7020, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7025, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7020..7030 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=7030, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7035, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7030..7040 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=7040, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7045, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7040..7050 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_green_out_of_range:1

[completion_log] step=7050, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7055, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7050..7060 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.040 (5/124) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/36) top=n/a

[completion_log] step=7060, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7065, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7060..7070 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.013 (1/80) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=7070, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7075, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7070..7080 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:7, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=7080, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7085, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7080..7090 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.091 (8/88) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=7090, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7095, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7090..7100 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=7100, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7105, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7100..7110 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.052 (5/96) top=extend_decision_final_green_out_of_bounds:3, extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=7110, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7115, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7110..7120 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_final_green_out_of_bounds:7, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=7120, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7125, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7120..7130 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=7130, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7135, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7130..7140 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.019 (2/108) top=extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=7140, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7145, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7140..7150 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=7150, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7155, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7150..7160 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (5/104) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.089 (5/56) top=signal_step_parse_failed:5

[completion_log] step=7160, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7165, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7160..7170 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=7170, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7175, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7170..7180 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.069 (5/72) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.011 (1/88) top=signal_step_parse_failed:1

[completion_log] step=7180, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7185, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7180..7190 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=7190, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7195, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7190..7200 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=7200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7205, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7200..7210 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=7210, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7215, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7210..7220 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.014 (1/72) top=extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.023 (2/88) top=signal_step_parse_failed:2

[completion_log] step=7220, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7225, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7220..7230 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=7230, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7235, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7230..7240 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=7240, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7245, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7240..7250 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=7250, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7255, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7250..7260 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=7260, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7265, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7260..7270 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/52) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.046 (5/108) top=signal_step_parse_failed:5

[completion_log] step=7270, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7275, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7270..7280 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.023 (2/88) top=signal_step_parse_failed:2

[completion_log] step=7280, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7285, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7280..7290 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.107 (12/112) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.021 (1/48) top=signal_step_parse_failed:1

[completion_log] step=7290, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7295, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7290..7300 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=7300, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7305, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7300..7310 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=7310, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7315, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7310..7320 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=7320, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7325, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7320..7330 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.098 (9/92) top=extend_decision_final_green_out_of_bounds:8, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.044 (3/68) top=signal_step_parse_failed:3

[completion_log] step=7330, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7335, num_completions=16
  [0] (signal_step): {"next_phase_id": 5, "green_sec": 30}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 60}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 3}
[reward_diag] steps 7330..7340 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.103 (7/68) top=signal_step_parse_failed:7

[completion_log] step=7340, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7345, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7340..7350 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=7350, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7355, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7350..7360 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/88) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=7360, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7365, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7360..7370 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=7370, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7375, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7370..7380 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=7380, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7385, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7380..7390 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.009 (1/116) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_parse_failed:1

[completion_log] step=7390, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7395, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7390..7400 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_phase_id_invalid:1

[completion_log] step=7400, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7405, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7400..7410 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/80) top=signal_step_parse_failed:1

[completion_log] step=7410, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7415, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7410..7420 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=7420, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7425, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7420..7430 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=7430, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7435, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7430..7440 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.071 (6/84) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:2
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=7440, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7445, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7440..7450 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=7450, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7455, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7450..7460 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/76) top=n/a

[completion_log] step=7460, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7465, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7460..7470 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.011 (1/88) top=signal_step_parse_failed:1

[completion_log] step=7470, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7475, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7470..7480 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.031 (3/96) top=extend_decision_parse_failed:3
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=7480, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7485, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7480..7490 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=7490, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7495, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7490..7500 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/100) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=7500, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7505, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7500..7510 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.010 (1/96) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=7510, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7515, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7510..7520 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=7520, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7525, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7520..7530 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/80) top=n/a

[completion_log] step=7530, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7535, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7530..7540 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.012 (1/84) top=signal_step_parse_failed:1

[completion_log] step=7540, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7545, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7540..7550 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/68) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=7550, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7555, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7550..7560 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.014 (1/72) top=signal_step_parse_failed:1

[completion_log] step=7560, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7565, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7560..7570 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=7570, num_completions=16
[12] (extend_decision):{'extend': '是', 'extend_sec': 7}
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7575, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7570..7580 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=7580, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7585, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7580..7590 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.107 (12/112) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.021 (1/48) top=signal_step_parse_failed:1

[completion_log] step=7590, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7595, num_completions=16
[10] (extend_decision):{'extend': '是', 'extend_sec': 60}
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7590..7600 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.069 (8/116) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:3, extend_decision_extend_when_at_max_green:1
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_phase_id_invalid:1

[completion_log] step=7600, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7605, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7600..7610 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.056 (4/72) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.011 (1/88) top=signal_step_parse_failed:1

[completion_log] step=7610, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7615, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7610..7620 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=7620, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7625, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7620..7630 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.077 (8/104) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.036 (2/56) top=signal_step_parse_failed:2

[completion_log] step=7630, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7635, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7630..7640 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_green_out_of_range:1

[completion_log] step=7640, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7645, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7640..7650 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (5/112) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=7650, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7655, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7650..7660 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=7660, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7665, num_completions=16
[9] (extend_decision):{'extend': '是', 'extend_sec': 3}
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7660..7670 invalid_rate=0.081 (13/160)
[reward_diag]  - extend_decision: invalid_rate=0.120 (12/100) top=extend_decision_final_green_out_of_bounds:12
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=7670, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7675, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7670..7680 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=7680, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7685, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7680..7690 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=7690, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7695, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7690..7700 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/64) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.010 (1/96) top=signal_step_parse_failed:1

[completion_log] step=7700, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7705, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7700..7710 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (5/112) top=extend_decision_final_green_out_of_bounds:4, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/48) top=n/a

[completion_log] step=7710, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7715, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7710..7720 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=7720, num_completions=16
  [0] (signal_step): {"next_phase_id": 6, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 30}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 20}

[completion_log] step=7725, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7720..7730 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.053 (4/76) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/84) top=n/a

[completion_log] step=7730, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7735, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7730..7740 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=7740, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7745, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7740..7750 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=7750, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7755, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7750..7760 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.087 (8/92) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=7760, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7765, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7760..7770 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/124) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.056 (2/36) top=signal_step_phase_id_invalid:1, signal_step_green_out_of_range:1

[completion_log] step=7770, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7775, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7770..7780 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=7780, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7785, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7780..7790 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=7790, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7795, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7790..7800 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/116) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.091 (4/44) top=signal_step_parse_failed:4

[completion_log] step=7800, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7805, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7800..7810 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.098 (9/92) top=extend_decision_final_green_out_of_bounds:8, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=7810, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7815, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 5}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 13}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 20}
[reward_diag] steps 7810..7820 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.048 (4/84) top=signal_step_parse_failed:3, signal_step_phase_id_invalid:1

[completion_log] step=7820, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7825, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7820..7830 invalid_rate=0.100 (16/160)
[reward_diag]  - extend_decision: invalid_rate=0.105 (8/76) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.095 (8/84) top=signal_step_parse_failed:8

[completion_log] step=7830, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7835, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7830..7840 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.036 (4/112) top=extend_decision_final_green_out_of_bounds:3, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.062 (3/48) top=signal_step_parse_failed:3

[completion_log] step=7840, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7845, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7840..7850 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.016 (1/64) top=signal_step_parse_failed:1

[completion_log] step=7850, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7855, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7850..7860 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/60) top=n/a

[completion_log] step=7860, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7865, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7860..7870 invalid_rate=0.100 (16/160)
[reward_diag]  - extend_decision: invalid_rate=0.125 (14/112) top=extend_decision_final_green_out_of_bounds:12, extend_decision_parse_failed:1, extend_decision_extend_sec_exceeds_max_soft:1
[reward_diag]  - signal_step: invalid_rate=0.042 (2/48) top=signal_step_parse_failed:2

[completion_log] step=7870, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7875, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7870..7880 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/68) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.033 (3/92) top=signal_step_parse_failed:2, signal_step_phase_id_invalid:1

[completion_log] step=7880, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 0.5}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 2}
  [2] (signal_step): {"next_phase_id": 3, "green_sec": 15}

[completion_log] step=7885, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7880..7890 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.044 (3/68) top=signal_step_parse_failed:3

[completion_log] step=7890, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7895, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7890..7900 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.013 (1/76) top=signal_step_parse_failed:1

[completion_log] step=7900, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7905, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7900..7910 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.080 (8/100) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.017 (1/60) top=signal_step_parse_failed:1

[completion_log] step=7910, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7915, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7910..7920 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=7920, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7925, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7920..7930 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.024 (2/84) top=signal_step_parse_failed:2

[completion_log] step=7930, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7935, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7930..7940 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=7940, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7945, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7940..7950 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.050 (4/80) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=7950, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7955, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7950..7960 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.042 (3/72) top=signal_step_parse_failed:3

[completion_log] step=7960, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7965, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7960..7970 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/84) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.053 (4/76) top=signal_step_parse_failed:4

[completion_log] step=7970, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7975, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7970..7980 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.048 (4/84) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=7980, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7985, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7980..7990 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=7990, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=7995, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 7990..8000 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/68) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/92) top=n/a

[completion_log] step=8000, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8005, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8000..8010 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=8010, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8015, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8010..8020 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.011 (1/92) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=8020, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8025, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8020..8030 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.029 (2/68) top=signal_step_parse_failed:2

[completion_log] step=8030, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8035, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8030..8040 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.018 (1/56) top=signal_step_parse_failed:1

[completion_log] step=8040, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8045, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8040..8050 invalid_rate=0.044 (7/160)
[reward_diag]  - extend_decision: invalid_rate=0.059 (4/68) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.033 (3/92) top=signal_step_parse_failed:3

[completion_log] step=8050, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8055, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8050..8060 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=8060, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8065, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8060..8070 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.012 (1/84) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.026 (2/76) top=signal_step_parse_failed:2

[completion_log] step=8070, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8075, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8070..8080 invalid_rate=0.075 (12/160)
[reward_diag]  - extend_decision: invalid_rate=0.089 (10/112) top=extend_decision_final_green_out_of_bounds:8, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.042 (2/48) top=signal_step_parse_failed:2

[completion_log] step=8080, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8085, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8080..8090 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.043 (4/92) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=8090, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8095, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8090..8100 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/108) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.019 (1/52) top=signal_step_parse_failed:1

[completion_log] step=8100, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8105, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8100..8110 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.023 (2/88) top=extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=8110, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8115, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8110..8120 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.057 (5/88) top=extend_decision_final_green_out_of_bounds:3, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=8120, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8125, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8120..8130 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=8130, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8135, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8130..8140 invalid_rate=0.031 (5/160)
[reward_diag]  - extend_decision: invalid_rate=0.069 (5/72) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:1
[reward_diag]  - signal_step: invalid_rate=0.000 (0/88) top=n/a

[completion_log] step=8140, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8145, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8140..8150 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.068 (6/88) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.000 (0/72) top=n/a

[completion_log] step=8150, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8155, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8150..8160 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/68) top=n/a

[completion_log] step=8160, num_completions=16
  [0] (signal_step): {"next_phase_id": 9, "green_sec": 15}
  [1] (signal_step): {"next_phase_id": 7, "green_sec": 6}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 14}

[completion_log] step=8165, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8160..8170 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=8170, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8175, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8170..8180 invalid_rate=0.050 (8/160)
[reward_diag]  - extend_decision: invalid_rate=0.067 (8/120) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.000 (0/40) top=n/a

[completion_log] step=8180, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8185, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8180..8190 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.036 (3/84) top=signal_step_parse_failed:3

[completion_log] step=8190, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8195, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8190..8200 invalid_rate=0.037 (6/160)
[reward_diag]  - extend_decision: invalid_rate=0.014 (1/72) top=extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.057 (5/88) top=signal_step_parse_failed:5

[completion_log] step=8200, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8205, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8200..8210 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/88) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.028 (2/72) top=signal_step_parse_failed:2

[completion_log] step=8210, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 3}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 5}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 10.5}

[completion_log] step=8215, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8210..8220 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.045 (4/88) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.069 (5/72) top=signal_step_parse_failed:5

[completion_log] step=8220, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8225, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8220..8230 invalid_rate=0.019 (3/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/116) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.068 (3/44) top=signal_step_parse_failed:3

[completion_log] step=8230, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8235, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8230..8240 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.038 (4/104) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=8240, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8245, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8240..8250 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.078 (9/116) top=extend_decision_final_green_out_of_bounds:8, extend_decision_parse_failed:1
[reward_diag]  - signal_step: invalid_rate=0.023 (1/44) top=signal_step_parse_failed:1

[completion_log] step=8250, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8255, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8250..8260 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=8260, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8265, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8260..8270 invalid_rate=0.056 (9/160)
[reward_diag]  - extend_decision: invalid_rate=0.062 (6/96) top=extend_decision_final_green_out_of_bounds:4, extend_decision_extend_sec_nonzero_when_no_soft:2
[reward_diag]  - signal_step: invalid_rate=0.047 (3/64) top=signal_step_parse_failed:3

[completion_log] step=8270, num_completions=16
  [0] (signal_step): {"next_phase_id": 7, "green_sec": 2.5}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 5}
  [2] (signal_step): {"next_phase_id": 7, "green_sec": 10}

[completion_log] step=8275, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8270..8280 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.100 (8/80) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=8280, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8285, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8280..8290 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.042 (4/96) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/64) top=n/a

[completion_log] step=8290, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8295, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 10}
  [1] (signal_step): {"next_phase_id": 3, "green_sec": 13}
  [2] (signal_step): {"next_phase_id": 9, "green_sec": 60}
[reward_diag] steps 8290..8300 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/64) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.010 (1/96) top=signal_step_parse_failed:1

[completion_log] step=8300, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8305, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8300..8310 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.013 (1/80) top=signal_step_parse_failed:1

[completion_log] step=8310, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8315, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8310..8320 invalid_rate=0.062 (10/160)
[reward_diag]  - extend_decision: invalid_rate=0.083 (8/96) top=extend_decision_final_green_out_of_bounds:8
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=8320, num_completions=16
[12] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8325, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8320..8330 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/76) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.048 (4/84) top=signal_step_parse_failed:3, signal_step_phase_id_invalid:1

[completion_log] step=8330, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8335, num_completions=16
[8] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8330..8340 invalid_rate=0.006 (1/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/92) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.015 (1/68) top=signal_step_parse_failed:1

[completion_log] step=8340, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8345, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8340..8350 invalid_rate=0.000 (0/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/104) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.000 (0/56) top=n/a

[completion_log] step=8350, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8355, num_completions=16
  [0] (signal_step): {"next_phase_id": 3, "green_sec": 20}
  [1] (signal_step): {"next_phase_id": 6, "green_sec": 60}
  [2] (signal_step): {"next_phase_id": 1, "green_sec": 13}
[reward_diag] steps 8350..8360 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/96) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.031 (2/64) top=signal_step_parse_failed:2

[completion_log] step=8360, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8365, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8360..8370 invalid_rate=0.025 (4/160)
[reward_diag]  - extend_decision: invalid_rate=0.037 (4/108) top=extend_decision_final_green_out_of_bounds:4
[reward_diag]  - signal_step: invalid_rate=0.000 (0/52) top=n/a

[completion_log] step=8370, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8375, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8370..8380 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/100) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.033 (2/60) top=signal_step_parse_failed:2

[completion_log] step=8380, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8385, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}
[reward_diag] steps 8380..8390 invalid_rate=0.013 (2/160)
[reward_diag]  - extend_decision: invalid_rate=0.000 (0/80) top=n/a
[reward_diag]  - signal_step: invalid_rate=0.025 (2/80) top=signal_step_parse_failed:2

[completion_log] step=8390, num_completions=16
[4] (extend_decision):{'extend': '否', 'extend_sec': 0}

[completion_log] step=8395, num_completions=16
[0] (extend_decision):{'extend': '否', 'extend_sec': 0}

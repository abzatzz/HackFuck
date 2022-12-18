

order_volume = 1000
fee_binance = 0.04 / 100
bar_volume_boost = 0.4
minute_bars_to_analize = 23  # amount of minute bars we need to calculate average volume

fractal_periods = 15
high_limit_m = 1.002
low_limit_m = 0.997
high_limit_1h = 1.008
low_limit_1h = 0.98
high_limit_4h = 1.016
low_limit_4h = 0.96

stop_loss_level = 0.4

request_pause = 0.25


fractal_periods_5m = list(range(15,31)) # 18,22,25,26,27,28,29,30
fractal_periods_15m = list(range(15,31))
fractal_periods_30m = list(range(12,26))
fractal_periods_45m = list(range(12,26))
fractal_periods_1h = list(range(10,21))
fractal_periods_2h = list(range(10,21))
fractal_periods_3h = list(range(8,16))
fractal_periods_4h = list(range(8,16))

time_frame_list = ['5m', '15m', '30m', '1h', '2h', '4h']
takes_level_list = ['timeFrame','SL','1T','2T','3T','4T','5T','AVG']
corridor = ['max','min']
intervals_5m = [0.5, 1, 1.5, 2, 3]
intervals_15m = [0.5, 1, 1.5, 2, 3]
intervals_30m = [0.7, 1.5, 2.3, 3, 4.5]
intervals_45m = [0.7, 1.5, 2.3, 3, 4.5]
intervals_1h = [1, 2, 3.5, 5, 7]
intervals_2h = [1, 2, 3.5, 5, 7]
intervals_3h = [2, 5, 8, 10, 13]
intervals_4h = [2, 5, 8, 10, 13]
m5_up_limit_list = [1.002]
m5_down_limit_list = [0.997]
m15_up_limit_list = [1.002,1.003,1.004]
m15_down_limit_list = [0.997,0.996,0.995,0.994]
m30_up_limit_list = [1.003,1.004,1.005]
m30_down_limit_list = [0.996]
m45_up_limit_list = [1.003]
m45_down_limit_list = [0.996,0.995,0.994,0.993]
h1_up_limit_list = [1.004,1.005,1.006, 1.007, 1.008]
h1_down_limit_list = [0.990, 0.989, 0.988, 0.987,0.986,0.985,0.984]
h2_up_limit_list = [1.006, 1.007, 1.008]
h2_down_limit_list = [0.980, 0.981, 0.982, 0.983, 0.984]
h3_up_limit_list = [1.012, 1.013, 1.014, 1.015, 1.016]
h3_down_limit_list = [0.960, 0.961, 0.962, 0.963, 0.964, 0.965, 0.966, 0.967, 0.968, 0.969, 0.970, 0.971, 0.972, 0.973, 0.974, 0.975]
h4_up_limit_list = [1.012, 1.013, 1.014, 1.015, 1.016]
h4_down_limit_list = [0.960, 0.961, 0.962, 0.963, 0.964, 0.965, 0.966, 0.967, 0.968, 0.969, 0.970]
min_volume = float(10000000)
amount_rows = 100

columns_list = ['Ticker','TimeFrame', 'FractPeriod', 'CorrMax(%)','CorrMin(%)','AVG','Trend','EarnedUSDT','Earned(%)','Situation','EnterPrice',
                'TimeEnter','1stLvlPrice','Time1stLvl','2ndLvlPrice','Time2ndLvl','3rdLvlPrice','Time3rdLvl',
                'OtskokBtw1_2Lvl','OtskokBtw2_3Lvl','OtskokBtw3_LastLvl','BarsBtw1_2Lvl','BarsBtw2_3Lvl','BarsBtw2_EnterLvl',
                'AvgEnterLvl','LvlConfig','VolBarEnterLvl','VolBarEnterLvl(-1)', 'VolBarEnterLvl(-2)', 'VolBarEnterLvl(-3)',
                 'VolBar1stLvl','VolBar1stLvl(-1)','VolBar1stLvl(-2)', 'VolBar1stLvl(-3)','IsVol1stLvlBoost',
                'VolBar2ndLvl','VolBar2ndLvl(-1)','VolBar2ndLvl(-2)', 'VolBar2ndLvl(-3)', 'IsVol2ndLvlBoost',
                'VolBar3rdLvl','VolBar3rdLvl(-1)','VolBar3rdLvl(-2)', 'VolBar3rdLvl(-3)', 'IsVol3rdLvlBoost' ]

fractal_5m = 25

high_limit_long_5m = 1.002
low_limit_long_5m = 0.997
high_limit_short_5m = 0.998
low_limit_short_5m = 1.003






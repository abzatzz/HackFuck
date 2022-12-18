from binance.um_futures import UMFutures
import keys
import pandas as pd
import time
import telebot
import creds

base_level_up = float()
max_level_up = float()
count_up = int()
first_level_high = int()
second_level_high = int()
third_level_high = int()
first_level_low = int()
second_level_low = int()
third_level_low = int()
base_level_down = float()
max_level_down = float()
count_down = int()
last_max_high = float()

# Constants
open_time = 0
open_kline = 1
high = 2
low = 3
close_kline = 4
volume = 5
close_time = 6
index_kline = 12

# Variables
is_high_fractal = True
is_low_fractal = True
up_fractals = []
down_fractals = []
data_to_write = []

bot = telebot.TeleBot(keys.telegram_api_key)
client = UMFutures(keys.api_key_real, keys.secret_key_real)
cl = UMFutures(key=keys.api_key_real, secret=keys.secret_key_real)
# Iterating
count_global = 0
count_timeframe = 0
count_ticker = 1
count_global_circle = 1



while True:
    try:
        count_timeframe = 1
        for time_frame in creds.time_frame_list:
            # Getting all tickers rated for last 24 hours
            if time_frame == '5m' or time_frame == '15m':
                high_limit_high = creds.high_limit_m
                low_limit_high = creds.low_limit_m
                high_limit_low = 1- (creds.high_limit_m - 1)
                low_limit_low = 1 - (creds.low_limit_m - 1)
            elif time_frame == '1h':
                high_limit_high = creds.high_limit_1h
                low_limit_high = creds.low_limit_1h
                high_limit_low = 1 - (creds.high_limit_1h - 1)
                low_limit_low = 1 - (creds.low_limit_1h - 1)
            elif time_frame == '4h':
                high_limit_high = creds.high_limit_4h
                low_limit_high = creds.low_limit_4h
                high_limit_low = 1 - (creds.high_limit_4h - 1)
                low_limit_low = 1 - (creds.low_limit_4h - 1)
            all_tickers = client.ticker_24hr_price_change()
            count_ticker = 1
            for el_tickers in all_tickers:
                current_voluve = float(el_tickers['lastPrice']) * float(el_tickers['volume'])
                if current_voluve > creds.min_volume and str(el_tickers['symbol']).endswith('USDT') \
                        and str(el_tickers['symbol']) != 'DEFIUSDT' \
                        and str(el_tickers['symbol']) != 'BLUEBIRDUSDT' \
                        and str(el_tickers['symbol']) != 'BTCDOMUSDT' \
                        and str(el_tickers['symbol']) != 'RAYUSDT' \
                        and str(el_tickers['symbol']) != 'SRMUSDT' \
                        and str(el_tickers['symbol']) != 'FOOTBALLUSDT' \
                        and str(el_tickers['symbol']) != 'FTTUSDT':
                    symbol_to_work = el_tickers['symbol']

                    print(count_global_circle, '/', count_timeframe, '/', count_ticker, '   ', symbol_to_work, time_frame)

                    mas = cl.klines(symbol_to_work, time_frame)
                    # Detecting fractal for highs
                    counter_mas = creds.fractal_periods
                    while counter_mas < len(mas)-creds.fractal_periods:
                        counter = 1
                        is_high_fractal = True
                        while counter < creds.fractal_periods:
                            if is_high_fractal \
                                and mas[counter_mas - counter][high] <= mas[counter_mas][high] \
                                and mas[counter_mas + counter][high] < mas[counter_mas][high]:
                                is_high_fractal = True
                            else: is_high_fractal = False
                            counter += 1
                        if is_high_fractal:
                            normal_time_high = pd.to_datetime(mas[counter_mas][open_time], unit='ms')
                            up_fractals.append(mas[counter_mas] + [counter_mas])
                            # print(counter_mas, normal_time_high, float(mas[counter_mas][high]), 'high')
                        counter_mas += 1
                    # Detected if this high is the fractal

                    # Comparising fractals and finding open levels with series of 3 fractals within limits
                    max_last_up = 0
                    max_last_down = 0
                    len_last = len(mas)-creds.fractal_periods
                    for last_up in mas[len_last:len(mas)][high]:
                        if max_last_up > float(last_up):
                            max_last_up = float(last_up)
                    for last_down in mas[len_last:len(mas)][low]:
                        if max_last_down < float(last_down):
                            max_last_down = float(last_down)

                    l_up = len(up_fractals)
                    for i_up in range(l_up):
                        count_up = 0
                        for el_up in up_fractals[i_up:l_up]:
                            if count_up == 0:
                                count_up = 1
                                base_level_up = float(el_up[high])
                                first_level_high = float(el_up[high])
                                max_level_up = float(el_up[high])
                                max_level_up_time = str(pd.to_datetime(el_up[open_time], unit='ms'))
                                f_high_1 = str(pd.to_datetime(el_up[open_time], unit='ms'))
                                # print(symbol_to_work, time_frame, 'LONG','Ind ', el_up[index_kline], 'Pos in series ', count_up,
                                #       '***', pd.to_datetime(el_up[open_time], unit='ms'), 'Cur- ',
                                #       float(el_up[high]), 'Max-','(', max_level_up, ')')
                            else:
                                if float(el_up[high]) <= base_level_up * high_limit_high \
                                        and float(el_up[high]) >= base_level_up * low_limit_high:
                                    count_up += 1
                                    if float(el_up[high]) > max_level_up:
                                        max_level_up = float(el_up[high])
                                    if count_up == 2:
                                        second_level_high = float(el_up[high])
                                        f_high_2 = str(pd.to_datetime(el_up[open_time], unit='ms'))
                                    # print(symbol_to_work, time_frame, 'LONG', 'Ind ', el_up[index_kline], 'Pos in series ', count_up,
                                    #       '----', pd.to_datetime(el_up[open_time], unit='ms'), 'Cur- ',
                                    #       float(el_up[high]), 'Max-', '(', max_level_up, ')')
                                    if count_up >= 3 and ((first_level_high > second_level_high and second_level_high < third_level_high) \
                                        or (first_level_high < second_level_high and second_level_high > third_level_high) \
                                        or (first_level_high == second_level_high and second_level_high > third_level_high) \
                                        or (first_level_high == second_level_high and second_level_high == third_level_high) \
                                        or (first_level_high < second_level_high and second_level_high == third_level_high)):
                                        third_level_high = float(el_up[high])
                                        f_high_3 = str(pd.to_datetime(el_up[open_time], unit='ms'))
                                        print(symbol_to_work, time_frame,'LONG', 'Ind ', el_up[index_kline], 'Pos in series ', count_up,
                                              '>>>>>>>>', pd.to_datetime(el_up[open_time], unit='ms'), 'Cur- ',
                                              float(el_up[high]), 'Max-', '(', max_level_up, ')')

                                elif float(el_up[high]) > base_level_up * high_limit_high:
                                    count_up = 0
                                    first_level_high = 0
                                    second_level_high = 0
                                    third_level_high = 0
                                    break
                        if count_up >= 3 and max_level_up > max_last_up \
                            and ((first_level_high > second_level_high and second_level_high < third_level_high) \
                            or (first_level_high < second_level_high and second_level_high > third_level_high) \
                            or (first_level_high == second_level_high and second_level_high > third_level_high) \
                            or (first_level_high == second_level_high and second_level_high == third_level_high) \
                            or (first_level_high < second_level_high and second_level_high == third_level_high)):
                            data_to_write = 'Level' + ';' + str(count_global) + ';' \
                                            + 'Ticker' + ';' + symbol_to_work + ';' + 'Trend' + ';' + 'LONG' + ';' + 'TimeFrame' + ';' \
                                            + time_frame + ';' + 'FirstLevel' + ';' + f_high_1 + '--' + str(first_level_high) + ';' + 'SecondLevel' \
                                            + ';' + f_high_2 + '--' + str(second_level_high) + ';' + 'ThirdLevel' + ';' + f_high_3 + '--' + str(third_level_high) + ';' + 'MaxLevel' \
                                            + ';' + str(max_level_up)
                            print(count_ticker, ':', data_to_write)
                            # If found active level parsing data file and checking if we already posted this level. If yes - ignore
                            is_to_post = True
                            with open(r'C:/TradeBot/file_cases.txt', 'r') as file:
                                for line in file:
                                    splitted_line = line.split(';')
                                    # print(splitted_line[1] , '---', max_level_up_time, '********', float(splitted_line[15].rstrip()) , '---', max_level_up, '********',splitted_line[1] , '---', max_level_up_time)
                                    if splitted_line[3] == symbol_to_work and float(splitted_line[15].rstrip()) == max_level_up \
                                            and splitted_line[7] == time_frame:
                                        is_to_post = False
                                        break
                                    else:
                                        is_to_post = True
                            if is_to_post:
                                count_global += 1
                                with open(r'C:/TradeBot/file_cases.txt', 'a') as file:
                                    file.write(data_to_write + '\n')
                                text_tele_to_post = '&#128276;' + 'Уровень : ' + str(count_global) + '\n'\
                                                    + '&#128994;' + '&#128994;' + '&#128994;' + 'Тикер : ' + symbol_to_work + '\n' + '&#128338;' + 'Тайм фрейм : ' + time_frame + '\n' \
                                                    + '&#49;&#65039;&#8419;' + '(' + f_high_1 + ') : ' + '<strong>' + str(first_level_high) + '</strong>' + '\n' \
                                                    + '&#50;&#65039;&#8419;' + '(' + f_high_2 + ') : ' + '<strong>' + str(second_level_high) + '</strong>' + '\n' \
                                                    + '&#51;&#65039;&#8419;' + '(' + f_high_3 + ') : ' + '<strong>' + str(third_level_high) + '</strong>' + '\n' \
                                                    + '&#128681;' + 'Максимум : ' + '<u>' + '<strong>' + str(max_level_up) + '</strong>' + '</u>'
                                # bot.send_message(chat_id=-1001854525697, text=text_tele_to_post, parse_mode='HTML')
                                time.sleep(1)

                    # Detecting fractal for lows
                    counter_mas = creds.fractal_periods
                    while counter_mas < len(mas)-creds.fractal_periods:
                        counter = 1
                        is_low_fractal = True
                        while counter < creds.fractal_periods:
                            if is_low_fractal \
                                and mas[counter_mas - counter][low] >= mas[counter_mas][low] \
                                and mas[counter_mas + counter][low] > mas[counter_mas][low]:
                                is_low_fractal = True
                            else: is_low_fractal = False
                            counter += 1
                        if is_low_fractal:
                            normal_time_low = pd.to_datetime(mas[counter_mas][open_time], unit='ms')
                            down_fractals.append(mas[counter_mas] + [counter_mas])
                            # print(counter_mas, normal_time_low, float(mas[counter_mas][low]), 'low')
                        counter_mas += 1
                    # Detected if this low is the fractal

                    l_down = len(down_fractals)
                    for i_down in range(l_down):
                        count_down = 0
                        for el_down in down_fractals[i_down:l_down]:
                            if count_down == 0:
                                count_down = 1
                                base_level_down = float(el_down[low])
                                first_level_low = float(el_down[low])
                                f_low_1 = str(pd.to_datetime(el_down[open_time], unit='ms'))
                                max_level_down = float(el_down[low])
                                max_level_down_time = str(pd.to_datetime(el_down[open_time], unit='ms'))
                                # print(symbol_to_work, time_frame, 'SHORT', 'Ind ', el_down[index_kline],
                                #       'Pos in series ', count_down,
                                #       '***', pd.to_datetime(el_down[open_time], unit='ms'), 'Cur- ',
                                #       float(el_down[low]), 'Max-', '(', max_level_down, ')')
                            else:
                                # print('-----', 'Current-', float(el_down[low]), 'Nije - ', base_level_down * high_limit_low , 'Base- ', base_level_down, 'Vishe - ', base_level_down * low_limit_low )
                                if base_level_down * high_limit_low <= float(el_down[low]) and  float(el_down[low]) <= base_level_down * low_limit_low:
                                    count_down += 1
                                    if float(el_down[low]) < max_level_down:
                                        max_level_down = float(el_down[low])
                                    if count_down == 2:
                                        second_level_low = float(el_down[low])
                                        f_low_2 = str(pd.to_datetime(el_down[open_time], unit='ms'))
                                        # print(symbol_to_work, time_frame, 'SHORT', 'Ind ', el_down[index_kline],
                                        #       'Pos in series ', count_down,
                                        #       '-----', pd.to_datetime(el_down[open_time], unit='ms'), 'Cur- ',
                                        #       float(el_down[low]), 'Max-', '(', max_level_down, ')')
                                    if count_down >= 3 and ((first_level_low < second_level_low and second_level_low > third_level_low) \
                                        or (first_level_low > second_level_low and second_level_low < third_level_low) \
                                        or (first_level_low == second_level_low and second_level_low < third_level_low) \
                                        or (first_level_low == second_level_low and second_level_low == third_level_low) \
                                        or (first_level_low > second_level_low and second_level_low == third_level_low)):
                                        third_level_low = float(el_down[low])
                                        f_low_3 = str(pd.to_datetime(el_down[open_time], unit='ms'))
                                        print(symbol_to_work, time_frame, 'SHORT', 'Ind ', el_down[index_kline],
                                              'Pos in series ', count_down,
                                              '>>>>>>>>', pd.to_datetime(el_down[open_time], unit='ms'), 'Cur- ',
                                              float(el_down[low]), 'Max-', '(', max_level_down, ')')
                                elif float(el_down[low]) < base_level_down * high_limit_low:
                                    # print('*********', float(el_down[low]))
                                    count_down = 0
                                    first_level_low = 0
                                    second_level_low = 0
                                    third_level_low = 0
                                    break
                        if count_down >= 3 and max_level_down < max_last_down \
                            and ((first_level_low < second_level_low and second_level_low > third_level_low) \
                            or (first_level_low > second_level_low and second_level_low < third_level_low) \
                            or (first_level_low == second_level_low and second_level_low < third_level_low) \
                            or (first_level_low == second_level_low and second_level_low == third_level_low) \
                            or (first_level_low > second_level_low and second_level_low == third_level_low)):
                            # print('Level to active to bet low - ', pd.to_datetime(el_down[open_time], unit='ms'), max_level_down, count_down)
                            data_to_write = 'Level' + ';' + str(count_global) + ';' \
                                            + 'Ticker' + ';' + symbol_to_work + ';' + 'Trend' + ';' + 'SHORT' + ';' + 'TimeFrame' + ';' \
                                            + time_frame + ';' + 'FirstLevel' + ';'+ f_low_1 + '--' + str(first_level_low) + ';'  + 'SecondLevel' \
                                            + ';' + f_low_2 + '--' + str(second_level_low) + ';'+ 'ThirdLevel' + ';' + f_low_3 + '--' + str(third_level_low) + ';' + 'MaxLevel' \
                                            + ';' + str(max_level_down)
                            print(count_ticker, ':', data_to_write)
                            is_to_post = True
                            with open(r'C:/TradeBot/file_cases.txt', 'r') as file:
                                for line in file:
                                    splitted_line = line.split(';')
                                    if splitted_line[3] == symbol_to_work and float(splitted_line[15].rstrip()) == max_level_down \
                                            and splitted_line[7] == time_frame:
                                        is_to_post = False
                                        break
                                    else:
                                        is_to_post = True
                            if is_to_post:
                                count_global += 1
                                with open(r'C:/TradeBot/file_cases.txt', 'a') as file:
                                    file.write(data_to_write + '\n')
                                text_tele_to_post = '&#128276;' + 'Уровень : '  + str(count_global) + '\n' \
                                                    + '&#128315;' + '&#128315;' + '&#128315;' + 'Тикер : ' + symbol_to_work + '\n' + '&#128338;' + 'Тайм фрейм : ' + time_frame + '\n' \
                                                    + '&#49;&#65039;&#8419;' + '(' + f_low_1 + ') : ' + '<strong>' + str(first_level_low) + '</strong>' + '\n' \
                                                    + '&#50;&#65039;&#8419;' + '(' + f_low_2 + ') : ' + '<strong>' + str(second_level_low) + '</strong>' + '\n' \
                                                    + '&#51;&#65039;&#8419;' + '(' + f_low_3 + ') : ' + '<strong>' + str(third_level_low) + '</strong>' + '\n' \
                                                    + '&#128681;' + 'Максимум : ' + '<u>' + '<strong>' + str(max_level_down) + '</strong>' + '</u>'
                                # bot.send_message(chat_id=-1001854525697, text=text_tele_to_post, parse_mode='HTML')
                                # time.sleep(1)
                    time.sleep(1)

                    mas.clear()
                    up_fractals.clear()
                    down_fractals.clear()
                count_ticker += 1
            count_timeframe += 1
        count_global_circle += 1
    except KeyboardInterrupt:
        break
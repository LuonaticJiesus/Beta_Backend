import datetime


def get_zero_time():
    now_time = datetime.datetime.now()
    zero_time_str = now_time.strftime('%Y-%m-%d %H:%M:%S')[:len('2000:01-01 ')] + '00:00:00'
    zero_time = datetime.datetime.strptime(zero_time_str, '%Y-%m-%d %H:%M:%S')
    return zero_time

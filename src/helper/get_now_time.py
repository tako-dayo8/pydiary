import time

def get_now_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
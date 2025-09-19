import enum , time , os

from helper.get_now_time import get_now_time

class LogLevel(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def create_log_file_name() -> str:
    # ログファイルの名前を生成する diarypy_YYYYMMDD_{prosses_id}.log
    t = time.localtime()
    year = t.tm_year
    month = t.tm_mon
    day = t.tm_mday
    pid = os.getpid()
    return f"logs/diarypy_{year}{month}{day}_{pid}.log"

def create_log_dir() -> None:
    # logsディレクトリが存在しない場合は作成
    if not os.path.exists("logs"):
        os.makedirs("logs")

def create_log_file() -> None:
    # ログファイルが存在しない場合は作成
    if not os.path.exists(log_file_name):
        with open(log_file_name, "w", encoding="utf-8") as f:
            f.write("")

# ログファイルの名前を取得
log_file_name = create_log_file_name()

create_log_dir()
create_log_file()

def write_log(message: str) -> None:
    with open(log_file_name, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

class Logger:
    @staticmethod
    def create_message(level: LogLevel ,message: str , *args) -> str:
        return f"[{level.value}][{get_now_time()}]: {message}" + " ".join(map(str, args))

    @staticmethod
    def log(level: LogLevel ,message: str , *args) -> None:
        log_msg = Logger.create_message(level , message , *args)
        print(log_msg)

    @staticmethod
    def log_dump(level: LogLevel ,message: str , *args) -> None:
        log_msg = Logger.create_message(level , message , *args)
        print(log_msg)
        write_log(log_msg)
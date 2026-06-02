import sys
from config.paths import LOG
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# 创建日志管理器
def setup_logger(name = "XiaoFu", log_level = logging.DEBUG, console_level = logging.INFO): 
    log_dir = LOG
    log_dir.mkdir(exist_ok = True)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        file_handler = RotatingFileHandler(
        log_dir / "xiaofu.log",
        maxBytes = 5*1024*1024,
        backupCount = 5,
        encoding = "utf-8",
    )

    file_handler.setLevel(log_level)

    # 控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    # 定义日志格式
    formatter = logging.Formatter("%(asctime)s | %(filename)s:%(lineno)d | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


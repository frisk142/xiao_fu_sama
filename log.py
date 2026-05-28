import sys
from config.paths import LOG
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name = "XiaoFu", log_level = logging.DEBUG, console_level = logging.INFO): 
    log_dir = LOG
    log_dir.mkdir(exist_ok = True)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    file_handler = RotatingFileHandler(
        log_dir / "xiaofu.log",
        maxBytes = 5*1024*1024,
        backupCount = 5,
        encoding = "utf-8",
    )

    file_handler.setLevel(logging.DEBUG)

    # 控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 定义日志格式
    formattler = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(formattler)
    console_handler.setFormatter(formattler)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


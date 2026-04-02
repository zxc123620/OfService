import sys
import logging.config
import os
if not os.path.exists("logs"):
    os.mkdir("logs")
# 日志配置字典（可从json/yaml文件加载，只需转成字典）
LOGGING_CONFIG = {
    "version": 1,  # 必须为1，固定格式
    "disable_existing_loggers": False,  # 不禁用已存在的日志器（建议设为False）

    # 格式器配置
    "formatters": {
        "simple": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {  # 额外定义一个详细格式器
            "format": "%(asctime)s | %(process)d | %(thread)d | %(name)s | %(levelname)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    # 处理器配置
    "handlers": {
        # 控制台处理器
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": sys.stdout,  # 输出流
            # "filters": ["exclude_root"]  # 应用过滤器（可选）
        },
        # 文件处理器（按大小分割）
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",  # 旋转文件处理器
            "level": "INFO",
            "formatter": "simple",
            "filename": "./logs/info.log",
            "when": "midnight",
            "backupCount": 10,  # 保留10个备份文件
            "encoding": "utf-8"
        }
    },

    # 日志器配置
    "loggers": {
        # 自定义日志器
        "appLogger": {
            "level": "INFO",
            "handlers": ["console", "file"],  # 关联两个处理器
            "propagate": False
        },
        # 第三方库日志器（示例：控制requests库的日志级别）
        "requests": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False
        }
    },

    # 根日志器配置
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

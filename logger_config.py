from loguru import logger

logger.add('logs/app.log', rotation = "5 MB", retention = "14 days", compression = "zip")
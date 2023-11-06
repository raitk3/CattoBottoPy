import logging

class ColorfulFormatter(logging.Formatter):
    debug = "\x1b[38;20m"
    info = "\033[92m"
    warn = "\x1b[33;20m"
    error = "\x1b[31;20m"
    critical = "\x1b[31;1m"

    blue = "\033[34m"
    purple = "\033[35m"
    reset = "\x1b[0m"
    
    datefmt = "AAAAA"
    time = purple + "%(asctime)s" + reset
    level_name = "%(levelname)s" + reset
    file = blue + "%(filename)s:%(lineno)d" + reset
    msg =  "%(message)s" + reset

    FORMATS = {
        logging.DEBUG: time + " <" + debug + level_name + "> (" + file + reset + "): " + msg,
        logging.INFO: time + " <" + info + level_name + "> (" + file + reset + "): " + msg,
        logging.WARNING: time + " <" + warn + level_name + "> (" + file + reset + "): " + msg,
        logging.ERROR: time + " <" + error + level_name + "> (" + file + reset + "): " + msg,
        logging.CRITICAL: time + " <" + critical + level_name + "> (" + file + reset + "): " + msg,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class ColorlessFormatter(logging.Formatter):
    time = "%(asctime)s"
    level_name = "%(levelname)s"
    file = "%(filename)s:%(lineno)d"
    msg =  "%(message)s"

    FORMATS = {
        logging.DEBUG: time + " <" + level_name + "> (" + file + "): " + msg,
        logging.INFO: time + " <" + level_name + "> (" + file + "): " + msg,
        logging.WARNING: time + " <" + level_name + "> (" + file + "): " + msg,
        logging.ERROR: time + " <" + level_name + "> (" + file + "): " + msg,
        logging.CRITICAL: time + " <" + level_name + "> (" + file + "): " + msg,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

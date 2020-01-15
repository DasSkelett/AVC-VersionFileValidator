import logging
import sys


def setup_logger(debug):
    log = logging.getLogger('')
    level = logging.DEBUG if debug else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LogFormatter())
    log.addHandler(handler)
    log.setLevel(level)
    log.info(f'Logging started with level {level}')


# https://stackoverflow.com/a/14859558
class LogFormatter(logging.Formatter):

    dbg_fmt = "::DEBUG::%(msg)s"
    info_fmt = "::INFO::%(msg)s"
    wrn_fmt = "::WARNING::%(msg)s"
    err_fmt = "::ERROR::%(msg)s"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = LogFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = LogFormatter.info_fmt

        elif record.levelno == logging.WARNING:
            self._style._fmt = LogFormatter.wrn_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = LogFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result
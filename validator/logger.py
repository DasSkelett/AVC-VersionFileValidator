import logging
import sys


def setup_logger(debug, logger_name=''):
    log = logging.getLogger(logger_name)
    level = logging.DEBUG if debug else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LogFormatter())
    log.addHandler(handler)
    log.setLevel(level)
    log.info(f'Logger {logger_name} started with level {level}')


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

        # If the log statements contains legacy formatted strings with %s / %d ...
        # logging.Formatter.format() apparently tries to handle it, but doesn't somehow.
        # Only encountered with requests.
        # Update 2020-05-21, Python 3.8.2, requests 2.23.0:
        # For some reason, this has changed now, and requests.exceptions are handled fine.
        # Instead, this line itself throws the following exception, even for exceptions of other packages:
        #     TypeError: not enough arguments for format string
        # Since I think there's the possibility that other error messages would still need the following extra step,
        # I'm going to keep the line for now, but put it behind an if-clause, which seems to work.
        if record.args:
            result = result % record.args

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result

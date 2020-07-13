import logging
import sys
from pathlib import Path


def setup_logger(debug, logger_name=''):
    log = logging.getLogger(logger_name)
    level = logging.DEBUG if debug else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LogFormatter())
    log.addHandler(handler)
    log.setLevel(level)
    log.info(f'Logger {logger_name} started with level {level}')


class LogExtra:
    file: Path
    line: int
    col: int

    def __init__(self, file: Path, line: int = 1, col: int = 1):
        self.file = file
        self.line = line
        self.col = col

    def asdict(self):
        return {'file': self.file, 'line': self.line, 'col': self.col}


def _ensure_line_col(record):
    if not getattr(record, 'line', None):
        record.line = 1
    if not getattr(record, 'col', None):
        record.col = 1


# https://stackoverflow.com/a/14859558
class LogFormatter(logging.Formatter):

    dbg_fmt = "::DEBUG::%(msg)s"
    info_fmt = "::INFO::%(msg)s"
    wrn_fmt = "::WARNING::%(msg)s"
    wrn_file_fmt = "::WARNING file=%(file)s,line=%(line)d,col=%(col)d::%(msg)s"
    err_fmt = "::ERROR::%(msg)s"
    err_file_fmt = "::ERROR file=%(file)s,line=%(line)d,col=%(col)d::%(msg)s"

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
            if getattr(record, 'file', None):
                self._style._fmt = LogFormatter.wrn_file_fmt
                _ensure_line_col(record)
            else:
                self._style._fmt = LogFormatter.wrn_fmt

        elif record.levelno == logging.ERROR:
            if getattr(record, 'file', None):
                self._style._fmt = LogFormatter.err_file_fmt
                _ensure_line_col(record)
            else:
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

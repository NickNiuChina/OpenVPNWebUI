import subprocess


class LogParser(object):
    @classmethod
    def read_log(cls, line_size=None, log_file=None) -> list:
        out = []
        if not line_size:
            size = None
        else:
            size = int(line_size)

        content = log_file.read_text().split("\n")

        if size and size > 0:
            result = content[-size:]
        else:
            result = content
        return result


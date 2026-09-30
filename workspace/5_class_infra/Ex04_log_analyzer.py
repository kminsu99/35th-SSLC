# 파일명: log_analyzer.py
import re

print("모듈 시작")

class LogAnalyzer:
    def __init__(self, log_lines):
        self.log_lines = log_lines
        self.parsed_logs = [
            parsed for line in log_lines
            if (parsed := self.__parse_line(line)) is not None
        ]
    def __parse_line(self, line):
        pattern = r"\[(.*?)\]\[(.*?)\] (.*)"
        match = re.match(pattern, line)
        if match:
            timestamp, level, message = match.groups()
            return {"timestamp": timestamp, "level": level, "message": message, "raw": line}
        return None

    def filter_by_level(self, level):
        return [log for log in self.parsed_logs if log and log['level'] == level]

    def search(self, keyword):
        return [log for log in self.parsed_logs if log and keyword in log['message']]


# 확인

import csv
from datetime import datetime, timedelta
import io
import re
import sys

from pytz import timezone

PACIFIC = timezone('US/Pacific')
EASTERN = timezone('US/Eastern')

DURATION_REGEX = re.compile(
    r'(?P<hours>\d+):(?P<minutes>\d{2,2}):(?P<seconds>\d{2,2})'
    r'\.(?P<milliseconds>\d{3,3})')


def normalize_csv(src, dest):
    reader = csv.DictReader(src)
    writer = csv.DictWriter(dest, fieldnames=reader.fieldnames)

    writer.writeheader()

    for row in reader:
        row["FullName"] = row["FullName"].upper()
        row["Timestamp"] = convert_timestamp(row["Timestamp"])
        row["ZIP"] = "{:05d}".format(int(row["ZIP"]))
        row["FooDuration"] = parse_duration(row["FooDuration"])
        row["BarDuration"] = parse_duration(row["BarDuration"])
        row["TotalDuration"] = row["FooDuration"] + row["BarDuration"]
        writer.writerow(row)

def convert_timestamp(timestamp):
    naive_datetime = datetime.strptime(timestamp, "%m/%d/%y %I:%M:%S %p")
    aware_datetime = PACIFIC.localize(naive_datetime)
    converted_datetime = aware_datetime.astimezone(EASTERN)
    return converted_datetime.isoformat()

def parse_duration(duration_str):
    match = DURATION_REGEX.match(duration_str)
    if match:
        td = timedelta(
            hours=int(match.group('hours')),
            minutes=int(match.group('minutes')),
            seconds=int(match.group('seconds')),
            milliseconds=int(match.group('milliseconds'))
        )
        return td.seconds + td.microseconds/1_000_000

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    normalize_csv(input_stream, sys.stdout)

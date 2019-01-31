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
        try:
            row["FullName"] = row["FullName"].upper()
            row["Timestamp"] = convert_timestamp(row["Timestamp"])
            row["ZIP"] = "{:05d}".format(int(row["ZIP"]))
            row["FooDuration"] = parse_duration(row["FooDuration"])
            row["BarDuration"] = parse_duration(row["BarDuration"])
            row["TotalDuration"] = row["FooDuration"] + row["BarDuration"]
            writer.writerow(row)
        except ValueError as e:
            print(e, file=sys.stderr)


def convert_timestamp(timestamp):
    """
    Convert timestamps from US/Pacific to to US/Eastern and format to ISO-8601.
    """
    naive_datetime = datetime.strptime(timestamp, "%m/%d/%y %I:%M:%S %p")
    pacific_datetime = PACIFIC.localize(naive_datetime)
    eastern_datetime = pacific_datetime.astimezone(EASTERN)
    return eastern_datetime.isoformat()


def parse_duration(duration_str):
    """
    Parse durations stored in HH:MM:SS.MS format (where MS is milliseconds)
    to a floating point seconds format.
    """
    match = DURATION_REGEX.match(duration_str)
    if match:
        td = timedelta(
            hours=int(match.group('hours')),
            minutes=int(match.group('minutes')),
            seconds=int(match.group('seconds')),
            milliseconds=int(match.group('milliseconds'))
        )
        return td.seconds + td.microseconds/1_000_000
    else:
        raise ValueError(
            "{} does not match format HH:MM:SS.MS".format(duration_str))


if __name__ == '__main__':
    # Wrap stdin to fix UTF-8 encoding errors
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8',
                                    errors='replace')
    normalize_csv(input_stream, sys.stdout)

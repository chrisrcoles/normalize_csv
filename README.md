Run this using Python3 and `pipenv` using:
```
    pipenv install --three
    pipenv run python normalize_csv.py <sample.csv
```

You can run tests using:
```
    pipenv run pytest
```

Note:
1. I tried sticking to just the standard libraries but it was difficult to
manage timezones without `pytz`.
2. Once external libraries were used, I chose to introduce `pytest` rather than
stay with `unittest`.

from normalize_csv import convert_timestamp, parse_duration


def test_convert_timestamp():
    assert (convert_timestamp("11/01/03 07:34:25 PM")
            == "2003-11-01T22:34:25-05:00")
    assert (convert_timestamp("11/01/03 11:34:25 PM")
            == "2003-11-02T02:34:25-05:00")

def test_parse_duration():
    assert parse_duration("10:23:12.456") == 37392.456
    assert parse_duration("110:03:12.456") == 50592.456

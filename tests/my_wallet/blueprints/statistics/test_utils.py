import datetime
from my_wallet.blueprints.statistics.utils import is_report_range_valid


def test_is_report_range_valid(date_from: datetime.date, date_to: datetime.date) -> None:
    assert is_report_range_valid(date_from, date_to)

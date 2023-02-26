import datetime
from decimal import Decimal
from io import BytesIO

import pytest
from flask import Flask, send_file

from my_wallet.blueprints.statistics.custom_types import ReportData
from my_wallet.blueprints.statistics.forms import StatReportForm
from my_wallet.blueprints.statistics.report_formatters import generate_xlsx_response, generate_html_response, \
    generate_pdf_response

PARAMETRIZE_SET = [
    (
        ReportData(columns=['Description', 'Total expenses'], data=[['test3', Decimal('-500')]]),
        'expenses_by_type',
    ),
    (
        ReportData(columns=['Week num', 'Total expenses'], data=[[8, Decimal('-500')]]),
        'expenses_by_week',
    ),
    (
        ReportData(columns=['Day of week', 'Total expenses'], data=[['Thursday', Decimal('-500')]]),
        'expenses_by_weekday',
    ),
    (
        ReportData(
            columns=['billed at', 'amount', 'description'],
            data=[[datetime.datetime(2023, 2, 22, 10, 20, 20), Decimal('-500'), 'test3']],
        ),
        'biggest_expenses',
    ),
    (
        ReportData(
            columns=['Week num', 'Total expenses', 'Total income', 'Week balance'],
            data=[[8, Decimal('-500'), Decimal('833'), Decimal('333')]],
        ),
        'weekly_balance',
    ),
]


@pytest.mark.parametrize(
    "report_data, expected_file_name",
    PARAMETRIZE_SET,
)
def test_generate_html_response(app: Flask, report_data: ReportData, expected_file_name: str):
    with open(f"tests/files/{expected_file_name}.html", "r") as file:
        exp = file.read()
    assert generate_html_response(report_data, StatReportForm()) == exp


@pytest.mark.parametrize(
    "report_data, expected_file_name",
    PARAMETRIZE_SET,
)
def test_generate_xlsx_response(app: Flask, report_data: ReportData, expected_file_name: str):
    with open(f"tests/files/{expected_file_name}.xlsx", "rb") as binary_file:
        data = binary_file.read()
    actual_result = generate_xlsx_response(report_data, StatReportForm())
    expected_result = send_file(BytesIO(data), download_name="report.xlsx", as_attachment=True)
    assert actual_result.status == expected_result.status


@pytest.mark.parametrize(
    "report_data, expected_file_name",
    PARAMETRIZE_SET,
)
def test_generate_pdf_response(app: Flask, report_data: ReportData, expected_file_name: str):
    with open(f"tests/files/{expected_file_name}.pdf", "rb") as binary_file:
        data = binary_file.read()
    actual_result = generate_pdf_response(report_data, StatReportForm())
    expected_result = send_file(BytesIO(data), download_name="report.pdf", as_attachment=True)
    assert actual_result.status == expected_result.status

from pathlib import Path

import pytest

from utils.format_results import get_tables

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def tables() -> dict[str, str]:
    return get_tables(FIXTURES / "results.csv")


def test_cpp_table(tables: dict[str, str]) -> None:
    expected = (FIXTURES / "cpp_table.txt").read_text(encoding="utf-8")
    assert tables["cpp"] == expected


def test_python_table(tables: dict[str, str]) -> None:
    expected = (FIXTURES / "python_table.txt").read_text(encoding="utf-8")
    assert tables["python"] == expected


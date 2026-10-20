import pytest

from tests.test_students_db import test_engine, Base


@pytest.fixture(autouse=True)
def clean_test_database():
    with test_engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
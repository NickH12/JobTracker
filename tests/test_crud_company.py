"""
Unit tests for app/crud/crud_company.py using a mocked DB session -
no real database involved. These test that the CRUD functions call
the session correctly, independent of SQLAlchemy/Postgres.
"""
from unittest.mock import MagicMock

from app.crud import crud_company
from app.schemas.company import CompanyCreate


def test_create_company_adds_commits_and_refreshes():
    mock_db = MagicMock()
    company_data = CompanyCreate(name="Mock Inc", website="https://mock.com", notes=None)

    result = crud_company.create_company(mock_db, company_data, user_id=1)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert result.user_id == 1
    assert result.name == "Mock Inc"


def test_get_company_by_id_filters_by_user_id():
    mock_db = MagicMock()
    mock_filter_result = mock_db.query.return_value.filter.return_value
    mock_filter_result.first.return_value = "fake_company"

    result = crud_company.get_company_by_id(mock_db, company_id=1, user_id=1)

    mock_db.query.assert_called_once()
    mock_filter_result.first.assert_called_once()
    assert result == "fake_company"


def test_get_company_by_id_returns_none_when_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = crud_company.get_company_by_id(mock_db, company_id=999, user_id=1)

    assert result is None


def test_delete_company_returns_false_when_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = crud_company.delete_company(mock_db, company_id=999, user_id=1)

    assert result is False
    mock_db.delete.assert_not_called()


def test_delete_company_deletes_and_commits_when_found():
    mock_db = MagicMock()
    fake_company = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = fake_company

    result = crud_company.delete_company(mock_db, company_id=1, user_id=1)

    assert result is True
    mock_db.delete.assert_called_once_with(fake_company)
    mock_db.commit.assert_called_once()
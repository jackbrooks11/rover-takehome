from app.models.base import Base
import pytest
from sqlalchemy.exc import NoSuchColumnError
from unittest.mock import MagicMock, patch

@pytest.fixture
def base():
    base = Base()
    return base

@pytest.fixture
def mock_session():
    mock_session = MagicMock()
    return mock_session

@pytest.fixture
def mock_insert():
    with patch('app.models.base.insert') as mock_insert:
        yield mock_insert

def test_bulk_add__empty_list(base, mock_session):
    data = []
    res = base.bulk_add(mock_session, data)
    assert res == []

def test_bulk_add__list_with_empty_dict(base, mock_session, mock_insert):
    data = [{}]
    mock_session.scalars.return_value = []

    res = base.bulk_add(mock_session, data)
    assert res == []

def test_bulk_add__list_with_dict_col_not_valid_property__raises_Exception(base, mock_session, mock_insert):
    data = [{"random" : 2}]
    mock_session.scalars.side_effect = NoSuchColumnError('mocked error')
    with pytest.raises(NoSuchColumnError):
        base.bulk_add(mock_session, data)

def test_bulk_add__list_with_dict_col_valid_property__returns_List(base, mock_session, mock_insert):
    data = [{"id" : 2}]
    mock_session.scalars.return_value = [2]
    res = base.bulk_add(mock_session, data)
    assert res == [2]

def test_bulk_add__list_with_dict_col_valid_property__sort_provided__returns_List(base, mock_session, mock_insert):
    data = [{"id" : 2}]
    mock_session.scalars.return_value = [2]
    res = base.bulk_add(mock_session, data, True)
    assert res == [2]
"""Unit tests for MachineService."""
from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.machine.model.machine_model import Machine
from app.modules.machine.service.machine_service import MachineService


def test_fetch_machine_found():
    """Test fetch_machine when machine is found."""
    # Arrange
    mock_db = Mock(spec=Session)
    mock_machine = Machine(id=1, name="Test Machine")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_machine

    # Act
    service = MachineService(db=mock_db)
    result = service.fetch_machine(machine_id=1)

    # Assert
    assert result is None  # Since the method doesn't return anything on success
    mock_db.query.assert_called_once_with(Machine)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

def test_fetch_machine_not_found():
    """Test fetch_machine when machine is not found."""
    # Arrange
    mock_db = Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act & Assert
    service = MachineService(db=mock_db)
    with pytest.raises(HTTPException) as exc_info:
        service.fetch_machine(machine_id=999)

    # Assert
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Machine not found"
    mock_db.query.assert_called_once_with(Machine)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

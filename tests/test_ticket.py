import pytest
import json
from pydantic import ValidationError
from ticket_cli.ticket import Ticket
from ticket_cli.cli import validate_tickets, load_tickets

@pytest.fixture
def data():
    return {
        "id": 108,
        "title": "Application crashes during login",
        "priority": "High",
        "status": "In Progress"
    }

@pytest.fixture
def incorrect_data():
    return {
        "id": 100,
        "title": "Application crashes during login",
        "priority": "Urgent",
        "status": "In Progress"
    }

@pytest.fixture
def multiple_tickets():
    return [
        {
            "id": 101,
            "title": "Login issue",
            "priority": "High",
            "status": "Open"
        },
        {
            "id": 102,
            "title": "Email notification issue",
            "priority": "Medium",
            "status": "In Progress"
        },
        {
            "id": 103,
            "title": "Payment failure",
            "priority": "Urgent",
            "status": "Open"
        }
    ]

def test_ticket(data):
    ticket = Ticket(**data)
    assert ticket.model_dump() == data



def test_invalid_ticket(incorrect_data):
    with pytest.raises(ValidationError):
        Ticket(**incorrect_data)

def test_validate_tickets_separates_valid_and_invalid(multiple_tickets):
    valid_tickets, invalid_tickets = validate_tickets(multiple_tickets)
    assert len(valid_tickets) == 2
    assert len(invalid_tickets) == 1
    assert isinstance(valid_tickets[101], Ticket)
    assert isinstance(invalid_tickets[103], ValidationError)

def test_load_tickets(tmp_path):
    data = [{
                "id": 101,
                "title": "Login issue",
                "priority": "High",
                "status": "Open"
            },
            {
                "id": 102,
                "title": "Email notification issue",
                "priority": "Medium",
                "status": "In Progress"
            }]
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(data), encoding = "utf-8")
    result = load_tickets(path)
    assert result == data

def test_missing_file(tmp_path):
    path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_tickets(path)

def test_malformed_json(tmp_path):
    path = tmp_path / "malformed.json"
    malformed_json = '{"id": 101, "title": "Login issue"'
    path.write_text(malformed_json, encoding = "utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_tickets(path)

@pytest.fixture
def missing_data():
    return {
            "title": "Email notification issue",
            "priority": "Medium",
            "status": "In Progress"
            }


def test_ticket_missing_id(missing_data):
    valid_tickets, invalid_tickets = validate_tickets([missing_data])

    assert "Unknown" in invalid_tickets
    assert isinstance(invalid_tickets["Unknown"], ValidationError)
    assert len(valid_tickets) == 0

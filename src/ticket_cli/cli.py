import json
from pathlib import Path
from pydantic import ValidationError
import logging


from ticket_cli.ticket import Ticket

logger = logging.getLogger(__name__)

def load_tickets(path : Path) -> list[dict]:
    logger.info("Reading ticket data from JSON file")
    with open(path, 'r', encoding = "utf-8") as fobj:
        tickets_data = json.load(fobj)
        logger.info("Successfully loaded ticket data from JSON file")
        return tickets_data

def validate_tickets(data : list[dict]) -> tuple[dict[int, Ticket], dict[int, ValidationError]]:
    valid_tickets = {}
    invalid_tickets = {}
    logger.info("Validating tickets using Pydantic")
    for value in data:

        try:
            ticket = Ticket(**value)
            valid_tickets[value["id"]] = ticket
            logger.info("Ticket %s validated successfully", value["id"])
        except ValidationError as error:
            invalid_tickets[value.get("id", "Unknown")] = error
            logger.warning("Ticket %s failed validation", value.get("id", "Unknown"))

    logger.info("Ticket validation completed")
    logger.info("Valid ticket count  : %s", len(valid_tickets))
    logger.info("Invalid ticket count : %s", len(invalid_tickets))
    return valid_tickets, invalid_tickets

def display_results(tickets : dict[int, Ticket]) -> None:
    for ticket in tickets.values():
        print(ticket)

def main() -> None:

    logging_path = Path(__file__).parents[2] / "logs/app.log"
    logging_path.parent.mkdir(parents=True, exist_ok = True)
    
    logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s",
    filename = logging_path,
    encoding = "utf-8"
    )


    logger.info("Application started")

    try:
        path = Path(__file__).parents[2] / "data/tickets.json"
        data = load_tickets(path = path)
        valid_tickets, invalid_tickets = validate_tickets(data)
        
        logger.info("Displaying the segregated tickets in command line")
        print("Valid tickets :")
        display_results(valid_tickets)
        print()
        print("Invalid tickets :")

        for ticket_id, error in invalid_tickets.items():
            print(f"Ticket ID : {ticket_id}")
            print(error)

        logger.info("Application completed")
    except FileNotFoundError as error1:
        logger.error("Failed to load the JSON file : %s", error1)


    except json.JSONDecodeError as error2:
        logger.error("Failed to decode JSON : %s", error2)


if __name__ == "__main__":
    main()
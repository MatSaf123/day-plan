import typer
import csv

from tabulate import tabulate
from datetime import datetime

from models import DayPlanEntry

DAY_PLAN_FILEPATH = "plan.csv"

app = typer.Typer()


@app.command()
def get_all(remote: bool = True) -> None:
    """Reads and prints all entries for today.
    If it's a work day, assumes it's remote-day by default.

    Example usage:
        ```sh
        python3 main.py get-all
        ```
    """

    entries = []
    with open(DAY_PLAN_FILEPATH, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for line in csv_reader:
            entries.append(line)
    print(tabulate(entries, headers='firstrow', tablefmt='fancy_grid'))


@app.command()
def get(remote: bool = True) -> None:
    """Reads the day plan entry based on the current time.
    If it's a work day, assumes it's remote-day by default.

    Example usage:
        ```sh
        python3 main.py get
        ```
    """

    with open(DAY_PLAN_FILEPATH, "r", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")

        # Iterate over plan entries and find the one for the current time
        now = datetime.now()
        for line in reader:
            plan_entry = DayPlanEntry.model_validate(line)

            # Extract hours and minutes
            start_h = int(plan_entry.start_time[0:2])
            start_m = int(plan_entry.start_time[3:5])
            end_h = int(plan_entry.end_time[0:2])
            end_m = int(plan_entry.end_time[3:5])

            start_time = datetime(
                now.year, now.month, now.day, start_h, start_m)  # noqa
            end_time = datetime(
                now.year, now.month, now.day, end_h, end_m)

            if start_time <= now and end_time > now:
                # Found it!
                print(tabulate(plan_entry,
                      tablefmt='fancy_grid'))
                break
        else:
            raise Exception(
                "No entry found for current time! (probably something wrong with input file)")


if __name__ == "__main__":
    app()

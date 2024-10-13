import typer
import csv

from tabulate import tabulate
from datetime import datetime

from plans import REMOTE_DAY

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

    # entries = []
    # with open(DAY_PLAN_FILEPATH, "r") as f:
    #     csv_reader = csv.reader(f, delimiter=",")
    #     for line in csv_reader:
    #         entries.append(line)
    print(tabulate(REMOTE_DAY, headers='firstrow', tablefmt='fancy_grid'))


@app.command()
def get(remote: bool = True) -> None:
    """Reads the day plan entry based on the current time.
    If it's a work day, assumes it's remote-day by default.

    Example usage:
        ```sh
        python3 main.py get
        ```
    """
    headers = REMOTE_DAY[0]
    now = datetime.now()
    for line in REMOTE_DAY[1:]:

        # Extract hours and minutes
        start_time, end_time = line[1:3]
        start_h = int(start_time[0:2])
        start_m = int(start_time[3:5])
        end_h = int(end_time[0:2])
        end_m = int(end_time[3:5])

        start_time = datetime(
            now.year, now.month, now.day, start_h, start_m)
        end_time = datetime(
            now.year, now.month, now.day, end_h, end_m)

        if start_time <= now and end_time > now:
            # Found it!
            print(tabulate([headers, line],
                           headers="firstrow",
                  tablefmt='fancy_grid'))
            break
    else:
        raise Exception(
            f"No entry found for current time! - {now}")


if __name__ == "__main__":
    app()

import csv
import sys
import datetime

from tabulate import tabulate

DAY_PLAN_FILEPATH = "plan.csv"


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
        entries = []
        # Skip the header line
        next(csv_reader)
        # We're displaying only name of the task and combined time to save screen space
        for line in csv_reader:
            name = line[0]
            combined_date = f"{line[1]}-{line[2]}"
            entries.append([name, combined_date])
    print(tabulate(entries, headers=["Task", "Time"], tablefmt='simple_grid'))


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
        now = datetime.datetime.utcnow()
        for line in reader:

            # Extract hours and minutes
            start_h = int(line["start_time"][0:2])
            start_m = int(line["start_time"][3:5])
            end_h = int(line["end_time"][0:2])
            end_m = int(line["end_time"][3:5])

            # Modifier to be added to the time in file (CEST) in order to turn it into UTC.
            # This is required because iSh does weird things and returns UTC for `dt.now()`
            modifier = datetime.timedelta(hours=2)

            start_time = datetime.datetime(
                now.year, now.month, now.day, start_h, start_m) - modifier
            end_time = datetime.datetime(
                now.year, now.month, now.day, end_h, end_m) - modifier

            if start_time <= now and end_time > now:
                # Found it!
                # We're transposing the table here: keys are in first column, values in the second
                print(tabulate([
                    ["Task", line["name"]],
                    ["Start time", line["start_time"]],
                    ["Finish time", line["end_time"]],
                    ["Comment", line["comment"]],
                ],
                    tablefmt="simple_grid",
                    maxcolwidths=[None, 16],
                ))

                break
        else:
            raise Exception(
                f"No entry found for current time! - {now}")


if __name__ == "__main__":
    func_name = sys.argv[1]
    if func_name == "get":
        get()
    elif func_name == "get-all":
        get_all()
    else:
        raise Exception(f"Unexpected option passed: {func_name}")

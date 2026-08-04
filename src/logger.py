import csv
import os
from datetime import datetime

LOG_FILE = "logs/detection_log.csv"


def save_log(person_count):

    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time", "Persons"])

        current_time = datetime.now().strftime("%H:%M:%S")

        writer.writerow([current_time, person_count])
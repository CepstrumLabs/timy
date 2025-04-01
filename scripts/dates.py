import random
from datetime import datetime, timedelta


def generate_random_timestamp(day):
    # Generate a random time within the given day
    random_time = timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
        microseconds=random.randint(0, 999999)
    )
    timestamp = day + random_time
    return timestamp.isoformat()


def generate_timestamps(n, count_per_day=5):
    today = datetime.now()
    timestamps = []

    for i in range(n):
        day = today - timedelta(days=i)
        for _ in range(count_per_day):
            timestamps.append(generate_random_timestamp(day))

    random.shuffle(timestamps)
    return timestamps


if __name__ == "__main__":
    n = int(input("Enter the number of days: "))
    count_per_day = int(input("Enter the number of timestamps per day: "))
    result = generate_timestamps(n, count_per_day)
    for ts in result:
        print(ts)

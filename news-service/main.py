"""
NEWS SERVICE (consumer)

It waits for new reviews and prints them.
"""
from kafka import KafkaConsumer


BOTTLE_REVIEW_TOPIC = "bottle-review"

consumer = KafkaConsumer(
    BOTTLE_REVIEW_TOPIC,
    bootstrap_servers=["localhost:9092"],
    # auto_offset_reset="earliest",
    # api_version=(0, 10),
    # consumer_timeout_ms=1000,
)


def main():
    # Consuming bottle-purchase.
    for message in consumer:
        key = message.key
        if key:
            key = key.decode("utf-8")
        value = message.value
        if value:
            value = value.decode("utf-8")
        # Generate a new review for the purchased bottle.
        print(f"New review: {key}|{value}")

    # consumer.close()


if __name__ == "__main__":
    print("Running NEWS-SERVICE..")
    print(
        "(consumer)"
        "It waits for new bottles to be reviewed (topic=bottle-review),\n"
        "then it prints the review\n"
    )
    main()


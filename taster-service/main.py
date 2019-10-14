"""
TASTER SERVICE (producer and consumer)

It waits for new purchases.
It reviews them and publishes the review.
"""
import random
import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError


BOTTLE_PURCHASE_TOPIC = "bottle-purchase"
BOTTLE_REVIEW_TOPIC = "bottle-review"

consumer = KafkaConsumer(
    BOTTLE_PURCHASE_TOPIC,
    bootstrap_servers=["localhost:9092"],
    # auto_offset_reset="earliest",
    # api_version=(0, 10),
    # consumer_timeout_ms=1000,
)
producer = KafkaProducer(bootstrap_servers=["localhost:9092"])


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
        print(f"New purchase found: {key}|{value}")
        generate_review(key, value)

    # consumer.close()


def generate_review(key, value):
    print(f"Tasting bottle: {key}|{value}...")
    time.sleep(2)
    result = random.choice(("bad", "good", "great", "excellent"))
    print(f"> {result}!!")

    # Publishing the review on bottle-review.
    future = producer.send(
        BOTTLE_REVIEW_TOPIC, key=bytes(key, "utf-8"), value=bytes(result, "utf-8")
    )
    # Block for 'synchronous' sends.
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        raise


if __name__ == "__main__":
    print("Running TASTER-SERVICE..")
    print(
        "(consumer and producer)"
        "It waits for new bottles to be purchased (topic=bottle-purchase),\n"
        "then it tastes them and publishes a review (topic=bottle-review)\n"
    )
    main()


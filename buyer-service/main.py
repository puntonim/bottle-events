"""
BUYER SERVICE (producer)

It buys a new bottle every 5 seconds and publishes the purchase event.
"""
import random
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError


BOTTLE_PURCHASE_TOPIC = "bottle-purchase"

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])


def main():
    while True:
        bottle = random.choice(("Prosecco", "Barolo", "Pinot Noir", "Bordeaux"))
        key = "b" + str(random.randint(1, 10000))
        print(f"Buying: {key}:{bottle}...")
        # Publishing the purchase on bottle-purchase.
        future = producer.send(
            BOTTLE_PURCHASE_TOPIC, key=bytes(key, "utf-8"), value=bytes(bottle, "utf-8")
        )
        # Block for 'synchronous' sends.
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            raise
        time.sleep(5)


if __name__ == "__main__":
    print("Running BUYER-SERVICE..")
    print(
        "(producer)"
        "It purchases a new bottle every 5 secs and publishes the purchase (topic=bottle-purchase)\n"
    )
    main()


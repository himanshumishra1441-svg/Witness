from kafka import KafkaConsumer
import json

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "loan-events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(
        m.decode("utf-8")
    ),
    auto_offset_reset="earliest"
)

print("Consumer started")

for message in consumer:
    print(message.value)
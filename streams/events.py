from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio, json

async def send_order_event(order_id: int, user_id: int, status: str):
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

    try:
        event = {
            "order_id": order_id,
            "user_id": user_id,
            "status": status
        }
        await producer.send_and_wait("order_events", json.dumps(event).encode('utf-8'))
    finally:
        await producer.stop()
    
    # print(f"Sent order event: {event}")
import faust 
from app.model import Order, Product, get_db, AsyncSessionLocal
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from .events import consumer_notification_event
from aiokafka import AIOKafkaConsumer
import json


app = faust.App('myapp', broker='kafka://localhost:9092')

class OrderEvent(faust.Record, serializer='json'):
    order_id: int
    user_id: int
    status: str 


order_topic = app.topic('order_events', value_type=OrderEvent)
# consumer_topic = app.topic('consumer_notification_events', value_type=ConsumerNotificationEvent)

@app.agent(order_topic)
async def process_order(orders):
    async for order in orders:
        print(f"Processing order: {order.order_id} for user: {order.user_id} with status: {order.status}")
        async with AsyncSessionLocal() as session:
            dbOrder = await session.get(Order, order.order_id)

            if not dbOrder:
                print(f"Order {order.order_id} not found in DB")
                continue
            
            dbOrder.status = "CONFIRMED"
            await session.commit()
            await consumer_notification_event(order.order_id, order.user_id, dbOrder.status)
            print(f"Order {order.order_id} status updated to CONFIRMED in DB")  

async def sse_generator(user_id: int):
    consumer = AIOKafkaConsumer(
        'consumer_notification_events',
        bootstrap_servers='localhost:9092',
        group_id="notification_group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            if data["user_id"] == user_id:
                yield f"data: {json.dumps(data)}\n\n"
    finally:
        await consumer.stop()
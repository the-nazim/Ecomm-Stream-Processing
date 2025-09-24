import faust 

app = faust.App('myapp', broker='kafka://localhost:9092')

class OrerEvent(faust.Record, serializer='json'):
    order_id: int
    user_id: int
    status: str 

order_topic = app.topic('order_events', value_type=OrerEvent)

@app.agent(order_topic)
async def process_order(orders):
    async for order in orders:
        print(f"Processing order: {order.order_id} for user: {order.user_id} with status: {order.status}")
        # Here you can add logic to update the database or perform other actions based on the order event
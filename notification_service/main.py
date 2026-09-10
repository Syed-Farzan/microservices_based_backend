import asyncio
import os
import json
import nats
from nats.js.errors import NotFoundError

NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")


async def message_handler(msg):
    try:
        data = json.loads(msg.data.decode())
        email = data.get("email")

        print(
            f"[{msg.subject}] Asynchronously sending welcome email to: {email}...",
            flush=True,
        )

        await msg.ack()
    except Exception as e:
        print(f"Error processing message: {e}", flush=True)

        await msg.nak()


async def main():
    print("Connecting to NATS...", flush=True)
    nc = await nats.connect(NATS_URL)
    js = nc.jetstream()

    try:
        await js.stream_info("USER_EVENTS")
    except NotFoundError:
        await js.add_stream(name="USER_EVENTS", subjects=["user.*"])

    await js.subscribe(
        "user.created", cb=message_handler, durable="notification_service_durable"
    )
    print("Notification Service active and listening...", flush=True)

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await nc.drain()


if __name__ == "__main__":
    asyncio.run(main())

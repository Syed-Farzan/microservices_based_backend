import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import nats
from nats.js.errors import NotFoundError

NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")
nc, js = None, None


class UserCreate(BaseModel):
    name: str
    email: EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):
    global nc, js

    nc = await nats.connect(NATS_URL)
    js = nc.jetstream()

    try:
        await js.stream_info("USER_EVENTS")
    except NotFoundError:
        await js.add_stream(name="USER_EVENTS", subjects=["user.*"])
    yield
    await nc.close()


app = FastAPI(title="User Service", lifespan=lifespan)


@app.post("/users")
async def create_user(user: UserCreate):
    user_data = user.model_dump()
    user_data["id"] = "USR-999"

    try:

        await js.publish("user.created", json.dumps(user_data).encode())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to publish system event")

    return {"status": "success", "data": user_data}

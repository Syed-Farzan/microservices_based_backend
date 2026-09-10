from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import httpx
import os

app = FastAPI(title="API Gateway")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:8000")


class UserCreate(BaseModel):
    name: str
    email: EmailStr


@app.post("/api/users")
async def route_create_user(user: UserCreate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{USER_SERVICE_URL}/users", json=user.model_dump()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="User Service is unavailable")

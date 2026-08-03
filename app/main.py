import time

from fastapi import FastAPI, HTTPException, Request

from app.config import APP_NAME, APP_VERSION
from app.data import users
from app.logger import logger
from app.models import User

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    elapsed = (time.perf_counter() - start) * 1000

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{elapsed:.2f}ms"
    )

    return response


@app.get("/")
def home():
    return {
        "message": "Ops Automation Toolkit API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/users")
def get_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    logger.warning(f"User not found | id={user_id}")

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@app.post("/users", status_code=201)
def create_user(user: User):
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
    }

    users.append(new_user)

    logger.info(
        f"User created | id={new_user['id']} | name={new_user['name']}"
    )

    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for user in users:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email

            logger.info(f"User updated | id={user_id}")

            return user

    logger.warning(f"User not found | id={user_id}")

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            logger.info(f"User deleted | id={user_id}")

            return {
                "message": "User deleted"
            }

    logger.warning(f"User not found | id={user_id}")

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
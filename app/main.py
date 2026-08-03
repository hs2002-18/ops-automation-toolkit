from fastapi import FastAPI, HTTPException
from app.models import User
from app.logger import logger

app = FastAPI(title="Ops Automation Toolkit")

# In-memory users
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]


@app.get("/")
def home():
    return {"message": "Ops Automation Toolkit API"}


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/users")
def get_users():
    logger.info("Retrieved all users")
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            logger.info(f"Retrieved user | id={user_id}")
            return user

    logger.warning(f"User not found | id={user_id}")
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users")
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
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            logger.info(f"User deleted | id={user_id}")

            return {"message": "User deleted"}

    logger.warning(f"User not found | id={user_id}")
    raise HTTPException(status_code=404, detail="User not found")
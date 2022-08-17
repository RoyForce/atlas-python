#!/usr/bin/env python3

from app.db.session import get_db
from app.db.users.crud import create_user
from app.db.users.schemas import UserCreate
from app.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="vsharma@atlasbeacon.com",
            password="123456",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser vsharma@atlasbeacon.com")
    init()
    print("Superuser created")

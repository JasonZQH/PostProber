#!/usr/bin/env python3
"""Initialize the database with all tables."""

from app.db.database import engine, Base
from models import User, Post, Account, MonitoringLog

def init_database():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print("Tables created:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")

if __name__ == "__main__":
    init_database()
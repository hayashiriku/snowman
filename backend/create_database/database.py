from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
import datetime

# データベースファイル名
sqlite_file_name = "/Users/riku/snowman/backend/snow.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# --- 都道府県マスタ (JISコード) ---
class Prefecture(SQLModel, table=True):
    # JISコード(1~47)をそのままIDとして使うため、自動採番(default=None)はしません
    id: int = Field(primary_key=True) 
    name: str = Field(index=True, unique=True)

# --- 日別データ ---
class DailySnow(SQLModel, table=True):
    date: datetime.date = Field(primary_key=True)
    # 県名ではなくID(数値)で紐付けます
    prefecture_id: int = Field(primary_key=True, foreign_key="prefecture.id")
    avg_depth: float = 0.0

# --- 月別データ ---
class MonthlySnow(SQLModel, table=True):
    month_date: datetime.date = Field(primary_key=True)
    prefecture_id: int = Field(primary_key=True, foreign_key="prefecture.id")
    avg_snowfall: float = 0.0

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func
import math
from datetime import date
from create_database.database import get_session, DailySnow, MonthlySnow, Prefecture
from sqlalchemy import distinct

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SnowRequest(BaseModel):
    prefecture_id: int
    target_date: str
    period_type: str
    # area はDBから取得するため削除

# --- 計算ロジック (指定仕様) ---
def calculate_snowman_height(snow_cm, area_km2):
    if snow_cm <= 0: return 0, 0
    
    # 単位変換
    area_m2 = area_km2 * 1_000_000 # km2 -> m2
    depth_m = snow_cm / 100        # cm -> m
    
    # 体積計算 (圧縮率 40%)
    volume = area_m2 * depth_m * 0.4
    
    # 高さ計算 (頭体比率8:10 -> 係数1.94)
    # Height = 1.94 * (Volume)^(1/3)
    height_m = 1.94 * math.pow(volume, 1/3)
    
    return height_m, volume

@app.get("/prefectures")
def get_prefectures(session: Session = Depends(get_session)):
    statement = select(Prefecture).order_by(Prefecture.id)
    return session.exec(statement).all()

# backend/main.py

# ★引数に pref_id: int を追加
@app.get("/available_dates")
def get_available_dates(pref_id: int, session: Session = Depends(get_session)):
    
    # ★重要: .filter(DailySnow.prefecture_id == pref_id) を追加して絞り込む
    # ※モデルの列名が 'prefecture_id' か 'point_id' かは環境に合わせてください
    records = session.query(DailySnow.date, DailySnow.avg_depth)\
                     .filter(DailySnow.prefecture_id == pref_id)\
                     .all()
    
    date_status = {}

    for r in records:
        d_str = r.date.isoformat()
        
        if date_status.get(d_str) == "positive":
            continue

        if r.avg_depth > 0:
            date_status[d_str] = "positive"
        else:
            date_status[d_str] = "zero"
            
    return date_status

@app.post("/calculate")
def calc_snow(req: SnowRequest, session: Session = Depends(get_session)):
    try:
        target = date.fromisoformat(req.target_date)
    except ValueError:
        return {"error": "日付エラー"}

    # DBから県データ（面積含む）を取得
    pref = session.get(Prefecture, req.prefecture_id)
    if not pref:
        return {"error": "県が見つかりません"}

    val_cm = 0
    message = ""
    
    # DBから雪の量(cm)を取得
    if req.period_type == "day":
        data = session.get(DailySnow, (target, req.prefecture_id))
        if not data: return {"error": "データがありません"}
        val_cm = data.avg_depth
        message = f"{pref.name} (面積{pref.area}km²) の積雪深 {round(val_cm, 1)}cm"

    elif req.period_type == "month":
        target_month = date(target.year, target.month, 1)
        data = session.get(MonthlySnow, (target_month, req.prefecture_id))
        if not data: return {"error": "データがありません"}
        val_cm = data.avg_snowfall
        message = f"{pref.name} (面積{pref.area}km²) の降雪量 {round(val_cm, 1)}cm"

    elif req.period_type == "year":
        statement = select(func.sum(MonthlySnow.avg_snowfall)).where(
            MonthlySnow.prefecture_id == req.prefecture_id,
            func.strftime('%Y', MonthlySnow.month_date) == str(target.year)
        )
        val_cm = session.exec(statement).first() or 0
        message = f"{pref.name} (面積{pref.area}km²) の年間降雪量 {round(val_cm, 1)}cm"

    # --- 計算実行 ---
    height_m, volume = calculate_snowman_height(val_cm, pref.area)

    return {
        "prefecture": pref.name,
        "volume_m3": volume,
        "height_m": height_m,
        "message": message
    }
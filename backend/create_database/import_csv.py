import pandas as pd
from sqlmodel import Session, select
from database import engine, create_db_and_tables, DailySnow, MonthlySnow, Prefecture

# ★ JISコード表 (都道府県コード)
JIS_MAP = {
    "北海道": 1, "青森県": 2, "岩手県": 3, "宮城県": 4, "秋田県": 5, "山形県": 6, "福島県": 7,
    "茨城県": 8, "栃木県": 9, "群馬県": 10, "埼玉県": 11, "千葉県": 12, "東京都": 13, "神奈川県": 14,
    "新潟県": 15, "富山県": 16, "石川県": 17, "福井県": 18, "山梨県": 19, "長野県": 20,
    "岐阜県": 21, "静岡県": 22, "愛知県": 23, "三重県": 24, "滋賀県": 25, "京都府": 26,
    "大阪府": 27, "兵庫県": 28, "奈良県": 29, "和歌山県": 30, "鳥取県": 31, "島根県": 32,
    "岡山県": 33, "広島県": 34, "山口県": 35, "徳島県": 36, "香川県": 37, "愛媛県": 38,
    "高知県": 39, "福岡県": 40, "佐賀県": 41, "長崎県": 42, "熊本県": 43, "大分県": 44,
    "宮崎県": 45, "鹿児島県": 46, "沖縄県": 47
}

def get_or_create_prefecture(session: Session, pref_name: str, area: float) -> int:
    """県名からJISコードを使ってマスタ登録し、IDを返す"""
    
    # 1. JISコード表からIDを探す
    jis_id = JIS_MAP.get(pref_name)
    if not jis_id:
        raise ValueError(f"エラー: '{pref_name}' のJISコードが見つかりません。")

    # 2. すでにDBにあるか確認
    pref = session.get(Prefecture, jis_id)
    if pref:
        pref.area = area
        session.add(pref)
        session.commit()
        return pref.id
    
    # 3. 未登録なら作成
    new_pref = Prefecture(id=jis_id, name=pref_name, area=area)
    session.add(new_pref)
    session.commit()
    return new_pref.id

def import_prefecture_data(pref_name: str, area: float, daily_csv_path: str, monthly_csv_path: str):
    print(f"=== {pref_name} のデータ移行を開始します ===")

    with Session(engine) as session:
        try:
            # マスタ登録してID取得
            pref_id = get_or_create_prefecture(session, pref_name, area)
            print(f"-> JISコード: {pref_id} ({pref_name}) を使用します")

            # --- 日別データ ---
            df_day = pd.read_csv(daily_csv_path, parse_dates=["Date"])
            # 数値列だけ抽出して平均化
            numeric_cols = df_day.select_dtypes(include='number').columns
            df_day["calc_avg"] = df_day[numeric_cols].mean(axis=1)

            for _, row in df_day.iterrows():
                session.merge(DailySnow(
                    date=row["Date"].date(),
                    prefecture_id=pref_id, # IDで保存
                    avg_depth=row["calc_avg"]
                ))

            # --- 月別データ ---
            df_mon = pd.read_csv(monthly_csv_path)
            df_mon["month_dt"] = pd.to_datetime(df_mon["month"])
            numeric_cols = df_mon.select_dtypes(include='number').columns
            df_mon["calc_avg"] = df_mon[numeric_cols].mean(axis=1)

            for _, row in df_mon.iterrows():
                session.merge(MonthlySnow(
                    month_date=row["month_dt"].date(),
                    prefecture_id=pref_id, # IDで保存
                    avg_snowfall=row["calc_avg"]
                ))
            
            session.commit()
            print(f"★完了: {pref_name} のデータを保存しました\n")

        except Exception as e:
            print(f"エラー発生: {e}")

if __name__ == "__main__":
    create_db_and_tables()
    # ここを実行するだけで、長野県が ID:20 として登録されます
    import_prefecture_data(
        pref_name="大阪府",
        area=1905, 
        daily_csv_path="~/snowman/backend/create_database/data/osaka.csv",
        monthly_csv_path="~/snowman/backend/create_database/data/osaka-mon.csv"
    )
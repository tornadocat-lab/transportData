import mysql.connector
from datetime import time
import os

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'Neko3120'),
    'database': os.getenv('MYSQL_DB', 'transportData'),
}

def get_db_conn():
    return mysql.connector.connect(**DB_CONFIG)

def serialize_time(obj):
    if isinstance(obj, time):
        return obj.strftime('%H:%M') # 只保留 時:分
    # 有些 driver 會回傳 timedelta
    if hasattr(obj, 'total_seconds'): 
        # 處理 timedelta 轉成 HH:MM
        total_seconds = int(obj.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    return str(obj)

def get_stations():
    """取得所有站點名稱與 ID"""
    conn = get_db_conn()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # 確保 SQL 有選取這兩個欄位
            cursor.execute("SELECT DISTINCT station_id, name_zh FROM stations ORDER BY station_id")
            # 直接回傳 fetchall() 的結果，它本身就是 List[dict]
            return cursor.fetchall()
    finally:
        conn.close()

def get_trains_between(from_station, to_station, train_date):
    """查詢經過兩站的所有車次與時間"""
    conn = get_db_conn()
    try:
        with conn.cursor(dictionary=True) as cursor:
            sql = '''
                SELECT 
                    s1.train_date, 
                    s1.train_no, 
                    st1.name_zh AS from_station_name, 
                    s1.departure_time AS from_departure, 
                    st2.name_zh AS to_station_name, 
                    s2.arrival_time AS to_arrival
                FROM stop_times s1
                JOIN stop_times s2 ON s1.train_date = s2.train_date AND s1.train_no = s2.train_no
                JOIN stations st1 ON s1.station_id = st1.station_id
                JOIN stations st2 ON s2.station_id = st2.station_id
                WHERE s1.station_id = %s 
                AND s2.station_id = %s 
                AND s1.stop_sequence < s2.stop_sequence
                AND s1.train_date = %s
                ORDER BY s1.departure_time
            '''
            cursor.execute(sql, (from_station, to_station, train_date))
            results = cursor.fetchall()
            # 序列化 TIME 物件為字串
            for row in results:
                row['from_departure'] = serialize_time(row['from_departure'])
                row['to_arrival'] = serialize_time(row['to_arrival'])
        return results
    finally:
        conn.close()
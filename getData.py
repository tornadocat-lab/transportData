import json
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# 1. 資料庫連線設定
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Neko3120',
    'database': 'transportData'
}

def process_and_import(json_list):
    connection = None
    try:
        # 建立連線
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 遍歷 JSON List 進行處理
            for item in json_list:
                # 這裡調用先前寫好的匯入邏輯
                insert_thsr_data(cursor, item)
            
            # 批次提交，這對效能很重要
            connection.commit()
            print(f"成功匯入 {len(json_list)} 筆車次資料。")

    except Error as e:
        print(f"資料庫連線或操作失敗: {e}")
        if connection:
            connection.rollback() # 失敗就回滾，保持資料一致性
    finally:
        # 確保資源釋放
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL 連線已安全關閉。")

def insert_thsr_data(cursor, data):
    """
    處理單筆車次與停靠站的邏輯 (承接之前的邏輯)
    """
    info = data['DailyTrainInfo']
    train_date = data['TrainDate']
    train_no = info['TrainNo']

    # 寫入主表 (train_schedules)
    main_sql = """
        INSERT INTO train_schedules 
        (train_date, train_no, direction, starting_station_id, ending_station_id, update_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE update_time = VALUES(update_time)
    """
    main_val = (
        train_date, train_no, info['Direction'],
        info['StartingStationID'], info['EndingStationID'],
        data['UpdateTime'].replace('T', ' ').split('+')[0]
    )
    cursor.execute(main_sql, main_val)

    # 寫入從表 (stop_times)
    stop_sql = """
        INSERT INTO stop_times 
        (train_date, train_no, stop_sequence, station_id, arrival_time, departure_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE arrival_time = VALUES(arrival_time)
    """
    stop_vals = [
        (train_date, train_no, s['StopSequence'], s['StationID'], s['ArrivalTime'], s['DepartureTime'])
        for s in data['StopTimes']
    ]
    cursor.executemany(stop_sql, stop_vals)

def batch_import_from_folder(folder_name):
    folder_path = Path(folder_name)
    
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Error: 找不到資料夾 '{folder_name}'")
        return

    # 取得所有 .json 檔案
    json_files = list(folder_path.glob("*.json"))
    print(f"找到 {len(json_files)} 個 JSON 檔案，準備開始匯入...")

    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        for file in json_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 統一轉成 List 處理
                records = data if isinstance(data, list) else [data]
                
                for record in records:
                    insert_thsr_data(cursor, record)
                
                print(f"已處理: {file.name}")
            except Exception as e:
                print(f"處理檔案 {file.name} 時發生錯誤: {e}")
                continue # 某個檔案壞掉就跳過，繼續處理下一個

        connection.commit()
        print("\n--- 所有檔案匯入完成 ---")

    except Error as e:
        print(f"資料庫連線失敗: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    batch_import_from_folder("trainData")

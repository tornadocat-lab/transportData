#基本可用，但容易跳error429，後續需要想辦法處理

import requests
import json
import time
from datetime import date, timedelta
from pathlib import Path

APP_ID = 'fivegeneration1006-42a9e23f-24e0-49af'
APP_KEY = '28fc9342-52e2-4306-aa9b-157b703b69ad'
AUTH_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

class TDXClient:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.token = self._get_token()

    def _get_token(self):
        """初始化時取得一次 Token"""
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.app_id,
            'client_secret': self.app_key
        }
        res = requests.post(AUTH_URL, data=payload)
        return res.json().get('access_token')

    def fetch_date_data(self, target_date):
        """抓取指定日期的車次資料"""
        api_url = f"https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/TrainDate/{target_date}?%24format=JSON"
        headers = {
            'authorization': f'Bearer {self.token}',
            'Accept-Encoding': 'gzip'
        }
        return requests.get(api_url, headers=headers)

if __name__ == '__main__':
    client = TDXClient(APP_ID, APP_KEY)
    
    # 建立資料夾
    folder = Path("trainData")
    folder.mkdir(parents=True, exist_ok=True)

    # 迴圈跑 11 天 (今天 + 往後 10 天)
    for i in range(11):
        # 計算日期
        current_date = (date.today() + timedelta(days=i)).isoformat()
        print(f"正在抓取 {current_date} 的資料...")

        response = client.fetch_date_data(current_date)

        if response.status_code == 200:
            file_path = folder / f"{current_date}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            print(f"-> 已存檔: {file_path}")
        else:
            print(f"-> {current_date} 抓取失敗: {response.status_code}")

        time.sleep(1)

    print("\n--- 所有任務已完成 ---")
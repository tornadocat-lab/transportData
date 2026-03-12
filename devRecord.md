0305
completed:
1. 設計表格
2. 讀取json並將資料放進table中

todos:
1. 功能設計
2. api獲取（註冊, wait for three days

----------------------------------------------------
0306
completed: 
1. 簡易的前端，支援基本查詢
2. 新增表格stations，存放station_id, station_name
3. query 
4. 新增日期選擇

遇到過的問題：
1. ResponseValidationError：在main.py裡限制了, response_model的類型，導致obj無法傳遞
    solve: 取消限制（先確保功能完善後再逐步完善
2. “要不要用空間換時間”：新增stations的表格還是直接修改train_schedule的欄位
    Solve: 考量資料一致性與高鐵站點有限（12 站），捨棄 Denormalization。改採用 Composite Index (station_id, train_date, train_no, departure_time) 達成 Covering Index 優化。
----------------------------------------------------------
0307
completed: 
1. 完成轉程邏輯及其對應的ＵＩ
2. 常用清單
3. transfer buffer

待優化：
    1. 有點兩光的ＵＩ
    2. 資料
    3. 轉成apk

-----------------------------------------------------------
0311
completed:
1. 串接web api key 拿資料


-----------------------------------------------------------
0312
completed:
1. 新增功能：使用者可選擇
    a. 列出當前時間之後的所有車次列表（含轉車)
    b. 最快到達的五個方案
2. 使用dominance principle，確保是按照抵達時間排序，不會出現繞路的狀況

待優化：
感覺還是有些混亂，功能上、func上、邏輯上，感覺有些冗
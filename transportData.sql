CREATE DATABASE transportData;

USE transportData;
-- 車次基本資訊
CREATE TABLE train_schedules (
    train_date DATE,
    train_no VARCHAR(10),
    direction TINYINT, -- 0: 南下, 1: 北上
    starting_station_id VARCHAR(10),
    ending_station_id VARCHAR(10),
    update_time DATETIME,
    PRIMARY KEY (train_date, train_no)
);

-- 停靠站點資訊
CREATE TABLE stop_times (
    train_date DATE,
    train_no VARCHAR(10),
    stop_sequence INT,
    station_id VARCHAR(10),
    arrival_time TIME,
    departure_time TIME,
    PRIMARY KEY (train_date, train_no, stop_sequence),
    FOREIGN KEY (train_date, train_no) REFERENCES train_schedules(train_date, train_no)
);
CREATE TABLE IF NOT EXISTS stations (
    station_id VARCHAR(10) PRIMARY KEY,
    name_zh VARCHAR(20) NOT NULL,
    name_en VARCHAR(50)
);
-- drop table `stations`;

-- INSERT INTO stations (station_id, name_zh, name_en) 
-- VALUES
--     ('0990', '南港', 'Nangang'),
--     ('1000', '台北', 'Taipei'),
--     ('1010', '板橋', 'Banqiao'),
--     ('1020', '桃園', 'Taoyuan'),
--     ('1030', '新竹', 'Hsinchu'),
--     ('1035', '苗栗', 'Miaoli'),
--     ('1040', '台中', 'Taichung'),
--     ('1043', '彰化', 'Changhua'),
--     ('1047', '雲林', 'Yunlin'),
--     ('1050', '嘉義', 'Chiayi'),
--     ('1060', '台南', 'Tainan'),
--     ('1070', '左營', 'Zuoying')
-- AS new_data -- 為插入的資料集取個別名
-- ON DUPLICATE KEY UPDATE 
--     name_zh = new_data.name_zh,
--     name_en = new_data.name_en;

-- 針對起訖站查詢進行優化
CREATE INDEX idx_stop_times_query 
ON stop_times (station_id, train_date, train_no, departure_time);


SHOW INDEX FROM stop_times;
DROP INDEX idx_stop_times_query ON stop_times;

--  drop table `train_schedules`;
--  drop table `stop_times`;

 select * from `train_schedules`;
-- select * from `stop_times`;



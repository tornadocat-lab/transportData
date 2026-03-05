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

describe `train_schedules`;
use  transportData;

drop table `train_schedules`;
drop table `stations`;
drop table `stop_times`;


select distinct train_date from train_schedules;

select  * from stations;
select  * from stop_times;
select  * from train_schedules;

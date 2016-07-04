
DROP TABLE IF EXISTS train_user;

CREATE TABLE  train_user(
user_id VARCHAR(10),
item_id VARCHAR(12),
behavior_type VARCHAR(2),
user_geohash VARCHAR(10),
item_category VARCHAR(8),
time_stamp datetime
);

LOAD DATA LOCAL INFILE '/home/lxin/machinelearning/tianchi/fresh_comp_offline/mobilRecommend/data/tianchi_fresh_comp_train_user_mysql.csv'
INTO TABLE train_user
FIELDS TERMINATED BY ','  OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
ignore 1 lines; 


drop table IF EXISTS train_item;

CREATE TABLE train_item(
item_id VARCHAR(12),
item_geohash VARCHAR(6),
item_category VARCHAR(8)
);

LOAD DATA LOCAL INFILE '/home/lxin/machinelearning/tianchi/fresh_comp_offline/mobilRecommend/data/tianchi_fresh_comp_train_item.csv'   
INTO TABLE train_item    
FIELDS TERMINATED BY ','  OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'   
LINES TERMINATED BY '\n'
ignore 1 lines; 


select *
from UI28Inter
into outfile '/var/lib/mysql-files/UI28Inter.csv'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

select count(distinct item_id)
from train_user
where time_stamp >= '2014-12-1 00:00:00' and
time_stamp < '2014-12-2 00:00:00' and
behavior_type = 4
group by user_id,item_id
into outfile '/var/lib/mysql-files/UI30RealBuy.csv'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';


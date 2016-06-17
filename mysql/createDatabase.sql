
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



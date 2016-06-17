-- 12月18号加入购物车但是没有购买与商品子集求交,并剔除30天都没买东西的人

select distinct user_id, item_id from
(select distinct user_id, item_id from train_user
where time_stamp > '2014-12-18 00:00:00' and
behavior_type = 3) T1
left join 
(select distinct user_id, item_id from train_user
where time_stamp > '2014-12-18 00:00:00' and
behavior_type = 4) T2
using(user_id, item_id)
where T2.user_id is null and
item_id in (SELECT distinct(item_id) FROM train_item) and
user_id in (SELECT user_id from train_user where behavior_type=4 group by user_id)
into outfile '/var/lib/mysql-files/rule.csv'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

-- select * from train_user
-- where time_stamp > '2014-12-18 00:00:00' and user_id = 138560071 AND
-- item_id = 100530226;

select distinct user_id, item_id from
(select distinct user_id, item_id from train_user
where time_stamp > '2014-12-18 15:00:00' and
behavior_type = 3) T1
left join 
(select distinct user_id, item_id from train_user
where time_stamp > '2014-12-18 15:00:00' and
behavior_type = 4) T2
using(user_id, item_id)
where T2.user_id is null and
item_id in (SELECT distinct(item_id) FROM train_item) and
user_id in (SELECT user_id from train_user where behavior_type=4 group by user_id)
into outfile '/var/lib/mysql-files/rule.csv'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

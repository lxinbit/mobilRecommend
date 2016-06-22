select count(item_id) from
(select distinct item_id
from train_user
where time_stamp >= '2014-12-17 00:00:00' and
time_stamp < '2014-12-18 00:00:00' and
behavior_type = 4) T1 inner join (select item_id from train_item) T2
using(item_id);

select count(*) from
(select distinct user_id,item_id
from train_user
where time_stamp >= '2014-12-7 00:00:00' and
time_stamp < '2014-12-16 00:00:00') T1 inner join 
(select distinct user_id,item_id
from train_user
where time_stamp >= '2014-12-16 00:00:00' and
time_stamp < '2014-12-17 00:00:00' and
behavior_type = 4) T2
using(user_id,item_id);

SELECT user_id, item_id,
if(sum(if(behavior_type=3,1,0))>0,1,0)*if(sum(if(behavior_type=4,1,0))=0,1,0) AS Num
FROM train_user
WHERE  time_stamp >= date_sub('2014-12-17 00:00:00', interval 1 hour) and
time_stamp < '2014-12-17 00:00:00'
GROUP BY user_id, item_id;

SELECT user_id, item_id,
count(distinct date(time_stamp)) AS Num
FROM train_user
WHERE  time_stamp >= date_sub('2014-12-17 00:00:00', interval 10 day) and
time_stamp < '2014-12-17 00:00:00'
GROUP BY user_id, item_id;


-- 12-16日(28d)对商品子集的购买数746
-- 12-17日(29d)对商品子集的购买数698
-- 12-18日(30d)对商品子集的购买数767
SELECT COUNT(*) FROM
(SELECT user_id, item_id
FROM train_user
WHERE  time_stamp >'2014-12-16 00:00:00' and
time_stamp < '2014-12-17 00:00:00' AND behavior_type=4
GROUP BY user_id, item_id) T1
INNER JOIN train_item T2
on T1.item_id = T2.item_id;
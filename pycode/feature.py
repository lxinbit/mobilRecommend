# !usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time


def ConnectMysql():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='lx525149',
                           port=3306, db='mobilRecommend')
    return conn


# 统计样本集, (U, I, C)
def QueryUI(tableName, time_start, time_end):
    conn = ConnectMysql()
    cur = conn.cursor()
    # cur.execute("DROP TABLE iF EXISTS %s" % tableName)

    sql = '''
          CREATE TABLE %s AS
          SELECT DISTINCT user_id, item_id, item_category
          FROM train_user
          WHERE time_stamp >= '%s' and time_stamp < '%s'
          ''' % (tableName, time_start, time_end)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


# 提取训练集标签
def QueryLabel(tableName, time_start_label, time_end_label):
    conn = ConnectMysql()
    cur = conn.cursor()
    cur.execute("ALTER TABLE %s ADD COLUMN Label INT DEFAULT 0" % tableName)

    sql = '''
          UPDATE %s T1, (SELECT DISTINCT user_id,  item_id
                         FROM train_user
                         WHERE behavior_type = 4 and
                         time_stamp >= '%s' and time_stamp < '%s') T2
          SET T1.Label = 1
          WHERE T1.user_id = T2.user_id AND
          T1.item_id = T2.item_id
          ''' % (tableName, time_start_label, time_end_label)

    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


#############################################################################
# UI特征
# 用户U对商品I行为次数
def UserActItemCount(tableName, time_start_label, behavior_type, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    behavior = ['Brow', 'Coll', 'Car', 'Buy']
    Column = 'UI' + behavior[behavior_type - 1] + 'Num' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_id, COUNT(*) AS Num
                         FROM train_user
                         WHERE behavior_type = %s and
                         time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_id) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_id = T2.item_id
          ''' % (tableName, behavior_type, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


# 用户U对商品I最早访问时间
def UserItemFirstHourGap(tableName, time_start_label, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    Column = 'UIFirstHourGap' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_id,
                         extract(hour from (timediff('%s',min(time_stamp)))) AS Num
                         FROM train_user
                         WHERE  time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_id) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_id = T2.item_id
          ''' % (tableName, time_start_label, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


# 用户U对商品I最近访问时间
def UserItemLastHourGap(tableName, time_start_label, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    Column = 'UILastHourGap' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_id,
                         extract(hour from (timediff('%s',max(time_stamp)))) AS Num
                         FROM train_user
                         WHERE  time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_id) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_id = T2.item_id
          ''' % (tableName, time_start_label, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


# 用户U对商品I访问的天数
def UserItemActDays(tableName, time_start_label, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    Column = 'UIActDays' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_id,
                         count(distinct date(time_stamp)) AS Num
                         FROM train_user
                         WHERE  time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_id) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_id = T2.item_id
          ''' % (tableName, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


# 用户U对商品I加入购物车但没买,6h,12h,24h
def UserItemIsCarNoBuy(tableName, time_start_label, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    Column = 'UIIsCarNoBuy' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_id,
                         if(sum(if(behavior_type=3,1,0))>0,1,0)*if(sum(if(behavior_type=4,1,0))=0,1,0) AS Num
                         FROM train_user
                         WHERE  time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_id) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_id = T2.item_id
          ''' % (tableName, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
##############################################################################


# UC特征
# 用户U对类别C行为次数
def UserActCateCount(tableName, time_start_label, behavior_type, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    behavior = ['Brow', 'Coll', 'Car', 'Buy']
    Column = 'UC' + behavior[behavior_type - 1] + 'Num' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_category, COUNT(*) AS Num
                         FROM train_user
                         WHERE behavior_type = %s and
                         time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_category) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_category = T2.item_category
          ''' % (tableName, behavior_type, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


# 用户U对类别C有没买过,10day,3day,24h
def UserCateNoBuy(tableName, time_start_label, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    Column = 'UCNoBuy' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, item_category,
                         if(sum(if(behavior_type=4,1,0))=0,1,0) AS Num
                         FROM train_user
                         WHERE  time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id, item_category) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id AND
          T1.item_category = T2.item_category
          ''' % (tableName, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


####################################################################################
# 用户特征
# 用户U行为次数
def UserActCount(tableName, time_start_label, behavior_type, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    behavior = ['Brow', 'Coll', 'Car', 'Buy']
    Column = 'U' + behavior[behavior_type - 1] + 'Num' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT user_id, COUNT(*) AS Num
                         FROM train_user
                         WHERE behavior_type = %s and
                         time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY user_id) T2
          SET T1.%s = T2.Num
          WHERE T1.User_id = T2.User_id
          ''' % (tableName, behavior_type, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


def UserBuyDivOther(tableName, behavior_type, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    behavior = ['Brow', 'Coll', 'Car']
    BuyName = 'UBuy' + 'Num' + str(time_offset) + unit
    OtherName = 'U' + behavior[behavior_type - 1] + 'Num' + str(time_offset) + unit
    Column = 'UBuyDiv' + behavior[behavior_type - 1] + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s FLOAT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s
          SET %s = %s / %s
          WHERE %s != 0;
          ''' % (tableName, Column, BuyName, OtherName, OtherName)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


##############################################################################


# 商品特征
# 商品I行为次数
def ItemActCount(tableName, time_start_label, behavior_type, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    behavior = ['Brow', 'Coll', 'Car', 'Buy']
    Column = 'I' + behavior[behavior_type - 1] + 'Num' + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s INT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s T1, (SELECT item_id, COUNT(*) AS Num
                         FROM train_user
                         WHERE behavior_type = %s and
                         time_stamp >= date_sub('%s', interval %s %s) and
                         time_stamp < '%s'
                         GROUP BY item_id) T2
          SET T1.%s = T2.Num
          WHERE T1.item_id = T2.item_id
          ''' % (tableName, behavior_type, time_start_label, time_offset,
                 unit, time_start_label, Column)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


def ItemBuyDivOther(tableName, behavior_type, time_offset, unit):
    conn = ConnectMysql()
    cur = conn.cursor()
    behavior = ['Brow', 'Coll', 'Car', 'Buy']
    BuyName = 'IBuy' + 'Num' + str(time_offset) + unit
    OtherName = 'I' + behavior[behavior_type - 1] + 'Num' + str(time_offset) + unit
    Column = 'IBuyDiv' + behavior[behavior_type - 1] + str(time_offset) + unit
    cur.execute("ALTER TABLE %s ADD COLUMN %s FLOAT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s
          SET %s = %s / %s
          WHERE %s != 0;
          ''' % (tableName, Column, BuyName, OtherName, OtherName)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


##########################################################################
# UI&UC特征
def IsCarNoBuy_NoBuyCate(tableName, time_offset1, unit1, time_offset2, unit2):
    conn = ConnectMysql()
    cur = conn.cursor()
    IsCarNoBuy = 'UIIsCarNoBuy' + str(time_offset1) + unit1
    UCNoBuy = 'UCNoBuy' + str(time_offset2) + unit2
    Column = IsCarNoBuy + UCNoBuy
    cur.execute("ALTER TABLE %s ADD COLUMN %s FLOAT DEFAULT 0" % (tableName, Column))

    sql = '''
          UPDATE %s
          SET %s = %s * %s;
          ''' % (tableName, Column, IsCarNoBuy, UCNoBuy)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


##########################################################################
# 得到训练or预测表
def GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag):

    # startTotal = time.time()

    # start = time.time()
    # QueryUI(tableName, time_start, time_end)
    # end = time.time()
    # print "样本集查找时间: ", end - start

    # if flag:
    #     start = time.time()
    #     QueryLabel(tableName, time_start_label, time_end_label)
    #     end = time.time()
    #     print "训练样本标签查找时间: ", end - start

    # #######################################################################
    # # UI feature
    # start = time.time()
    # UserActItemCount(tableName, time_start_label, 1, 10, 'day')
    # UserActItemCount(tableName, time_start_label, 2, 10, 'day')
    # UserActItemCount(tableName, time_start_label, 3, 10, 'day')
    # UserActItemCount(tableName, time_start_label, 4, 10, 'day')
    # end = time.time()
    # print "用户对商品行为次数查找时间: ", end - start

    # start = time.time()
    # UserItemFirstHourGap(tableName, time_start_label, 10, 'day')
    # UserItemLastHourGap(tableName, time_start_label, 10, 'day')
    # end = time.time()
    # print "用户对商品最早最晚访问时间查找时间: ", end - start

    # start = time.time()
    # UserItemActDays(tableName, time_start_label, 10, 'day')
    # end = time.time()
    # print "用户U对商品I访问的天数查找时间: ", end - start

    # start = time.time()
    # UserItemIsCarNoBuy(tableName, time_start_label, 6, 'hour')
    # UserItemIsCarNoBuy(tableName, time_start_label, 12, 'hour')
    # UserItemIsCarNoBuy(tableName, time_start_label, 24, 'hour')
    # end = time.time()
    # print "用户U对商品I加入购物车但没买,6h,12h,24h查找时间: ", end - start

    # ##########################################################################
    # # UC feature
    # start = time.time()
    # UserActCateCount(tableName, time_start_label, 1, 10, 'day')
    # UserActCateCount(tableName, time_start_label, 2, 10, 'day')
    # UserActCateCount(tableName, time_start_label, 3, 10, 'day')
    # UserActCateCount(tableName, time_start_label, 4, 10, 'day')
    # end = time.time()
    # print "用户对类别行为次数查找时间: ", end - start

    # start = time.time()
    # UserCateNoBuy(tableName, time_start_label, 24, 'hour')
    # UserCateNoBuy(tableName, time_start_label, 3, 'day')
    # UserCateNoBuy(tableName, time_start_label, 10, 'day')
    # end = time.time()
    # print "用户U对类别没买,24h,3d,10d查找时间: ", end - start

    # ############################################################################
    # # U feature
    # start = time.time()
    # UserActCount(tableName, time_start_label, 1, 10, 'day')
    # UserActCount(tableName, time_start_label, 2, 10, 'day')
    # UserActCount(tableName, time_start_label, 3, 10, 'day')
    # UserActCount(tableName, time_start_label, 4, 10, 'day')
    # end = time.time()
    # print "用户行为次数查找时间: ", end - start

    # start = time.time()
    # UserBuyDivOther(tableName, 1, 10, 'day')
    # UserBuyDivOther(tableName, 2, 10, 'day')
    # UserBuyDivOther(tableName, 3, 10, 'day')
    # end = time.time()
    # print "用户购买除以其他行为查找时间: ", end - start

    # #######################################################################
    # # I feature
    # start = time.time()
    # ItemActCount(tableName, time_start_label, 1, 10, 'day')
    # ItemActCount(tableName, time_start_label, 2, 10, 'day')
    # ItemActCount(tableName, time_start_label, 3, 10, 'day')
    # ItemActCount(tableName, time_start_label, 4, 10, 'day')
    # end = time.time()
    # print "商品行为次数查找时间: ", end - start

    # start = time.time()
    # ItemBuyDivOther(tableName, 1, 10, 'day')
    # ItemBuyDivOther(tableName, 2, 10, 'day')
    # ItemBuyDivOther(tableName, 3, 10, 'day')
    # end = time.time()
    # print "商品购买除以其他行为查找时间: ", end - start

    # #####################################################################
    # # UI&UC feature
    # start = time.time()
    # IsCarNoBuy_NoBuyCate(tableName, 6, 'hour', 24, 'hour')
    # IsCarNoBuy_NoBuyCate(tableName, 12, 'hour', 24, 'hour')
    # IsCarNoBuy_NoBuyCate(tableName, 24, 'hour', 24, 'hour')
    # IsCarNoBuy_NoBuyCate(tableName, 24, 'hour', 3, 'day')
    # end = time.time()
    # print "没买I且没买与I相同类别的商品查找时间: ", end - start

    # endTotal = time.time()
    # print 'total time is: ', endTotal - startTotal

    ####################################################################
    # new feature
    start = time.time()
    UserActItemCount(tableName, time_start_label, 1, 3, 'day')
    UserActItemCount(tableName, time_start_label, 2, 3, 'day')
    UserActItemCount(tableName, time_start_label, 3, 3, 'day')
    UserActItemCount(tableName, time_start_label, 4, 3, 'day')
    end = time.time()
    print "用户对商品行为次数查找时间: ", end - start

    start = time.time()
    UserItemActDays(tableName, time_start_label, 3, 'day')
    end = time.time()
    print "用户U对商品I访问的天数查找时间: ", end - start

    start = time.time()
    UserActCateCount(tableName, time_start_label, 1, 3, 'day')
    UserActCateCount(tableName, time_start_label, 2, 3, 'day')
    UserActCateCount(tableName, time_start_label, 3, 3, 'day')
    UserActCateCount(tableName, time_start_label, 4, 3, 'day')
    end = time.time()
    print "用户对类别行为次数查找时间: ", end - start

    start = time.time()
    UserActCount(tableName, time_start_label, 1, 3, 'day')
    UserActCount(tableName, time_start_label, 2, 3, 'day')
    UserActCount(tableName, time_start_label, 3, 3, 'day')
    UserActCount(tableName, time_start_label, 4, 3, 'day')
    end = time.time()
    print "用户行为次数查找时间: ", end - start

    start = time.time()
    UserBuyDivOther(tableName, 1, 3, 'day')
    UserBuyDivOther(tableName, 2, 3, 'day')
    UserBuyDivOther(tableName, 3, 3, 'day')
    end = time.time()
    print "用户购买除以其他行为查找时间: ", end - start

    start = time.time()
    ItemActCount(tableName, time_start_label, 1, 3, 'day')
    ItemActCount(tableName, time_start_label, 2, 3, 'day')
    ItemActCount(tableName, time_start_label, 3, 3, 'day')
    ItemActCount(tableName, time_start_label, 4, 3, 'day')
    end = time.time()
    print "商品行为次数查找时间: ", end - start

    start = time.time()
    ItemBuyDivOther(tableName, 1, 3, 'day')
    ItemBuyDivOther(tableName, 2, 3, 'day')
    ItemBuyDivOther(tableName, 3, 3, 'day')
    end = time.time()
    print "商品购买除以其他行为查找时间: ", end - start


############################################################################
# 得到与商品子集交集的表
def GetInterTable(tableName):
    conn = ConnectMysql()
    cur = conn.cursor()
    InterTable = tableName + 'Inter'
    sql = '''
          CREATE TABLE %s AS
          SELECT T1.* FROM %s T1 INNER JOIN (SELECT item_id FROM train_item) T2
          ON T1.item_id = T2.item_id
          ''' % (InterTable, tableName)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()


###########################################################################
if __name__ == '__main__':

    # time_start = '2014-12-06 00:00:00'
    # time_end = '2014-12-16 00:00:00'
    # time_start_label = '2014-12-16 00:00:00'
    # time_end_label = '2014-12-17 00:00:00'
    # tableName = 'UI28'

    # start = time.time()
    # flag = True
    # GetTrainOrPredictTable(time_start, time_end, time_start_label,
    #                        time_end_label, tableName, flag)
    # end = time.time()
    # print "Get Train table UI28 time is :", end - start

    # time_start = '2014-12-07 00:00:00'
    # time_end = '2014-12-17 00:00:00'
    # time_start_label = '2014-12-17 00:00:00'
    # time_end_label = '2014-12-18 00:00:00'
    # tableName = 'UI29'

    # start = time.time()
    # flag = True
    # GetTrainOrPredictTable(time_start, time_end, time_start_label,
    #                        time_end_label, tableName, flag)
    # end = time.time()
    # print "Get Train table UI29 time is :", end - start

    time_start = '2014-12-08 00:00:00'
    time_end = '2014-12-18 00:00:00'
    time_start_label = '2014-12-18 00:00:00'
    time_end_label = '2014-12-19 00:00:00'
    tableName = 'UI30'

    start = time.time()
    flag = True
    GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag)
    end = time.time()
    print "Get Train table UI30 time is :", end - start

    time_start = '2014-12-09 00:00:00'
    time_end = '2014-12-19 00:00:00'
    time_start_label = '2014-12-19 00:00:00'
    time_end_label = '2014-12-20 00:00:00'
    tableName = 'UI31'

    start = time.time()
    flag = False
    GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag)
    end = time.time()
    print "Get Predict table UI31 time is :", end - start

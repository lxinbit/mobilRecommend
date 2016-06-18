# !usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time


def ConnectMysql():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='lx525149',
                           port=3306, db='mobilRecommend')
    return conn


# 统计样本集, (U, I)
def QueryUI(tableName, time_start, time_end):
    conn = ConnectMysql()
    cur = conn.cursor()
    # cur.execute("DROP TABLE iF EXISTS %s" % tableName)

    sql = '''
          CREATE TABLE %s AS
          SELECT DISTINCT user_id, item_id
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


##############################################################################


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
    behavior = ['Brow', 'Coll', 'Car', 'Buy']
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
def GetFeature(tableName, time_start_label, time_offset, unit):

    start = time.time()
    UserActItemCount(tableName, time_start_label, 1, time_offset, unit)
    UserActItemCount(tableName, time_start_label, 2, time_offset, unit)
    UserActItemCount(tableName, time_start_label, 3, time_offset, unit)
    UserActItemCount(tableName, time_start_label, 4, time_offset, unit)
    end = time.time()
    print "用户对商品行为次数查找时间: ", end - start

    ########################################################################

    start = time.time()
    UserActCount(tableName, time_start_label, 1, time_offset, unit)
    UserActCount(tableName, time_start_label, 2, time_offset, unit)
    UserActCount(tableName, time_start_label, 3, time_offset, unit)
    UserActCount(tableName, time_start_label, 4, time_offset, unit)
    end = time.time()
    print "用户行为次数查找时间: ", end - start

    start = time.time()
    UserBuyDivOther(tableName, 1, time_offset, unit)
    UserBuyDivOther(tableName, 2, time_offset, unit)
    UserBuyDivOther(tableName, 3, time_offset, unit)
    end = time.time()
    print "用户购买除以其他行为查找时间: ", end - start

    #########################################################################

    start = time.time()
    ItemActCount(tableName, time_start_label, 1, time_offset, unit)
    ItemActCount(tableName, time_start_label, 2, time_offset, unit)
    ItemActCount(tableName, time_start_label, 3, time_offset, unit)
    ItemActCount(tableName, time_start_label, 4, time_offset, unit)
    end = time.time()
    print "商品行为次数查找时间: ", end - start

    start = time.time()
    ItemBuyDivOther(tableName, 1, time_offset, unit)
    ItemBuyDivOther(tableName, 2, time_offset, unit)
    ItemBuyDivOther(tableName, 3, time_offset, unit)
    end = time.time()
    print "商品购买除以其他行为查找时间: ", end - start


# 得到训练or预测表
def GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag):

    startTotal = time.time()

    start = time.time()
    QueryUI(tableName, time_start, time_end)
    end = time.time()
    print "样本集查找时间: ", end - start

    if flag:
        start = time.time()
        QueryLabel(tableName, time_start_label, time_end_label)
        end = time.time()
        print "训练样本标签查找时间: ", end - start

    GetFeature(tableName, time_start_label, 1, 'day')

    endTotal = time.time()
    print 'total time is: ', endTotal - startTotal


if __name__ == '__main__':

    time_start = '2014-12-10 00:00:00'
    time_end = '2014-12-17 00:00:00'
    time_start_label = '2014-12-17 00:00:00'
    time_end_label = '2014-12-18 00:00:00'
    tableName = 'UI29'

    start = time.time()
    flag = True
    GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag)
    end = time.time()
    print "Get Train table UI29 time is :", end - start

    time_start = '2014-12-11 00:00:00'
    time_end = '2014-12-18 00:00:00'
    time_start_label = '2014-12-18 00:00:00'
    time_end_label = '2014-12-19 00:00:00'
    tableName = 'UI30'

    start = time.time()
    GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag)
    end = time.time()
    print "Get Train table UI30 time is :", end - start

    time_start = '2014-12-12 00:00:00'
    time_end = '2014-12-19 00:00:00'
    time_start_label = '0'
    time_end_label = '0'
    tableName = 'UI31'

    start = time.time()
    GetTrainOrPredictTable(time_start, time_end, time_start_label,
                           time_end_label, tableName, flag)
    end = time.time()
    print "Get Predict table UI31 time is :", end - start

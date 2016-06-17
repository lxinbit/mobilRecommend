# !usr/bin/env python
# -*- coding:-utf-8 -*-

infile = "../data/tianchi_fresh_comp_train_user.csv"
outfile = "../data/tianchi_fresh_comp_train_user_mysql.csv"


fp = open(outfile, 'w')
print 'start read file'
with open(infile, 'r') as fp0:
    fp.write(fp0.readline())
    for line in fp0:
        fp.write(line.replace('\r\n', ':00:00\n'))
    fp.close()
print 'over'

#!/usr/bin/env python3

import re
import operator
import csv

INFO = MSG = USER = 0
ERROR = COUNT = 1

# Path to syslog
# syslog_path = "syslog.log"
syslog_path = "C:\\Temp\\PythonPW7\syslog.txt"

# regex
regex = re.compile(r"^[a-zA-Z]{3} [\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2} [\w.]{1,} [\w]{1,}: (?P<msgtype>[A-Z]{1,}) (?P<msg>[\w' ]{1,}) \[{0,1}#{0,1}[0-9]{0,1}[0-9]{0,1}[0-9]{0,1}[0-9]{0,1}\]{0,1}[ ]{0,1}\((?P<username>[\w.]{1,})\)")
# Number of err per err type
err_dict = {}
# Number of info and err per user
err_user = {}

def populate_dicti(per_err, per_user, logs):
    with open(logs) as fd:
        for log in fd.readlines():
            m = regex.match(log)
            if m == None:
                print("UNABLE TO PARSE: {}".format(log))
            else:
                # populating the per user dict
                usr = (m.groupdict()["username"])
                msg = (m.groupdict()["msg"])
                if (m.groupdict()['msgtype'] == 'ERROR'): # Working only on error logs
                    if usr in per_user:
                        per_user[usr][ERROR] += 1
                    else:
                        per_user[usr] = [0, 1]
                    if msg in per_err: # populating the per err dict
                        per_err[msg] += 1
                    else:
                       per_err[msg] = 1
                if (m.groupdict()['msgtype'] == 'INFO'): # Working only on info logs
                    if usr in per_user:
                        per_user[usr][INFO] += 1
                    else:
                        per_user[usr] = [0, 1]

def create_US(file):
    with open(file, 'w') as fdus:
        fdus.write("Username,INFO,ERROR\n")
        for data in (sorted(err_user.items())):
            fdus.write("{},{},{}\n".format(data[USER], data[ERROR][INFO], data[ERROR][ERROR]))

def create_EM(file):
    with open(file, 'w') as fdem:
        fdem.write("Error,Count\n")
        for data in sorted(err_dict.items(), key=operator.itemgetter(COUNT), reverse=True):
            fdem.write("{},{}\n".format(data[MSG], data[COUNT]))

if __name__ == "__main__":

    populate_dict(err_dict, err_user, syslog_path)
    create_US('user_statistics.csv')
    create_EM('error_message.csv')



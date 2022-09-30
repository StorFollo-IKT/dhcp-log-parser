import datetime
import os
from glob import glob
from parse import parse

# path = 'C:\Windows\System32\dhcp'
path = 'logs'

logs = glob(path + '/DhcpSrvLog*')
for log in logs:
    timestamp = os.path.getmtime(log)
    time = datetime.datetime.fromtimestamp(timestamp)
    name, extension = os.path.splitext(log)
    dated_name = '%s %s%s' % (name, time.strftime('%Y-%m-%d'), extension)
    parse(log)
    if not os.path.exists(dated_name):
        os.rename(log, dated_name)

    pass

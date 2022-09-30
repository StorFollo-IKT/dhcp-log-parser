import datetime
import json
import sys

import dateutil.parser
from rich.console import Console
from rich.table import Table

if len(sys.argv) >= 3:
    date_obj = dateutil.parser.parse(sys.argv[2])
else:
    date_obj = datetime.datetime.today()

date = date_obj.strftime('%Y-%m-%d')

with open('logs_parsed/%s.json' % date) as fp:
    data = json.load(fp)

table = Table(title="DHCP events")

fields = ['datetime', 'Description', 'IP Address', 'Host Name', 'MAC Address']

for field in fields:
    table.add_column(field)

for event in data:
    if event['Host Name'].upper().find(sys.argv[1]) == -1 and event['MAC Address'] != sys.argv[1]:
        continue

    row = []

    for field in fields:
        row.append(event[field])
    table.add_row(*row)
    pass

console = Console()
console.print(table)

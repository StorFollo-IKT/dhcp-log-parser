# Event ID  Meaning
# 00	The log was started.
# 01	The log was stopped.
# 02	The log was temporarily paused due to low disk space.
# 10	A new IP address was leased to a client.
# 11	A lease was renewed by a client.
# 12	A lease was released by a client.
# 13	An IP address was found to be in use on the network.
# 14	A lease request could not be satisfied because the scope's address pool was exhausted.
# 15	A lease was denied.
# 16	A lease was deleted.
# 17	A lease was expired and DNS records for an expired leases have not been deleted.
# 18	A lease was expired and DNS records were deleted.
# 20	A BOOTP address was leased to a client.
# 21	A dynamic BOOTP address was leased to a client.
# 22	A BOOTP request could not be satisfied because the scope's address pool for BOOTP was exhausted.
# 23	A BOOTP IP address was deleted after checking to see it was not in use.
# 24	IP address cleanup operation has began.
# 25	IP address cleanup statistics.
# 30	DNS update request to the named DNS server.
# 31	DNS update failed.
# 32	DNS update successful.
# 33	Packet dropped due to NAP policy.
# 34	DNS update request failed.as the DNS update request queue limit exceeded.
# 35	DNS update request failed.
# 36	Packet dropped because the server is in failover standby role or the hash of the client ID does not match.
# 50+	Codes above 50 are used for Rogue Server Detection information.
import json
import os
import sys

import dateutil.parser

events_ignore = [24, 25, 30, 31, 34, 35]


def parse(file_name):
    header = {}
    events = []
    with open(file_name) as fp:
        for line in fp.readlines():
            data = line.strip().split(',')
            if line[0:2] == 'ID':
                header = data
            elif not header:
                continue
            else:
                data = dict(zip(header, data))
                data['ID'] = int(data['ID'])

                if int(data['ID']) in events_ignore:
                    continue

                data['datetime'] = dateutil.parser.parse('%s %s' % (data['Date'], data['Time']))
                events.append(data)

    file = os.path.join('logs_parsed', events[0]['datetime'].strftime('%Y-%m-%d') + '.json')
    if os.path.exists(file):
        return

    with open(file, 'w') as fp:
        json.dump(events, fp, default=str)


if __name__ == '__main__':
    parse(sys.argv[1])

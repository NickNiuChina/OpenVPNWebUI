
#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
""" Update Router53 record for openvpn client and update client status in DB
Parameter:
    option, address, cn[only for op(add, update)]
Returns:
    _type_: None
"""

from __future__ import print_function
import sys
import os
import json
import boto3
import MySQLdb
import datetime
import uuid

def R53_Upsert_A(r53zoneid, record, ip, ttl):

    try:
        botor53client = boto3.client('route53')
        response = botor53client.change_resource_record_sets(
            HostedZoneId=r53zoneid,
            ChangeBatch= {
                    "Comment": "upsert %s <> %s in zone %s" % (record, ip, r53zoneid),
                    'Changes': [
                        {
                         'Action': 'UPSERT',
                         'ResourceRecordSet':
                            {
                             'Name': record,
                             'Type': 'A',
                             'TTL': ttl,
                             'ResourceRecords': [{'Value': ip}]
                            }
                        }
                    ]
            }
        )
    except Exception as e:
        print(e)
        exit(1)


def R53_Delete_A(r53zoneid, record, ip, ttl):
    try:
        botor53client = boto3.client('route53')
        response = botor53client.change_resource_record_sets(
            HostedZoneId=r53zoneid,
            ChangeBatch= {
                    "Comment": "delete %s in zone %s" % (record, r53zoneid),
                    'Changes': [
                        {
                         'Action': 'DELETE',
                         'ResourceRecordSet':
                            {
                             'Name': record,
                             'Type': 'A',
                             'TTL': ttl,
                             'ResourceRecords': [{'Value': ip}]
                            }
                        }
                    ]
            }
        )
    except Exception as e:
        print(e)
        exit(1)


def openvpn_ipp_get_cn(ipp_filename, ip):
    try:
        with open(ipp_filename, "r") as f:
            for line in f:
                l = line.strip().split(',')[0:2]
                cn = l[0]
                ipp = l[1]
                if ip == ipp:
                    return cn
    except:
        return None


def openvpn_get_ipp_filename(cfg_filename):
    try:
        with open(cfg_filename, "rt") as f:
            for line in f:
                if 'ifconfig-pool-persist' in line:
                    x = line.strip().split()
                    if 'ifconfig-pool-persist' == x[0]:
                        return x[1]
    except:
        return None

def log(lines):
    for line in lines.strip().split("\n"):
        print(os.path.basename(__file__) + " " + line)

config = {
    "server_name": "openvpn-udp-tun-1194",
    "db_host": '127.0.0.1',
    "db_port": 3306,
    "db_name": "ovpnmgmt",
    "db_user": "root",
    "db_password": "rootroot",
    "openvpn_service_table": "ovpn_servers",
    "openvpn_client_table": "ovpn_clientlist"
}


def op_db_ovpn_client_status(op, cn, ip):
    try:
        conn = MySQLdb.connect(
            db=config["db_name"],
            user=config["db_user"],
            password=config["db_password"],
            host=config["db_host"],
            port=config["db_port"]
            )
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        sql = """SELECT cn FROM {} where cn = %s""".format(config["openvpn_client_table"])
        input=(cn,)
        cur.execute(sql, input)
        result = cur.fetchall()
        if op == "update" or op == "add":
            status = 1
        else:
            status = 0
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if result:
            log ("CN: %s found, will update the status now." % cn)
            log ("Prepared SQL:")
            sql = """UPDATE {} SET ip = %s, toggle_time = %s, status = %s, update_time = %s WHERE cn = %s""".format(config["openvpn_client_table"])
            input = (ip, times, status, datetime.datetime.now(), cn)
            log ( sql + " With args: " + str(input))
            result = cur.execute(sql, input)            
            conn.commit()
            conn.close()
            if result > 0:
                 log ("Successfully insert the above record.")               
            else:
                log ("ERROR: Failed to insert the above record.")
            log ("\t Update sql exec done.")
        else:
            if op == "update" or op == "add":
                log ("CN: %s not found, will and the status list now." % cn)
                log ("Get OpenVPN service UUID:")
                sql = """ select id from {} where server_name=%s""".format(config["openvpn_service_table"])
                cur.execute(sql, (config["server_name"],))
                result = cur.fetchone()
                service_uuid = result["id"]
                log ("Prepared Update SQL:")
                sql = """INSERT INTO {} (id, cn, ip, toggle_time, expire_date, status, create_time, update_time, server_id, enabled) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(config["openvpn_client_table"])
                input = (uuid.uuid4().hex, cn, ip, times, datetime.datetime(1970, 1, 1),status, datetime.datetime.now(), datetime.datetime.now(), service_uuid, 1)
                log (sql + " With args: " + str(input))
                result = cur.execute(sql, input)
                if result > 0:
                    log ("Successfully update the above record.")               
                else:
                    log ("ERROR: Failed to update the above record.")
                log("result: " + str(result))
                conn.commit()
                conn.close()
                log ("Insert sql exec done.")
            if op == "delete":
                log ("CN: %s not found, try to delete an list which does not exist!!" % cn)
    except Exception as e:
        log ("Exception Occured: %s" % e)
        exit (0)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print("Syntax: add|update|delete <ipaddress> [<CertificateCN>]")
            exit(3)

        log ("executed start!")
        log ("***************************************************************")
        # OPENVPN_CACHE_JSON_FILENAME = r'/run/shm/openvpn-cloud-init.json'
        # with open(OPENVPN_CACHE_JSON_FILENAME) as cache_json_file:
        #     cfgcache_json = json.load(cache_json_file)

        # if cfgcache_json['DIRTY'] == True:
        #     print("FATAL ERROR: JSON Config Cache is corrupt")
        #     exit(5)

        # SSMPATH=cfgcache_json['AWS_EC2_TAGS']['SSMPath']

        # domain=cfgcache_json['AWS_SSM'][SSMPATH+'OpenVPN_R53_ZONE_NAME']
        # zoneid=cfgcache_json['AWS_SSM'][SSMPATH+'OpenVPN_R53_ZONE_ID']


        op = sys.argv[1]
        ip = sys.argv[2]
        if op == 'update' or op == 'add':
            if len(sys.argv) != 4:
                exit(3)
            cn = sys.argv[3]
            # record = cn + '.' + domain
            # print("config=%s - %s: %s %s" % (os.environ['config'],op,ip,record))
            # R53_Upsert_A(zoneid, record, ip, 60)
        elif op == 'delete':
            cn = openvpn_ipp_get_cn(openvpn_get_ipp_filename("openvpn-udp-tun-1194.conf"), ip)
            # record = cn + '.' + domain
            # print("config=%s - %s: %s %s" % (os.environ['config'],op,ip,record))
            # R53_Delete_A(zoneid, record, ip, 60)

        else:
            exit(1)
        log("op: " + op + " " + "cn: " + cn + " " + "ip: " + ip)
        op_db_ovpn_client_status(op, cn, ip)
        log("executed done!")
        log ("***************************************************************")
        exit(0)
    except Exception as e:
        print("Exception Occured: %s" % e)
        exit(5)
        
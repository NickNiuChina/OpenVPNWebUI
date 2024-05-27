#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from __future__ import print_function
import sys, os, json, boto3

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
                cn,ipp = line.strip().split(',')
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


if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print("Syntax: add|update|delete <ipaddress> [<CertificateCN>]")
            exit(3)


        OPENVPN_CACHE_JSON_FILENAME = r'/run/shm/openvpn-cloud-init.json'
        with open(OPENVPN_CACHE_JSON_FILENAME) as cache_json_file:
            cfgcache_json = json.load(cache_json_file)

        if cfgcache_json['DIRTY'] == True:
            print("FATAL ERROR: JSON Config Cache is corrupt")
            exit(5)

        SSMPATH=cfgcache_json['AWS_EC2_TAGS']['SSMPath']

        domain=cfgcache_json['AWS_SSM'][SSMPATH+'OpenVPN_R53_ZONE_NAME']
        zoneid=cfgcache_json['AWS_SSM'][SSMPATH+'OpenVPN_R53_ZONE_ID']


        op = sys.argv[1]
        ip = sys.argv[2]
        if op == 'update' or op == 'add':
            if len(sys.argv) != 4:
                exit(3)
            cn = sys.argv[3]
            record = cn + '.' + domain
            print("config=%s - %s: %s %s" % (os.environ['config'],op,ip,record))
            R53_Upsert_A(zoneid, record, ip, 60)
        elif op == 'delete':
            cn = openvpn_ipp_get_cn(openvpn_get_ipp_filename(os.environ['config']), ip)
            record = cn + '.' + domain
            print("config=%s - %s: %s %s" % (os.environ['config'],op,ip,record))
            R53_Delete_A(zoneid, record, ip, 60)
            exit(0)
        else:
            exit(1)
    except Exception as e:
        print("Exception Occured: %s" % e)
        exit(5)

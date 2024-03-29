#!/usr/bin/python3
import requests
import socket
import sys
global domainlist
global outputfile
global resfile

try:
    domainlist = sys.argv[1]
except Exception as e:
    print('[ERROR] Please provide domain list!')
    exit()

try:
    outputfile = sys.argv[2]
except Exception as e:
    print('[ERROR] Please provide output file!')
    exit()

try:
    resfile = sys.argv[3]
except Exception as e:
    print('[ERROR] Please provide output file!')
    exit()


def check_domain(d):
    try:
        data = socket.gethostbyname(d)
        write_file(d, resfile)
        return False
    except Exception:
        return True


def write_file(data, file):
    try:
        with open(file, 'a+') as line:
            line.write(data+'\n')

    except Exception as e:
        print('Something went wrong while writing the file!!! <<{}>> '.format(e))


def domaincount():
    try:
        totaldomains = 0
        with open(domainlist, 'r') as f:
            for i in f:
                totaldomains = totaldomains + 1
        return totaldomains
    except Exception as e:
        print('Something went wrong while reading the file!!! <<{}>> '.format(e))
        exit()


if __name__ == '__main__':
    try:
        count = 0
        totalcount = domaincount()
        with open(domainlist, 'r') as domains:
            for domain in domains:
                count = count + 1
                if not check_domain(domain.strip()):
                    continue
                print('Checking for {} in wayback machine!!! ({}/{})'.format(domain,count,totalcount))
                r = requests.get(url='http://archive.org/wayback/available?url={}'.format(domain))
                data = r.json()
                if len(data['archived_snapshots']) > 0:
                    print("[OK]WayBack found!!! ::: URL : {}\n".format(data['archived_snapshots']['closest']['url']))
                    write_file(data['archived_snapshots']['closest']['url'], outputfile)
                else:
                    print("[EH]WayBack not found!!!\n")
        print('Dumped all the positive url to {}'.format(outputfile))
    except Exception as e:
        print('Something went wrong!!! <<{}>> '.format(e))

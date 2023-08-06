from IPy import IP
import re


def IPSplitStar(ips):  # 192.168.1.*  --->   192.168.1.1   到    192.168.1.255
    ip_1 = ips.split('.')[-4]
    ip_2 = ips.split('.')[-3]
    ip_3 = ips.split('.')[-2]
    ip_4 = ips.split('.')[-1]
    ip_to = []
    for i in range(1, 256):
        ip_result = ip_1 + '.' + ip_2 + '.' + ip_3 + '.' + str(i)
        ip_to.append(ip_result)
    return ip_to


def IPSplit_Star(ips):  # 192.168.1-10.*
    ip_1 = ips.split('-')[-2].split('.')[-3]
    ip_2 = ips.split('-')[-2].split('.')[-2]
    ip_3 = ips.split('-')[-2].split('.')[-1]  # 1
    ip_last = ips.split('-')[-1]  # 10
    ip_last_1 = ip_last.split('.')[-2]
    ip_3p = []
    for i in range(int(ip_3), int(ip_last_1) + 1):
        for j in range(1, 256):
            ip_3p.append(ip_1 + '.' + ip_2 + '.' + str(i) + '.' + str(j))
    return ip_3p


def IPSplit(ip2ip_str):
    dic = []
    dic1 = []
    # filename = 'IP-range.txt'       #IP segment filename to be processed
    # fo = open(filename,"r")
    for line in ip2ip_str:  # for line in fo:
        data = line
        ips = re.search(r'((2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)\.){3}(2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)[-/]',
                        line)  # Select the network segment type
        if (ips != None):
            ips = re.search(r'((2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)\.){3}(2[0-4]\d|25[0-5]|[01]{0,1}\d{0,1}\d)[/]',
                            line)  # Separate/type and -type

            # Processing/type
            if (ips != None):
                ip = IP(data)
                for x in ip:
                    dic.append(str(x))

            # process-type
            else:
                ip_1 = line.split('-')[-2].split('.')[-4]
                ip_2 = line.split('-')[-2].split('.')[-3]
                ip_3 = line.split('-')[-2].split('.')[-2]
                ip_4 = line.split('-')[-2].split('.')[-1]
                ip_last = line.split('-')[-1]
                ip_last.strip()
                ip_len = int(ip_last) - int(ip_4) + 1
                for i in range(ip_len):
                    ip_last = int(ip_4) + i
                    ip_result = ip_1 + '.' + ip_2 + '.' + ip_3 + '.' + str(ip_last)
                    dic.append(ip_result)
        else:
            # dic.append(data)
            if '*' in line and '-' in line:
                dic = dic + IPSplit_Star(line)
            elif '*' in line:
                dic = dic + IPSplitStar(line)
            else:
                dic.append(line)
    # print '查看结果  开始'
    # print dic
    # print '查看结果  结束'
    return list(set(dic))  # 目的是为了去重


def IPSplitBlocks(ip2ip_str):  # 192.168.1.250-192.168.2.5
    ipx = ip2ip_str.split('-')
    ip2num = lambda x: sum([256 ** i * int(j) for i, j in enumerate(x.split('.')[::-1])])
    num2ip = lambda x: '.'.join([str(x // (256 ** i) % 256) for i in range(3, -1, -1)])
    a = [num2ip(i) for i in range(ip2num(ipx[0]), ip2num(ipx[1]) + 1) if not ((i + 1) % 256 == 0 or (i) % 256 == 0)]
    return a


def IPSplit_d(line):
    """
    分割网段形如192.168.1.0-255
    """
    return [str(i) for i in IP(line)]
# !/usr/bin/env python3
# coding=utf-8
__Author__ = 'Hanson'

import time
import json
import requests


def time_to_timestamp(time1):  # 对应time_data1
    # 传入可读正常日期时间,比如'2019-08-01 00:00:00'，类型为str
    data_str = time.strptime(time1, "%Y-%m-%d %H:%M:%S")  # 定义时间格式
    time_int = int(time.mktime(data_str))  # 正常时间转换为时间戳
    return time_int  # 返回传入时间的时间戳，类型为int


def timestamp_to_time(timestamp1):  # 对应time_data2
    # 传入时间的时间戳，比如'1583909443',类型为int
    data_str = time.localtime(int(timestamp1))  # 时间戳转换为正常时间
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", data_str)  # 定义时间格式
    return time_str  # 返回可读正常日期，类型为str


# noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker
class LibrenmsAPI(object):
    # 初始化参数
    def __init__(self, service_url, token):
        self.service_url = service_url
        self.token = token

    # 通用requests调用函数
    def get_res_token(self, url, mode, data=None):
        headers = {
            'Accept-Charset': 'UTF-8',
            'Content-Type': "application/json",
            'X-Auth-Token': self.token
        }
        res = "none"
        if mode == "get":
            response = requests.get(url, json=data, headers=headers)
            res = json.loads(response.text)

        elif mode == "post":
            # data_json = json.dumps(data)
            response = requests.post(url, json=data, headers=headers)  # 此处一定是json=data，否则不能使用
            res = json.loads(response.text)
        elif mode == "put":
            response = requests.put(url, json=data, headers=headers)
            res = json.loads(response.text)
        elif mode == "delete":
            response = requests.delete(url, json=data, headers=headers)
            res = json.loads(response.text)
        elif mode == "patch":
            response = requests.patch(url, json=data, headers=headers)
            res = json.loads(response.text)
        return res

    # noinspection PyTypeChecker
    def get_device_info(self, ip):
        # 根据设备ip获取详细信息
        device_info = self.get_res_token(self.service_url + "/devices/" + ip, "get")
        if device_info['status'] == "ok":
            # res = device_info['devices'][0]
            return device_info

    def get_device(self, type1="all", query_str=None):
        """
        :param type1 all,up,down,active,ignored,disabled,ipv4,ipv6,hostname
        :param query_str 具体数值
        """
        # 获取所有设备信息
        data_dict = {"type": type1,
                     "query": query_str,
                     }
        device_info = self.get_res_token(self.service_url + "/devices", "get", data_dict)
        # noinspection PyTypeChecker
        if device_info['status'] == "ok":
            # res = device_info['devices']
            return device_info

    def add_device(self, hostname, ip, port, community, version="v2c", poller_group=0, force_add=True):
        # 添加设备
        data_dict = {
            "hostname": hostname,
            "overwrite_ip": ip,
            "port": port,
            "community": community,
            # "transport": transport,
            "version": version,
            "poller_group": poller_group,
            "force_add": force_add,
        }
        device_info = self.get_res_token(self.service_url + "/devices", "post", data_dict)
        if device_info['status'] == "ok":
            return device_info

    def delete_device(self, ip):
        # 根据设备ip获取详细信息
        device_info = self.get_res_token(self.service_url + "/devices/" + ip, "delete")
        if device_info['status'] == "ok":
            return device_info

    def update_device(self, deviceID, data_dict):
        # 根据设备主机名修改相关信息
        device_info = self.get_res_token(self.service_url + "/devices/" + str(deviceID), "patch", data_dict)
        if device_info['status'] == "ok":
            return device_info
        # elif device_info['status'] == "error":
        #     return device_info

    def get_device_log(self, deviceID, log_type="eventlog"):
        # 根据设备主机名获取日志信息 log_type：eventlog，syslog，alertlog，authlogv0/logs/eventlog/:hostname
        device_log = self.get_res_token(self.service_url + "/logs/" + str(log_type) + "/" + str(deviceID), "get")
        if device_log['status'] == "ok":
            return device_log

    def get_group(self):
        # 获取所有群组信息
        group_info = self.get_res_token(self.service_url + "/devicegroups", "get")
        if group_info['status'] == "ok":
            return group_info

    def get_device_by_group(self, group_name):
        # 根据群组获取设备信息
        group_info = self.get_res_token(self.service_url + "/devicegroups/" + str(group_name), "get")
        if group_info['status'] == "ok":
            return group_info

    def add_group(self, group_name, group_type, desc=None, device_id_list=None, rule_dict=None):
        # 添加群组，静态和动态，group_type为dynamic和static两种
        data_dict = {"name": group_name,
                     "type": group_type,
                     "desc": desc,
                     }
        print(type(device_id_list), device_id_list)
        if group_type == "static":
            data_dict['devices'] = device_id_list
        elif group_type == "dynamic":
            data_dict['rules'] = rule_dict
        print("data_dict:", data_dict)
        group_info = self.get_res_token(self.service_url + "/devicegroups", "post", data_dict)
        return group_info
        # if group_info['status'] == "ok":
        #     return group_info

    def get_system_info(self):
        # 获取系统信息
        system_info = self.get_res_token(self.service_url + "/system", "get")
        if system_info['status'] == "ok":
            return system_info


if __name__ == "__main__":
    print("LibrenmsAPI调用")
    LibrenmsAPI_1 = LibrenmsAPI("http://124.250.245.138:8001/api/v0", "da1932db082292c4fbae9cd840f33d4d")
    # res = LibrenmsAPI_1.get_device_info("211.99.176.11")
    res = LibrenmsAPI_1.get_device("ipv4", "211.99.192.245")
    # res = LibrenmsAPI_1.add_device(789, "120.133.15.66", 161, "WG@21vianet-RO")
    # res = LibrenmsAPI_1.delete_device("211.151.128.250")
    # data_dict = {"field": "overwrite_ip", "data": "211.151.227.238"}  # 修改ip的前提是前后IP都是同一个厂商的，否则web设备列表不会及时更新
    # res = LibrenmsAPI_1.update_device(14, data_dict)
    # res = LibrenmsAPI_1.update_device(456, data_dict)  # 如果设备主机名是数字的话，用主机名进行更新会失败，它会自动人为是设备ID，因此会找不到
    # res = LibrenmsAPI_1.update_device("211.99.176.11", data_dict)
    # res = LibrenmsAPI_1.get_device_log(14)
    # res = LibrenmsAPI_1.get_group()
    # res = LibrenmsAPI_1.get_device_by_group("H3c")
    # res = LibrenmsAPI_1.get_system_info()
    print(res)

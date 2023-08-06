本模块是librenms 官方api的python版本模块，结合官方api实现了更加复杂的功能，调用起来相当方便：

1. *根据设备IP获取具体信息*，对应函数 *get_device_info*

    

以上功能使用首先实例化类，然后调用各个函数调用，也可以根据 需求查看源码进行二次开发使用：

```
from librenms import LibrenmsAPI

if __name__=="__main__":
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
```

以上是部分测试代码，大家可以放心使用

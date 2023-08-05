#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
import inspect
import os
import re
import uuid

RE_IGNORE_PATH = os.getenv("FastTracker_ReIgnorePath") or re.compile("^$")  # type: re.Pattern

service_instance = os.getenv("FastTracker_Instance") or str(uuid.uuid1()).replace("-", "")  # type: str
protocol = (os.getenv("FastTracker_Protocol") or "udp").lower()  # type: str
ignore_suffix = (
    os.getenv("FastTracker_IgnoreSuffix") or ".jpg,.jpeg,.js,.css,.png,.bmp,.gif,.ico,.mp3," ".mp4,.html,.svg "
)  # type: str
correlation_element_max_number = int(os.getenv("FastTracker_CorrelationElementMaxNumber") or "3")  # type: int
correlation_value_max_length = int(os.getenv("FastTracker_CorrelationValueMaxLength") or "128")  # type: int
trace_ignore_path = os.getenv("FastTracker_IgnorePath") or ""  # type: str

############################# fast_tracker默认配置信息开始 ###############################
# agent全局开关，默认false
enable = False  # type: bool
# 环境编码 默认test
env_code = "test"  # type: str
# 日志等级 默认 DEBUG
log_level = "ERROR"  # type: str
# 租户编码 默认zsdc
tenant_code = ""  # type: str
# 用户编码 默认zhangsan
user_code = ""  # type: str
# 服务名称 默认"天眼平台"
service_name = ""  # type: str
# 产品编码 默认fast
product_code = ""  # type: str
# 服务编码 默认"analysis"
app_code = ""  # type: str
# 上报地址 默认"udp://127.0.0.1:5140"
collector_address = ""  # type: str
# 缓冲区大小 默认1
buffer_size = 1  # type: int
# 上报超时时间 默认1（秒）
socket_timeout = 1  # type: int
# 兼容原Event模块，目前一般只有Components
event = {"Components": {"SqlClient": True, "HttpClient": True}}
# 租户code，一般SaaS化租户会在运行时才知道此值，所以动态传值，ReaderType表示从哪里获取，ReaderKey表示字段名称
# tenant_code_reader = {"ReaderType": "Cookie", "ReaderKey": "tenant_code"}
# tenant_code_reader = {"ReaderType": "RequestHeader", "ReaderKey": "tcode"}
tenant_code_reader = {"ReaderType": "QueryString", "ReaderKey": "tentcode"}
# 用户code，一般会在运行时才知道此值，所以动态传值，ReaderType表示从哪里获取，ReaderKey表示字段名称
user_code_reader = {"ReaderType": "Cookie", "ReaderKey": "user_code"}
# 环境code，一般会在运行时才知道此值，所以动态传值，ReaderType表示从哪里获取，ReaderKey表示字段名称
env_code_reader = {"ReaderType": "Cookie", "ReaderKey": "env_code"}
# 前端Header
carrier_header = {"TrackerName": "fast-tracker", "TraceIdName": "x-fast-trace-id"}
############################# fast_tracker默认配置信息结束 ###############################


def init(
    service: str = None, instance: str = None, collector: str = None, protocol_type: str = "udp", token: str = None
):
    # 先根据环境变量 FastTracker_ConfigPath 加载配置文件并赋值
    config_file = os.environ.get("FastTracker_ConfigPath", None)
    print("FAST: FastTracker_ConfigPath is %s " % config_file)
    from fast_tracker.fast_tracker_configer import FastTrackerConfiger

    if config_file:
        FastTrackerConfiger.load_configuration(config_file)

    # 再根据环境变量加载配置
    FastTrackerConfiger.set_config_by_env()

    # 再自定义设置的配置
    global service_name
    service_name = service or service_name

    global service_instance
    service_instance = instance or service_instance

    global collector_address
    collector_address = collector or collector_address

    global protocol
    protocol = protocol_type or protocol


def set_enable(cus_enable: bool = False):
    """
    设置enable值
    :param cus_enable:
    :return:
    """
    global enable
    enable = cus_enable


def set_env_code(cus_env_code: str = ""):
    """
    设置env_code值
    :param cus_env_code:
    :return:
    """
    global env_code
    env_code = cus_env_code


def set_tenant_code(cus_tenant_code: str = ""):
    """
    设置tenant_code值
    :param cus_tenant_code:
    :return:
    """
    global tenant_code
    tenant_code = cus_tenant_code


def set_user_code(cus_user_code: str = ""):
    """
    设置user_code值
    :param cus_user_code:
    :return:
    """
    global user_code
    user_code = cus_user_code


def set_product_code(cus_product_code: str = ""):
    """
    设置 product_code 值
    :param cus_product_code:
    :return:
    """
    global product_code
    product_code = cus_product_code


def set_app_code(cus_app_code: str = ""):
    """
    设置 app_code 值
    :param cus_app_code:
    :return:
    """
    global app_code
    app_code = cus_app_code


def set_service_name(cus_service_name: str = ""):
    """
    设置 service_name 值
    :param cus_service_name:
    :return:
    """
    global service_name
    service_name = cus_service_name


def set_socket_path(cus_collector_address: str = ""):
    """
    设置 collector_address 值
    :param cus_collector_address:
    :return:
    """
    global collector_address
    collector_address = cus_collector_address


def set_buffer_size(cus_buffer_size: int = 1):
    """
    设置 buffer_size 值
    :param cus_buffer_size:
    :return:
    """
    global buffer_size
    buffer_size = cus_buffer_size


def set_socket_timeout(cus_socket_timeout: int = 1):
    """
    设置 socket_timeout 值
    :param cus_socket_timeout:
    :return:
    """
    global socket_timeout
    socket_timeout = cus_socket_timeout


def set_event(cus_event: dict):
    """
    设置 event 值
    :param cus_event:
    :return:
    """
    global event
    if not cus_event:
        return False
    event = cus_event


def set_tenant_code_reader(cus_tenant_code_reader: dict):
    """
    设置 tenant_code_reader 值
    :param cus_tenant_code_reader:
    :return:
    """
    global tenant_code_reader
    if not cus_tenant_code_reader:
        return False
    tenant_code_reader = cus_tenant_code_reader


def set_user_code_reader(cus_user_code_reader: dict):
    """
    设置 user_code_reader 值
    :param cus_user_code_reader:
    :return:
    """
    global user_code_reader
    if not cus_user_code_reader:
        return False
    user_code_reader = cus_user_code_reader


def set_carrier_header(cus_carrier_header: dict):
    """
    设置 carrier_header 值
    :param cus_carrier_header:
    :return:
    """
    global carrier_header
    if not cus_carrier_header:
        return False
    carrier_header = cus_carrier_header


def set_env_code_reader(cus_env_code_reader: dict):
    """
    设置 env_code_reader 值
    :param cus_env_code_reader:
    :return:
    """
    global env_code_reader
    if not cus_env_code_reader:
        return False
    env_code_reader = cus_env_code_reader


def set_trace_id_name(trace_id_name: str):
    """
    设置trace_id_name
    :param str trace_id_name:
    :return:
    """
    global carrier_header
    if not trace_id_name:
        return False
    carrier_header["TraceIdName"] = trace_id_name


def get_trace_id_name():
    """
    获取trace_id_name
    :return str
    """
    global carrier_header
    return carrier_header.get("TraceIdName")


def set_tracker_name(tracker_name):
    """
    设置 tracker_name
    :param tracker_name:
    :return:
    """
    global carrier_header
    if not tracker_name:
        return False
    carrier_header["TrackerName"] = tracker_name


def get_tracker_name():
    """
    获取 tracker_name
    :return str
    """
    global carrier_header
    return carrier_header.get("TrackerName")


def finalize():
    """
    通过忽略后缀的文件找到忽略的文件夹
    :return:
    """
    reesc = re.compile(r"([.*+?^=!:${}()|\[\]\\])")
    suffix = r"^.+(?:" + "|".join(reesc.sub(r"\\\1", s.strip()) for s in ignore_suffix.split(",")) + ")$"
    path = (
        "^(?:"
        + "|".join(  # replaces ","
            "(?:(?:[^/]+/)*[^/]+)?".join(  # replaces "**"
                "[^/]*".join(  # replaces "*"
                    "[^/]".join(reesc.sub(r"\\\1", s) for s in p2.split("?")) for p2 in p1.split("*")  # replaces "?"
                )
                for p1 in p0.strip().split("**")
            )
            for p0 in trace_ignore_path.split(",")
        )
        + ")$"
    )

    global RE_IGNORE_PATH
    RE_IGNORE_PATH = re.compile("%s|%s" % (suffix, path))


def serialize():
    from fast_tracker import config

    return {
        key: value
        for key, value in config.__dict__.items()
        if not (
            key.startswith("_")
            or key == "TYPE_CHECKING"
            or key == "RE_IGNORE_PATH"
            or inspect.isfunction(value)
            or inspect.ismodule(value)
            or inspect.isbuiltin(value)
            or inspect.isclass(value)
        )
    }


def deserialize(data):
    from fast_tracker import config

    for key, value in data.items():
        if key in config.__dict__:
            config.__dict__[key] = value
    finalize()

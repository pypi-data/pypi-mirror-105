#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by iprobeyang@gmail.com 2021/5/14
"""
# a = "http://localhost:8111/api/err"
a = "localhost:8111/api/err"
# b = a.split("//")
# print(b[1])
# c = b[1].split("/")
# print(c)
# del c[0]
# print(c)
# print("/"+"/".join(c))

def get_url_path(url):
    split_args = url.split("//")
    path = split_args[0] if len(split_args) == 1 else split_args[1]
    path_list = path.split("/")
    del path_list[0]
    return "/" + "/".join(path_list)

a = "http://localhost:8111"
print(get_url_path(a))
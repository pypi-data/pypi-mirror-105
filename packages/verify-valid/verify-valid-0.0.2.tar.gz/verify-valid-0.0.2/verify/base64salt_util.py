# !/usr/bin/env python
# encoding: utf-8

import base64
import hashlib
import re
from itertools import chain


def base_encode(string):
    if string:
        salt = hashlib.sha256("hisuntest@#".encode('utf-8')).hexdigest()
        pattern_one = re.compile('.{16}')
        a = pattern_one.findall(salt)
        handle_string = base64.b64encode(string.encode("utf-8"))
        pattern_two = re.compile('.{5}')
        b = pattern_two.findall(handle_string.decode("utf-8"))
        c = list(chain.from_iterable(zip(a, b)))
        d = "".join([x for x in c])
        final_string = base64.b64encode(d.encode("utf-8"))
        return final_string
    else:
        raise ValueError


def base_decode(string):
    if string:
        handle_result = base64.b64decode(string).decode("utf-8")
        b = handle_result[16:21] + handle_result[37:42] + handle_result[58:63] + handle_result[79:84]
        result = base64.b64decode(b).decode("utf-8")
        return result
    else:
        raise ValueError

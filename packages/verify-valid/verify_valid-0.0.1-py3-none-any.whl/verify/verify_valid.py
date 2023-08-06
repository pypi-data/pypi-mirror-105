# !/usr/bin/env python
# encoding: utf-8

import base64
import hashlib
import re
from itertools import chain
import os
import pathlib
from base64salt_util import base_decode


class VerifyValid:
    def __init__(self, file_path):
        if file_path:
            self.file_path = file_path

    def verify(self):
        try:
            path = pathlib.Path(self.file_path)
            boolean = path.is_file()
            if boolean:
                with open(self.file_path) as f:
                    content = f.read()
                    if content:
                        result = base_decode(content)
                        return result
            else:
                raise FileNotFoundError
        except FileNotFoundError as e:
            print("FileNotFoundError", e)
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError", e)


if __name__ == "__main__":
    file_path = r'D:\PyCharmProject\hall\register.hisuntest'
    # file_path = r'D:\PyCharmProject\hall\223232111111.txt'

    result = VerifyValid(file_path).verify()
    print("result", result)


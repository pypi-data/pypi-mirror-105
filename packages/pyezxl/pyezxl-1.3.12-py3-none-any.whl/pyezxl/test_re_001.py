# -*- coding: utf-8 -*-

import pyezxl_re

aaa=pyezxl_re.pyezxl_re()

ggg="(20년 정수)전해 소금야적장 장장컨베어 소금야적장보수작업(Z-012,015,9012,9015)"
zzz = aaa.between_a_b(ggg, "정수", "업")
print (zzz)
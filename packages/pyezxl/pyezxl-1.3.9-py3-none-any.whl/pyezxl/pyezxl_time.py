# -*- coding: cp949 -*-

import time
import string
import re

class pyezxl_data:
	my_web_site="www.halmoney.com"

	def delete_value_continious (self, input_datas):
		#���ӵ� �ڷ��� ���� ���� ������ ���� �����ϴ� ���̴�
		#1��������Ʈ�� �����ϰ� �Ͽ���
		temp_basic=""
		for one_num in range(len(input_data)-1):
			if one_num == 0 :
				temp_basic=input_datas[one_num]
			elif temp_basic==input_datas[one_num+1]:
				input_datas[one_num+1]=[]
			else:
				temp_basic=input_datas[one_num]
		return input_datas

	def delete_value_step (self, input_datas, num):
		#���ϴ� ����°�� �ڷḦ �����ϱ�
		input_datas.insert(0,[])
		for a in rng(len(input_datas)):
			if (a%num) == 0 :
				input_datas[a]=[]
		result=input_datas[1:]
		return result

	def insert_value_step (self, input_datas, num = 1,input_data=[]):
		#����Ʈ�� ������ �������� �ڷ����
		total_number = len(input_datas)
		dd=0
		for a in rng(len(input_datas)):
			if a%num == 0 and a!=0:
				if total_number!=a:
					input_datas.insert(dd,input_data)
					dd=dd+1
			dd=dd+1
		return input_datas

	def read_time_day(self, time_char=time.localtime(time.time())):
		#�� -----> ['05', '095']
		return [time.strftime('%d',time_char),time.strftime('%j',time_char)]

	def read_time_hour(self, time_char=time.localtime(time.time())):
		#�� -----> ['10', '22', 'PM']
		return [time.strftime('%I',time_char),time.strftime('%H',time_char),time.strftime('%P',time_char)]

	def read_time_minute(self, time_char=time.localtime(time.time())):
		#�� -----> ['07']
		return [time.strftime('%M',time_char)]

	def read_time_month(self, time_char=time.localtime(time.time())):
		#�� -----> ['04', 'Apr', 'April']
		return [time.strftime('%m',time_char),time.strftime('%b',time_char),time.strftime('%B', time_char)]

	def read_time_second(self, time_char=time.localtime(time.time())):
		#�� -----> ['48']
		return [time.strftime('%S',time_char)]

	def read_time_today(self, time_char=time.localtime(time.time())):
		#���� -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
		aaa = string.split(time.strftime('%c',time_char))
		total_dash = time.strftime('%Y', time_char)+"-"+time.strftime('%m',time_char)+"-"+time.strftime('%d',time_char)
		return [aaa[0], aaa[1], time.strftime('%c',time_char), total_dash]

	def read_time_week(self, time_char=time.localtime(time.time())):
		#�� -----> ['5', '13', 'Fri', 'Friday']
		return [time.strftime('%w',time_char),time.strftime('%W',time_char),time.strftime('%a',time_char),time.strftime('%A',time_char)]

	def read_time_year(self, time_char=time.localtime(time.time())):
		#�� -----> ['02', '2002']
		return [time.strftime('%y', time_char), time.strftime('%Y', time_char)]

	def sort_datas_on (self, input_datas):
		#aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		#�����ϴ� ����Դϴ�
		temp_result=[]
		for one_data in input_datas:
			for one in one_data:
				temp_resultappend(one.sort())
		return result



	def delete_same_data (self, input_data):
	#����Ʈ�������� ���� �ڷḸ ����
		return "assa"

	def set_unique_data (self, input_data):
	#����Ʈ�������� ������ �ڷḸ ����
		return "assa"




#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 10:54:23 2017
########################################################################################
# @ File name: init_nasa_wind.py
# @ Function: The class of NASA wind speed.
# 	Importing, preprocessing, and basic operation of solar data.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 0.1.2
# @ Revision date: Jun/16/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np 
from pyhdf.SD import SD


class WindData(object):
	'''NASA wind speed data class'''
	version = '0.1.1'
	month_name = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
		'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
	leap_year = {'Jan': (31, 101, 131, True), 'Feb': (29, 201, 229, True), 'Mar': (31, 301, 331, True), 
	'Apr': (30, 401, 430, True), 'May': (31, 501, 531, True), 'Jun': (30, 601, 630, True), 
	'Jul': (31, 701, 731, True), 'Aug': (31, 801, 831, True), 'Sep': (30, 901, 930, True), 
	'Oct': (31, 1001, 1031, False), 'Nov': (30, 1101, 1130, False), 'Dec': (31, 1201, 1231, False)}
	nonleap_year = {'Jan': (31,101,131,True), 'Feb': (28,201,228,True), 'Mar': (31, 301, 331, True), 
	'Apr': (30, 401, 430, True), 'May': (31, 501, 531, True), 'Jun': (30, 601, 630, True), 'Jul': (31, 701, 731, True), 
	'Aug': (31, 801, 831, True), 'Sep': (30, 901, 930, True), 'Oct': (31, 1001, 1031, False), 
	'Nov': (30, 1101, 1130, False), 'Dec': (31, 1201, 1231, False)}
	fnamesa = '/MERRA301.prod.assim.tavg1_2d_slv_Nx.'
	fnamesb = '/MERRA300.prod.assim.tavg1_2d_slv_Nx.'
	fnamee = '.SUB.hdf'
	spl_month2010 = ('Jun', 'Jul', 'Aug')

	def __init__(self, ifile_name, isite_index, istart_year, iend_year):
		"""Create an object. 
		Args:
			ifile_name: str; the folder name of NASA file.
			isite_index: list; the list site indice in NASA file.
			istart_year: int; the start year.
			iend_year: inlt; the end year.
			Returns:
				an instances
		"""
		
		self.file_name = ifile_name
		self.site_index = isite_index
		self.start_year = istart_year
		self.end_year = iend_year
		self.dict_ref_wind = {}
		self.dict_hw_wind = {}
		self.dict_wind_cf = {}

	def cuv2speed(self, u, v):
		'''Converter u and v to the wind speed. 
		Args:
			u: the U data in NASA file.
			v: the V data in NASA file.
		Returns:
			the wind speed
		'''
		return (u ** 2 + v ** 2) ** 0.5

	def cimport_data(self, idata_name=('V50M', 'U50M')):
		'''Import ten-year data. 
		Args:
			idata_name: the data name.
		Returns: 
			self.dict_ref_wind: imported data.
		'''
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		zero = str(0)
		for each_siteth in range(1, site_num + 1):
			self.dict_ref_wind[each_siteth] = {}
			for each_year in year_index:
				self.dict_ref_wind[each_siteth][each_year] = {}
				for each_month in WindData.month_name:
					self.dict_ref_wind[each_siteth][each_year][each_month] = np.empty((0,24), np.float32)
		for each_year in year_index:
			if ((each_year % 400 == 0) or ((each_year % 4 == 0) and (each_year % 100 != 0))):
				year_feature = WindData.leap_year
			else:
				year_feature = WindData.nonleap_year
			for each_month in WindData.month_name:
				if ((each_year == 2010) and (each_month in WindData.spl_month2010)):
					fnames = self.file_name + WindData.fnamesa
				else:
					fnames = self.file_name + WindData.fnamesb 
				day_s = year_feature[each_month][1]
				day_e = year_feature[each_month][2]
				if year_feature[each_month][3]:
					for each_day in range(day_s, day_e + 1):
						fname = fnames + str(each_year) + zero + str(each_day) + WindData.fnamee
						print fname
						fid = SD(fname)
						tmpv = fid.select(idata_name[0])[:, :, :]
						tmpu = fid.select(idata_name[1])[:, :, :]
						fid.end()
						for each_siteth in range(1, site_num + 1):
							tmpv_site = tmpv[:, self.site_index[each_siteth - 1][0], \
							self.site_index[each_siteth - 1][1]].reshape(1, -1)
							tmpu_site = tmpu[:, self.site_index[each_siteth - 1][0], \
							self.site_index[each_siteth - 1][1]].reshape(1, -1)
							tmpwind_site = self.cuv2speed(tmpv_site, tmpu_site)
							self.dict_ref_wind[each_siteth][each_year][each_month] = \
							np.vstack((self.dict_ref_wind[each_siteth][each_year][each_month], tmpwind_site))
				else:
					for each_day in range(day_s, day_e + 1):
						fname = fnames + str(each_year) + str(each_day) + WindData.fnamee
						print fname
						fid = SD(fname)
						tmpv = fid.select(idata_name[0])[:, :, :]
						tmpu = fid.select(idata_name[1])[:, :, :]
						fid.end()
						for each_siteth in range(1, site_num + 1):
							tmpv_site = tmpv[:, self.site_index[each_siteth - 1][0], \
							self.site_index[each_siteth-1][1]].reshape(1, -1)
							tmpu_site = tmpu[:, self.site_index[each_siteth - 1][0], \
							self.site_index[each_siteth-1][1]].reshape(1, -1)
							tmpwind_site = self.cuv2speed(tmpv_site,tmpu_site)
							self.dict_ref_wind[each_siteth][each_year][each_month] = \
							np.vstack((self.dict_ref_wind[each_siteth][each_year][each_month], tmpwind_site))
		return self.dict_ref_wind

	def cref2hw(self, ihref=50.0, ihw=65.0, ialpha=0.35):
		'''Converter the speed at reference height to the one at WTGs height. 
		Args:
			ihref: the reference height.
			ihref: the WTGs height.
			ialpha: the exponent coefficient
		Returns:
			self.dict_hw_wind: wind speed at WTGs height
		'''
		year_index = range(self.start_year, self.end_year+1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			self.dict_hw_wind[each_siteth] = {}
			for each_year in year_index:
				self.dict_hw_wind[each_siteth][each_year] = {}
				for each_month in WindData.month_name:
					self.dict_hw_wind[each_siteth][each_year][each_month] = \
					self.dict_ref_wind[each_siteth][each_year][each_month] * (ihw / ihref) ** ialpha
		return self.dict_hw_wind

	def cuv2cf(self, idata, ispeed_in, ispeed_out, ispeed_rate, inita):
		'''Converter wind speed to capacity factors.
		Args:
			idata: the source wind speed.
			ispeed_in: cut-in speed.
			ispeed_out: cut-out speed.
			ispeed_rate: rate speed.
			inita: the efficiency.
		Returns:
			capacity factors
		'''
		return np.piecewise(
			idata, 
			[np.logical_or(idata < ispeed_in, idata > ispeed_out), 
			np.logical_and(idata >= ispeed_in, idata <= ispeed_rate), 
			np.logical_and(idata > ispeed_rate, idata <= ispeed_out)], 
			[0, 
			lambda idata: (idata - ispeed_in) / (ispeed_rate - ispeed_in) * inita, 
			1 * inita])

	def cwind2cf(self, ispeed_in=3.0, ispeed_out=25.0, ispeed_rate=13.5, inita=0.95):
		'''Converter NASA wind speed to capacity factors.
		Args:
			idata: the source wind speed.
			ispeed_in: cut-in speed.
			ispeed_out: cut-out speed.
			ispeed_rate: rate speed.
			inita: the efficiency.
		Returns:
			self.dict_wind_cf: capacity factors
		'''
		year_index = range(self.start_year, self.end_year+1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			self.dict_wind_cf[each_siteth]={}
			for each_year in year_index:
				self.dict_wind_cf[each_siteth][each_year]={}
				for each_month in WindData.month_name:
					self.dict_wind_cf[each_siteth][each_year][each_month] = \
					self.cuv2cf(self.dict_hw_wind[each_siteth][each_year][each_month], \
						ispeed_in, ispeed_out, ispeed_rate, inita)
		return self.dict_wind_cf

	def c2style_1month(self, imode=True):
		'''Converter NASA data to 1 month style.
		Args:
			imode: True or False; wind speed or capacity factors.
		Returns:
			dict_data_1month: data in 1 month style.
		'''
		if imode == True:
			dict_data = self.dict_wind_cf
		else:
			dict_data = self.dict_hw_wind
		dict_data_1month = {}
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			dict_data_1month[each_siteth] = {}
			for each_year in year_index:
				dict_data_1month[each_siteth][each_year] = {}
				for each_month in WindData.month_name:
					dict_data_1month[each_siteth][each_year][each_month] = \
					dict_data[each_siteth][each_year][each_month].reshape(1, -1)
		return dict_data_1month

	def c2style_1year(self, imode=True):
		'''Converter NASA data to 1 year style.
		Args:
			imode: True or False; wind speed or capacity factors.
		Returns:
			dict_data_1year: data in 1 year style.
		'''
		if imode == True:
			dict_data = self.dict_wind_cf
		else:
			dict_data = self.dict_hw_wind
		dict_data_1year = {}
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			dict_data_1year[each_siteth] = {};
			for each_year in year_index:
				dict_data_1year[each_siteth][each_year] = np.empty((1, 0), np.float32)
				for each_month in WindData.month_name:
					tmp = dict_data[each_siteth][each_year][each_month].reshape(1, -1)
					dict_data_1year[each_siteth][each_year] = np.hstack((dict_data_1year[each_siteth][each_year], tmp))
		return dict_data_1year

	def c2style_10year(self, imode=True):
		'''Converter NASA data to 10 years style.
		Args:
			imode: True or False; wind speed or capacity factors.
		Returns:
			dict_data_10year: data in 10 year style.
		'''
		dict_data_1year = self.c2style_1year(imode)
		dict_data_10year = {}
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			dict_data_10year[each_siteth] = np.empty((1, 0), np.float32)
			for each_year in year_index:
				dict_data_10year[each_siteth] = \
				np.hstack((dict_data_10year[each_siteth], dict_data_1year[each_siteth][each_year]))
		return dict_data_10year

	def cselect_1site_1day(self, isiteth, iyear, imonth, iday, imode=True):
		'''select data of 1 site, 1 day.
		Args:
			isiteth: the serial number of site.
			iyear: the year.
			imonth: the month.
			iday: the day.
			imode: True or False; wind speed or capacity factors.
		Returns:
			data of 1 site, 1 day.
		'''
		if imode == True:
			dict_data = self.dict_wind_cf
		else:
			dict_data = self.dict_hw_wind
		return dict_data[isiteth][iyear][imonth][iday-1, :].reshape(1, -1)

	def cselect_1site_1month(self, isiteth, iyear, imonth, imode=True):
		'''select data of 1 site, 1 month.
		Args:
			isiteth: the serial number of site.
			iyear: the year.
			imonth: the month.
			imode: True or False; wind speed or capacity factors.
		Returns:
			data of 1 site, 1 month.
		'''
		return self.c2style_1month(imode)[isiteth][iyear][imonth]

	def cselect_1site_1year(self, isiteth, iyear, imode=True):
		'''select data of 1 site, 1 year.
		Args:
			isiteth: the serial number of site.
			iyear: the year.
			imode: True or False; wind speed or capacity factors.
		Returns:
			data of 1 site, 1 year.
		'''
		return self.c2style_1year(imode)[isiteth][iyear]

	def cselect_1site_10year(self, isiteth, imode=True):
		'''select data of 1 site in 10 year style.
		Args:
			isiteth: the serial number of site.
			imode: True or False; wind speed or capacity factors.
		Returns:
			data of 1 site, 10 year.
		'''
		return self.c2style_10year(imode)[isiteth]


if __name__ == '__main__':
	'''Examples.'''
	file_name = 'sd_wind_data'
	wind_site_index = [(-3, 6), (-9, 7)]
	start_year = 2006
	end_year = 2015

	wind_data = WindData(file_name, wind_site_index, start_year, end_year)
	wind_speed_ref = wind_data.cimport_data()
	wind_speed_hw = wind_data.cref2hw()
	wind_capacity_factor = wind_data.cwind2cf()
	wind_cf_1monthstl = wind_data.c2style_1month()
	wind_cf_1yearstl = wind_data.c2style_1year()
	wind_cf_10yearstl = wind_data.c2style_10year()
	wind_cf_1s1day = wind_data.cselect_1site_1day(1, 2006, 'Jan', 22)
	wind_cf_1s1month = wind_data.cselect_1site_1month(1, 2006, 'Jan')
	wind_cf_1s1year = wind_data.cselect_1site_1year(1, 2006)
	wind_cf_1s10year = wind_data.cselect_1site_10year(1)





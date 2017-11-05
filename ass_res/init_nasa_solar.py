#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 21:53:47 2017
########################################################################################
# @ File name: init_nasa_solar.py
# @ Function: The class of NASA solar irradiation. 
# 	Importing, preprocessing, and basic operation of solar data.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 1.1.2
# @ Revision date: Nov./05/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np
from pyhdf.SD import SD


class SolarData(object):
	'''NASA solar irradiation data class'''
	version = '1.1.2'
	month_name = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
		'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
	leap_year = {'Jan': (31, 101, 131, True), 'Feb': (29, 201, 229, True), 'Mar': (31, 301, 331, True), 
	'Apr': (30, 401, 430, True), 'May': (31, 501, 531, True), 'Jun': (30, 601, 630, True), 
	'Jul': (31, 701, 731, True), 'Aug': (31, 801, 831, True), 'Sep': (30, 901, 930, True), 
	'Oct': (31, 1001, 1031, False), 'Nov':(30, 1101, 1130, False), 'Dec':(31, 1201, 1231, False)}
	nonleap_year = {'Jan':(31, 101, 131, True), 'Feb':(28, 201, 228, True), 'Mar':(31, 301, 331, True), 
	'Apr': (30, 401, 430, True), 'May': (31, 501, 531, True), 'Jun': (30, 601, 630, True), 'Jul': (31, 701, 731, True), 
	'Aug': (31, 801, 831, True), 'Sep': (30, 901, 930, True), 'Oct': (31, 1001, 1031, False), 
	'Nov': (30, 1101, 1130, False), 'Dec': (31, 1201, 1231, False)}
	#fnamesa and fnamsb are the middle names of sloar irrdiation.
	fnamesa = '/MERRA301.prod.assim.tavg1_2d_rad_Nx.'
	fnamesb = '/MERRA300.prod.assim.tavg1_2d_rad_Nx.'
	fnamee = '.SUB.hdf'
	#fnameta and fnamtb are the middle names of ambient temperature.
	fnameta = '/MERRA301.prod.assim.tavg1_2d_slv_Nx.'
	fnametb = '/MERRA300.prod.assim.tavg1_2d_slv_Nx.'
	spl_month2010 = ('Jun', 'Jul', 'Aug')

	def __init__(self, ifile_path, isite_index, istart_year, iend_year):
		'''Create an object. 
		Args:
			ifile_name: str; the folder name of NASA file.
			isite_index: list; the list site indice in NASA file.
			istart_year: int; the start year.
			iend_year: inlt; the end year.
		Returns:
			an instances
		'''
		self.file_path = ifile_path
		self.site_index = isite_index
		self.start_year = istart_year
		self.end_year = iend_year
		self.dict_solar = {}
		self.dict_solar_cf = {}
		self.dict_temperature = {}

	def cimport_data(self, idata_name=('SWGNT',)):
		'''Import ten-year dsolar irradiation ata. 
		Args:
			idata_name: the data name.
		Returns: 
			self.dict_solar: imported data.
		'''
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		zero = str(0)
		for each_siteth in range(1, site_num + 1):
			self.dict_solar[each_siteth] = {}
			for each_year in year_index:
				self.dict_solar[each_siteth][each_year] = {}
				for each_month in SolarData.month_name:
					self.dict_solar[each_siteth][each_year][each_month] = np.empty((0,24), np.float32)
		for each_year in year_index:
			if ((each_year % 400 == 0) or ((each_year % 4 == 0) and (each_year % 100 != 0))):
				year_feature = SolarData.leap_year
			else:
				year_feature = SolarData.nonleap_year
			for each_month in SolarData.month_name:
				if ((each_year < 2010) or ((each_year == 2010) and (each_month in SolarData.spl_month2010))):
					fnames = self.file_path + SolarData.fnamesa
				else:
					fnames = self.file_path + SolarData.fnamesb
				day_s = year_feature[each_month][1]
				day_e = year_feature[each_month][2]
				if year_feature[each_month][3]:
					for each_day in range(day_s, day_e + 1):
						fname = fnames + str(each_year) + zero + str(each_day) + SolarData.fnamee
						print fname
						fid = SD(fname)
						tmpirrad = fid.select(idata_name[0])[:, :, :]
						fid.end()
						for each_siteth in range(1, site_num + 1):
							tmpirrad_site = tmpirrad[:, self.site_index[each_siteth - 1][0], \
							self.site_index[each_siteth - 1][1]].reshape(1, -1)
							self.dict_solar[each_siteth][each_year][each_month] = \
							np.vstack((self.dict_solar[each_siteth][each_year][each_month], tmpirrad_site))
				else:
					for each_day in range(day_s, day_e + 1):
						fname = fnames + str(each_year) + str(each_day) + SolarData.fnamee
						print fname
						fid = SD(fname)
						tmpirrad = fid.select(idata_name[0])[:, :, :]
						fid.end()
						for each_siteth in range(1, site_num + 1):
							tmpirrad_site = tmpirrad[:, self.site_index[each_siteth - 1][0], \
							self.site_index[each_siteth - 1][1]].reshape(1, -1)
							self.dict_solar[each_siteth][each_year][each_month] = \
							np.vstack((self.dict_solar[each_siteth][each_year][each_month], tmpirrad_site))
		return self.dict_solar

	def cimport_datat(self, idata_name=('TS',)):
		'''Import ten-year ambient temperature data. 
		Args:
			idata_name: the data name.
		Returns: 
			self.dict_solar: imported data.
		'''
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_indext)
		zero = str(0)
		for each_siteth in range(1, site_num + 1):
			self.dict_temperature[each_siteth] = {}
			for each_year in year_index:
				self.dict_temperature[each_siteth][each_year] = {}
				for each_month in SolarData.month_name:
					self.dict_temperature[each_siteth][each_year][each_month] = np.empty((0,24), np.float32)
		for each_year in year_index:
			if ((each_year % 400 == 0) or ((each_year % 4 == 0) and (each_year % 100 != 0))):
				year_feature = SolarData.leap_year
			else:
				year_feature = SolarData.nonleap_year
			for each_month in SolarData.month_name:
				if ((each_year == 2010) and (each_month in SolarData.spl_month2010)):
					fnames = self.file_patht + SolarData.fnameta
				else:
					fnames = self.file_patht + SolarData.fnametb
				day_s = year_feature[each_month][1]
				day_e = year_feature[each_month][2]
				if year_feature[each_month][3]:
					for each_day in range(day_s, day_e + 1):
						fname = fnames + str(each_year) + zero + str(each_day) + SolarData.fnamee
						print fname
						fid = SD(fname)
						tmpirrad = fid.select(idata_name[0])[:, :, :]
						fid.end()
						for each_siteth in range(1, site_num + 1):
							tmpirrad_site = tmpirrad[:, self.site_indext[each_siteth - 1][0], \
							self.site_indext[each_siteth - 1][1]].reshape(1, -1)
							self.dict_temperature[each_siteth][each_year][each_month] = \
							np.vstack((self.dict_temperature[each_siteth][each_year][each_month], tmpirrad_site))
						# print(tmpirrad_site)
				else:
					for each_day in range(day_s, day_e + 1):
						fname = fnames + str(each_year) + str(each_day) + SolarData.fnamee
						print fname
						fid = SD(fname)
						tmpirrad = fid.select(idata_name[0])[:, :, :]
						fid.end()
						for each_siteth in range(1, site_num + 1):
							tmpirrad_site = tmpirrad[:, self.site_indext[each_siteth - 1][0], \
							self.site_indext[each_siteth - 1][1]].reshape(1, -1)
							self.dict_temperature[each_siteth][each_year][each_month] = \
							np.vstack((self.dict_temperature[each_siteth][each_year][each_month], tmpirrad_site))
						# print(tmpirrad_site)
		return self.dict_temperature

	def csolar2cf_model1(self, irated_powr=255.0, iarea_m2=1.6368, ieffi_ratio=0.1248):
		'''Converter solar irradiation to capacity factors.
			PV Model1: Ff = (idata * iarea_m2 * ieffi_ratio) / ieffi_ratio
		Args:
			idata: the source solar irradiation.
			irated_powr: the rated power.
			iarea_m2: the area of a PV module.
			ieffi_ratio: the efficiency.
		Returns:
			capacity factors
		'''
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			self.dict_solar_cf[each_siteth] = {}
			for each_year in year_index:
				self.dict_solar_cf[each_siteth][each_year] = {}
				for each_month in SolarData.month_name:
					self.dict_solar_cf[each_siteth][each_year][each_month] = \
					self.dict_solar[each_siteth][each_year][each_month] * ieffi_ratio * iarea_m2 / irated_powr
		return self.dict_solar_cf

	def csolar2cf_model2(self, iHSTC=1000.0, iC1=0.93, iC2=-0.005, iTSTC=25.0, iTfTETC=47.0, iTaTETC=20.0, iHTETC=800.0):
		'''Converter solar irradiation to capacity factors.
		PV Model2: Ff = (idataf / iHSTC) * iC1 * (1 + iC2(Tf - iTSTC))
							Tf = idatat + idataf * (iTfTETC - iTaTETC) / iHTETC
		Args:
			idata: the source solar irradiation and ambient temperature.
			iHSTC: the solar irradiation at standard test condition.
			iC1: the derating coefficient.
			iC2: the power temperature coefficient.
			iTSTC: is the temperature at standard test condition.
			iTfTETC: the solar irradiation at temperature estimation test condition.
			iTaTETC: the ambient temperature at temperature estimation test condition.
		Returns:
			capacity factors
		'''
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			self.dict_solar_cf[each_siteth] = {}
			for each_year in year_index:
				self.dict_solar_cf[each_siteth][each_year] = {}
				for each_month in SolarData.month_name:
#					print each_month
					self.dict_solar_cf[each_siteth][each_year][each_month] = \
					self.dict_solar[each_siteth][each_year][each_month] / iHSTC * iC1 * \
					(1 + iC2 * (self.dict_temperature[each_siteth][each_year][each_month] 
					- 273.15 - iTSTC + self.dict_solar[each_siteth][each_year][each_month] 
					* (iTfTETC - iTaTETC) / iHTETC))
		return self.dict_solar_cf

	def c2style_1month(self, imode=True):
		'''Converter NASA data to 1 month style.
		Args:
			imode: True or False; wind speed or capacity factors.
		Returns:
			dict_data_1month: data in 1 month style.
		'''
		if imode == True:
			dict_data = self.dict_solar_cf
		else:
			dict_data = self.dict_solar
		dict_data_1month = {}
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			dict_data_1month[each_siteth] = {}
			for each_year in year_index:
				dict_data_1month[each_siteth][each_year] = {}
				for each_month in SolarData.month_name:
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
			dict_data = self.dict_solar_cf
		else:
			dict_data = self.dict_solar
		dict_data_1year = {}
		year_index = range(self.start_year, self.end_year + 1)
		site_num = len(self.site_index)
		for each_siteth in range(1, site_num + 1):
			dict_data_1year[each_siteth] = {};
			for each_year in year_index:
				dict_data_1year[each_siteth][each_year] = np.empty((1, 0), np.float32)
				for each_month in SolarData.month_name:
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
			dict_data = self.dict_solar_cf
		else:
			dict_data = self.dict_solar
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
	file_name = 'sd_solar_data'
	irrad_site_index = [(-3, 6), (-9, 7)]
	start_year = 2006
	end_year = 2006

	solar_data = SolarData(file_name, irrad_site_index, start_year, end_year)
	solar_irrad_data = solar_data.cimport_data()
	solar_capacity_factor = solar_data.csolar2cf_model1()
	# solar_temperature_data = solar_data.cimport_datat()
	# solar_capacity_factor = solar_data.csolar2cf_model2()
	solar_cf_1monthstl = solar_data.c2style_1month()
	solar_cf_1yearstl = solar_data.c2style_1year()
	solar_cf_10yearstl = solar_data.c2style_10year()
	solar_cf_1s1day = solar_data.cselect_1site_1day(1, 2006, 'Jan', 22)
	solar_cf_1s1month = solar_data.cselect_1site_1month(1, 2006, 'Jan')
	solar_cf_1s1year = solar_data.cselect_1site_1year(1, 2006)
	solar_cf_1s10year = solar_data.cselect_1site_10year(1)
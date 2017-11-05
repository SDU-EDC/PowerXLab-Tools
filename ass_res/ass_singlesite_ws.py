#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 18:51:22 2017
########################################################################################
# @ File name: ass_singlesite_ws.py
# @ Function: Perform single-site assessment.
# 	Assess the variation and reserves of wind and solar resources.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 0.1.2
# @ Revision date: Jun/16/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

import init_nasa_wind as mwind
import init_nasa_solar as msolar


def cass_varws_annual(isource_data, isiteth_plotted=[1, 2, 3], plot_flag=False):
	'''Assess annual variation of selected sites.
		Output statistical indices and graphs 
	Args:
		isource_data: the source data.
		isiteth_plotted: the serial number of selected site.
		plot_flag: True or False. Draw graphs or not.
	Returns: 
		the graphs of annual variation.
		means, std, and variable coefficient of selected site in year scale.
	'''
	year_index = range(isource_data.start_year, isource_data.end_year + 1)
	year_num = len(year_index)
	site_num = len(isource_data.site_index)
	fc_sum_yearly = np.empty((site_num, year_num), np.float32)
	fc_mean_yearly = np.empty((site_num, 1), np.float32)
	fc_std_yearly = np.empty((site_num, 1), np.float32)
	fc_varcoef_yearly = np.empty((site_num, 1), np.float32)
	for each_siteth in range(1, site_num + 1):
		for each_yearth in range(0, year_num, 1):
			fc_sum_yearly[each_siteth - 1, each_yearth] = \
			np.sum(isource_data.cselect_1site_1year(each_siteth, year_index[each_yearth]), axis=1)
		fc_mean_yearly[each_siteth - 1, 0] = \
		np.sum(isource_data.cselect_1site_10year(each_siteth), axis=1) / year_num
		fc_std_yearly[each_siteth - 1, 0] = \
		np.std(fc_sum_yearly[each_siteth - 1, :])
		fc_varcoef_yearly[each_siteth - 1, 0] = \
		fc_std_yearly[each_siteth - 1, 0] * 1.0 / fc_mean_yearly[each_siteth - 1, 0]
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax = plt.subplot(111)
		width = 1 * 0.25 * 3 / site_num
		ind = np.arange(0, year_num, 1)
		if len(isiteth_plotted) == 3:
			ax.bar(ind - width, fc_sum_yearly[isiteth_plotted[0] - 1, :], width, 
				color='k', label='Siteth ' + str(isiteth_plotted[0]))
			ax.bar(ind, fc_sum_yearly[isiteth_plotted[1] - 1, :], width, 
				color='b', label='Siteth ' + str(isiteth_plotted[1]))
			ax.bar(ind + width, fc_sum_yearly[isiteth_plotted[2] - 1, :], width, 
				color='r', label='Siteth ' + str(isiteth_plotted[2]))
		elif len(isiteth_plotted) == 2:
			ax.bar(ind - width, fc_sum_yearly[isiteth_plotted[0] - 1, :], width, 
				color='k', label='Siteth ' + str(isiteth_plotted[0]))
			ax.bar(ind, fc_sum_yearly[isiteth_plotted[1] - 1, :], width, 
				color='b', label='Siteth ' + str(isiteth_plotted[1]))
		else:
			ax.bar(ind, fc_sum_yearly[isiteth_plotted[0] - 1, :], width, 
				color='k', label='Siteth ' + str(isiteth_plotted[0]))
		ax.set_xticks(np.linspace(0, 9, 10))
		x_lable = tuple([str(each) for each in year_index])
		ax.set_xticklabels(x_lable)
		ax.set_xlabel('Year')
		ax.set_ylabel('Capacity factors')
		# ax.grid(True)
		ax.legend(loc=1)
		plt.title('The annual variation')
		plt.show()
		# plt.savefig('cPlotW1.png', dpi=300, bbox_inches='tight')
	if isinstance(isiteth_plotted, list):
		ositeth_plotted = [each - 1 for each in list(isiteth_plotted)]
	else:
		ositeth_plotted = isiteth_plotted - 1
	return fc_mean_yearly[ositeth_plotted, 0], fc_std_yearly[ositeth_plotted, 0], fc_varcoef_yearly[ositeth_plotted, 0]


def cass_varws_monthly(isource_data, isiteth_plotted=[1, 2, 3], iyear_plotted=2010, plot_flag=False):
	'''Assess monthly variation of selected sites, selected year.
		Output graphs 
	Args:
		isource_data: the source data.
		isiteth_plotted: the serial number of selected site.
		iyear_plotted: the selected year.
		plot_flag: True or False. Draw graphs or not.
	Returns: 
		the graphs of monthly variation.
	'''
	year_index = range(isource_data.start_year, isource_data.end_year + 1)
	year_num = len(year_index)
	site_num = len(isource_data.site_index)
	month_index = isource_data.month_name
	fc_mean_monthly = np.empty((site_num, 12), np.float32)
	fc_sum_monthly = np.empty((site_num, 12, year_num), np.float32)
	fc_ploted = np.empty((site_num, 12), np.float32)
	for each_siteth in range(1, site_num + 1):
		for each_monthth in range(0, 12, 1):
			for each_year in year_index:
				fc_mean_monthly[each_siteth - 1, each_monthth] = \
				fc_mean_monthly[each_siteth - 1, each_monthth] + \
				np.sum(isource_data.cselect_1site_1month(each_siteth, each_year, month_index[each_monthth]), axis=1)
				fc_mean_monthly[each_siteth - 1, each_monthth] = \
				fc_mean_monthly[each_siteth - 1, each_monthth] * 1.0 / year_num
				fc_sum_monthly[each_siteth - 1, each_monthth, each_year - isource_data.start_year] = \
				np.sum(isource_data.cselect_1site_1month(each_siteth, each_year, month_index[each_monthth]), axis=1)
	for each_plotsiteth in isiteth_plotted:
		for each_monthth in range(0, 12, 1):
			fc_ploted[each_plotsiteth - 1, each_monthth] = \
			np.sum(isource_data.cselect_1site_1month(each_plotsiteth, iyear_plotted, month_index[each_monthth]), axis=1)
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax=plt.subplot(111)
		width = 1 * 0.25 * 3 / site_num
		ind = np.arange(0, 12, 1)
		if len(isiteth_plotted) == 3:
			ax.bar(ind - width, fc_ploted[isiteth_plotted[0] - 1, :], width, 
				color='k', label='Siteth ' + str(isiteth_plotted[0]))
			ax.bar(ind, fc_ploted[isiteth_plotted[1] - 1, :], width, 
				color='b', label='Siteth ' + str(isiteth_plotted[1]))
			ax.bar(ind + width, fc_ploted[isiteth_plotted[2] - 1, :], width, 
				color='r', label='Siteth ' + str(isiteth_plotted[2]))
		elif len(isiteth_plotted) == 2:
			ax.bar(ind - width, fc_ploted[isiteth_plotted[0] - 1, :], width, 
				color='k', label='Siteth ' + str(isiteth_plotted[0]))
			ax.bar(ind, fc_ploted[isiteth_plotted[1] - 1, :], width, 
				color='b', label='Siteth ' + str(isiteth_plotted[1]))
		else:
			ax.bar(ind, fc_ploted[isiteth_plotted[0] - 1, :], width, 
				color='k', label='Siteth ' + str(isiteth_plotted[0]))
		ax.set_xticks(np.linspace(0, 11, 12))
		ax.set_xticklabels(('Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 
			'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'), rotation=45, fontsize=8)
		ax.set_xlabel('Month')
		ax.set_ylabel('Capacity factors')
		# ax.grid(True)
		ax.legend(loc=1)
		plt.title('The monthly variation')
		plt.show()
		# plt.savefig('cPlotW1.png', dpi=300, bbox_inches='tight')


def cass_varws_hourly(isource_data, isiteth_plotted=[1, 2, 3], imonth_ploted='Apr', plot_flag=False):
	'''Assess hourly variation of selected sites, selected month.
		Output graphs 
	Args:
		isource_data: the source data.
		isiteth_plotted: the serial number of selected site.
		imonth_ploted: the selected month.
		plot_flag: True or False. Draw graphs or not.
	Returns: 
		the graphs of monthly variation.
	'''
	year_index = range(isource_data.start_year, isource_data.end_year + 1)
	year_num = len(year_index)
	site_num = len(isource_data.site_index)
	fc_mean_hourly = np.zeros((site_num, year_num, 24), np.float32)
	for each_siteth in range(1, site_num + 1):
		for each_yearth in range(0, year_num, 1):
			for each_day in range(2, 29, 1):
				fc_mean_hourly[each_siteth - 1, each_yearth, :] = \
				fc_mean_hourly[each_siteth - 1, each_yearth, :] + \
				np.hstack((isource_data.cselect_1site_1day(each_siteth,year_index[each_yearth], imonth_ploted,each_day-1)[0, 16:24], \
					isource_data.cselect_1site_1day(each_siteth, year_index[each_yearth], imonth_ploted, each_day)[0, 0:16]))
	fc_ploted = np.mean(fc_mean_hourly, axis=1) / 27.0
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax = host_subplot(111)
		ind = np.arange(0, 24, 1)
		if len(isiteth_plotted) == 3:
			ax.plot(ind, fc_ploted[isiteth_plotted[0] - 1, :], 'k-o', label='Siteth ' + str(isiteth_plotted[0]))
			ax.plot(ind, fc_ploted[isiteth_plotted[1] - 1, :], 'b-^', label='Siteth ' + str(isiteth_plotted[1]))
			ax.plot(ind, fc_ploted[isiteth_plotted[2] - 1, :], 'r-d', label='Siteth ' + str(isiteth_plotted[2]))
		elif len(isiteth_plotted) == 2:
			ax.plot(ind, fc_ploted[isiteth_plotted[0] - 1, :], 'k-o', label='Siteth ' + str(isiteth_plotted[0]))
			ax.plot(ind, fc_ploted[isiteth_plotted[1] - 1, :], 'b-^', label='Siteth ' + str(isiteth_plotted[1]))
		else:
			ax.plot(ind, fc_ploted[isiteth_plotted[0] - 1, :], 'k-o', label='Siteth ' + str(isiteth_plotted[0]))
		ax.set_xticks(np.linspace(0, 23, 24))
		x_lables=('00:30', '', '02:30', '', '04:30', '', '06:30', '', '08:30', '', '10:30', \
			'', '12:30', '', '14:30', '', '16:30', '', '18:30', '', '20:30', '', '22:30', '')
		ax.set_xticklabels(x_lables)
		ax.set_xlabel('Time')
		ax.set_ylabel('Wind capacity factors')
		ax.set_xlim(-0.7, 23.7)
		#plt.grid()
		ax.legend(loc = 1)
		plt.title('The hourly variation')
		plt.show()
		# plt.savefig('cwp43000.png', dpi=300, bbox_inches='tight')


def cass_rampws(isource_data, isiteth_plotted=3, plot_flag=False):
	'''Assess ramp rate of selected sites.
		Output statistical indices and graphs 
	Args:
		isource_data: the source data.
		isiteth_plotted: the serial number of selected site.
		plot_flag: True or False. Draw graphs or not.
	Returns: 
		the graphs of monthly variation.
		fc_ramp_rate: ramp rate.
	'''
	fc_10years = isource_data.cselect_1site_10year(isiteth_plotted)
	fc_10years_tmp = np.hstack((fc_10years[0, 1:].reshape(-1, 1), fc_10years[0, 0:-1].reshape(-1, 1)))
	fc_ramp_rate = np.subtract.reduce(fc_10years_tmp, axis=1)
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax = plt.subplot(111)
		cn, bins, step = ax.hist(fc_ramp_rate, bins=40, normed=True, histtype='barstacked', color='b')
		ax.set_ylabel('Probability density')
		ax.set_xlabel('ramp rate')
		ax.set_xticks(np.arange(-0.2, 0.3, 0.1))
		ax.set_xticklabels((-0.2, -0.1, 0.0, 0.1, 0.2))
		ax.set_yticks(np.linspace(0, 15, 4))
		ax.set_yticklabels((0, 5, 10, 15))
		#ax.grid(True)
		plt.title('The distribution of ramp rate')
		plt.show()
		# plt.savefig('cwp43000.png', dpi=300, bbox_inches='tight')
	return fc_ramp_rate


def cass_single_site(isource_data, isiteth=3):
	'''Assess selected sites.
		Output statistical indices 
	Args:
		isource_data: the source data.
		isiteth: the serial number of selected site.
	Returns: 
		fc_mean_yearly: means of selected site in year scale.
		fc_std_yearly: std of selected site in year scale.
		fc_varcoef_yearly: variable coefficient of selected site in year scale.
		fc_mean_hourly: means of selected site in hour scale.
		fc_std_hourly: std of selected site in hour scale.
		fc_varcoef_hourly: variable coefficient of selected site in hour scale.
		fc_half_prob: half power probability. 
		fc_ramp_rate: ramp rate.
		fc_ramp_mean: mean of ramp rate.
		fc_ramp_std: std of ramp rate.
		fc_ramp_max: max of ramp rate. 
		fc_ramp_min: min of ramp rate.
		fc_ramp_upper: upper value of 95% confidence interval ramp rate.
		fc_ramp_lower: lower value of 95% confidence interval ramp rate.
	'''
	(fc_mean_yearly, fc_std_yearly, fc_varcoef_yearly) = cass_varws_annual(isource_data, isiteth, False)
	fc_10years = isource_data.cselect_1site_10year(isiteth)
	fc_mean_hourly = np.mean(fc_10years)
	fc_std_hourly = np.std(fc_10years)
	fc_varcoef_hourly = fc_mean_hourly * 1.0 / fc_std_hourly
	fc_half_prob = (fc_10years[0, fc_10years[0, :] > 0.5].shape[0] * 1.0)/ (fc_10years.shape[1] * 1.0)
	fc_ramp_rate = cass_rampws(isource_data, isiteth, False)
	fc_ramp_mean = np.mean(fc_ramp_rate)
	fc_ramp_std = np.std(fc_ramp_rate)
	fc_ramp_max = np.max(fc_ramp_rate)
	fc_ramp_min = np.min(fc_ramp_rate)
	fc_ramp_upper = fc_ramp_mean + 1.96 * fc_ramp_std
	fc_ramp_lower = fc_ramp_mean - 1.96 * fc_ramp_std
	return fc_mean_yearly, fc_std_yearly, fc_varcoef_yearly, fc_mean_hourly, fc_std_hourly, fc_varcoef_hourly, \
	fc_half_prob, fc_ramp_rate, fc_ramp_mean, fc_ramp_std, fc_ramp_max, fc_ramp_min, fc_ramp_upper, fc_ramp_lower


def cass_attr_constr(isource_data, imode=0):
	'''Construct new attirbutes.
		Output statistical indices 
	Args:
		isource_data: the source data.
		imode: 0, 1, 2, 3. means in year scale, std in hour scale, variable coefficient in hour scale, means in hour scale
	Returns: 
		the constructed attributes.
	'''
	cf_10yearstl = isource_data.c2style_10year(True)
	year_index = range(isource_data.start_year, isource_data.end_year + 1)
	year_num = len(year_index)
	site_num = len(isource_data.site_index)
	if imode == 0:
		fc_mean_yearly = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			fc_mean_yearly[0, each_siteth-1] = \
			np.sum(cf_10yearstl[each_siteth], axis=1) * 1.0 / year_num
		return fc_mean_yearly
	elif imode == 1:
		fc_std_hourly = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			fc_std_hourly[0, each_siteth-1] = \
			np.std(cf_10yearstl[each_siteth], axis=1) * 1.0
		return fc_std_hourly
	elif imode == 2:
		fc_varcoef_hourly = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			fc_varcoef_hourly[0, each_siteth-1] = \
			np.std(cf_10yearstl[each_siteth], axis=1) * 1.0 / np.mean(cf_10yearstl[each_siteth], axis=1)
		return fc_varcoef_hourly
	else:
		fc_mean_hourly = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			fc_mean_hourly[0, each_siteth-1] = \
			np.mean(cf_10yearstl[each_siteth], axis=1)
		return fc_mean_hourly


if __name__ == '__main__':
	'''Examples.'''
	start_year = 2006
	end_year = 2015
	site_index = [(-6, 2), (-6, 6), (-6, 10)]
	wfile_name = 'sd_wind_data'
	sfile_name = 'sd_solar_data'

	wind_data = mwind.WindData(wfile_name, site_index, start_year, end_year)
	wind_speed_ref = wind_data.cimport_data()
	wind_speed_hw = wind_data.cref2hw()
	wind_capacity_factor = wind_data.cwind2cf()
	solar_data = msolar.SolarData(sfile_name, site_index, start_year, end_year)
	solar_irrad_data = solar_data.cimport_data()
	solar_capacity_factor = solar_data.csolar2cf_model1()
	# solar_temperature_data = solar_data.cimport_datat()
	# solar_capacity_factor = solar_data.csolar2cf_model2()

	(fc_mean_yearly, fc_std_yearly, fc_varcoef_yearly) = cass_varws_annual(wind_data, [1,2,3], True)
	cass_varws_monthly(wind_data, [1,2,3], 2010, True)
	cass_varws_hourly(wind_data, [1,2,3], 'Apr', True)
	fc_ramp_rate = cass_rampws(wind_data, 3, True)
	assess_result = cass_single_site(wind_data, 3)
	attr = cass_attr_constr(wind_data, 0)



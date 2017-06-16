#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 18:54:30 2017
########################################################################################
# @ File name: ass_singlesite_lsy.py
# @ Function: Perform single-site assessment.
# 	Assess the local synergy effects.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 0.1.2
# @ Revision date: Jun/16/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from mpl_toolkits.axes_grid1 import host_subplot

import init_nasa_wind as mwind
import init_nasa_solar as msolar
import ass_singlesite_ws as masw


def cass_varh_monthly(iwind_data, isolar_data, isiteth_plotted=3, iyear_plotted=2010, plot_flag=False):
	'''Assess local synergy of selected sites in month style.
		Output graphs 
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		isiteth_plotted: the serial number of selected site.
		iyear_plotted: the selected year
		plot_flag: True or False. Draw graphs or not.
	Returns: 
		the graphs of monthly variation.
	'''
	year_index = range(iwind_data.start_year, iwind_data.end_year + 1)
	year_num = len(year_index)
	site_num = len(iwind_data.site_index)
	month_index = iwind_data.month_name
	wfc_mean_monthly = np.empty((site_num, 12), np.float32)
	wfc_sum_monthly = np.empty((site_num, 12, year_num), np.float32)
	sfc_mean_monthly = np.empty((site_num, 12), np.float32)
	sfc_sum_monthly = np.empty((site_num, 12, year_num), np.float32)
	wfc_ploted = np.empty((1, 12), np.float32)
	sfc_ploted = np.empty((1, 12), np.float32)
	for each_siteth in range(1, site_num + 1):
		for each_monthth in range(0, 12, 1):
			for each_year in year_index:
				wfc_mean_monthly[each_siteth-1,each_monthth] = \
				wfc_mean_monthly[each_siteth-1,each_monthth] + \
				np.sum(iwind_data.cselect_1site_1month(each_siteth, each_year, month_index[each_monthth]), axis=1)
				wfc_mean_monthly[each_siteth-1,each_monthth] = \
				wfc_mean_monthly[each_siteth-1,each_monthth] * 1.0 / year_num
				wfc_sum_monthly[each_siteth - 1, each_monthth, each_year - iwind_data.start_year] = \
				np.sum(iwind_data.cselect_1site_1month(each_siteth, each_year, month_index[each_monthth]), axis=1)
				
				sfc_mean_monthly[each_siteth-1,each_monthth] = \
				sfc_mean_monthly[each_siteth-1,each_monthth] + \
				np.sum(isolar_data.cselect_1site_1month(each_siteth, each_year, month_index[each_monthth]), axis=1)
				sfc_mean_monthly[each_siteth-1,each_monthth] = \
				sfc_mean_monthly[each_siteth-1,each_monthth] * 1.0 / year_num
				sfc_sum_monthly[each_siteth - 1, each_monthth, each_year - iwind_data.start_year] = \
				np.sum(isolar_data.cselect_1site_1month(each_siteth, each_year, month_index[each_monthth]), axis=1)
	for each_monthth in range(0, 12, 1):
			wfc_ploted[0, each_monthth] = \
			np.sum(iwind_data.cselect_1site_1month(isiteth_plotted, iyear_plotted, month_index[each_monthth]), axis=1)
			sfc_ploted[0, each_monthth] = \
			np.sum(isolar_data.cselect_1site_1month(isiteth_plotted, iyear_plotted, month_index[each_monthth]), axis=1)
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax1_varann_wfc = host_subplot(111)
		ax2_varann_sfc = ax1_varann_wfc.twinx()
		width = 1 * 0.43
		ind = np.arange(0, 12, 1)
		ax1_varann_wfc.bar(ind-width/2.0, wfc_ploted[0, :], width, color='k', label='Wind')
		ax2_varann_sfc.bar(ind+width/2.0, sfc_ploted[0, :], width, color='b', label='Solar')
		ax1_varann_wfc.set_xticks(np.linspace(0, 11, 12))
		ax1_varann_wfc.set_xticklabels(('Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', \
			'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'))
		ax1_varann_wfc.set_xlabel('Month')
		ax1_varann_wfc.set_ylabel('Wind capacity factors')
		ax2_varann_sfc.set_ylabel('Solar capacity factors')
		ax1_varann_wfc.set_xlim(-0.575, 11.575)
		#ax1_varann_wfc.grid(True)
		ax1_varann_wfc.legend(loc=1)
		plt.title('Annual variation')
		plt.show()
		# plt.savefig('cwp43000.png', dpi=300, bbox_inches='tight')


def cass_varh_hourly(iwind_data, isolar_data, isiteth_plotted=3, imonth_ploted='Apr', plot_flag=False):
	'''Assess local synergy of selected sites in hour style.
		Output graphs.
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		isiteth_plotted: the serial number of selected site.
		imonth_ploted: the selected month
		plot_flag: True or False. Draw graphs or not.
	Returns:
		the graphs of hourly variation.
	'''
	year_index = range(iwind_data.start_year, iwind_data.end_year + 1)
	year_num = len(year_index)
	site_num = len(iwind_data.site_index)
	wfc_mean_hourly = np.zeros((site_num, year_num, 24), np.float32)
	sfc_mean_hourly = np.zeros((site_num, year_num, 24), np.float32)
	for each_siteth in range(1, site_num + 1):
		for each_yearth in range(0, year_num, 1):
			for each_day in range(2, 29, 1):
				wfc_mean_hourly[each_siteth - 1, each_yearth, :] = \
				wfc_mean_hourly[each_siteth - 1, each_yearth, :] + \
				np.hstack((iwind_data.cselect_1site_1day(each_siteth, year_index[each_yearth], imonth_ploted, each_day - 1)[0, 16:24], \
					iwind_data.cselect_1site_1day(each_siteth, year_index[each_yearth], imonth_ploted,each_day)[0, 0:16]))
				sfc_mean_hourly[each_siteth - 1, each_yearth, :] = \
				sfc_mean_hourly[each_siteth - 1, each_yearth, :] + \
				np.hstack((isolar_data.cselect_1site_1day(each_siteth, year_index[each_yearth], imonth_ploted, each_day - 1)[0, 16:24], \
					isolar_data.cselect_1site_1day(each_siteth, year_index[each_yearth], imonth_ploted, each_day)[0, 0:16]))
	wfc_ploted = np.mean(wfc_mean_hourly, axis=1) / 27.0
	sfc_ploted = np.mean(sfc_mean_hourly, axis=1) / 27.0
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax1_varhour_wfc = host_subplot(111)
		ax2_varhour_sfc = ax1_varhour_wfc.twinx()
		ind = np.arange(0, 24, 1)
		ax1_varhour_wfc.plot(ind, wfc_ploted[isiteth_plotted - 1, :], 'k-o', label='Wind')
		ax2_varhour_sfc.plot(ind, sfc_ploted[isiteth_plotted - 1, :], 'b-^', label='Solar')
		ax1_varhour_wfc.set_xticks(np.linspace(0, 23, 24))
		x_lables=('00:30', '', '02:30', '', '04:30', '', '06:30', '', '08:30', '', '10:30', '', '12:30', '', '14:30', '', '16:30', \
			'', '18:30', '', '20:30', '', '22:30', '')
		ax1_varhour_wfc.set_xticklabels(x_lables)
		ax1_varhour_wfc.set_xlabel('Time')
		ax1_varhour_wfc.set_ylabel('Wind capacity factors')
		ax2_varhour_sfc.set_ylabel('Solar capacity factors')
		ax1_varhour_wfc.set_xlim(-0.7, 23.7)
		#plt.grid()
		ax1_varhour_wfc.legend(loc=1)
		plt.title('Hourly variation')
		plt.show()
		# plt.savefig('cwp43000.png', dpi=300, bbox_inches='tight')


def cass_configh(iwind_data, isolar_data, isiteth_plotted=3, plot_flag=False):
	'''Assess local synergy of selected sites.
		Search the optimal ratio of wind and solar.
		Output statistical indices and graphs.
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		isiteth_plotted: the serial number of selected site.
		plot_flag: True or False. Draw graphs or not.
	Returns:
		the graphs of hourly variation.
		optimal_raio: optimal ratio of wind and solar
	'''
	wfc_10years = iwind_data.cselect_1site_10year(isiteth_plotted)
	sfc_10years = isolar_data.cselect_1site_10year(isiteth_plotted)
	wfc_variable_coef = np.std(wfc_10years, axis=1) / np.mean(wfc_10years, axis=1)
	sfc_variable_coef = np.std(sfc_10years, axis=1) / np.mean(sfc_10years, axis=1)
	hfcvc_list=[]
	ind = np.arange(0, 1.02, 0.02)
	for each_ratio in ind:
		hfc_10years = wfc_10years * each_ratio + sfc_10years * (1 - each_ratio)
		hfc_variable_coef = np.std(hfc_10years, axis=1) / np.mean(hfc_10years, axis=1)
		hfcvc_list.append(hfc_variable_coef)
	optimal_raio = ind[np.argmin(hfcvc_list)]
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi=300)
		ax = plt.subplot(111)
		ax.axhline(y=wfc_variable_coef, xmin=0, xmax=1, color='k', ls='-.', label='Wind')
		ax.axhline(y=sfc_variable_coef, xmin=0, xmax=1, color='b', ls='--', label='Solar')
		ax.plot(ind, hfcvc_list, color='r', marker='.', label='Wind-Solar') 
		ax.set_xticks(np.arange(0, 1.1, 0.1))
		ax.set_xticklabels((0.0, '', 0.2, '', 0.4, '', 0.6, '', 0.8, '', 1.0))
		ax.set_yticks(np.linspace(0.8, 1.4, 4))
		ax.set_yticklabels((0.8, 1.0, 1.2, 1.4))
		ax.legend(loc=1)
		#ax.grid(True)
		ax.set_ylabel('Variable coefficient')
		ax.set_xlabel('Matching coefficient')
		ax.set_xlim(0, 1)
		ax.set_ylim(0.7, 1.5)
		# plt.savefig('cwp43000.png', dpi=300, bbox_inches='tight')
		plt.title('The curve of matching coefficient and variable coefficient')
		plt.show()
	return optimal_raio


def cass_rampopt(iwind_data, isolar_data, ioptimal_ratio, isiteth_plotted=3, plot_flag=False):
	'''Assess local synergy of selected sites.
		The probability distribution of ramp rate of optimal wind and solar configuration.
		Output statistical indices and graphs.
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		isiteth_plotted: the serial number of selected site.
		plot_flag: True or False. Draw graphs or not.
	Returns:
		the graphs of hourly variation.
		hfc_ramp_rate: the ramp rate of optimal wind and solar configuration.
	'''
	wfc_10years = iwind_data.cselect_1site_10year(isiteth_plotted)
	sfc_10years = isolar_data.cselect_1site_10year(isiteth_plotted)
	hfc_10years = wfc_10years * ioptimal_ratio + (1 - ioptimal_ratio) * sfc_10years
	hfc_10years_tmp = np.hstack((hfc_10years[0, 1:].reshape(-1, 1), hfc_10years[0, 0:-1].reshape(-1, 1)))
	hfc_ramp_rate = np.subtract.reduce(hfc_10years_tmp, axis=1)
	if plot_flag == True:
		plt.rcParams['font.family'] = 'Times New Roman'
		plt.figure(dpi = 300)
		axh = plt.subplot(111)
		cnh,binsh,steph = axh.hist(hfc_ramp_rate, bins=40, normed=True, histtype='barstacked', color='b')
		axh.set_ylabel('Probability density')
		axh.set_xlabel('Wind-solar ramp rate')
		axh.set_xticks(np.arange(-0.2, 0.3, 0.1))
		axh.set_xticklabels((-0.2, -0.1, 0.0, 0.1, 0.2))
		axh.set_yticks(np.linspace(0, 15, 4))
		axh.set_yticklabels((0, 5, 10, 15))
		#axh.grid(True)
		plt.title('The distribution of ramp rate')
		plt.show()
		# plt.savefig('cwp43000.png', dpi=300, bbox_inches='tight')
	return hfc_ramp_rate


def cass_single_site(iwind_data, isolar_data, isiteth=3):
	'''Assess local synergy of selected sites.
		Output statistical indices.
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		isiteth: the serial number of selected site.
	Returns:
		matching_coef_opt: optimal ratio of wind and solar.
		hfc_mean_yearly: means of optimal wind and solar configuration in year scale.
		hfc_mean_hourly: means of optimal wind and solar configuration in hour scale.
		hfc_std_hourly: std of optimal wind and solar configuration in hour scale.
		hfc_varcoef_hourly: variable coefficient of optimal wind and solar configuration in hour scale.
		hfc_half_prob: half power probability
		hfc_ramp_rate: the ramp rate of optimal wind and solar configuration.
		fc_ramp_mean: mean of ramp rate.
		fc_ramp_std: std of ramp rate.
		fc_ramp_max: max of ramp rate. 
		fc_ramp_min: min of ramp rate.
		fc_ramp_upper: upper value of 95% confidence interval ramp rate.
		fc_ramp_lower: lower value of 95% confidence interval ramp rate.
		improving_coef: the improving coefficient
		local_synergy_coef: the local synergy coefficient
	'''
	matching_coef_opt = cass_configh(iwind_data, isolar_data, isiteth, False)
	hfc_ramp_rate = cass_rampopt(iwind_data, isolar_data, matching_coef_opt, 3, False)
	wfc_10years = iwind_data.cselect_1site_10year(isiteth)
	sfc_10years = isolar_data.cselect_1site_10year(isiteth)
	hfc_10years = wfc_10years * matching_coef_opt + (1 - matching_coef_opt) * sfc_10years
	hfc_mean_yearly = np.sum(hfc_10years) / 10.0
	hfc_mean_hourly = np.mean(hfc_10years)
	hfc_std_hourly = np.std(hfc_10years)
	hfc_varcoef_hourly = hfc_mean_hourly * 1.0 / hfc_std_hourly
	hfc_half_prob = (hfc_10years[0, hfc_10years[0, :] > 0.5].shape[0]) / (hfc_10years.shape[1])
	hfc_ramp_rate = cass_rampopt(wind_data, solar_data, matching_coef_opt, 3, False)
	hfc_ramp_mean = np.mean(hfc_ramp_rate)
	hfc_ramp_std = np.std(hfc_ramp_rate)
	hfc_ramp_max = np.max(hfc_ramp_rate)
	hfc_ramp_min = np.min(hfc_ramp_rate)
	hfc_ramp_upper = hfc_ramp_mean + 1.96 * hfc_ramp_std
	hfc_ramp_lower = hfc_ramp_mean - 1.96 * hfc_ramp_std
	wfc_mean_hourly = np.mean(wfc_10years)
	wfc_std_hourly = np.std(wfc_10years)
	wfc_varcoef_hourly = wfc_mean_hourly * 1.0 / wfc_std_hourly
	sfc_mean_hourly = np.mean(sfc_10years)
	sfc_std_hourly = np.std(sfc_10years)
	sfc_varcoef_hourly = sfc_mean_hourly * 1.0 / sfc_std_hourly
	improving_coef = 1 - hfc_varcoef_hourly / (matching_coef_opt * wfc_varcoef_hourly + \
		(1 - matching_coef_opt)* sfc_varcoef_hourly)
	local_synergy_coef = 1 - 0.5 * stats.pearsonr(wfc_10years[0, :], sfc_10years[0, :])[0]
	return matching_coef_opt, hfc_mean_yearly, hfc_mean_hourly, hfc_std_hourly, hfc_varcoef_hourly, hfc_half_prob, hfc_ramp_rate, \
	hfc_ramp_mean, hfc_ramp_std, hfc_ramp_max, hfc_ramp_min, hfc_ramp_upper, hfc_ramp_lower, improving_coef, local_synergy_coef


def cass_attr_constr(iwind_data, isolar_data, imode=0):
	'''Construct new attirbutes.
		Output statistical indices 
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		imode: 0, 1, 2, 3. means in year scale variable coefficient in hour scale, matching coefficient, local synergy coefiicient
	Returns: 
		the constructed attributes.
	'''
	wf_10yearstl = iwind_data.c2style_10year(True)
	sf_10yearstl = isolar_data.c2style_10year(True)
	hf_10yearstl = {}
	site_num = len(iwind_data.site_index)
	year_index = range(iwind_data.start_year, iwind_data.end_year + 1)
	year_num = len(year_index)
	matching_coef_opt = np.zeros((1, site_num), np.float32)
	interval = np.arange(0, 1.02, 0.02)
	for each_siteth in range(1, site_num + 1, 1):
		hfcvc_list=[]
		for each_ratio in interval:
			hf_10yearstl_tmp = wf_10yearstl[each_siteth] * each_ratio + sf_10yearstl[each_siteth] * (1 - each_ratio)
			hfc_variable_coef = np.std(hf_10yearstl_tmp, axis=1) / np.mean(hf_10yearstl_tmp, axis=1)
			hfcvc_list.append(hfc_variable_coef)
		matching_coef_opt[0, each_siteth - 1] = interval[np.argmin(hfcvc_list)]
		hf_10yearstl[each_siteth] = \
		wf_10yearstl[each_siteth] * matching_coef_opt[0,each_siteth-1] + sf_10yearstl[each_siteth] * (1-matching_coef_opt[0,each_siteth-1])
	if imode == 0:
		hfc_mean_yearly = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			hfc_mean_yearly[0, each_siteth-1] = \
			np.sum(hf_10yearstl[each_siteth], axis=1) * 1.0 / year_num
		return hfc_mean_yearly
	elif imode == 1:
		hfc_varcoef_hourly = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			hfc_varcoef_hourly[0, each_siteth-1] = \
			np.std(hf_10yearstl[each_siteth], axis=1) * 1.0 / np.mean(hf_10yearstl[each_siteth], axis=1)
		return hfc_varcoef_hourly
	elif imode == 2:
		improving_coef = np.zeros((1, site_num), np.float32)
		wfc_varcoef_hourly = masw.cass_attr_constr(iwind_data, 2)
		sfc_varcoef_hourly = masw.cass_attr_constr(isolar_data, 2)
		for each_siteth in range(1, site_num + 1, 1):
			improving_coef[0, each_siteth-1] = \
			1 - ((np.std(hf_10yearstl[each_siteth], axis=1) * 1.0 / np.mean(hf_10yearstl[each_siteth], axis=1))) / \
			(wfc_varcoef_hourly[0, each_siteth-1] * matching_coef_opt[0, each_siteth - 1] + 
				sfc_varcoef_hourly[0, each_siteth-1] * (1 - matching_coef_opt[0, each_siteth - 1]))
		return improving_coef
	else:
		local_synergy_coef = np.zeros((1, site_num), np.float32)
		for each_siteth in range(1, site_num + 1, 1):
			local_synergy_coef[0, each_siteth-1] = \
			0.5 - 0.5 * stats.pearsonr(wf_10yearstl[each_siteth][0, :], sf_10yearstl[each_siteth][0, :])[0]
		return local_synergy_coef


def cass_output_prob(iwind_data, isolar_data, isiteth=3):
	'''Assess local synergy of selected sites.
		The probability distribution of capacity factors.
		Output statistical indices 
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		isiteth: the serial number of selected site.
	Returns: 
		the garphs of pdfs and cdfs.
	'''
	matching_coef_opt = cass_configh(iwind_data, isolar_data, isiteth, False)
	wfc_10years = iwind_data.cselect_1site_10year(isiteth)
	sfc_10years = isolar_data.cselect_1site_10year(isiteth)
	hfc_10years = wfc_10years * matching_coef_opt + (1 - matching_coef_opt) * sfc_10years 
	wfc_output = np.empty((0,),np.float32)
	sfc_output = np.empty((0,),np.float32)
	hfc_output = np.empty((0,),np.float32)
	interval = np.arange(-0, 1.05, 0.05)
	for each in interval:
		hfc_output = np.hstack((hfc_output,(hfc_10years[0, hfc_10years[0, :] <= each].shape[0] * 100.0 / hfc_10years.shape[1])))
		sfc_output = np.hstack((sfc_output,(sfc_10years[0, sfc_10years[0, :] <= each].shape[0] * 100.0 / sfc_10years.shape[1])))
		wfc_output = np.hstack((wfc_output,(wfc_10years[0, wfc_10years[0, :] <= each].shape[0] * 100.0 / wfc_10years.shape[1])))
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.figure(dpi=300)
	plt.title('The PDF and CDF of capacity factors', fontsize=8)
	ax1 = plt.subplot(221)
	cn1, bins1, step1 = ax1.hist(wfc_10years.reshape(-1, 1), bins=20, normed=True, histtype='barstacked', color='b')
	ax1.set_xticks(np.linspace(0,1,6))
	ax1.set_xticklabels((0.0, 0.2, 0.4, 0.6, 0.8, 1.0), rotation=0, fontsize=8)
	ax1.set_yticks(np.linspace(0, 4, 5))
	ax1.set_yticklabels((0, 1, 2, 3, 4), rotation=90, fontsize=8)
	ax1.set_xlim(-0.005, 1.005)
	ax1.set_ylim(-0.005, 4.5)
	ax1.set_xlabel('Wind capacity factor\n(a)', fontsize=8)
	ax1.set_ylabel('Probability density', fontsize=8)
	ax2 = plt.subplot(222)
	cn2, bins2, step2 = ax2.hist(sfc_10years.reshape(-1, 1), bins=20 , normed=True, histtype='stepfilled', color='b')
	ax2.set_xticks(np.linspace(0, 1, 6))
	ax2.set_xticklabels((0.0, 0.2, 0.4, 0.6, 0.8, 1.0), rotation=0, fontsize=8)
	ax2.set_yticks(np.linspace(0, 4, 5))
	ax2.set_yticklabels((0, 1, 2, 3, 4), rotation=90, fontsize=8)
	ax2.set_xlim(-0.005, 1.005)
	ax2.set_ylim(-0.005, 4.5)
	ax2.set_xlabel('Solar capacity factor\n(b)', fontsize=8)
	ax2.set_ylabel('Probability density', fontsize=8)
	ax3 = plt.subplot(223)
	cn3, bins3, step3 = ax3.hist(hfc_10years.reshape(-1, 1), bins=20, normed=True, histtype='stepfilled', color='b')
	ax3.set_xticks(np.linspace(0, 1, 6))
	ax3.set_xticklabels((0.0, 0.2, 0.4, 0.6, 0.8, 1.0), rotation=0, fontsize=8)
	ax3.set_yticks(np.linspace(0, 4, 5))
	ax3.set_yticklabels((0, 1, 2, 3, 4), rotation=90, fontsize=8)
	ax3.set_xlim(-0.005, 1.005)
	ax3.set_ylim(-0.005, 4.5)
	ax3.set_xlabel('Wind-solar capacity factor\n(c)', fontsize=8)
	ax3.set_ylabel('Probability density', fontsize=8)
	ax4 = plt.subplot(224)
	ax4.plot(interval, wfc_output, 'k-o', label='Wind', markersize=3, linewidth=1)
	ax4.plot(interval, sfc_output, 'b-^', label='Solar', markersize=3, linewidth=1)
	ax4.plot(interval, hfc_output, 'r-d', label='Wind-solar', markersize=3, linewidth=1)
	ax4.legend(fontsize=6, loc=4, ncol=1)
	ax4.set_xticks(np.linspace(0, 1, 5))
	ax4.set_xticklabels((0.0, 0.25, 0.5, 0.75, 1.00), rotation=0, fontsize=8)
	ax4.set_yticks(np.linspace(0, 100, 6))
	ax4.set_yticklabels((0, 20, 40, 60, 80,100), rotation=90, fontsize=8)
	ax4.set_xlim(-0.025, 1.005)
	ax4.set_ylim(-2.5, 105)
	ax4.set_xlabel('Capacity factor\n(d)', fontsize=8)
	ax4.set_ylabel('Probability (%)', fontsize=8)
	plt.subplots_adjust(wspace=0.25, hspace=0.42)
	plt.show()
	# plt.savefig('cPlotHNew0.png', dpi=300, bbox_inches='tight')


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
	solar_capacity_factor = solar_data.csolar2cf()

	cass_single_site(wind_data, solar_data, 3)
	cass_varh_monthly(wind_data, solar_data, 3, 2010, True)
	cass_varh_hourly(wind_data, solar_data, 3, 'Apr', True)
	optimal_raio = cass_configh(wind_data, solar_data, 3, True)
	print optimal_raio
	hfc_ramp_rate = cass_rampopt(wind_data, solar_data, optimal_raio, 3, True)
	assess_result = cass_single_site(wind_data, solar_data, 3)
	attr = cass_attr_constr(wind_data, solar_data, 0)
	cass_output_prob(wind_data, solar_data, 3)
	
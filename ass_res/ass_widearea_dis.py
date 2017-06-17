#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 09:31:51 2017
########################################################################################
# @ File name: ass_widearea_dis.py
# @ Function: Perform wide-area assessment.
# 	Assess the spatial distribution of resources, local synergy effects, 
# 	and the spatial effects of one site.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 0.1.2
# @ Revision date: Jun/17/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np

import init_nasa_wind as mwind
import init_nasa_solar as msolar
import draw_geo_fig as mdgf
import ass_singlesite_ws as masw
import ass_singlesite_lsy as maslsy
import ass_widearea_wsy as mawwsy


def ass_wide_ws(isource_data, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat, imode=0):
	'''Assess the spatial distribution of wind and solar resources.
		Output statistical indices and graphs.
	Args:
		isource_data: the source data.
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, and region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
		imode: 0, 1, 2, 3. means in year scale, std in hour scale, variable coefficient in hour scale, means in hour scale
	Returns:
		the graphs.
		attri: the selected attribute.
		the max value of the selected attribute.
		the serial number of site of the max value.
		the min value of the selected attribute.
		the serial number of site of the min value.
	'''
	attri = masw.cass_attr_constr(isource_data, imode)
	mdgf.cdraw_contour_fig(attri, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat)
	return attri, np.max(attri, axis=1), np.argmax(attri, axis=1) + 1, \
	np.min(attri, axis=1), np.argmin(attri, axis=1) + 1


def ass_wide_lsy(iwind_data, isolar_data, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat, imode=0):
	'''Assess the spatial distribution of local synergy effects.
		Output statistical indices and graphs.
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, the region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
		imode: 0, 1, 2, 3. means in year scale variable coefficient in hour scale, matching coefficient, local synergy coefiicient
	Returns:
		the graphs.
		attri: the selected attribute.
		the max value of the selected attribute.
		the serial number of site of the max value.
		the min value of the selected attribute.
		the serial number of site of the min value.
	'''
	attri = maslsy.cass_attr_constr(iwind_data, isolar_data, imode)
	mdgf.cdraw_contour_fig(attri, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat)
	return attri, np.max(attri, axis=1), np.argmax(attri, axis=1) + 1, \
	np.min(attri, axis=1), np.argmin(attri, axis=1) + 1


def ass_site_wsy(iwind_data, isolar_data, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat, isiteth=71, imode=0):
	'''Assess the spatial distribution of the spatial effects of a selected site.
		Output statistical indices and graphs.
	Args:
		iwind_data: the source wind data.
		isolar_data: the source solar data.
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, and region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
		isiteth: the serial number of the selected site.
		imode: 0, 1, 2, 3. the spatial wind-wind synergy coefficient, spatial solar-solar synergy coefficient, 
			spatial wind-solar synergy coefficient, spatial solar-wind synergy coefficient
	Returns:
		the graphs.
		attri: the selected attribute.
		the max value of the selected attribute.
		the serial number of site of the max value.
		the min value of the selected attribute.
		the serial number of site of the min value.
	'''
	attri = mawwsy.ccalc_synergy_coef(iwind_data, isolar_data, imode, isiteth)
	mdgf.cdraw_contour_fig(attri, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat)
	return attri, np.max(attri, axis=1), np.argmax(attri, axis=1) + 1, \
	np.min(attri, axis=1), np.argmin(attri, axis=1) + 1


if __name__ == '__main__':
	'''Examples.'''
	start_year = 2006
	end_year = 2015
	site_index = [(-2, 0), (-2, 1), (-2, 2), (-2, 3), (-2, 4), (-2, 5), (-2, 6), 
	(-2, 7), (-2, 8), (-2, 9), (-2, 10), (-2, 11), (-2, 12), (-2, 13), (-2, 14), 
	(-3, 0), (-3, 1), (-3, 2), (-3, 3), (-3, 4), (-3, 5), (-3, 6), 
	(-3, 7), (-3, 8), (-3, 9), (-3, 10), (-3, 11), (-3, 12), (-3, 13), (-3, 14), 
	(-4, 0), (-4, 1), (-4, 2), (-4, 3), (-4, 4), (-4, 5), (-4, 6), 
	(-4, 7), (-4, 8), (-4, 9), (-4, 10), (-4, 11), (-4, 12), (-4, 13), (-4, 14), 
	(-5, 0), (-5, 1), (-5, 2), (-5, 3), (-5, 4), (-5, 5), (-5, 6), 
	(-5, 7), (-5, 8), (-5, 9), (-5, 10), (-5, 11), (-5, 12), (-5, 13), (-5, 14), 
	(-6, 0), (-6, 1), (-6, 2), (-6, 3), (-6, 4), (-6, 5), (-6, 6), 
	(-6, 7), (-6, 8), (-6, 9), (-6, 10), (-6, 11), (-6, 12), (-6, 13), (-6, 14), 
	(-7, 0), (-7, 1), (-7, 2), (-7, 3), (-7, 4), (-7, 5), (-7, 6), 
	(-7, 7), (-7, 8), (-7, 9), (-7, 10), (-7, 11), (-7, 12), (-7, 13), (-7, 14), 
	(-8, 0), (-8, 1), (-8, 2), (-8, 3), (-8, 4), (-8, 5), (-8, 6), 
	(-8, 7), (-8, 8), (-8, 9), (-8, 10), (-8, 11), (-8, 12), (-8, 13), (-8, 14), 
	(-9, 0), (-9, 1), (-9, 2), (-9, 3), (-9, 4), (-9, 5), (-9, 6), 
	(-9, 7), (-9, 8), (-9, 9), (-9, 10), (-9, 11), (-9, 12), (-9, 13), (-9, 14), 
	(-10, 0), (-10, 1), (-10, 2), (-10, 3), (-10, 4), (-10, 5), (-10, 6), 
	(-10, 7), (-10, 8), (-10, 9), (-10, 10), (-10, 11), (-10, 12), (-10, 13), (-10, 14), 
	(-11, 0), (-11, 1), (-11, 2), (-11, 3), (-11, 4), (-11, 5), (-11, 6), 
	(-11, 7), (-11, 8), (-11, 9), (-11, 10), (-11, 11), (-11, 12), (-11, 13), (-11, 14)]
	wfile_name = 'sd_wind_data'
	sfile_name = 'sd_solar_data'

	outline = (114, 34, 123, 38.5)
	names = ('CHN_adm_shp/CHN_adm3', 'NAME_1', 'Shandong')
	lat_lable = (34, 39, 0.5)
	lon_lable = (114, 124, 1)
	site_lon = [118, 118.667, 
	116.667, 117.333, 118, 118.667, 120, 120.667, 121.333, 122, 
	116, 116.667, 117.333, 118, 118.667, 119.333, 120, 120.667, 121.333, 122, 
	115.333, 116, 116.667, 117.333, 118, 118.667, 119.333, 120, 120.667, 
	115.333, 116, 116.667, 117.333, 118, 118.667, 119.333, 120, 120.667, 
	115.333, 116, 116.667, 117.333, 118, 118.667, 119.333, 
	115.333, 116, 116.667, 117.333, 118, 118.667, 
	115.333, 116, 117.333, 118]
	site_lat = [38, 38, 
	37.5, 37.5, 37.5, 37.5, 37.5, 37.5, 37.5, 37.5, 
	37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 
	36.5, 36.5, 36.5, 36.5, 36.5, 36.5, 36.5, 36.5, 36.5, 
	36, 36, 36, 36, 36, 36, 36, 36, 36, 
	35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 35.5, 
	35, 35, 35, 35, 35, 35, 
	34.5, 34.5, 34.5, 34.5]

	wind_data = mwind.WindData(wfile_name, site_index, start_year, end_year)
	wind_speed_ref = wind_data.cimport_data()
	wind_speed_hw = wind_data.cref2hw()
	wind_capacity_factor = wind_data.cwind2cf()
	solar_data = msolar.SolarData(sfile_name, site_index, start_year, end_year)
	solar_irrad_data = solar_data.cimport_data()
	solar_capacity_factor = solar_data.csolar2cf()

	fc_mean_yearly = ass_wide_ws(wind_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 0)
	fc_std_hourly = ass_wide_ws(wind_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 1)
	fc_varcoef_hourly = ass_wide_ws(wind_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 2)
	fc_mean_hourly = ass_wide_ws(wind_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 3)

	hfc_mean_yearly = ass_wide_lsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 0)
	hfc_varcoef_hourly = ass_wide_lsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 1)
	improving_coef = ass_wide_lsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 2)
	local_synergy_coef = ass_wide_lsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 3)

	synergy_1coef_ww = ass_site_wsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 71, 0)
	synergy_1coef_ss = ass_site_wsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 71, 1)
	synergy_1coef_ws = ass_site_wsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 71, 2)
	synergy_1coef_sw = ass_site_wsy(wind_data, solar_data, outline, names, lat_lable, lon_lable, site_lon, site_lat, 71, 3)
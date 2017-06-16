#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 11:12:21 2017
########################################################################################
# @ File name: ass_widearea_wsy.py
# @ Function: Perform wide-area assessment.
# 	Assess the spatial synergy effects.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 0.1.2
# @ Revision date: Jun/16/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score

import init_nasa_wind as mwind
import init_nasa_solar as msolar
import draw_geo_fig as mdgf


def ccalc_synergy_coef(iwind_data, isolar_data, imode=0, isiteth=0):
	'''Calculate the spatial synergy coefficients
	Args:
		iwind_data: the source wind data.
		isource_data: the source solar data.
		imode: 0, 1, 2, 3. the spatial wind-wind synergy coefficient, spatial solar-solar synergy coefficient, 
			spatial wind-solar synergy coefficient, spatial solar-wind synergy coefficient
		isiteth: the serial number of the selected site.
	Returns:
		synergy_coef_nor: the spatial synergy coefficients.
	'''
	wf_10yearstl = iwind_data.c2style_10year(True)
	sf_10yearstl = isolar_data.c2style_10year(True)
	site_num = len(iwind_data.site_index)
	year_index = range(iwind_data.start_year, iwind_data.end_year + 1)
	year_num = len(year_index)
	if isiteth == 0:
		pearson_coef = np.zeros((site_num, site_num), np.float32)
		if imode == 0:
			fc_0 = wf_10yearstl
			fc_1 = wf_10yearstl
		elif imode == 1:
			fc_0 = sf_10yearstl
			fc_1 = sf_10yearstl
		elif imode == 2:
			fc_0 = wf_10yearstl
			fc_1 = sf_10yearstl
		else:
			fc_0 = sf_10yearstl
			fc_1 = wf_10yearstl
		for each_siteth0 in range(1, site_num + 1, 1):
			for each_siteth1 in range(1, site_num + 1, 1):
				pearson_coef[each_siteth0 - 1, each_siteth1 - 1] = \
				stats.pearsonr(fc_0[each_siteth0][0, :], fc_1[each_siteth1][0, :])[0]
		synergy_coef = (1 - pearson_coef) / 2.0
		synergy_coef_nor = np.empty((site_num, site_num), np.float32)
		for each_siteth in range(0, site_num, 1):
			synergy_coef_nor = \
			np.hstack((synergy_coef_nor, ((synergy_coef[:, each_siteth] - \
				np.min(synergy_coef[:, each_siteth])) / np.ptp(synergy_coef[:, each_siteth])).reshape(site_num, - 1)))
	else:
		pearson_coef = np.zeros((1, site_num), np.float32)
		if imode == 0:
			fc_0 = wf_10yearstl[isiteth]
			fc_1 = wf_10yearstl
		elif imode == 1:
			fc_0 = sf_10yearstl[isiteth]
			fc_1 = sf_10yearstl
		elif imode == 2:
			fc_0 = wf_10yearstl[isiteth]
			fc_1 = sf_10yearstl
		else:
			fc_0 = sf_10yearstl[isiteth]
			fc_1 = wf_10yearstl
		for each_siteth in range(1, site_num + 1, 1):
			pearson_coef[0, each_siteth - 1] = \
			stats.pearsonr(fc_0[0, :], fc_1[each_siteth][0, :])[0]
		synergy_coef = (1 - pearson_coef) / 2.0
		synergy_coef_nor = synergy_coef
	return synergy_coef_nor


def csearch_centroid (idata_index, isy_coef, icluster_num=6):
	'''Search the centroid of each cluster.
	Args:
		idata_index: the clustering indices of source data.
		isy_coef: the spatial synergy coefficients processed by the PCA.
		icluster_num: the number of clusters.
	Returns:
		centroid_site + 1: the serial number of the searched centroids.
	'''
	centroid_site = np.zeros((1, icluster_num), np.float32)
	for each0 in range(0,icluster_num,1):
		num = len(idata_index[each0])
		tmp = np.zeros((1,num), np.float32)
		for each1 in range(num):
			for each2 in idata_index[each0]:
				if idata_index[each0][each1] != each2:
					tmp[0, each1] = tmp[0,each1] + ((isy_coef[idata_index[each0][each1], 0]) ** \
						2 - (isy_coef[each2, 0]) ** 2) ** 0.5
		centroid_site[0, each0] = idata_index[each0][np.argmin(tmp)]
	return centroid_site + 1


def cpca_and_cluster(ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat, isynergy_coef, icomponent_num=1, icluster_num=6):
	'''Assess the spatial synergy effects by the PCA and k-menas clustering.
	Args:
		ioutline: the outlines of the background.
		inames: the filename of geographical data, information name, and the region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
		isynergy_coef: the spatial synergy coefficients.
		icomponent_num: the number of principal components.
		icluster_num: the number of clusters
	Returns:
		the graphs.
		pca_evr: the explained variance of each components of the PCA
		centroid_site: the serial number of the searched centroids.
		data_index: the clustering indices of source data.
		sycoef_pca_nor: he spatial synergy coefficients processed by the PCA.
		silhouette_avg: the average silhouette coefficients.
		silhouette_sample: the silhouette coefficients.
	'''
	pca_instance = PCA(n_components=icomponent_num)
	pca_instance.fit(isynergy_coef)
	pca_component = pca_instance.components_
	pca_evr = pca_instance.explained_variance_ratio_

	sycoef_pca = pca_instance.transform(isynergy_coef)
	sycoef_pca_nor = (sycoef_pca - np.mean(sycoef_pca, axis=0)) / np.std(sycoef_pca, axis=0)
	kmeans_instance = KMeans(n_clusters=icluster_num)
	sycoef_kmeans = kmeans_instance.fit(sycoef_pca_nor)
	sycoef_km_label = sycoef_kmeans.labels_
	sycoef_km_center = sycoef_kmeans.cluster_centers_
	sycoef_km_inertia = sycoef_kmeans.inertia_
	data_index = []
	for each_cluster in range(0, icluster_num, 1):
		data_index.append([x for x in range(0, isynergy_coef.shape[0]) if sycoef_km_label[x] == each_cluster])
	silhouette_avg = silhouette_score(sycoef_pca_nor, sycoef_km_label)
	silhouette_sample = silhouette_samples(sycoef_pca_nor, sycoef_km_label)
	centroid_site = csearch_centroid (data_index, sycoef_pca_nor, icomponent_num)
	mdgf.cdraw_cluster_fig(data_index, icluster_num, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat)
	return pca_evr, centroid_site, data_index, sycoef_pca_nor, silhouette_avg, silhouette_sample


def canal_cluster(iwind_data, isolar_data, icentroid_site0, icentroid_site1, imode=0, icluster_num=6):
	'''Assess the spatial synergy effects by the PCA and k-menas clustering.
	Args:
		wind_data: the source wind data.
		isource_data: the source solar data.
		icentroid_site0: the serial number of the searched centroids of mode 0 of spatial synergy effects.
		icentroid_site1: the serial number of the searched centroids of mode 1 of spatial synergy effects.
		imode: 0, 1, 2, 3. the spatial wind-wind synergy coefficient, spatial solar-solar synergy coefficient, 
			spatial wind-solar synergy coefficient, spatial solar-wind synergy coefficient
		icluster_num: the number of clusters
	Returns:
		the max value of the selected attribute.
		the serial number of site of the max value.
		the min value of the selected attribute.
		the serial number of site of the min value.
	'''
	wf_10yearstl = iwind_data.c2style_10year(True)
	sf_10yearstl = isolar_data.c2style_10year(True)
	synergy_coef = np.zeros((icluster_num, icluster_num), np.float32)
	if imode == 0:
		fc_0 = wf_10yearstl
		fc_1 = wf_10yearstl
	elif imode == 1:
		fc_0 = sf_10yearstl
		fc_1 = sf_10yearstl
	elif imode == 2:
		fc_0 = wf_10yearstl
		fc_1 = sf_10yearstl
	else:
		fc_0 = sf_10yearstl
		fc_1 = wf_10yearstl
	for each0 in range(0, icluster_num, 1):
		for each1 in range(0, icluster_num, 1):
			synergy_coef[each0, each1] = \
			stats.pearsonr(fc_0[icentroid_site0[each0]][0, :], fc_1[icentroid_site1[each1]][0, :])[0]
	synergy_coef = (1 - synergy_coef) /2.0
	return icentroid_site1[np.argmax(synergy_coef, axis=0)], np.max(synergy_coef, axis=0), \
	icentroid_site1[np.argmin(synergy_coef, axis=0)], np.min(synergy_coef, axis=0)


if __name__ == '__main__':
	'''Examples.'''
	start_year = 2006
	end_year = 2015
	site_index = [(-3, 6), (-3, 7), 
	(-4, 4), (-4, 5), (-4, 6), (-4, 7), (-4, 9), (-4, 10), (-4, 11), (-4, 12), 
	(-5, 3), (-5, 4), (-5, 5), (-5, 6), (-5, 7), (-5, 8), (-5, 9), (-5, 10), (-5, 11), (-5, 12), 
	(-6, 2), (-6, 3), (-6, 4), (-6, 5), (-6, 6), (-6, 7), (-6, 8), (-6, 9), (-6, 10), 
	(-7, 2), (-7, 3), (-7, 4), (-7, 5), (-7, 6), (-7, 7), (-7, 8), (-7, 9), (-7, 10), 
	(-8, 2), (-8, 3), (-8, 4), (-8, 5), (-8, 6), (-8, 7), (-8, 8), 
	(-9, 2), (-9, 3), (-9, 4), (-9, 5), (-9, 6), (-9, 7), 
	(-10, 2), (-10, 3), (-10, 5), (-10, 6)]
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

	synergy_coef_ww = ccalc_synergy_coef(wind_data, solar_data, 0, 0)
	assess_result_ww = cpca_and_cluster(outline, names, lat_lable, lon_lable, site_lon, site_lat, synergy_coef_ww, 3, 6)

	assresult_centroid_ww=canal_cluster(wind_data, solar_data, assess_result_ww[1], assess_result_ww[1], 0, 6)

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 20:40:31 2017
########################################################################################
# @ File name: draw_geo_fig.py
# @ Function: Draw geographical graphs.
# 	Basic graphs, contour graphs, and clustering graphs.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Version: 0.1.2
# @ Revision date: Jun/17/2017
# @ Copyright (c) 2016-2017 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def anno_txt(imap, isite_lon, isite_lat, itxt, imode=False, imarker='.', icolor='k', ilabelname='Cluster 1'):
	'''Annotate on the geographical graphs.
	Args:
		imap: the handle of the geographical graphs.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
		itxt: the annotated text.
		imode: True or False. Annote labelname or not.
		imarker: the annotated marker.
		icolor: the annotated colar.
		ilabelname: the labelname.
	Returns:
		null.
	'''
	x0, y0 = imap(isite_lon, isite_lat)
	if imode == True:
		imap.scatter(x0, y0, marker=imarker, color=icolor, label=ilabelname)
	else:
		imap.scatter(x0, y0, marker=imarker, color=icolor,)
	for x1, y1, z1 in zip(x0, y0, itxt):
		plt.text(x1, y1, z1, fontweight='bold', fontsize=12, ha='left', 
			va='bottom', color=icolor)


def cdraw_geo_ax(iax, ioutline, inames, ilat_lable, ilon_lable):
	'''Draw the geographical graphs on the given ax.
	Args:
		iax: the handle of given ax.
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, and region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
	Returns:
		bmap: the handle of the geographical graphs.
	'''
	illlong = ioutline[0]
	illlat = ioutline[1]
	iurlong = ioutline[2]
	iurlat = ioutline[3]
	bmap = Basemap(llcrnrlon=illlong, llcrnrlat=illlat, urcrnrlon=iurlong, 
		urcrnrlat=iurlat, projection='cyl', ax=iax)
	ifile_name = inames[0]
	iinfo_name = inames[1]
	iobj_name = inames[2]
	shp_info = bmap.readshapefile(ifile_name, 'states', drawbounds=False)
	for info, shp in zip(bmap.states_info, bmap.states):
		proid = info[iinfo_name]
		if proid == iobj_name:
			xc, yc = zip(*shp)
			bmap.plot(xc, yc, marker=None, color='k', lw=0.7)
	bmap.drawcountries()
	ilat_start = ilat_lable[0]
	ilat_end = ilat_lable[1]
	ilat_step = ilat_lable[2]
	ilon_start = ilon_lable[0]
	ilon_end = ilon_lable[1]
	ilon_step = ilon_lable[2]
	bmap.drawparallels(np.arange(ilat_start, ilat_end, ilat_step), labels=[1, 0, 0, 0])
	bmap.drawmeridians(np.arange(ilon_start, ilon_end, ilon_step), labels=[0, 0, 0, 1])
	return bmap


def cdraw_basic_fig(ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat):
	'''Draw the basic geographical graphs.
	Args:
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, and region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
	Returns:
		the basic geographical graphs.
	'''
	fig = plt.figure(dpi=300)
	plt.rcParams['font.family'] = 'Times New Roman'
	axc = fig.add_subplot(111)
	bmapc = cdraw_geo_ax(axc, ioutline, inames, ilat_lable, ilon_lable)
	siteth = [str(x) for x in range(1, len(isite_lon) + 1, 1)]
	anno_txt(bmapc, isite_lon, isite_lat, siteth)
	axc.set_xlabel(r'Longitude ($\mathrm{^\circ}$)', labelpad=13)
	axc.set_ylabel(r'Latitude ($\mathrm{^\circ}$)', labelpad=34)
	plt.title('The geographical graph')
	plt.show()
#	plt.savefig('Geo_graph.png', dpi=300, bbox_inches='tight')


def cdraw_contour_fig(idata, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat):
	'''Draw the contour geographical graphs.
	Args:
		idata: the source data
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, and region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
	Returns:
		the contour geographical graphs.
	'''
	fig = plt.figure(dpi=300)
	plt.rcParams['font.family'] = 'Times New Roman'
	axc = fig.add_subplot(111)
	siteth = [str(x) for x in range(1, len(isite_lon) + 1, 1)]
	lon0_num = (ioutline[2] + 1 - ioutline[0]) /2 *3 + 1
	lon0 = np.linspace(ioutline[0], ioutline[2] + 1, lon0_num)[0: -1]
	lat0_num = (ioutline[3] - ioutline[1]) * 2 + 1
	lat0 = np.linspace(ioutline[3], ioutline[1], lat0_num)
	lon1, lat1 = np.meshgrid(lon0, lat0)
	bmapc = cdraw_geo_ax(axc, ioutline, inames, ilat_lable, ilon_lable)
	data_reshape = idata.reshape((int(lat0_num), int(lon0_num) - 1))
	contourc = bmapc.contourf(lon1, lat1, data_reshape, cmap=plt.cm.jet)
	barc = bmapc.colorbar(contourc, location='bottom', pad="11%")
	anno_txt(bmapc, isite_lon, isite_lat, siteth)
	plt.title('The geographical contour')
	plt.show()
#	plt.savefig('Geo_contour.png', dpi=300, bbox_inches='tight')


def cdraw_cluster_fig(idata_index, icluster_num, ioutline, inames, ilat_lable, ilon_lable, isite_lon, isite_lat):
	'''Draw the clustering geographical graphs.
	Args:
		idata_index: the clustering indices of source data.
		icluster_num: the number of clusters.
		ioutline: the outlines of the background.
		inames: the filename of geographical data, attribute/column name, and region name.
		ilat_lable: the latitude label.
		ilon_lable: the longitude label.
		isite_lon: the longitude of the annotated site.
		isite_lat: the latitude of the annotated sites.
	Returns:
		the clustering geographical graphs.
	'''
	fig = plt.figure(dpi=300)
	plt.rcParams['font.family'] = 'Times New Roman'
	axc = fig.add_subplot(111)
	siteth = [str(x) for x in range(1, len(isite_lon) + 1, 1)]
	bmapc = cdraw_geo_ax(axc, ioutline, inames, ilat_lable, ilon_lable)
	marker_list = ['.', 'o', '^', 'd', 's', 'h']
	color_list = ['k', 'r', 'b', 'g', 'm', 'c']
	labelname_list = ['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Cluster 6']
	siteth = [str(x) for x in range(1, len(isite_lon) + 1, 1)]
	for each0 in range(0, icluster_num):
		lonth_list = []
		latth_list = []
		siteth_list = []
		for each1 in idata_index[each0]:
			lonth_list.append(isite_lon[each1])
			latth_list.append(isite_lat[each1])
			siteth_list.append(siteth[each1])
		anno_txt(bmapc, lonth_list, latth_list, siteth_list, True, marker_list[each0], color_list[each0], labelname_list[each0])
	# plt.legend(loc=3,ncol=3)
	plt.legend(fontsize=9, loc=4, ncol=1)
	# plt.savefig('clusteringWW.png', dpi=300, bbox_inches='tight')
	plt.title('The clustering graph')
	plt.show()


if __name__ == '__main__':
	'''Examples.'''
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

	cdraw_basic_fig(outline, names, lat_lable, lon_lable, site_lon, site_lat)
#	cdraw_contour_fig(c1HyMean, outline, names, lat_lable, lon_lable, site_lon, site_lat)
#	cdraw_cluster_fig(indexWW, kWW.n_clusters, outline, names, lat_lable, lon_lable, site_lon, site_lat)
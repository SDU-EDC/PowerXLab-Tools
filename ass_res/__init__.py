#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 15:42:16 2017
########################################################################################
# @ File name: __init_.py
# @ Function: Assess and visualize the spatiotemporal characteristics of regional wind 
	and solar energy sources to support perliminary regional planning.
# @ Author: Yongji Cao, Hengxu Zhang
# @ Requirements：
# 	Python 2.7 (or higher)
# 	numpy (Python package)
# 	matplotlib (Python package)
# 	basemap (Python package)
# 	scipy (Python package)
# 	pyhdf (Python package)
# 	sklearn (Python package)
# 	Ten-year wind speed, solar irradiation and ambient temperature data (Data)
# 	Geographical data in shapefile file format (Data)
# 	In-situ measured data for correction (Data)
# @ Version: 1.0
# @ Revision date: Jan/19/2018
# @ Copyright (c) 2016-2018 School of Electrical Engineering, Shandong University, China
########################################################################################
"""


__all__ = ['init_nasa_wind', 'init_nasa_solar', 'ass_singlesite_ws', 
'ass_singlesite_lsy', 'draw_geo_fig', 'ass_widearea_dis', 'ass_widearea_wsy']

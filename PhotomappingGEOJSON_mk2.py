import pandas as pd
import numpy as np
import geopandas as gpd 
from shapely import wkt

from sys import argv
import time

script, feeder_file = argv
print("Begin" + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

photomapping_gdf = gpd.GeoDataFrame.from_file(feeder_file)

print("GDF Created" + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

#photomapping_gdf['location_wkt'] = photomapping_gdf['location_wkt'].apply(wkt.loads)
#photomapping_gdf.set_geometry(col='location_wkt', drop=True, inplace=True)
photomapping_gdf.drop(columns = ['DOCUMENT_TYPE', 'DOCUMENT_UPDATE_DATE', 'DOCUMENT_SECURITY_CLASSIFICATION',
       'DOCUMENT_STATUS', 'DOCUMENT_PURPOSE',
       'DOCUMENT_TEMPLATE', 'ASSET_CATEGORY', 'SERVICE_STATUS', 'DEPOT',
       'WORK_ACTIVITY_ID', 'WORK_ORDER_ID',
       'LOCATION_ID', 'PROJECT_ID', 'DESIGN_ID', 'ATTACHEMENT_ID', 'USER_ID',
       'PROCESSSTATUS', 'RECORD_INSERT_DATETIME', 'RECORD_UPDATE_DATETIME',
       'RECORD_INSERTE_BY', 
       'URL_TYPE'], axis = 1, inplace = True)

print("Columns Dropped" + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

photomapping_gdf['geometry'] = gpd.points_from_xy(photomapping_gdf.W1_GEO_LONG, photomapping_gdf.W1_GEO_LAT)
photomapping_gdf.set_geometry(col='geometry', drop=True, inplace=True)

print("Geometry Dropped")

photomapping_gdf.replace("NULL", np.nan, inplace = True)

print("Nulls replaced" + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))


print(photomapping_gdf.columns)

#photomapping_df.to_json(r'C:\Users\mdawson\OneDrive - Essential Energy\Documents\DAM\PhotoIntegration_NearaWACs\PhotoMapping_FileFormat.json',orient='records')

#photomapping_gdf.to_file(r'C:\Users\mdawson\OneDrive - Essential Energy\Documents\DAM\PhotoIntegration_NearaWACs\PhotoMapping_assets01oct24.geojson', driver='GeoJSON')

with open(r'C:\Users\mdawson\OneDrive - Essential Energy\Documents\DAM\PhotoIntegration_NearaWACs\fullruns\UATLocationImages.geojson', "w") as f:
    f.write(photomapping_gdf.to_json(na="drop"))


print("end" + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

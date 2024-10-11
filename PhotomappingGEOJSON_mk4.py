import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import wkt

from sys import argv
import time

#full run
script, asset_images, location_images, workactivity_images, output_filename = argv 
#partial run - assets only
#script, asset_images, output_filename = argv 

AssetImagesRaw = pd.read_csv(asset_images)
print("Asset Raw " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

LocationImagesRaw = pd.read_csv(location_images)
print("Location Raw " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

WorkActivityRaw = pd.read_csv(workactivity_images)
print("Activity Raw " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))


frames = [AssetImagesRaw, LocationImagesRaw, WorkActivityRaw]
photomapping_df = pd.concat(frames)
print("Combined DF Created " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

photomapping_df.drop(columns = ['DOCUMENT_TYPE', 'DOCUMENT_UPDATE_DATE', 'DOCUMENT_SECURITY_CLASSIFICATION',
       'DOCUMENT_STATUS', 'DOCUMENT_PURPOSE',
       'DOCUMENT_TEMPLATE', 'ASSET_CATEGORY', 'SERVICE_STATUS', 'DEPOT',
       'WORK_ACTIVITY_ID', 'WORK_ORDER_ID',
       'LOCATION_ID', 'PROJECT_ID', 'DESIGN_ID', 'ATTACHEMENT_ID', 'USER_ID',
       'PROCESSSTATUS', 'RECORD_INSERT_DATETIME', 'RECORD_UPDATE_DATETIME',
       'RECORD_INSERTE_BY', 
       'URL_TYPE'], axis = 1, inplace = True)
print("Columns Dropped " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

photomapping_df.replace("NULL", np.nan, inplace = True)
print("Nulls replaced " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

photomapping_gdf = gpd.GeoDataFrame(photomapping_df,geometry=gpd.points_from_xy(photomapping_df.W1_GEO_LONG, photomapping_df.W1_GEO_LAT))
photomapping_gdf.set_geometry(col='geometry', drop=True, inplace=True)
print("Geometry Set and Dropped")

print(photomapping_gdf.columns)


with open(output_filename, "w") as f:
    f.write(photomapping_gdf.to_json(na="drop"))


print(output_filename + " created - end process " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))

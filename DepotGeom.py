import pandas as pd
import geopandas as gpd
import numpy as np
from shapely import wkt

from sys import argv

#pd.set_option('display.max_rows', None)

script, input_file1, input_file2 = argv

depot_geom = pd.read_csv(input_file1)
depot_geom['label'] = depot_geom['label'].apply(lambda x: x.replace(" Depot", ""))

inventory_file_df = pd.read_csv(input_file2)

merged_df = pd.merge(left=inventory_file_df, right=depot_geom[["label","location_wkt"]], left_on="ORG_NAME",right_on="label", how='left')

gdf = gpd.GeoDataFrame(merged_df)

gdf['location_wkt'] = gdf['location_wkt'].apply(wkt.loads)
gdf.set_geometry(col='location_wkt', drop=True, inplace=True)
gdf.replace(np.nan, '-', inplace = True)
print(gdf)

gdf.to_file(r'C:\Users\mdawson\Downloads\InventoryValuationReport.json', driver='GeoJSON')





import utm
import sys
import pandas as pd
import numpy as np

# Input lat-lon csv file name
latlon_fn = sys.argv[1]

df = pd.read_csv(latlon_fn,usecols=[0,1,2],dtype={'UID':'string', 'Lat':np.float32, 'Lon': np.float32}) # somehow it also read an extra column with all NaN values
df.dropna(axis=0,how='any',inplace=True) # remove rows with any N/A values
# This is only to find out UTM zone number and letter range
# Result: UTM range from zone 13 to 15, at letter S
# So we choose zone 14 as fixed zone number (middle)
# minlat = df['Lat'].min()
# maxlat = df['Lat'].max()
# minlon = df['Lon'].min()
# maxlon = df['Lon'].max()
# print(utm.from_latlon(minlat, minlon))
# print(utm.from_latlon(minlat, maxlon))
# print(utm.from_latlon(maxlat, minlon))
# print(utm.from_latlon(maxlat, maxlon))

# Convert lat long to x y in meter
lat = df['Lat'].iloc[:].to_numpy()
lon = df['Lon'].iloc[:].to_numpy()
x, y, dummy_zone_num, dummy_zone_letter = utm.from_latlon(lat, lon, force_zone_number=14)
df['X'] = x.astype(np.float32)
df['Y'] = y.astype(np.float32)
xy_fn = 'xy.csv'
df[['UID','X','Y']].to_csv(xy_fn,index=False)

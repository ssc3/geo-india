# required imports
import xlrd
import random
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import shapefile as shp
import requests
from typing import NamedTuple
from logging import log



DataPoint = NamedTuple(
    "_DataPoint",
    [
        ("district", str),
        ("active", str),
        ("confirmed", str),
        ('deceased', str),
        ('recovered', str),
    ],
)

# reading the state wise shapefile of India in a GeoDataFrame and preview it

fp = "../gadm36_IND_shp/gadm36_IND_2.shp"
map_df = gpd.read_file(fp)
map_df.head()
print(map_df.NAME_2)
# Plot the default map



'''data_source = [("Adilabad", 1000),
               ("Anantapur", 23),
               ]'''


resp = requests.get("https://api.covid19india.org/state_district_wise.json")
if resp.status_code != 200:
    log.error("No response from covid19india")

json_resp = resp.json()

dp_list = []
for k, v in json_resp.items():
    for k1, v1 in v.items():
        if isinstance(v1, dict):
            for k2, v2 in v1.items():
                print("KEY =" + k2)
                print(v2)
                dp = DataPoint(k2, v2["active"], v2["confirmed"], v2["deceased"], v2["recovered"])
                print(dp)
                dp_list.append(dp)





# create DataFrame using data
df = pd.DataFrame(dp_list, columns=['District', 'active', 'confirmed', 'deceased', 'recovered'])
print(df)


merged = map_df.set_index('NAME_2').join(df.set_index('District'))
print(merged.head())



# create figure and axes for Matplotlib and set the title
fig, ax = plt.subplots(1, figsize=(10, 6))

ax.axis('off')
ax.set_title('District Wise Covid cases', fontdict={'fontsize': '25', 'fontweight' : '3'})
merged.plot(column='confirmed', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

plt.show()

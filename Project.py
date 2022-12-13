#!/usr/bin/env python
# coding: utf-8

# # Important Imports

# In[121]:


import pandas as pd
import csv
import numpy as np
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import plotly.graph_objects as go
get_ipython().run_line_magic('matplotlib', 'inline')


# # Data Cleaning

# In[182]:


df = pd.read_csv("Data/city_day.csv")
df


# In[123]:


city = ["Ahmedabad", "Delhi"]

ad = df.loc[df['City'].isin(city)]


# In[124]:


ad.isna().sum()


# In[125]:


amd = ad.loc[df['City'] == "Ahmedabad"]


# In[126]:


amd 


# In[186]:


amd.describe()


# In[128]:


ameans = {"PM2.5": 67.854497,
         "PM10": 114.584029,
         "NO": 22.428021, 
         "NO2": 59.025496,
         "NOx": 47.366898,
         "NH3": 0,
         "CO": 22.193407,
         "SO2": 55.253733,
         "O3": 39.155408,
         "Benzene": 5.413807,
         "Toluene": 27.740524,
         "Xylene": 4.248341,
         "AQI": 452.122939}


# In[129]:


amd = amd.fillna(ameans)


# In[187]:


dhl = ad.loc[df['City'] == "Delhi"]
dhl


# In[189]:


dhl.describe()


# In[131]:


dmeans = {"PM2.5": 117.196153,
         "PM10": 232.809229,
         "NO": 38.985595, 
         "NO2": 50.785182,
         "NOx": 58.567023,
         "NH3": 41.997150,
         "CO": 1.976053,
         "SO2": 15.901253,
         "O3": 51.32361,
         "Benzene": 3.544480,
         "Toluene": 17.185042,
         "Xylene": 1.438339,
         "AQI": 259.487744}


# In[132]:


dhl = dhl.fillna(dmeans)


# In[133]:


fad = pd.concat([amd, dhl])


# In[195]:


fad


# In[135]:


#fad.to_csv('Data/FAD.csv')


# In[136]:


dffad = pd.read_csv("Data/FAD.csv", parse_dates=['Date'])


# In[137]:


dffad


# In[138]:


sorting = ["City", "Date"]
dffad.sort_values(by=sorting, inplace=True)
sortDffad = dffad
sortDffad = sortDffad.groupby(pd.Grouper(key='Date', axis=0, freq='Y')).mean()


# In[139]:


sortDffad


# In[140]:


saqi = pd.read_csv("Data/saqi.csv")
saqi["Date"] = pd.to_datetime(saqi.Date)
saqi['Date'] = saqi['Date'].dt.strftime('%Y')
saqi.rename(columns = {'Date':'year'}, inplace = True)

saqi


# In[141]:


ahmd = pd.read_excel("Data/Ahmd.xlsx")
ahmd


# In[142]:


delhi = pd.read_excel("Data/Delhi.xlsx")
delhi


# In[235]:


aadd = pd.merge(ahmd, delhi, how='inner', on = 'year')
aadd['Licensed vehicle'] = aadd['sales in millions_x'] + aadd['sales in millions_y']
aadd.rename(columns = {'sales in millions_x':'Ahmedabad', 'sales in millions_y':'Delhi'}, inplace = True)

aadd


# In[237]:


maadd = pd.concat([saqi, aadd], axis=1, join="inner")
maadd


# In[239]:


maadd = maadd.loc[:,~maadd.columns.duplicated()].copy()
maadd


# In[241]:


maadd["Growth"] = pd.DataFrame(maadd["Licensed vehicle"].pct_change())
maadd = maadd.fillna(0)


# In[242]:


maadd


# # EDA

# ### Typically a vehicle emits CO, NOx, NO, NO2, PM10, PM2.5, SO2, Benzene& O3
# 
# ### Hence, lets find if with growing car sales does these emission fairly increases or not

# In[231]:


dv = ["Licensed vehicle", "Growth"]

palette = sns.cubehelix_palette(light = 0.9, n_colors = 6)

for d in dv:
    sns.barplot(x = "year", y = d, data = maadd, palette=palette)
    plt.savefig("Images/graphs/{}.png".format(d), dpi = 1200, facecolor='w')
    plt.show()
    


# In[225]:


fig, ax = plt.subplots(3, 3, figsize = (20, 20))

palette = "ch:0.150"

sns.barplot(x = "year", y="CO", data = maadd, hue = "AQI_Bucket", ax = ax[0][0], palette=palette)
sns.barplot(x = "year", y="NOx", data = maadd, hue = "AQI_Bucket", ax = ax[0][1], palette=palette)
sns.barplot(x = "year", y="NO", data = maadd, hue = "AQI_Bucket", ax = ax[0][2], palette=palette)
sns.barplot(x = "year", y="NO2", data = maadd, hue = "AQI_Bucket", ax = ax[1][0], palette=palette)
sns.barplot(x = "year", y="PM10", data = maadd, hue = "AQI_Bucket", ax = ax[1][1], palette=palette)
sns.barplot(x = "year", y="PM2.5", data = maadd, hue = "AQI_Bucket", ax = ax[1][2], palette=palette)
sns.barplot(x = "year", y="O3", data = maadd, hue = "AQI_Bucket", ax = ax[2][0], palette=palette)
sns.barplot(x = "year", y="SO2", data = maadd, hue = "AQI_Bucket", ax = ax[2][1], palette=palette)
sns.barplot(x = "year", y="Benzene", data = maadd, hue = "AQI_Bucket", ax = ax[2][2], palette=palette)

plt.title("Bar plots to get each gas's presence in each year")

plt.savefig("Images/graphs/Second.png", dpi=500, facecolor='w')

plt.show()


# In[98]:


maadddesc = maadd.describe()
maaddMean = maadddesc.loc["mean"]
maaddMean = maaddMean.drop(["NH3", "Toluene", "Xylene", "AQI", "Ahmedabad", "Delhi", "vehicle sales", "Growth"], axis=0, inplace=False)
maaddMean


# In[223]:


plt.figure(figsize = (10, 6))
plt.style.use("seaborn")
fig, ax = plt.subplots(figsize = (10, 6), dpi = 100)
explode = [0.1, 0, 0.1, 0, 0, 0.2, 0.1, 0, 0.1]
maaddMean.plot.pie(autopct='%1.1f%%', explode = explode)
plt.savefig("Images/graphs/pie.png", dpi = 1200, facecolor='w')
plt.show()


# In[233]:


iv = ["CO", "NOx", "NO", "NO2", "PM10", "PM2.5", "O3", "SO2", "Benzene"]
corrdata = pd.DataFrame()
for i in iv:
    print("Correlation coefficient of {} is".format(i), maadd['Licensed vehicle'].corr(maadd[i]))
    v = maadd['Licensed vehicle'].corr(maadd[i])    
    df2 = {'Gas Name': i, 'Corr Coef': v}
    corrdata = corrdata.append(df2, ignore_index = True)  


# In[101]:


corrdata


# In[224]:


palette = sns.cubehelix_palette(light = 0.9, n_colors = 6)
sns.barplot(data=corrdata, x="Gas Name", y="Corr Coef", palette=palette)
plt.savefig("Images/graphs/corrcoef.png", dpi = 1200, facecolor='w')
plt.show()


# # End

#!/usr/bin/env python
# coding: utf-8

# In[17]:


#requirements.txt
#pip install pandas
#pip install glob


# In[18]:


import glob
import pandas as pd


# In[19]:


fracfocus_data_location = "C:\VD\WARWICK\FracFocusData"
occ_data_location = "C:\VD\WARWICK\W27base\W27base.csv"


# In[20]:


# Load fracfocus data
df = pd.concat(map(pd.read_csv, glob.glob(fracfocus_data_location + "/*.csv")))


# In[21]:


#Preare Year & Month from JobStartDate
df['JobStartDate'] = pd.to_datetime(df['JobStartDate'], errors = 'coerce')
df['year'] = pd.DatetimeIndex(df['JobStartDate']).year
df['month'] = pd.DatetimeIndex(df['JobStartDate']).month
print(df['month'])


# In[22]:


#1 Number of jobs started by supplier by well by month
df.groupby(['Supplier','WellName','month',]).size().reset_index(name='counts')


# In[23]:


#1 Number of jobs started by supplier by well by year, month
df.groupby(['Supplier','WellName','year','month']).size().reset_index(name='counts')


# In[24]:


#2 Max and Min Percentage of Ingredients used per Well
df.groupby(['WellName']).agg({'PercentHighAdditive': ['min', 'max'],
                             'PercentHFJob': ['min', 'max']})


# In[25]:


#3 Total Base Water Volume by State, County and Well
df.groupby(['StateNumber', 'CountyNumber', 'WellName']).agg({'TotalBaseWaterVolume': ['sum']})


# In[26]:


### Load OCC Data
data= pd.read_csv(occ_data_location, encoding= 'unicode_escape')
occ_data = data[['Well_Name', 'API_Number', 'Well_Status', 'Spud', 'First_Prod']]
occ_data['API_Number'] = occ_data['API_Number'].str[1:]


# In[29]:


#Filter for Oklahoma state
state = ['Oklahoma']
frac_focus_df = df[df.StateName.isin(state)]
#frc_fo_state = df[df['StateName'] == 'Oklahoma']
#frc_fo_state['StateName']


# In[30]:


#Create a query for reporting to integrate the FracFocus header table with the OCC data
merged_df = pd.merge(frac_focus_df, occ_data, how='inner', left_on = 'APINumber', right_on = 'API_Number')


# In[31]:


merged_df


# In[32]:


occ_data


# In[ ]:





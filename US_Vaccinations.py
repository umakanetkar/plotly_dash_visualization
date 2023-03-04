#!/usr/bin/env python
# coding: utf-8

# In[43]:


import pandas as pd
import numpy as np


# In[44]:


# print all the outputs in a cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# In[45]:


vaccine_data= "https://raw.githubusercontent.com/umakanetkar/plotly_dash_visualization/main/us_state_vaccinations1.csv"


# In[46]:


df = pd.read_csv(vaccine_data)


# In[47]:


df.columns


# In[48]:


df.shape


# In[49]:


df.isna().sum()


# In[50]:


df = df.fillna(method='bfill')


# In[51]:


df.isna().sum()


# In[52]:


population_data = "https://raw.githubusercontent.com/umakanetkar/plotly_dash_visualization/main/US_POP.xlsx"


# In[53]:


pop=  pd.read_excel(population_data)
#pop=  pd.read_excel("US_POP.xlsx")


# In[54]:


pop.head()


# In[55]:


pop.head(2)
df.head(2)


# In[56]:


df.State.unique()


# In[57]:


pop.State.unique()


# In[58]:


pop['State'] = pop['State'].str.replace('.', '')


# In[59]:


merged_df = pd.merge(df, pop, on='State')


# In[60]:


df.shape
pop.shape
merged_df.shape


# In[61]:


merged_df.head(2)


# In[62]:


merged_df['population'] = merged_df.apply(lambda row: row[2021] if row['year'] == 2021 else row[2022], axis=1)


# In[63]:


merged_df.head(2)


# In[64]:


merged_df.isna().any()


# In[65]:


df=merged_df[['date','State','daily_vaccinations','day','month','year','population' ]]


# In[66]:


df['cumulative_vaccinations'] = df.groupby(['State'])['daily_vaccinations'].cumsum()


# In[67]:


df.head()


# In[68]:


#to get % of population vaccinated
df['percent'] = df.apply(lambda row: (row['cumulative_vaccinations'] / row['population']) * 100, axis=1)


# In[69]:


df = df.groupby(['State','year','month']).agg({'daily_vaccinations': 'sum','percent': 'max'}).reset_index()


# In[70]:


df.head()


# In[71]:


#since we dont have population data of 2023
df = df[df['year']!=2023]


# In[72]:


#converting state names to state abbreviations
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


# In[73]:


df['state_abbr'] = df['State'].map(us_state_abbrev)


# In[74]:


df.head(2)


# ### Building a Dashboard

# In[75]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, Input, Output  # pip install dash (version 2.0.0 or higher)
#from dash import  dcc, html


# In[76]:


# Define the app
app = dash.Dash(__name__)

server=app.server

# Layout
app.layout = html.Div([
    html.H1("Choropleth Map with Plotly Dash"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": year, "value": year} for year in df["year"].unique()],
        value=df["year"].min()
    ),
    dcc.Dropdown(
        id="month-dropdown",
        options=[{"label": month, "value": month} for month in df["month"].unique()],
        value=df["month"].min()
    ),
    dcc.Graph(id="choropleth-map")
])

# Callback
@app.callback(
    Output("choropleth-map", "figure"),
    [Input("year-dropdown", "value"), Input("month-dropdown", "value")]
)
def update_choropleth_map(year, month):
    filtered_df = df[(df["year"] == year) & (df["month"] == month)]
    fig = px.choropleth(
        filtered_df, 
        locations="state_abbr", 
        locationmode="USA-states", 
        color="percent", 
        scope="usa",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        #labels={'percent': '% of Vaccinated Population'}
        #labels={'percent': '% of population vaccinated', 'state_abbr': 'State'}
        labels={'percent': '% of Population Vaccinated', 'State': 'State'}
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        template="plotly_dark"
    )
    return fig

# Running the app
if __name__ == "__main__":
    app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:





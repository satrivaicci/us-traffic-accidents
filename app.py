import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'US Accidents'
sourceurl = 'https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents'
githublink = 'https://github.com/satrivaicci/us-traffic-accidents'

########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/US_Accidents_Dec21_small.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


#### Get Years list
years_list = df.Year.unique()
years_list.sort()


### Group by year and state
dfByState = df.groupby(['Year', 'State']).size().reset_index(name='Counts')
### Group by year and city
dfByCity = df.groupby(['Year', 'City']).size().sort_values(ascending=False).reset_index(name='Counts')
### Group by year and weather condition
dfByWeather = df.groupby(['Year', 'Weather_Condition']).size().sort_values(ascending=False).reset_index(name='Counts')

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2020-2021 US Traffic Accidents analysis'),
    html.Div([
        html.Div([
                html.H6('Select a year for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in years_list],
                    value=2021
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
                  dcc.Graph(id='top-cities-bar'),
                  dcc.Graph(id='top-weatherc-bar')
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
              Output('top-cities-bar', 'figure'),
              Output('top-weatherc-bar', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(year):
    mygraphtitle = f'Traffic accidents in {year}'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "Total count"

    # Choropleth data
    data=go.Choropleth(
        locations=dfByState['State'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = dfByState[dfByState['Year'] == year]['Counts'], # Data to be color-coded
        colorscale = ['lightgrey','blue'],
        colorbar_title = 'some title',
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    
    
    
    # Top cities bar chart
    
    topCitiesData = dfByCity.loc[dfByCity['Year'] == year].nlargest(n=15, columns=['Counts'])
    
    topCitiesBarData = go.Bar(
        x=topCitiesData['City'],
        y=topCitiesData['Counts'],
        name=""
    )
    
    topCitiesLayout = go.Layout(
        title=f'Top 15 Cities with the most accidents in {year}',
        xaxis = dict(title = 'City'), # x-axis label
        yaxis = dict(title = 'Total accidents'), # y-axis label

    )

    topCitiesBar = go.Figure(data=[topCitiesBarData], layout=topCitiesLayout)
    
    
    # Top weather bar chart
    
    topWeatherData = dfByWeather.loc[dfByWeather['Year'] == year].nlargest(n=15, columns=['Counts'])
    
    topWeatherBarData = go.Bar(
        x=topWeatherData['Weather_Condition'],
        y=topWeatherData['Counts'],
        name=""
    )
    
    topWeatherLayout = go.Layout(
        title=f'Top 15 Weather Conditions with the most accidents in {year}',
        xaxis = dict(title = 'Weather condition'), # x-axis label
        yaxis = dict(title = 'Total accidents'), # y-axis label

    )

    topWeatherBar = go.Figure(data=[topWeatherBarData], layout=topWeatherLayout)
    
    
    return fig, topCitiesBar, topWeatherBar


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('data/cleaned_AQI.csv')

# Sample dataframe
fire_AQI = pd.read_csv('data/fire_AQI.csv')
df1 = pd.DataFrame({
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Site ID': [123, 456, 789],
    'Daily Mean PM2.5 Concentration': [15.6, 18.2, 14.8],
    'UNITS': ['ug/m3 LC', 'ug/m3 LC', 'ug/m3 LC'],
    'DAILY_AQI_VALUE': [50, 60, 40],
    'AQS_PARAMETER_DESC': ['PM2.5 - Local Conditions', 'PM2.5 - Local Conditions', 'PM2.5 - Local Conditions'],
    'STATE': ['California', 'California', 'California'],
    'COUNTY': ['Los Angeles', 'San Francisco', 'San Diego'],
    'attr_IncidentName': ['Fire A', 'Fire B', 'Fire C'],
    'poly_Acres_AutoCalc': [1000, 2000, 1500],
    'attr_FireCauseGeneral': ['Human', 'Unknown', 'Natural'],
    'attr_FireDiscoveryDateTime': ['2022-01-01 08:00:00', '2022-01-02 12:00:00', '2022-01-03 10:00:00'],
    'attr_FireOutDateTime': ['2022-01-01 18:00:00', '2022-01-02 16:00:00', '2022-01-03 14:00:00'],
    'attr_InitialLatitude': [34.0522, 37.7749, 32.7157],
    'attr_InitialLongitude': [-118.2437, -122.4194, -117.1611],
    'attr_InitialResponseDateTime': ['2022-01-01 08:30:00', '2022-01-02 12:30:00', '2022-01-03 10:30:00'],
    'attr_POOState': ['US-CA', 'US-CA', 'US-CA'],
    'attr_PredominantFuelGroup': ['Grass', 'Forest', 'Shrub'],
    'Time': ['08:00:00', '12:00:00', '10:00:00']
})

# Create figure 1
fig1 = go.Figure(data=[
    go.Scatter(x=df['first_max_value'], y=df['aqi'], mode='markers')
])
fig1.update_layout(title='AQI vs Stuff', xaxis_title='first_max_value', yaxis_title='aqi')

# Create figure 2
fig2 = go.Figure(data=[
    go.Scatter(x=df1['Date'], y=df1['Daily Mean PM2.5 Concentration'], mode='lines', name='PM2.5 Concentration'),
    go.Scatter(x=df1['Date'], y=df1['DAILY_AQI_VALUE'], mode='lines', name='AQI')
])
fig2.update_layout(title='PM2.5 Concentration and AQI', xaxis_title='Date', yaxis_title='Value')

# Create the HTML table rows for the DataFrame data
table_rows = []
for index, row in fire_AQI.iterrows():
    table_row = html.Tr([html.Td(col) for col in row])
    table_rows.append(table_row)






# Calculate mean acreage by fuel type
mean_acreage = fire_AQI.groupby('attr_PredominantFuelGroup')['poly_Acres_AutoCalc'].mean().tolist()
median_acreage = fire_AQI.groupby('attr_PredominantFuelGroup')['poly_Acres_AutoCalc'].median().tolist()

# Define fuel labels
fuel_labels = fire_AQI['attr_PredominantFuelGroup'].unique().tolist()

# Create the bar chart for means by fuel type
fig_mean = go.Figure()
fig_mean.add_trace(go.Bar(x=fuel_labels, y=mean_acreage, marker_color='#ADD8E6', name='Mean Acreage'))
fig_mean.update_layout(title='Mean Fire Acreage by Fuel Type')
fig_mean.update_yaxes(title='Acreage')




import plotly.graph_objects as go

# Create the bar chart for means by fuel type
fig_mean = go.Figure()
fig_mean.add_trace(go.Bar(x=fuel_labels, y=mean_acreage, marker_color='#ADD8E6', name='Mean Acreage'))
fig_mean.update_layout(title='Mean Fire Acreage by Fuel Type')
fig_mean.update_yaxes(title='Acreage')

# Create the bar chart for medians by fuel type
fig_median = go.Figure()
fig_median.add_trace(go.Bar(x=fuel_labels, y=median_acreage, marker_color='#ADD8E6', name='Median Acreage'))
fig_median.update_layout(title='Median Fire Acreage by Fuel Type')
fig_median.update_yaxes(title='Acreage')


## COUNTY ACREAGE PLOT
# Calculate the median acre size by county
county_median = fire_AQI.groupby('COUNTY')['poly_Acres_AutoCalc'].median().sort_values(ascending=False)

# Sort the data in descending order
county_median = county_median.sort_values(ascending=True)

# Create the bar chart data
data = [
    go.Bar(
        x=county_median.values,
        y=county_median.index,
        orientation='h',
        marker=dict(color='lightblue')
    )
]

# Add the median of medians line
median_of_medians = county_median.median()
data.append(
    go.Scatter(
        x=[median_of_medians],
        y=county_median.index,
        mode='lines',
        name='Median of Medians',
        line=dict(color='red', dash='dot')
    )
)

# Add value labels at the end of each bar
annotations = []
for i, (county, acreage) in enumerate(zip(county_median.index, county_median.values)):
    annotations.append(
        dict(
            x=acreage,
            y=county,
            text=f'{acreage:.2f}',
            font=dict(color='black', size=10),
            showarrow=False,
            xanchor='left',
            yanchor='middle'
        )
    )

# Create the layout
layout = go.Layout(
    title='Median Fire Acreage by County',
    xaxis=dict(title='Median Acre Size'),
    yaxis=dict(title='County'),
    annotations=annotations,
    barmode='stack',
    bargap=0.1,
    height=600,
    margin=dict(l=100, r=20, t=70, b=70)
)

# Create the figure
fig3 = go.Figure(data=data, layout=layout)


import dash_leaflet as dl
import folium
from folium.plugins import MarkerCluster

# Create map
center_lat = 36.7783
center_long = -119.4179
m = folium.Map(location=[center_lat,center_long], zoom_start=10)

# Add markers to the map
marker_cluster = MarkerCluster().add_to(m)
for lat, lon, name in zip(df1['attr_InitialLatitude'], df1['attr_InitialLongitude'], df1['attr_IncidentName']):
    folium.Marker(location=[lat, lon], popup=name).add_to(marker_cluster)

# Create Folium map
m = folium.Map(location=[df1['attr_InitialLatitude'].mean(), df1['attr_InitialLongitude'].mean()], zoom_start=6)

# Add markers to the map
for index, row in df1.iterrows():
    folium.Marker(
        location=[row['attr_InitialLatitude'], row['attr_InitialLongitude']],
        popup=row['attr_IncidentName'],
        icon=folium.Icon(icon='fire', color='red')
    ).add_to(m)

# Convert Folium map to HTML
map_html = m.get_root().render()





app.layout = html.Div(className='row', children=[
    html.H1("Dataframe Visualization"),
    html.Div([
        dcc.Dropdown(
            id='location-dropdown',
            options=[{'label': county, 'value': county} for county in df['county'].unique()],
            value=None,
            placeholder='Select a location'
        ),
        dcc.DatePickerSingle(
            id='date-picker',
            date=None,
            placeholder='Select a date',
            display_format='YYYY-MM-DD'
        ),
    ]),
    html.Div(children=[
        # dcc.Graph(id="fig", figure=fig1, style={'display': 'inline-block'}),
        dcc.Graph(id='fig_county_acreage',figure=fig3, style={'display': 'inline-block'}),
        dcc.Graph(id="fig2", figure=fig2, style={'display': 'inline-block'}),
        html.H3('Dataframe Table'),
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in fire_AQI.columns])] 
            # +
            # Data rows
            # table_rows,

        #     style_table={'overflowY': 'scroll', 'height': '300px'},  # Make the table scrollable
        #     page_action='none',  # Disable pagination
        #     sort_action='native',  # Enable sorting
        #     style_cell={
        #         'whiteSpace': 'normal',
        #         'textAlign': 'left'
        # }
),


        dcc.Graph(id="fig_mean", figure=fig_mean, style={'display': 'inline-block'}),
        dcc.Graph(id="fig_median", figure=fig_median, style={'display': 'inline-block'}),

    html.Div(id='folium-map', children=[html.Iframe(srcDoc=map_html, style={'width': '100%', 'height': '500px'})])
])
])


@app.callback(
    dash.dependencies.Output('folium-map', 'children'), 
    dash.dependencies.Input('location-dropdown', 'value'))
def update_map(selected_county):
    filtered_df = df1[df1['County'] == selected_county] if selected_county else df1
    m = folium.Map(location=[filtered_df['attr_InitialLatitude'].mean(), filtered_df['attr_InitialLongitude'].mean()], zoom_start=6)
    for index, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['attr_InitialLatitude'], row['attr_InitialLongitude']],
            popup=row['attr_IncidentName'],
            icon=folium.Icon(icon='fire', color='red')
        ).add_to(m)
    map_html = m.get_root().render()
    return html.Iframe(srcDoc=map_html, style={'width': '100%', 'height': '500px'})


@app.callback(
    dash.dependencies.Output('fig', 'figure'),
    dash.dependencies.Output('fig2', 'figure'),
    dash.dependencies.Input('location-dropdown', 'value'),
    dash.dependencies.Input('date-picker', 'date')
)
def update_figures(location, date):
    filtered_df = df if location is None else df[df['COUNTY'] == location]
    filtered_df1 = df1 if date is None else df1[df1['Date'] == date]

    fig1 = go.Figure(data=[
        go.Scatter(x=filtered_df['first_max_value'], y=filtered_df['aqi'], mode='markers')
    ])
    fig1.update_layout(title='AQI vs Stuff', xaxis_title='first_max_value', yaxis_title='aqi')

    fig2 = go.Figure(data=[
        go.Scatter(x=filtered_df1['Date'], y=filtered_df1['Daily Mean PM2.5 Concentration'], mode='lines',
                   name='PM2.5 Concentration'),
        go.Scatter(x=filtered_df1['Date'], y=filtered_df1['DAILY_AQI_VALUE'], mode='lines', name='AQI')
    ])
    fig2.update_layout(title='PM2.5 Concentration and AQI', xaxis_title='Date', yaxis_title='Value')

    return fig1, fig2,fig3


if __name__ == '__main__':
    app.run_server(debug=True)



    # html.H1(children='Hello Group2!'),

    # html.H2('Dataframe Visualization'),

    # dcc.Row([
    #     dcc.Col(dcc.Graph(id='first-graph', figure=fig), width=3),
    #     dcc.Col(dcc.Graph(id='dataframe-graph', figure=fig2), width=3),
    # ], className='mb-4'),



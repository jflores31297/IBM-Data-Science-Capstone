# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("/Users/juanflores/Desktop/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
                    {'label': 'All Sites', 'value': 'ALL'}
                ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',  # Default to 'ALL' to show all sites
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # Pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Payload range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # Scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# Callback for the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Total success and failure count for all sites
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches for All Sites'
        )
    else:
        # Success and failure count for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success vs Failure Launches for Site {selected_site}'
        )
    return fig


# Callback for the scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if selected_site == 'ALL':
        # Scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites'
        )
    else:
        # Scatter plot for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {selected_site}'
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()


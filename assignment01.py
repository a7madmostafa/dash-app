

# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Incorporate data
df = pd.read_csv('canadian_immegration_data.csv')

# Initialize the app
app = Dash()

# App layout
app.layout = [
                html.Div(children='Canadian Immigration Data', style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

                html.Hr(),

                dcc.RadioItems(options=['Continents', 'Top10Regions', 'Top10Countries'], value='Continents', id='radio'),

                dcc.Graph(figure={}, id='graph')
            ]

# Add controls to build the interaction
@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='radio', component_property='value')
)
def update_graph(col_chosen):
    # Calculate the average of the chosen column for each continent
    if col_chosen == 'Continents':
        fig = px.histogram(df, x='Continent', y='Total', title='Immigration to Canada by Region', histfunc='avg', 
             category_orders={'Continent': ['Northern America', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Africa', 'Oceania']})

    elif col_chosen == 'Top10Regions':
        top10regions = df.groupby('Region')['Total'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top10regions, x='Region', y='Total', title='Immigration to Canada by Region')

    else:
        top10countries = df.nlargest(10, 'Total').reset_index()[['Country', 'Total']]
        top10countries.loc[2, 'Country'] = 'United Kingdom'
        fig = px.bar(top10countries, x='Country', y='Total', title='Immigration to Canada by Country')

    return fig

# Run the app
app.run(debug=True, port=8053)
import os
print("Current Working Directory:", os.getcwd())

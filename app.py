import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha2, country_name_to_country_alpha3
from pycountry_convert.convert_country_alpha2_to_continent_code import COUNTRY_ALPHA2_TO_CONTINENT_CODE
from dash.dependencies import Output, Input
from pycountry_convert.country_wikipedia import WIKIPEDIA_COUNTRY_NAME_TO_COUNTRY_ALPHA2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
text = "For **{0}**, map shows the countries with which it should open its " \
       "air corridor basis the **{1}** Strictness Level of Policy. The map also shows the COVID Infection Rate for the countries from which the " \
       "flights will operate."

def try_convert(country_name):
    try:
        return country_name_to_country_alpha3(country_name)
    except:
        return None

flights_data = pd.read_csv("dataset/merged-airlines.csv")
flights_data['CC'] = flights_data['source_airport_country'].apply(lambda x: try_convert(x))
latlon = pd.read_csv("dataset/latlon.csv", encoding='latin-1')

continent_filter = {}
for country_code, continent in COUNTRY_ALPHA2_TO_CONTINENT_CODE.items():
    countries = continent_filter.get(continent, [])
    try:
        countries.append(country_alpha2_to_country_name(country_code))
    except:
        continue
    continent_filter[continent] = countries

country_options = []
for country, country_code in WIKIPEDIA_COUNTRY_NAME_TO_COUNTRY_ALPHA2.items():
    country_options.append({'label': country, 'value': country_code})

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2('COVID Recovery Dashboard'),
            html.H5('Team 162 - DVA Nightwalkers')
        ], className = 'columns', style = {'textAlign': 'center'})
    ]),
    html.Div([
        html.Div([
            html.H6("Select Country and Policy", className = "control_label"),
            html.P("Filter by Continent", className = "control_label"),
            dcc.RadioItems(
                id='continent-selector',
                options = [
                    {'label': 'All', 'value': 'all'},
                    {'label': 'Africa', 'value': 'AF'},
                    {'label': 'Asia', 'value': 'AS'},
                    {'label': 'Europe', 'value': 'EU'},
                    {'label': 'Oceania', 'value': 'OC'},
                    {'label': 'North America', 'value': 'NA'},
                    {'label': 'South America', 'value': 'SA'}
                ],
                value = 'all',
                className = "dcc_control"
            ),
            html.P("Select the Country", className = "control_label"),
            dcc.Dropdown(
                id = "country-selector",
                options = country_options,
                value = "US",
                className = "dcc_control"
            ),
            html.P("Select Strictness Level of Policy", className = "control_label"),
            dcc.RadioItems(
                id = 'strictness',
                options = [
                    {'label': 'Lowest Level of Strictness', 'value': 'low'},
                    {'label': 'Moderate Level of Strictness', 'value': 'med'},
                    {'label': 'Highest Level of Strictness', 'value': 'high'}
                ],
                value = 'low',
                className = "dcc_control"
            ),
            html.Span("Policy Selected:", className = "control_label"),
            html.Span("Moderate", id="policy_selected", className = "control_label"),
            html.P(),
            html.Div(id="policy-indicator", style = {'padding': '0px 10px 10px 10px'})
        ], className = "pretty_container four columns"),
        html.Div([
            html.P(dcc.Markdown(text.format("United States", "Lowest")), id="text"),
            html.P(),
            dcc.Graph(
                id = 'world_map'
            )
        ], className = "pretty_container eight columns", id='rightCol')
    ], className = "row",),
], id="mainContainer"
)

@app.callback(Output('country-selector', 'options'),
              [Input('continent-selector', 'value')])
def continent_filer_options(continent):
    if continent == 'all':
        return country_options
    else:
        options = []
        countries = continent_filter[continent]
        for country in countries:
            options.append({
                'label': country,
                'value': country_name_to_country_alpha2(country)
            })
        return options


@app.callback([Output('policy-indicator', 'children'), Output('policy_selected', 'children'), Output('policy_selected', 'style')],
              [Input('strictness', 'value')])
def policy_indicator(strictness):
    policy = {
        "low": [
            {'label': 'Public Transport', 'value': 'yes'},
            {'label': 'Internal Movements', 'value': 'yes'},
            {'label': 'Schools', 'value': 'yes'},
            {'label': 'Public Events', 'value': 'yes'},
            {'label': 'Workplaces', 'value': 'yes'},
            {'label': 'Stay at Home', 'value': 'yes'}
        ],
        "med": [
            {'label': 'Public Transport', 'value': 'no'},
            {'label': 'Internal Movements', 'value': 'yes'},
            {'label': 'Schools', 'value': 'no'},
            {'label': 'Public Events', 'value': 'no'},
            {'label': 'Workplaces', 'value': 'yes'},
            {'label': 'Stay at Home', 'value': 'yes'}
        ],
        "high": [
            {'label': 'Public Transport', 'value': 'no'},
            {'label': 'Internal Movements', 'value': 'no'},
            {'label': 'Schools', 'value': 'no'},
            {'label': 'Public Events', 'value': 'no'},
            {'label': 'Workplaces', 'value': 'no'},
            {'label': 'Stay at Home', 'value': 'no'}
        ]
    }
    restrictions = policy[strictness]
    elements = []
    for restriction in restrictions:
        elements.append(html.P())
        value = restriction['value']
        label = restriction['label']
        resp = "✔️" if value == "yes" else "❌"
        elements.append(html.Span(resp, className = f"{value}"))
        elements.append(html.Span(f" {label}"))

    strictness_lbl = {
        'high': 'Strict',
        'med': 'Moderate',
        'low': 'Lenient'
    }
    color = {
        'low': 'green',
        'med': 'orange',
        'high': 'red'
    }

    return elements, strictness_lbl[strictness], {'color': color[strictness]}

@app.callback(
    [Output('world_map', 'figure'), Output('text', 'children')],
    [Input('country-selector', 'value'), Input('strictness', 'value')])
def update_graph(country_code, strictness):
    country = country_alpha2_to_country_name(country_code)
    dest_lat = latlon.loc[latlon['name'] == country]['latitude'].iloc[0]
    dest_lon = latlon.loc[latlon['name'] == country]['longitude'].iloc[0]
    dest_flights = flights_data[flights_data['dest_airport_country'] == country]
    fig = px.choropleth(dest_flights, locationmode = "ISO-3", locations = 'CC', color = 'flight_capacity', color_continuous_scale="blues", template = 'seaborn')

    for val in dest_flights.itertuples():
        source = val[1]
        try:
            lat = latlon.loc[latlon['name'] == source]['latitude'].iloc[0]
            lon = latlon.loc[latlon['name'] == source]['longitude'].iloc[0]
            fig = fig.add_scattergeo(lat = [lat, dest_lat], lon = [lon, dest_lon], line = dict(width = 1, color = '#1F1F1F'),
                                     mode = 'lines', showlegend = False)
        except:
            continue
    strictness_level  = {
        'low': "Lowest",
        'med': "Moderate",
        'high': "Highest"
    }[strictness]
    return fig, dcc.Markdown(text.format(country, strictness_level))

if __name__ == '__main__':
    app.run_server()

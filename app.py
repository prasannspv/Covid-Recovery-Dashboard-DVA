import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from plotly.graph_objects import layout
import json
import plotly.express as px
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha2, \
    country_name_to_country_alpha3, map_country_alpha2_to_country_alpha3
from pycountry_convert.convert_country_alpha2_to_continent_code import COUNTRY_ALPHA2_TO_CONTINENT_CODE
from dash.dependencies import Output, Input
from pycountry_convert.country_wikipedia import WIKIPEDIA_COUNTRY_NAME_TO_COUNTRY_ALPHA2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

tabs_styles = {
    'height': '20px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    # 'padding': '6px',
    # 'fontWeight': 'bold'
}

tab_selected_style = {
    # 'borderTop': '1px solid #d6d6d6',
    # 'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#F2F2F2',
    'color': 'black',
    'fontWeight': 'bold'
    # 'padding': '6px'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
server = app.server
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
inf_policy = pd.read_csv("dataset/infection_policy.csv")
inf_choropleth_recent_data = inf_policy[inf_policy.date == '2020-10-06']
a2toa3 = map_country_alpha2_to_country_alpha3()

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


def get_filtered_map():
    return html.Div([
        html.Div([
            html.Div([
                html.H6("Select Country and Policy", className="control_label"),
                html.P("Filter by Continent", className="control_label"),
                get_filter_by_continent(),
                html.P("Select the Country", className="control_label"),
                get_filter_by_country(),
                html.P("Select Strictness Level of Policy", className="control_label"),
                dcc.RadioItems(
                    id='strictness',
                    options=[
                        {'label': 'Lowest Level of Strictness', 'value': 'low'},
                        {'label': 'Moderate Level of Strictness', 'value': 'med'},
                        {'label': 'Highest Level of Strictness', 'value': 'high'}
                    ],
                    value='low',
                    className="dcc_control"
                ),
                html.Span("Policy Selected:", className="control_label"),
                html.Span("Moderate", id="policy_selected", className="control_label"),
                html.P(),
                html.Div(id="policy-indicator", style={'padding': '0px 10px 10px 10px'})
            ], className="pretty_container four columns"),
            html.Div([
                html.P(dcc.Markdown(text.format("United States", "Lowest")), id="text"),
                html.P(),
                dcc.Graph(
                    id='world_map'
                )
            ], className="pretty_container eight columns", id='rightCol')
        ], className="row", ),
    ], id="mainContainer"
    )


def get_kpi_plots():
    return html.Div([
        html.Div([
            html.Div([
                html.P("Select the Continent", className="control_label"),
                get_filter_by_continent(id="kpi-continent"),
                html.P("Select the Country", className="control_label"),
                get_filter_by_country(id="kpi-country"),
                html.Div(id="policy-indicator", style={'padding': '0px 10px 10px 10px'})
            ], className="pretty_container four columns"),
            html.Div([
                html.P(dcc.Markdown(text.format("United States", "Lowest")), id="text"),
                html.P(),
                dcc.Graph(
                    id='new_cases'
                )
            ], className="pretty_container eight columns", id='rightCol')
        ], className="row", ),
    ], id="mainContainer"
    )


def get_filter_by_country(id=None):
    id = "country-selector" if id is None else id
    return dcc.Dropdown(
        id=id,
        options=country_options,
        value="US",
        className="dcc_control"
    )


def get_filter_by_continent(id=None):
    id = "continent-selector" if id is None else id
    return dcc.RadioItems(
        id=id,
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'Africa', 'value': 'AF'},
            {'label': 'Asia', 'value': 'AS'},
            {'label': 'Europe', 'value': 'EU'},
            {'label': 'Oceania', 'value': 'OC'},
            {'label': 'North America', 'value': 'NA'},
            {'label': 'South America', 'value': 'SA'}
        ],
        value='all',
        className="dcc_control"
    )


# app.layout = get_filtered_map()
app.layout = html.Div([
    html.Div([
        html.H2('COVID Recovery Dashboard'),
        html.H5('Team 162 - DVA Nightwalkers')
    ], style = {'textAlign': 'center'}),
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Key Performance Indicators', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Prediction Engine', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='tabs-content-props')
])


@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return get_kpi_plots()
    elif tab == 'tab-2':
        return get_filtered_map()


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

@app.callback(Output('kpi-country', 'options'),
              [Input('kpi-continent', 'value')])
def kpi_continent_filer_options(continent):
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


@app.callback(
    Output('new_cases', 'figure'),
    [Input('kpi-continent', 'value'), Input('kpi-country', 'value')]
)
def kpi_plots(continent_code, country_code):
    continent = {
        "AF": "africa",
        "AS": "asia",
        "NA": "north america",
        "SA": "south america",
        "EU": "europe",
        "AU": "australia",
        "OC": None,
        "all": None
    }[continent_code]
    fig = px.choropleth(inf_choropleth_recent_data, locationmode="ISO-3", locations='iso_code', color='positive_rate', color_continuous_scale="reds", template='seaborn', range_color = [0, 0.25], scope = continent)
    if continent_code == "OC":
        fig.update_geos(
            lataxis_range = [-50, 0], lonaxis_range = [50, 250]
        )

    return fig

@app.callback(
    [Output('policy-indicator', 'children'), Output('policy_selected', 'children'), Output('policy_selected', 'style')],
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
        elements.append(html.Span(resp, className=f"{value}"))
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
    fig = px.choropleth(dest_flights, locationmode="ISO-3", locations='CC', color='flight_capacity',
                        color_continuous_scale="blues", template='seaborn')

    for val in dest_flights.itertuples():
        source = val[1]
        try:
            lat = latlon.loc[latlon['name'] == source]['latitude'].iloc[0]
            lon = latlon.loc[latlon['name'] == source]['longitude'].iloc[0]
            fig = fig.add_scattergeo(lat=[lat, dest_lat], lon=[lon, dest_lon], line=dict(width=1, color='#1F1F1F'),
                                     mode='lines', showlegend=False)
        except:
            continue
    strictness_level = {
        'low': "Lowest",
        'med': "Moderate",
        'high': "Highest"
    }[strictness]
    return fig, dcc.Markdown(text.format(country, strictness_level))


if __name__ == '__main__':
    app.run_server()

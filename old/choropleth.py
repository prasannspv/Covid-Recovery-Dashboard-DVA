import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3
import time
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
available_indicators = ['Sentiment']


def get_dataframe():
    df = pd.read_csv('final_op_sentiments_daily.csv')


    def to_timestamp(value):
        return time.mktime(datetime.datetime.strptime(value, "%Y-%m-%d").timetuple())

    df['timestamp'] = df.Date.apply(lambda x: to_timestamp(x))
    df['Country Name'] = df.Country.apply(lambda x: country_name_to_country_alpha3(country_alpha2_to_country_name(x)))
    df['Ratio'] = df.Positive/df.Negative
    return df

df = get_dataframe()
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Sentiment'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='world_map',
            hoverData={'points': [{'location': 'USA'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series')
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['timestamp'].min(),
        max=df['timestamp'].max(),
        value=df['timestamp'].max(),
        marks={int(date): datetime.datetime.fromtimestamp(date).strftime('%m/%d') if i%14 == 0 else "" for i, date in enumerate(df['timestamp'].unique())},
        step = None
    ), style={'width': '50%', 'padding': '0px 20px 20px 20px', 'size': '3px'})
])


@app.callback(
    dash.dependencies.Output('world_map', 'figure'),
    [
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(date):
    date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    dff = df.loc[df['Date'] == date].copy()
    fig = px.choropleth(dff, locationmode = "ISO-3", locations = 'Country Name', color = 'Sentiment Score', color_continuous_scale="Viridis")
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, text):

    fig = px.scatter(dff, x='Date', y='Ratio')
    # fig.add_trace(px.scatter(dff, x='Date', y='Negative'))

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=text)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('world_map', 'hoverData')])
def update_y_timeseries(hoverData):
    country_name = hoverData['points'][0]['location']
    dff = df[df['Country Name'] == country_name]
    return create_time_series(dff, f"Weekly Average Sentiment of {country_name}")


if __name__ == '__main__':
    app.run_server(debug=True, port=7777)
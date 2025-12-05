
import pandas as pd
import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px

# CSV laden
df = pd.read_csv("Dashboard/gaming_sales_data.csv", sep=";")  

# Beispiel: Top 10 Spiele nach Global_Sales
top10 = df.sort_values("Global_Sales", ascending=False).head(10)

# App initialisieren
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Gaming Sales Dashboard"),
    html.Div([
        html.Label("Jahr:"),
        dcc.Dropdown(
            id='year-filter',
            options=[{'label': str(y), 'value': y} for y in sorted(df['Year'].dropna().unique())],
            value=None,
            multi=True,
            placeholder="Jahr wählen"
        ),
        html.Label("Genre:"),
        dcc.Dropdown(
            id='genre-filter',
            options=[{'label': g, 'value': g} for g in sorted(df['Genre'].dropna().unique())],
            value=None,
            multi=True,
            placeholder="Genre wählen"
        ),
        html.Label("Plattform:"),
        dcc.Dropdown(
            id='platform-filter',
            options=[{'label': p, 'value': p} for p in sorted(df['Platform'].dropna().unique())],
            value=None,
            multi=True,
            placeholder="Plattform wählen"
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    html.Div([
        dcc.Graph(id='pie-genre'),
        dcc.Graph(id='pie-platform'),
        dcc.Graph(id='sales-time'),
        dcc.Graph(id='heatmap'),
    ], style={'width': '68%', 'display': 'inline-block'}),
    html.H2("Daten-Tabelle"),
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        filter_action="native",
        sort_action="native",
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    )
])

# Callback für Filter und Visualisierungen
@app.callback(
    [Output('pie-genre', 'figure'),
     Output('pie-platform', 'figure'),
     Output('sales-time', 'figure'),
     Output('heatmap', 'figure'),
     Output('datatable', 'data')],
    [Input('year-filter', 'value'),
     Input('genre-filter', 'value'),
     Input('platform-filter', 'value')]
)
def update_dashboard(years, genres, platforms):
    dff = df.copy()
    if years:
        dff = dff[dff['Year'].isin(years)]
    if genres:
        dff = dff[dff['Genre'].isin(genres)]
    if platforms:
        dff = dff[dff['Platform'].isin(platforms)]

    # Pie-Chart Genre
    pie_genre = px.pie(dff, names='Genre', values='Global_Sales', title='Verteilung nach Genre')

    # Pie-Chart Plattform
    pie_platform = px.pie(dff, names='Platform', values='Global_Sales', title='Verteilung nach Plattform')

    # Zeitreihe: Verkäufe pro Jahr
    sales_time = px.line(
        dff.groupby('Year')['Global_Sales'].sum().reset_index(),
        x='Year', y='Global_Sales', title='Globale Verkäufe pro Jahr'
    )

    # Heatmap: Genre vs. Plattform
    heatmap_data = dff.pivot_table(index='Genre', columns='Platform', values='Global_Sales', aggfunc='sum', fill_value=0)
    heatmap = px.imshow(heatmap_data, title='Heatmap: Genre vs. Plattform')

    # Tabelle
    table_data = dff.to_dict('records')

    return pie_genre, pie_platform, sales_time, heatmap, table_data

if __name__ == '__main__':
    app.run(debug=True)



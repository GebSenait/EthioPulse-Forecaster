"""
EthioPulse-Forecaster Dashboard

Interactive dashboard for visualizing Ethiopia's financial inclusion trends and forecasts.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "EthioPulse-Forecaster Dashboard"

# Define data paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "ethiopia_fi_enriched.csv"

# Load data
try:
    df = pd.read_csv(PROCESSED_DATA_PATH)
    data_loaded = True
except FileNotFoundError:
    df = pd.DataFrame()
    data_loaded = False

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("EthioPulse-Forecaster Dashboard", 
                style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': 30}),
        html.P("Financial Inclusion Forecasting System for Ethiopia",
               style={'textAlign': 'center', 'fontSize': 18, 'color': '#666'})
    ]),
    
    html.Div([
        dcc.Tabs(id="tabs", value='trends', children=[
            dcc.Tab(label='Trends', value='trends'),
            dcc.Tab(label='Events', value='events'),
            dcc.Tab(label='Composition', value='composition'),
        ]),
        html.Div(id='tab-content')
    ])
])

@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if not data_loaded:
        return html.Div([
            html.H3("Data Not Available"),
            html.P("Please run Task 1 data enrichment pipeline first.")
        ])
    
    if tab == 'trends':
        return render_trends_tab()
    elif tab == 'events':
        return render_events_tab()
    elif tab == 'composition':
        return render_composition_tab()
    else:
        return html.Div("Select a tab")

def render_trends_tab():
    """Render trends visualization"""
    access_obs = df[(df['record_type'] == 'observation') & (df['pillar'] == 'access')]
    usage_obs = df[(df['record_type'] == 'observation') & (df['pillar'] == 'usage')]
    
    fig = go.Figure()
    
    if len(access_obs) > 0:
        access_ts = access_obs.groupby('year')['value'].mean().sort_index()
        fig.add_trace(go.Scatter(
            x=access_ts.index,
            y=access_ts.values,
            mode='lines+markers',
            name='Access (Account Ownership)',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
    
    if len(usage_obs) > 0:
        usage_ts = usage_obs.groupby('year')['value'].mean().sort_index()
        fig.add_trace(go.Scatter(
            x=usage_ts.index,
            y=usage_ts.values,
            mode='lines+markers',
            name='Usage (Digital Payments)',
            line=dict(color='#A23B72', width=3),
            marker=dict(size=8, symbol='square')
        ))
    
    fig.update_layout(
        title='Financial Inclusion Trends (2011-2024)',
        xaxis_title='Year',
        yaxis_title='Rate (%)',
        hovermode='closest',
        template='plotly_white',
        height=500
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.Div([
            html.H4("Key Insights"),
            html.Ul([
                html.Li("Access (Account Ownership) shows steady growth"),
                html.Li("Usage (Digital Payments) lags behind access"),
                html.Li("Growth deceleration observed post-2021")
            ])
        ], style={'marginTop': 30, 'padding': 20, 'backgroundColor': '#f5f5f5'})
    ])

def render_events_tab():
    """Render events visualization"""
    events = df[df['record_type'] == 'event']
    
    if len(events) == 0:
        return html.Div("No events data available")
    
    event_types = events['event_type'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=event_types.index,
            y=event_types.values,
            marker_color=['#2E86AB', '#A23B72', '#F18F01']
        )
    ])
    
    fig.update_layout(
        title='Events by Type',
        xaxis_title='Event Type',
        yaxis_title='Count',
        template='plotly_white',
        height=400
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.Div([
            html.H4("Events Timeline"),
            html.Table([
                html.Thead([
                    html.Tr([html.Th("Year"), html.Th("Event Name"), html.Th("Type")])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(str(row['year'])),
                        html.Td(row.get('event_name', 'N/A')),
                        html.Td(row.get('event_type', 'N/A'))
                    ]) for _, row in events.head(10).iterrows()
                ])
            ], style={'width': '100%', 'marginTop': 20})
        ])
    ])

def render_composition_tab():
    """Render dataset composition"""
    composition_stats = {
        'Total Records': len(df),
        'Observations': len(df[df['record_type'] == 'observation']),
        'Events': len(df[df['record_type'] == 'event']),
        'Impact Links': len(df[df['record_type'] == 'impact_link'])
    }
    
    return html.Div([
        html.H4("Dataset Composition"),
        html.Div([
            html.Div([
                html.H3(str(count), style={'color': '#2E86AB', 'margin': 0}),
                html.P(label, style={'margin': 0, 'fontSize': 14})
            ], style={
                'display': 'inline-block',
                'margin': 20,
                'padding': 20,
                'backgroundColor': '#f5f5f5',
                'borderRadius': 5,
                'textAlign': 'center',
                'minWidth': 150
            })
            for label, count in composition_stats.items()
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from utils.database import Database
from utils.market_data import MarketData
from utils.styles import *

db = Database()
market = MarketData()

def layout():
    return html.Div([
        html.Div([
            html.H2([
                html.I(className="fas fa-pie-chart me-3"),
                "Análisis de Fondos de Inversión"
            ], style={"color": PRIMARY_COLOR, "fontWeight": "700"}),
            html.P("Visualiza la distribución de tu cartera de fondos",
                  style={"color": "#aaa", "marginTop": "10px"})
        ], style={"marginBottom": "30px"}),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Distribución por Fondo", 
                               className="text-center mb-4",
                               style={"color": PRIMARY_COLOR, "fontWeight": "600"}),
                        dcc.Graph(id='graph-fondos-distribution', config=CHART_CONFIG)
                    ])
                ], style=CARD_STYLE)
            ], width=12, lg=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Distribución por Tipo (RF/RV)", 
                               className="text-center mb-4",
                               style={"color": PRIMARY_COLOR, "fontWeight": "600"}),
                        dcc.Graph(id='graph-fondos-tipo', config=CHART_CONFIG)
                    ])
                ], style=CARD_STYLE)
            ], width=12, lg=6),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Rendimiento de Fondos", 
                               className="text-center mb-4",
                               style={"color": PRIMARY_COLOR, "fontWeight": "600"}),
                        dcc.Graph(id='graph-fondos-performance', config=CHART_CONFIG)
                    ])
                ], style=CARD_STYLE)
            ], width=12)
        ]),
        
        dcc.Interval(id='interval-graph-fondos', interval=120000, n_intervals=0)
    ])

@callback(
    Output('graph-fondos-distribution', 'figure'),
    Input('interval-graph-fondos', 'n_intervals')
)
def update_fondos_distribution(n):
    fondos = db.get_fondos()
    
    if not fondos:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de fondos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#aaa")
        )
        fig.update_layout(**CHART_LAYOUT, height=400)
        return fig
    
    labels = []
    values = []
    colors = ['#00d4ff', '#6c63ff', '#00e676', '#ff1744', '#ffc107', 
              '#e91e63', '#9c27b0', '#3f51b5', '#009688', '#ff5722']
    
    for i, fondo in enumerate(fondos):
        current_price = market.get_current_price(fondo['ticker'])
        valor_actual = current_price * fondo['cantidad'] if current_price else 0
        labels.append(fondo['nombre'])
        values.append(valor_actual)
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors[:len(labels)],
                   line=dict(color=CARD_BG, width=3)),
        textinfo='label+percent',
        textfont=dict(size=12, color='#fff'),
        hovertemplate='<b>%{label}</b><br>Valor: €%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    total = sum(values)
    fig.add_annotation(
        text=f"<b>Total</b><br>€{total:,.0f}",
        x=0.5, y=0.5,
        font=dict(size=16, color=PRIMARY_COLOR),
        showarrow=False
    )
    
    fig.update_layout(
        **CHART_LAYOUT,
        height=450,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    return fig

@callback(
    Output('graph-fondos-tipo', 'figure'),
    Input('interval-graph-fondos', 'n_intervals')
)
def update_fondos_tipo(n):
    fondos = db.get_fondos()
    
    if not fondos:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de fondos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#aaa")
        )
        fig.update_layout(**CHART_LAYOUT, height=400)
        return fig
    
    rf_total = 0
    rv_total = 0
    
    for fondo in fondos:
        current_price = market.get_current_price(fondo['ticker'])
        valor_actual = current_price * fondo['cantidad'] if current_price else 0
        
        if fondo['tipo'] == 'RF':
            rf_total += valor_actual
        else:
            rv_total += valor_actual
    
    fig = go.Figure(data=[go.Pie(
        labels=['Renta Fija', 'Renta Variable'],
        values=[rf_total, rv_total],
        hole=0.5,
        marker=dict(colors=[PRIMARY_COLOR, SECONDARY_COLOR],
                   line=dict(color=CARD_BG, width=3)),
        textinfo='label+percent',
        textfont=dict(size=14, color='#fff', weight='bold'),
        hovertemplate='<b>%{label}</b><br>Valor: €%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    total = rf_total + rv_total
    fig.add_annotation(
        text=f"<b>Total</b><br>€{total:,.0f}",
        x=0.5, y=0.5,
        font=dict(size=16, color=PRIMARY_COLOR),
        showarrow=False
    )
    
    fig.update_layout(
        **CHART_LAYOUT,
        height=450,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

@callback(
    Output('graph-fondos-performance', 'figure'),
    Input('interval-graph-fondos', 'n_intervals')
)
def update_fondos_performance(n):
    fondos = db.get_fondos()
    
    if not fondos:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de fondos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#aaa")
        )
        fig.update_layout(**CHART_LAYOUT, height=400)
        return fig
    
    nombres = []
    rendimientos = []
    colors_bar = []
    
    for fondo in fondos:
        current_price = market.get_current_price(fondo['ticker'])
        if current_price:
            valor_actual = current_price * fondo['cantidad']
            invertido = fondo['valor_compra'] * fondo['cantidad']
            rendimiento_pct = ((valor_actual - invertido) / invertido * 100) if invertido > 0 else 0
            
            nombres.append(fondo['nombre'][:25])
            rendimientos.append(rendimiento_pct)
            colors_bar.append(SUCCESS_COLOR if rendimiento_pct >= 0 else DANGER_COLOR)
    
    fig = go.Figure(data=[go.Bar(
        x=nombres,
        y=rendimientos,
        marker=dict(color=colors_bar,
                   line=dict(color=CARD_BG, width=1)),
        text=[f"{r:+.2f}%" for r in rendimientos],
        textposition='outside',
        textfont=dict(size=11, color='#fff'),
        hovertemplate='<b>%{x}</b><br>Rendimiento: %{y:.2f}%<extra></extra>'
    )])
    
    fig.update_layout(
        **CHART_LAYOUT,
        height=450,
        xaxis=dict(
            title='Fondo',
            tickangle=-45,
            gridcolor='rgba(255,255,255,0.05)'
        ),
        yaxis=dict(
            title='Rendimiento (%)',
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=True,
            zerolinecolor=PRIMARY_COLOR,
            zerolinewidth=2
        ),
        showlegend=False
    )
    
    return fig

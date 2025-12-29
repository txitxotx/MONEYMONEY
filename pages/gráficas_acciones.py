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
                html.I(className="fas fa-chart-area me-3"),
                "Análisis de Acciones"
            ], style={"color": PRIMARY_COLOR, "fontWeight": "700"}),
            html.P("Visualiza la distribución de tu cartera de acciones",
                  style={"color": "#aaa", "marginTop": "10px"})
        ], style={"marginBottom": "30px"}),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Distribución por Acción", 
                               className="text-center mb-4",
                               style={"color": PRIMARY_COLOR, "fontWeight": "600"}),
                        dcc.Graph(id='graph-acciones-distribution', config=CHART_CONFIG)
                    ])
                ], style=CARD_STYLE)
            ], width=12, lg=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Distribución por Sector", 
                               className="text-center mb-4",
                               style={"color": PRIMARY_COLOR, "fontWeight": "600"}),
                        dcc.Graph(id='graph-acciones-sector', config=CHART_CONFIG)
                    ])
                ], style=CARD_STYLE)
            ], width=12, lg=6),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Rendimiento de Acciones", 
                               className="text-center mb-4",
                               style={"color": PRIMARY_COLOR, "fontWeight": "600"}),
                        dcc.Graph(id='graph-acciones-performance', config=CHART_CONFIG)
                    ])
                ], style=CARD_STYLE)
            ], width=12)
        ]),
        
        dcc.Interval(id='interval-graph-acciones', interval=120000, n_intervals=0)
    ])

@callback(
    Output('graph-acciones-distribution', 'figure'),
    Input('interval-graph-acciones', 'n_intervals')
)
def update_acciones_distribution(n):
    acciones = db.get_acciones()
    
    if not acciones:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de acciones para mostrar",
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
    
    for i, accion in enumerate(acciones):
        current_price = market.get_current_price(accion['ticker'])
        valor_actual = current_price * accion['num_acciones'] if current_price else 0
        labels.append(f"{accion['nombre']} ({accion['ticker']})")
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
    Output('graph-acciones-sector', 'figure'),
    Input('interval-graph-acciones', 'n_intervals')
)
def update_acciones_sector(n):
    acciones = db.get_acciones()
    
    if not acciones:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de acciones para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#aaa")
        )
        fig.update_layout(**CHART_LAYOUT, height=400)
        return fig
    
    sectores = {}
    
    for accion in acciones:
        current_price = market.get_current_price(accion['ticker'])
        valor_actual = current_price * accion['num_acciones'] if current_price else 0
        sector = accion.get('sector', 'Sin Clasificar')
        
        if sector in sectores:
            sectores[sector] += valor_actual
        else:
            sectores[sector] = valor_actual
    
    labels = list(sectores.keys())
    values = list(sectores.values())
    
    colors = ['#00d4ff', '#6c63ff', '#00e676', '#ff1744', '#ffc107', 
              '#e91e63', '#9c27b0', '#3f51b5']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors[:len(labels)],
                   line=dict(color=CARD_BG, width=3)),
        textinfo='label+percent',
        textfont=dict(size=13, color='#fff', weight='bold'),
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
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

@callback(
    Output('graph-acciones-performance', 'figure'),
    Input('interval-graph-acciones', 'n_intervals')
)
def update_acciones_performance(n):
    acciones = db.get_acciones()
    
    if not acciones:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de acciones para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#aaa")
        )
        fig.update_layout(**CHART_LAYOUT, height=400)
        return fig
    
    nombres = []
    rendimientos = []
    colors_bar = []
    
    for accion in acciones:
        current_price = market.get_current_price(accion['ticker'])
        if current_price:
            valor_actual = current_price * accion['num_acciones']
            invertido = accion['precio_compra'] * accion['num_acciones']
            rendimiento_pct = ((valor_actual - invertido) / invertido * 100) if invertido > 0 else 0
            
            nombres.append(f"{accion['ticker']}")
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
            title='Acción (Ticker)',
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

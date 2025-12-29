import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os

# NO importes Database aquí globalmente si usa Supabase
# from utils.database import Database  # ❌ QUITAR ESTO

from pages import fondos, acciones, graficas_fondos, graficas_acciones
from utils.styles import NAVBAR_STYLE, PRIMARY_COLOR

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    title="Investment Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

server = app.server  # ← CRÍTICO: Esto DEBE estar aquí

# Layout (sin cambios)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    dbc.Navbar(
        dbc.Container([
            html.Div([
                html.I(className="fas fa-chart-line me-2", 
                      style={"fontSize": "1.8rem", "color": PRIMARY_COLOR}),
                dbc.NavbarBrand("Investment Dashboard", 
                              className="fw-bold",
                              style={"fontSize": "1.5rem", "color": "#fff"})
            ], style={"display": "flex", "alignItems": "center"}),
            
            dbc.Nav([
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="fas fa-wallet me-2"), "Fondos"],
                    href="/fondos", id="nav-fondos", className="nav-link-custom"
                )),
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="fas fa-chart-bar me-2"), "Acciones"],
                    href="/acciones", id="nav-acciones", className="nav-link-custom"
                )),
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="fas fa-pie-chart me-2"), "Gráficas Fondos"],
                    href="/graficas-fondos", id="nav-graf-fondos", className="nav-link-custom"
                )),
                dbc.NavItem(dbc.NavLink(
                    [html.I(className="fas fa-chart-area me-2"), "Gráficas Acciones"],
                    href="/graficas-acciones", id="nav-graf-acciones", className="nav-link-custom"
                )),
            ], navbar=True, className="ms-auto"),
        ], fluid=True),
        color="dark", dark=True, className="mb-4 navbar-custom",
        style=NAVBAR_STYLE
    ),
    
    dbc.Container(
        html.Div(id='page-content'),
        fluid=True,
        style={"padding": "0 20px 40px"}
    )
], style={
    "backgroundColor": "#0a0e27",
    "minHeight": "100vh",
    "fontFamily": "'Inter', 'Segoe UI', sans-serif"
})

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/acciones':
        return acciones.layout()
    elif pathname == '/graficas-fondos':
        return graficas_fondos.layout()
    elif pathname == '/graficas-acciones':
        return graficas_acciones.layout()
    else:
        return fondos.layout()

# Solo para ejecución local
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

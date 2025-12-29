from dash import html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
from utils.database import Database
from utils.market_data import MarketData
from utils.styles import *
from datetime import datetime

db = Database()
market = MarketData()

def layout():
    return html.Div([
        # Header
        html.Div([
            html.H2([
                html.I(className="fas fa-wallet me-3"),
                "Gestión de Fondos de Inversión"
            ], style={"color": PRIMARY_COLOR, "fontWeight": "700"}),
            html.P("Monitorea y gestiona tu cartera de fondos en tiempo real",
                  style={"color": "#aaa", "marginTop": "10px"})
        ], style={"marginBottom": "30px"}),
        
        # Botones de acción
        html.Div([
            dbc.Button([
                html.I(className="fas fa-plus me-2"),
                "Añadir Fondo"
            ], id="btn-add-fondo", color="primary", className="me-2",
               style=BUTTON_PRIMARY),
            
            dbc.Button([
                html.I(className="fas fa-sync-alt me-2"),
                "Actualizar Datos"
            ], id="btn-refresh-fondos", color="success",
               style=BUTTON_SUCCESS)
        ], style={"marginBottom": "25px"}),
        
        # Tabla
        html.Div(id="fondos-table-container"),
        
        # Modal añadir/editar
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="modal-fondos-title")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Nombre del Fondo", style={"fontWeight": "600"}),
                        dbc.Input(id="input-fondo-nombre", type="text", 
                                 placeholder="Ej: Vanguard S&P 500", style=INPUT_STYLE)
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Ticker", style={"fontWeight": "600"}),
                        dbc.Input(id="input-fondo-ticker", type="text",
                                 placeholder="Ej: VOO", style=INPUT_STYLE)
                    ], width=6),
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Tipo de Inversión", style={"fontWeight": "600"}),
                        dbc.Select(
                            id="input-fondo-tipo",
                            options=[
                                {"label": "Renta Fija (RF)", "value": "RF"},
                                {"label": "Renta Variable (RV)", "value": "RV"}
                            ],
                            style=INPUT_STYLE
                        )
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Valor de Compra (€)", style={"fontWeight": "600"}),
                        dbc.Input(id="input-fondo-valor", type="number",
                                 placeholder="100.50", style=INPUT_STYLE)
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Cantidad Invertida", style={"fontWeight": "600"}),
                        dbc.Input(id="input-fondo-cantidad", type="number",
                                 placeholder="10", style=INPUT_STYLE)
                    ], width=4),
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Fecha de Compra", style={"fontWeight": "600"}),
                        dbc.Input(id="input-fondo-fecha", type="date",
                                 value=datetime.now().strftime('%Y-%m-%d'),
                                 style=INPUT_STYLE)
                    ], width=6),
                ]),
                
                html.Div(id="input-fondo-id", style={"display": "none"})
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancel-fondo", 
                          color="secondary", className="me-2"),
                dbc.Button("Guardar", id="btn-save-fondo",
                          style=BUTTON_PRIMARY)
            ])
        ], id="modal-fondos", size="lg", is_open=False,
           style={"color": "#000"}),
        
        # Modal eliminar
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirmar Eliminación")),
            dbc.ModalBody("¿Estás seguro de que deseas eliminar este fondo?"),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancel-delete-fondo", 
                          color="secondary", className="me-2"),
                dbc.Button("Eliminar", id="btn-confirm-delete-fondo",
                          style=BUTTON_DANGER)
            ])
        ], id="modal-delete-fondo", is_open=False,
           style={"color": "#000"}),
        
        html.Div(id="fondo-to-delete", style={"display": "none"}),
        dcc.Interval(id='interval-fondos', interval=60000, n_intervals=0)
    ])

@callback(
    Output("fondos-table-container", "children"),
    [Input("btn-refresh-fondos", "n_clicks"),
     Input("interval-fondos", "n_intervals"),
     Input("btn-save-fondo", "n_clicks"),
     Input("btn-confirm-delete-fondo", "n_clicks")]
)
def update_fondos_table(refresh_clicks, intervals, save_clicks, delete_clicks):
    fondos = db.get_fondos()
    
    if not fondos:
        return html.Div([
            html.I(className="fas fa-inbox fa-3x mb-3", 
                  style={"color": "#555"}),
            html.P("No hay fondos registrados. ¡Añade tu primer fondo!",
                  style={"color": "#aaa", "fontSize": "1.1rem"})
        ], style={"textAlign": "center", "padding": "60px 20px"})
    
    # Calcular datos con Yahoo Finance
    table_data = []
    total_invertido = 0
    total_valor_actual = 0
    
    for fondo in fondos:
        current_price = market.get_current_price(fondo['ticker'])
        daily_change_pct, daily_change_abs = market.get_daily_change(fondo['ticker'])
        ytd_change = market.get_ytd_change(fondo['ticker'], fondo['fecha_compra'])
        
        valor_actual = current_price * fondo['cantidad'] if current_price else 0
        invertido = fondo['valor_compra'] * fondo['cantidad']
        ganancia_perdida = valor_actual - invertido
        ganancia_perdida_pct = (ganancia_perdida / invertido * 100) if invertido > 0 else 0
        
        total_invertido += invertido
        total_valor_actual += valor_actual
        
        table_data.append({
            'id': fondo['id'],
            'Nombre': fondo['nombre'],
            'Ticker': fondo['ticker'],
            'Tipo': fondo['tipo'],
            'Valor Compra': f"€{fondo['valor_compra']:.2f}",
            'Cantidad': f"{fondo['cantidad']:.2f}",
            'Valor Actual': f"€{current_price:.2f}" if current_price else "N/A",
            'Cambio Diario': f"{daily_change_pct:+.2f}% (€{daily_change_abs:+.2f})",
            'Cambio YTD': f"{ytd_change:+.2f}%",
            'Ganancia/Pérdida': f"€{ganancia_perdida:+,.2f} ({ganancia_perdida_pct:+.2f}%)",
            'Fecha Compra': fondo['fecha_compra'],
            'Acciones': fondo['id']
        })
    
    # Fila de totales
    total_ganancia = total_valor_actual - total_invertido
    total_ganancia_pct = (total_ganancia / total_invertido * 100) if total_invertido > 0 else 0
    
    table_data.append({
        'id': 'total',
        'Nombre': 'TOTAL',
        'Ticker': '',
        'Tipo': '',
        'Valor Compra': '',
        'Cantidad': '',
        'Valor Actual': f"€{total_valor_actual:,.2f}",
        'Cambio Diario': '',
        'Cambio YTD': '',
        'Ganancia/Pérdida': f"€{total_ganancia:+,.2f} ({total_ganancia_pct:+.2f}%)",
        'Fecha Compra': f"Total Invertido: €{total_invertido:,.2f}",
        'Acciones': ''
    })
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {'name': 'Nombre', 'id': 'Nombre'},
            {'name': 'Ticker', 'id': 'Ticker'},
            {'name': 'Tipo', 'id': 'Tipo'},
            {'name': 'Valor Compra', 'id': 'Valor Compra'},
            {'name': 'Cantidad', 'id': 'Cantidad'},
            {'name': 'Valor Actual', 'id': 'Valor Actual'},
            {'name': 'Cambio Diario', 'id': 'Cambio Diario'},
            {'name': 'Cambio YTD', 'id': 'Cambio YTD'},
            {'name': 'Ganancia/Pérdida', 'id': 'Ganancia/Pérdida'},
            {'name': 'Fecha Compra', 'id': 'Fecha Compra'},
            {'name': 'Acciones', 'id': 'Acciones', 'presentation': 'markdown'}
        ],
        style_table=TABLE_STYLE,
        style_header=TABLE_HEADER_STYLE,
        style_cell=TABLE_CELL_STYLE,
        style_data_conditional=[
            {
                'if': {'row_index': len(table_data) - 1},
                'backgroundColor': CARD_BG_LIGHTER,
                'fontWeight': '700',
                'borderTop': f'2px solid {PRIMARY_COLOR}'
            },
            {
                'if': {'filter_query': '{Ganancia/Pérdida} contains "+"'},
                'color': SUCCESS_COLOR
            },
            {
                'if': {'filter_query': '{Ganancia/Pérdida} contains "-"'},
                'color': DANGER_COLOR
            }
        ],
        page_size=20,
        id='fondos-datatable'
    )

@callback(
    [Output("modal-fondos", "is_open"),
     Output("modal-fondos-title", "children"),
     Output("input-fondo-nombre", "value"),
     Output("input-fondo-ticker", "value"),
     Output("input-fondo-tipo", "value"),
     Output("input-fondo-valor", "value"),
     Output("input-fondo-cantidad", "value"),
     Output("input-fondo-fecha", "value"),
     Output("input-fondo-id", "children")],
    [Input("btn-add-fondo", "n_clicks"),
     Input("btn-cancel-fondo", "n_clicks"),
     Input("btn-save-fondo", "n_clicks")],
    [State("input-fondo-nombre", "value"),
     State("input-fondo-ticker", "value"),
     State("input-fondo-tipo", "value"),
     State("input-fondo-valor", "value"),
     State("input-fondo-cantidad", "value"),
     State("input-fondo-fecha", "value"),
     State("input-fondo-id", "children"),
     State("modal-fondos", "is_open")]
)
def toggle_modal_fondos(add_clicks, cancel_clicks, save_clicks, 
                        nombre, ticker, tipo, valor, cantidad, fecha, fondo_id, is_open):
    ctx = callback_context
    if not ctx.triggered:
        return False, "", "", "", "RV", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "btn-add-fondo":
        return True, "Añadir Nuevo Fondo", "", "", "RV", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    if button_id == "btn-save-fondo":
        if all([nombre, ticker, tipo, valor, cantidad, fecha]):
            if fondo_id:
                db.update_fondo(int(fondo_id), nombre, ticker, tipo, float(valor), float(cantidad), fecha)
            else:
                db.add_fondo(nombre, ticker, tipo, float(valor), float(cantidad), fecha)
            return False, "", "", "", "RV", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    if button_id == "btn-cancel-fondo":
        return False, "", "", "", "RV", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    return is_open, "Añadir Nuevo Fondo", "", "", "RV", "", "", datetime.now().strftime('%Y-%m-%d'), ""

@callback(
    [Output("modal-delete-fondo", "is_open"),
     Output("fondo-to-delete", "children")],
    [Input("btn-confirm-delete-fondo", "n_clicks"),
     Input("btn-cancel-delete-fondo", "n_clicks")],
    [State("fondo-to-delete", "children"),
     State("modal-delete-fondo", "is_open")]
)
def toggle_delete_modal(confirm_clicks, cancel_clicks, fondo_id, is_open):
    ctx = callback_context
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "btn-confirm-delete-fondo" and fondo_id:
        db.delete_fondo(int(fondo_id))
        return False, ""
    
    if button_id == "btn-cancel-delete-fondo":
        return False, ""
    
    return is_open, fondo_id

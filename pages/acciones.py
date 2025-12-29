from dash import html, dcc, Input, Output, State, callback, dash_table, callback_context
import dash_bootstrap_components as dbc
from utils.database import Database
from utils.market_data import MarketData
from utils.styles import *
from datetime import datetime

db = Database()
market = MarketData()

def layout():
    return html.Div([
        html.Div([
            html.H2([
                html.I(className="fas fa-chart-bar me-3"),
                "Gestión de Acciones"
            ], style={"color": PRIMARY_COLOR, "fontWeight": "700"}),
            html.P("Monitorea tu cartera de acciones en tiempo real",
                  style={"color": "#aaa", "marginTop": "10px"})
        ], style={"marginBottom": "30px"}),
        
        html.Div([
            dbc.Button([
                html.I(className="fas fa-plus me-2"),
                "Añadir Acción"
            ], id="btn-add-accion", color="primary", className="me-2",
               style=BUTTON_PRIMARY),
            
            dbc.Button([
                html.I(className="fas fa-sync-alt me-2"),
                "Actualizar Datos"
            ], id="btn-refresh-acciones", color="success",
               style=BUTTON_SUCCESS)
        ], style={"marginBottom": "25px"}),
        
        html.Div(id="acciones-table-container"),
        
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="modal-acciones-title")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Nombre de la Acción", style={"fontWeight": "600"}),
                        dbc.Input(id="input-accion-nombre", type="text", 
                                 placeholder="Ej: Apple Inc.", style=INPUT_STYLE)
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Ticker", style={"fontWeight": "600"}),
                        dbc.Input(id="input-accion-ticker", type="text",
                                 placeholder="Ej: AAPL", style=INPUT_STYLE)
                    ], width=6),
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Sector", style={"fontWeight": "600"}),
                        dbc.Input(id="input-accion-sector", type="text",
                                 placeholder="Ej: Tecnología", style=INPUT_STYLE)
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Precio de Compra (€)", style={"fontWeight": "600"}),
                        dbc.Input(id="input-accion-precio", type="number",
                                 placeholder="150.50", style=INPUT_STYLE)
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Número de Acciones", style={"fontWeight": "600"}),
                        dbc.Input(id="input-accion-num", type="number",
                                 placeholder="10", style=INPUT_STYLE)
                    ], width=4),
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Fecha de Compra", style={"fontWeight": "600"}),
                        dbc.Input(id="input-accion-fecha", type="date",
                                 value=datetime.now().strftime('%Y-%m-%d'),
                                 style=INPUT_STYLE)
                    ], width=6),
                ]),
                
                html.Div(id="input-accion-id", style={"display": "none"})
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancel-accion", 
                          color="secondary", className="me-2"),
                dbc.Button("Guardar", id="btn-save-accion",
                          style=BUTTON_PRIMARY)
            ])
        ], id="modal-acciones", size="lg", is_open=False,
           style={"color": "#000"}),
        
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirmar Eliminación")),
            dbc.ModalBody("¿Estás seguro de que deseas eliminar esta acción?"),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancel-delete-accion", 
                          color="secondary", className="me-2"),
                dbc.Button("Eliminar", id="btn-confirm-delete-accion",
                          style=BUTTON_DANGER)
            ])
        ], id="modal-delete-accion", is_open=False,
           style={"color": "#000"}),
        
        html.Div(id="accion-to-delete", style={"display": "none"}),
        dcc.Interval(id='interval-acciones', interval=60000, n_intervals=0)
    ])

@callback(
    Output("acciones-table-container", "children"),
    [Input("btn-refresh-acciones", "n_clicks"),
     Input("interval-acciones", "n_intervals"),
     Input("btn-save-accion", "n_clicks"),
     Input("btn-confirm-delete-accion", "n_clicks")]
)
def update_acciones_table(refresh_clicks, intervals, save_clicks, delete_clicks):
    acciones = db.get_acciones()
    
    if not acciones:
        return html.Div([
            html.I(className="fas fa-inbox fa-3x mb-3", 
                  style={"color": "#555"}),
            html.P("No hay acciones registradas. ¡Añade tu primera acción!",
                  style={"color": "#aaa", "fontSize": "1.1rem"})
        ], style={"textAlign": "center", "padding": "60px 20px"})
    
    table_data = []
    total_invertido = 0
    total_valor_actual = 0
    
    for accion in acciones:
        current_price = market.get_current_price(accion['ticker'])
        daily_change_pct, daily_change_abs = market.get_daily_change(accion['ticker'])
        ytd_change = market.get_ytd_change(accion['ticker'], accion['fecha_compra'])
        
        valor_actual = current_price * accion['num_acciones'] if current_price else 0
        invertido = accion['precio_compra'] * accion['num_acciones']
        ganancia_perdida = valor_actual - invertido
        ganancia_perdida_pct = (ganancia_perdida / invertido * 100) if invertido > 0 else 0
        
        total_invertido += invertido
        total_valor_actual += valor_actual
        
        table_data.append({
            'id': accion['id'],
            'Nombre': accion['nombre'],
            'Ticker': accion['ticker'],
            'Sector': accion.get('sector', 'N/A'),
            'Precio Compra': f"€{accion['precio_compra']:.2f}",
            'Num. Acciones': accion['num_acciones'],
            'Valor Actual': f"€{current_price:.2f}" if current_price else "N/A",
            'Cambio Diario': f"{daily_change_pct:+.2f}% (€{daily_change_abs:+.2f})",
            'Cambio YTD': f"{ytd_change:+.2f}%",
            'Ganancia/Pérdida': f"€{ganancia_perdida:+,.2f} ({ganancia_perdida_pct:+.2f}%)",
            'Fecha Compra': accion['fecha_compra']
        })
    
    total_ganancia = total_valor_actual - total_invertido
    total_ganancia_pct = (total_ganancia / total_invertido * 100) if total_invertido > 0 else 0
    
    table_data.append({
        'id': 'total',
        'Nombre': 'TOTAL',
        'Ticker': '',
        'Sector': '',
        'Precio Compra': '',
        'Num. Acciones': '',
        'Valor Actual': f"€{total_valor_actual:,.2f}",
        'Cambio Diario': '',
        'Cambio YTD': '',
        'Ganancia/Pérdida': f"€{total_ganancia:+,.2f} ({total_ganancia_pct:+.2f}%)",
        'Fecha Compra': f"Total Invertido: €{total_invertido:,.2f}"
    })
    
    return dash_table.DataTable(
        data=table_data,
        columns=[
            {'name': 'Nombre', 'id': 'Nombre'},
            {'name': 'Ticker', 'id': 'Ticker'},
            {'name': 'Sector', 'id': 'Sector'},
            {'name': 'Precio Compra', 'id': 'Precio Compra'},
            {'name': 'Num. Acciones', 'id': 'Num. Acciones'},
            {'name': 'Valor Actual', 'id': 'Valor Actual'},
            {'name': 'Cambio Diario', 'id': 'Cambio Diario'},
            {'name': 'Cambio YTD', 'id': 'Cambio YTD'},
            {'name': 'Ganancia/Pérdida', 'id': 'Ganancia/Pérdida'},
            {'name': 'Fecha Compra', 'id': 'Fecha Compra'}
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
        page_size=20
    )

@callback(
    [Output("modal-acciones", "is_open"),
     Output("modal-acciones-title", "children"),
     Output("input-accion-nombre", "value"),
     Output("input-accion-ticker", "value"),
     Output("input-accion-sector", "value"),
     Output("input-accion-precio", "value"),
     Output("input-accion-num", "value"),
     Output("input-accion-fecha", "value"),
     Output("input-accion-id", "children")],
    [Input("btn-add-accion", "n_clicks"),
     Input("btn-cancel-accion", "n_clicks"),
     Input("btn-save-accion", "n_clicks")],
    [State("input-accion-nombre", "value"),
     State("input-accion-ticker", "value"),
     State("input-accion-sector", "value"),
     State("input-accion-precio", "value"),
     State("input-accion-num", "value"),
     State("input-accion-fecha", "value"),
     State("input-accion-id", "children"),
     State("modal-acciones", "is_open")]
)
def toggle_modal_acciones(add_clicks, cancel_clicks, save_clicks,
                          nombre, ticker, sector, precio, num, fecha, accion_id, is_open):
    ctx = callback_context
    if not ctx.triggered:
        return False, "", "", "", "", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "btn-add-accion":
        return True, "Añadir Nueva Acción", "", "", "", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    if button_id == "btn-save-accion":
        if all([nombre, ticker, precio, num, fecha]):
            sector_val = sector if sector else "N/A"
            if accion_id:
                db.update_accion(int(accion_id), nombre, ticker, sector_val, float(precio), int(num), fecha)
            else:
                db.add_accion(nombre, ticker, sector_val, float(precio), int(num), fecha)
            return False, "", "", "", "", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    if button_id == "btn-cancel-accion":
        return False, "", "", "", "", "", "", datetime.now().strftime('%Y-%m-%d'), ""
    
    return is_open, "Añadir Nueva Acción", "", "", "", "", "", datetime.now().strftime('%Y-%m-%d'), ""

@callback(
    [Output("modal-delete-accion", "is_open"),
     Output("accion-to-delete", "children")],
    [Input("btn-confirm-delete-accion", "n_clicks"),
     Input("btn-cancel-delete-accion", "n_clicks")],
    [State("accion-to-delete", "children"),
     State("modal-delete-accion", "is_open")]
)
def toggle_delete_modal(confirm_clicks, cancel_clicks, accion_id, is_open):
    ctx = callback_context
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "btn-confirm-delete-accion" and accion_id:
        db.delete_accion(int(accion_id))
        return False, ""
    
    if button_id == "btn-cancel-delete-accion":
        return False, ""
    
    return is_open, accion_id

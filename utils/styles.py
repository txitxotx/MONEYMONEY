# Colores principales
PRIMARY_COLOR = "#00d4ff"
SECONDARY_COLOR = "#6c63ff"
SUCCESS_COLOR = "#00e676"
DANGER_COLOR = "#ff1744"
DARK_BG = "#0a0e27"
CARD_BG = "#141b3a"
CARD_BG_LIGHTER = "#1a2342"

# Estilos del navbar
NAVBAR_STYLE = {
    "boxShadow": "0 4px 20px rgba(0,212,255,0.15)",
    "borderBottom": f"2px solid {PRIMARY_COLOR}",
    "padding": "0.8rem 0"
}

# Estilos de cards
CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "borderRadius": "12px",
    "boxShadow": "0 8px 32px rgba(0,0,0,0.4)",
    "border": f"1px solid rgba(0,212,255,0.1)",
    "marginBottom": "20px",
    "transition": "all 0.3s ease"
}

# Estilos de botones
BUTTON_PRIMARY = {
    "background": f"linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR})",
    "border": "none",
    "borderRadius": "8px",
    "padding": "10px 24px",
    "fontWeight": "600",
    "transition": "all 0.3s ease",
    "boxShadow": "0 4px 15px rgba(0,212,255,0.3)"
}

BUTTON_SUCCESS = {
    "backgroundColor": SUCCESS_COLOR,
    "border": "none",
    "borderRadius": "8px",
    "padding": "10px 24px",
    "fontWeight": "600",
    "transition": "all 0.3s ease"
}

BUTTON_DANGER = {
    "backgroundColor": DANGER_COLOR,
    "border": "none",
    "borderRadius": "8px",
    "padding": "10px 24px",
    "fontWeight": "600",
    "transition": "all 0.3s ease"
}

# Estilos de tabla
TABLE_STYLE = {
    "backgroundColor": CARD_BG,
    "borderRadius": "12px",
    "overflow": "hidden",
    "boxShadow": "0 8px 32px rgba(0,0,0,0.4)"
}

TABLE_HEADER_STYLE = {
    "backgroundColor": CARD_BG_LIGHTER,
    "fontWeight": "700",
    "textTransform": "uppercase",
    "fontSize": "0.85rem",
    "letterSpacing": "0.5px",
    "color": PRIMARY_COLOR,
    "padding": "16px",
    "borderBottom": f"2px solid {PRIMARY_COLOR}"
}

TABLE_CELL_STYLE = {
    "padding": "14px 16px",
    "borderBottom": "1px solid rgba(255,255,255,0.05)"
}

# Estilos de inputs
INPUT_STYLE = {
    "backgroundColor": CARD_BG_LIGHTER,
    "border": f"1px solid rgba(0,212,255,0.2)",
    "borderRadius": "8px",
    "color": "#fff",
    "padding": "10px 14px"
}

# Configuración de gráficas
CHART_CONFIG = {
    'displayModeBar': False,
    'responsive': True
}

CHART_LAYOUT = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#fff', 'family': 'Inter, sans-serif'},
    'margin': {'l': 40, 'r': 40, 't': 60, 'b': 40},
    'showlegend': True,
    'legend': {
        'bgcolor': CARD_BG_LIGHTER,
        'bordercolor': PRIMARY_COLOR,
        'borderwidth': 1
    }
}

import json
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path='data/investments.json'):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Crea el directorio y archivo JSON si no existen"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.db_path):
            initial_data = {
                "fondos": [],
                "acciones": []
            }
            self._save_data(initial_data)
    
    def _load_data(self):
        """Carga datos desde JSON"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"fondos": [], "acciones": []}
    
    def _save_data(self, data):
        """Guarda datos en JSON"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _get_next_id(self, items):
        """Obtiene el siguiente ID disponible"""
        if not items:
            return 1
        return max([item.get('id', 0) for item in items]) + 1
    
    # FONDOS
    def get_fondos(self):
        data = self._load_data()
        return data.get('fondos', [])
    
    def add_fondo(self, nombre, ticker, tipo, valor_compra, cantidad, fecha_compra):
        data = self._load_data()
        new_fondo = {
            'id': self._get_next_id(data['fondos']),
            'nombre': nombre,
            'ticker': ticker.upper(),
            'tipo': tipo,
            'valor_compra': float(valor_compra),
            'cantidad': float(cantidad),
            'fecha_compra': fecha_compra
        }
        data['fondos'].append(new_fondo)
        self._save_data(data)
        return new_fondo
    
    def update_fondo(self, id, nombre, ticker, tipo, valor_compra, cantidad, fecha_compra):
        data = self._load_data()
        for i, fondo in enumerate(data['fondos']):
            if fondo['id'] == id:
                data['fondos'][i] = {
                    'id': id,
                    'nombre': nombre,
                    'ticker': ticker.upper(),
                    'tipo': tipo,
                    'valor_compra': float(valor_compra),
                    'cantidad': float(cantidad),
                    'fecha_compra': fecha_compra
                }
                self._save_data(data)
                return True
        return False
    
    def delete_fondo(self, id):
        data = self._load_data()
        data['fondos'] = [f for f in data['fondos'] if f['id'] != id]
        self._save_data(data)
    
    # ACCIONES
    def get_acciones(self):
        data = self._load_data()
        return data.get('acciones', [])
    
    def add_accion(self, nombre, ticker, sector, precio_compra, num_acciones, fecha_compra):
        data = self._load_data()
        new_accion = {
            'id': self._get_next_id(data['acciones']),
            'nombre': nombre,
            'ticker': ticker.upper(),
            'sector': sector,
            'precio_compra': float(precio_compra),
            'num_acciones': int(num_acciones),
            'fecha_compra': fecha_compra
        }
        data['acciones'].append(new_accion)
        self._save_data(data)
        return new_accion
    
    def update_accion(self, id, nombre, ticker, sector, precio_compra, num_acciones, fecha_compra):
        data = self._load_data()
        for i, accion in enumerate(data['acciones']):
            if accion['id'] == id:
                data['acciones'][i] = {
                    'id': id,
                    'nombre': nombre,
                    'ticker': ticker.upper(),
                    'sector': sector,
                    'precio_compra': float(precio_compra),
                    'num_acciones': int(num_acciones),
                    'fecha_compra': fecha_compra
                }
                self._save_data(data)
                return True
        return False
    
    def delete_accion(self, id):
        data = self._load_data()
        data['acciones'] = [a for a in data['acciones'] if a['id'] != id]
        self._save_data(data)

from utils.supabase_client import get_supabase_client
from datetime import datetime

class Database:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    # ============== FONDOS ==============
    
    def get_fondos(self):
        """Obtiene todos los fondos"""
        try:
            response = self.supabase.table('fondos').select('*').order('id').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al obtener fondos: {e}")
            return []
    
    def add_fondo(self, nombre, ticker, tipo, valor_compra, cantidad, fecha_compra):
        """Añade un nuevo fondo"""
        try:
            data = {
                'nombre': nombre,
                'ticker': ticker.upper(),
                'tipo': tipo,
                'valor_compra': float(valor_compra),
                'cantidad': float(cantidad),
                'fecha_compra': fecha_compra
            }
            response = self.supabase.table('fondos').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error al añadir fondo: {e}")
            return None
    
    def update_fondo(self, id, nombre, ticker, tipo, valor_compra, cantidad, fecha_compra):
        """Actualiza un fondo existente"""
        try:
            data = {
                'nombre': nombre,
                'ticker': ticker.upper(),
                'tipo': tipo,
                'valor_compra': float(valor_compra),
                'cantidad': float(cantidad),
                'fecha_compra': fecha_compra
            }
            response = self.supabase.table('fondos').update(data).eq('id', id).execute()
            return True if response.data else False
        except Exception as e:
            print(f"Error al actualizar fondo: {e}")
            return False
    
    def delete_fondo(self, id):
        """Elimina un fondo"""
        try:
            self.supabase.table('fondos').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print(f"Error al eliminar fondo: {e}")
            return False
    
    # ============== ACCIONES ==============
    
    def get_acciones(self):
        """Obtiene todas las acciones"""
        try:
            response = self.supabase.table('acciones').select('*').order('id').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error al obtener acciones: {e}")
            return []
    
    def add_accion(self, nombre, ticker, sector, precio_compra, num_acciones, fecha_compra):
        """Añade una nueva acción"""
        try:
            data = {
                'nombre': nombre,
                'ticker': ticker.upper(),
                'sector': sector if sector else 'N/A',
                'precio_compra': float(precio_compra),
                'num_acciones': int(num_acciones),
                'fecha_compra': fecha_compra
            }
            response = self.supabase.table('acciones').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error al añadir acción: {e}")
            return None
    
    def update_accion(self, id, nombre, ticker, sector, precio_compra, num_acciones, fecha_compra):
        """Actualiza una acción existente"""
        try:
            data = {
                'nombre': nombre,
                'ticker': ticker.upper(),
                'sector': sector if sector else 'N/A',
                'precio_compra': float(precio_compra),
                'num_acciones': int(num_acciones),
                'fecha_compra': fecha_compra
            }
            response = self.supabase.table('acciones').update(data).eq('id', id).execute()
            return True if response.data else False
        except Exception as e:
            print(f"Error al actualizar acción: {e}")
            return False
    
    def delete_accion(self, id):
        """Elimina una acción"""
        try:
            self.supabase.table('acciones').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print(f"Error al eliminar acción: {e}")
            return False

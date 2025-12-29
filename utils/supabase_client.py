from supabase import create_client, Client
import os

def get_supabase_client() -> Client:
    """Crea y retorna cliente de Supabase"""
    # En Vercel, las variables vienen directo del entorno
    url = os.environ.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError(
            "❌ SUPABASE_URL y SUPABASE_KEY deben estar configuradas. "
            f"URL encontrada: {bool(url)}, KEY encontrada: {bool(key)}"
        )
    
    return create_client(url, key)

# config.py
import os

# ============================================
# TEMA - Cambia aquí para modificar todos los colores
# ============================================
TEMA_ACTUAL = "oscuro"  # Opciones: "oscuro", "claro", "verde", "azul", "rojo"

# Definición de temas
TEMAS = {
    "oscuro": {
        "primary": "gray",        # Color principal (naranja)
        "secondary": "#FF6B6B",      # Color secundario (rojo)
        "success": "#4CAF50",        # Color de éxito (verde)
        "bg_dark": "black",        # Fondo oscuro
        "bg_card": "#1a1a1a",        # Fondo de tarjetas
        "bg_input": "#2a2a2a",       # Fondo de inputs
        "text_primary": "white",     # Texto principal
        "text_secondary": "#999999", # Texto secundario
        "text_accent": "#CCCCCC",    # Texto acentuado
        "border": "gray",         # Bordes
    },
    "claro": {
        "primary": "#FF6B35",        # Naranja más vivo
        "secondary": "#FF4757",      # Rojo
        "success": "#2ED573",        # Verde
        "bg_dark": "#F5F5F5",        # Fondo claro
        "bg_card": "#FFFFFF",        # Tarjetas blancas
        "bg_input": "#E8E8E8",       # Input gris claro
        "text_primary": "#1a1a1a",   # Texto oscuro
        "text_secondary": "#666666", # Texto gris
        "text_accent": "#333333",    # Texto oscuro acentuado
        "border": "#CCCCCC",         # Bordes claros
    },
    "verde": {
        "primary": "#10B981",        # Verde principal
        "secondary": "#F59E0B",      # Ámbar
        "success": "#34D399",        # Verde claro
        "bg_dark": "#0F172A",        # Azul muy oscuro
        "bg_card": "#1E293B",        # Azul oscuro
        "bg_input": "#334155",       # Azul grisáceo
        "text_primary": "white",
        "text_secondary": "#94A3B8",
        "text_accent": "#E2E8F0",
        "border": "#475569",
    },
    "azul": {
        "primary": "#3B82F6",        # Azul principal
        "secondary": "#EF4444",      # Rojo
        "success": "#10B981",        # Verde
        "bg_dark": "#0F172A",        # Azul muy oscuro
        "bg_card": "#1E293B",        # Azul oscuro
        "bg_input": "#334155",       # Azul grisáceo
        "text_primary": "white",
        "text_secondary": "#94A3B8",
        "text_accent": "#E2E8F0",
        "border": "#475569",
    },
    "rojo": {
        "primary": "#DC2626",        # Rojo principal
        "secondary": "#F59E0B",      # Ámbar
        "success": "#10B981",        # Verde
        "bg_dark": "#1F1F1F",        # Gris muy oscuro
        "bg_card": "#2D2D2D",        # Gris oscuro
        "bg_input": "#3D3D3D",       # Gris
        "text_primary": "white",
        "text_secondary": "#A0A0A0",
        "text_accent": "#E5E5E5",
        "border": "#4D4D4D",
    },
}

# Obtener colores del tema actual
COLORES = TEMAS[TEMA_ACTUAL]

# Exportar colores individuales (para compatibilidad con código existente)
PRIMARY_COLOR = COLORES["primary"]
SECONDARY_COLOR = COLORES["secondary"]
SUCCESS_COLOR = COLORES["success"]
BG_DARK = COLORES["bg_dark"]
BG_CARD = COLORES["bg_card"]
BG_INPUT = COLORES["bg_input"]
TEXT_PRIMARY = COLORES["text_primary"]
TEXT_SECONDARY = COLORES["text_secondary"]
TEXT_ACCENT = COLORES["text_accent"]
BORDER_COLOR = COLORES["border"]

# ============================================
# CONSTANTES DE COMPORTAMIENTO (NUEVAS)
# ============================================
DELAY_SNACKBAR = 2  # segundos
DELAY_WHATSAPP = 1  # segundos
ESPACIO_CONTENEDOR = 20  # píxeles
ESPACIO_PEQUEÑO = 15  # píxeles
GRID_CHILD_ASPECT_RATIO = 0.75
TIMEOUT_WHATSAPP = 5  # segundos antes de timeout

# ============================================
# RUTAS
# ============================================
def get_logo_path():
    """Obtiene la ruta del logo"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "images", "logo.png")

def get_titulo_path():
    """Obtiene la ruta del título"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "images", "titulo.png")

def get_gif_path():
    """Obtiene la ruta del GIF"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "videos", "intro.gif")

# ============================================
# PRODUCTOS
# ============================================
PRODUCTOS = [
    {
        "id": 1,
        "nombre": "Hongos Frescos Ostra",
        "precio": 12.99,
        "emoji": "🍄",
        "descripcion": "Hongos ostra frescos de alta calidad",
        "categoria": "Hongos Frescos"
    },
    {
        "id": 2,
        "nombre": "Hongos Shiitake",
        "precio": 14.99,
        "emoji": "🍄",
        "descripcion": "Shiitake premium importado",
        "categoria": "Hongos Frescos"
    },
    {
        "id": 3,
        "nombre": "Hongos Champiñones",
        "precio": 8.99,
        "emoji": "🍄",
        "descripcion": "Champiñones frescos locales",
        "categoria": "Hongos Frescos"
    },
    {
        "id": 4,
        "nombre": "Hongos Secos Porcini",
        "precio": 18.99,
        "emoji": "🌾",
        "descripcion": "Porcini deshidratado premium",
        "categoria": "Hongos Secos"
    },
    {
        "id": 5,
        "nombre": "Mix Hongos Secos",
        "precio": 16.99,
        "emoji": "🌾",
        "descripcion": "Mezcla de hongos deshidratados",
        "categoria": "Hongos Secos"
    },
    {
        "id": 6,
        "nombre": "Extracto de Reishi",
        "precio": 24.99,
        "emoji": "🧪",
        "descripcion": "Extracto concentrado de Reishi",
        "categoria": "Extractos"
    },
    {
        "id": 7,
        "nombre": "Extracto Lion's Mane",
        "precio": 22.99,
        "emoji": "🧪",
        "descripcion": "Extracto de melena de león",
        "categoria": "Extractos"
    },
    {
        "id": 8,
        "nombre": "Kit Cultivo Ostra",
        "precio": 29.99,
        "emoji": "🌱",
        "descripcion": "Kit completo para cultivar hongos ostra",
        "categoria": "Kits de Cultivo"
    },
    {
        "id": 9,
        "nombre": "Kit Cultivo Shiitake",
        "precio": 34.99,
        "emoji": "🌱",
        "descripcion": "Kit profesional para shiitake",
        "categoria": "Kits de Cultivo"
    },
]

# ============================================
# BENEFICIOS
# ============================================
BENEFICIOS = [
    {"titulo": "100% Orgánico", "descripcion": "Cultivado sin químicos", "icon": "🌿"},
    {"titulo": "Entrega Rápida", "descripcion": "En 24-48 horas", "icon": "🚚"},
    {"titulo": "Garantía", "descripcion": "Satisfacción garantizada", "icon": "✅"},
    {"titulo": "Expertos", "descripcion": "Soporte especializado", "icon": "👨‍🔬"},
]

# ============================================
# TESTIMONIOS
# ============================================
TESTIMONIOS = [
    {
        "texto": "Los mejores hongos que he probado. La calidad es increíble.",
        "autor": "María García",
        "rating": "⭐⭐⭐⭐⭐"
    },
    {
        "texto": "Envío rápido y productos frescos. Muy recomendado.",
        "autor": "Juan Pérez",
        "rating": "⭐⭐⭐⭐⭐"
    },
]

# ============================================
# CONFIGURACIÓN NEQUI
# ============================================
NUMERO_NEQUI = "+573218870869"
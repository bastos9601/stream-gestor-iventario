#!/usr/bin/env python3
"""
Script para generar iconos en diferentes tamaños para la PWA
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Crear un icono del tamaño especificado"""
    # Crear imagen con fondo azul
    img = Image.new('RGB', (size, size), color='#0d6efd')
    draw = ImageDraw.Draw(img)
    
    # Calcular tamaño del texto
    text = "GS"
    font_size = size // 3
    
    try:
        # Intentar usar una fuente del sistema
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            # Fuente por defecto
            font = ImageFont.load_default()
    
    # Calcular posición del texto para centrarlo
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Dibujar texto blanco
    draw.text((x, y), text, fill='white', font=font)
    
    # Crear directorio si no existe
    os.makedirs('static/icons', exist_ok=True)
    
    # Guardar icono
    img.save(f'static/icons/{filename}')
    print(f"✅ Icono creado: {filename}")

def create_shortcut_icon(size, filename, text):
    """Crear icono para shortcuts"""
    img = Image.new('RGB', (size, size), color='#28a745')
    draw = ImageDraw.Draw(img)
    
    font_size = size // 4
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Calcular posición del texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Dibujar texto blanco
    draw.text((x, y), text, fill='white', font=font)
    
    # Crear directorio si no existe
    os.makedirs('static/icons', exist_ok=True)
    
    # Guardar icono
    img.save(f'static/icons/{filename}')
    print(f"✅ Icono de shortcut creado: {filename}")

def main():
    """Función principal"""
    print("🎨 Generando iconos para la PWA...")
    
    # Tamaños de iconos requeridos
    icon_sizes = [
        (72, "icon-72x72.png"),
        (96, "icon-96x96.png"),
        (128, "icon-128x128.png"),
        (144, "icon-144x144.png"),
        (152, "icon-152x152.png"),
        (192, "icon-192x192.png"),
        (384, "icon-384x384.png"),
        (512, "icon-512x512.png")
    ]
    
    # Crear iconos principales
    for size, filename in icon_sizes:
        create_icon(size, filename)
    
    # Crear iconos para shortcuts
    shortcut_sizes = [
        (96, "add-account.png", "+"),
        (96, "list-accounts.png", "📋")
    ]
    
    for size, filename, text in shortcut_sizes:
        create_shortcut_icon(size, filename, text)
    
    print("\n🎉 ¡Todos los iconos han sido generados!")
    print("📁 Ubicación: static/icons/")
    print("\n📱 Ahora puedes:")
    print("1. Usar PWA Builder para crear el APK")
    print("2. O usar Bubblewrap para generar TWA")
    print("3. Los iconos se cargarán automáticamente")

if __name__ == "__main__":
    main()

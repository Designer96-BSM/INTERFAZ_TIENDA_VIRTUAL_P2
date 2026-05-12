# logic.py
import json
import re
import urllib.parse
from config import PRODUCTOS


class CarritoManager:
    """Gestiona el carrito de compras"""

    def __init__(self):
        self.carrito = {}
        self.cargar_carrito()

    def agregar(self, producto):
        """Agrega producto al carrito"""
        producto_id = producto["id"]

        if producto_id in self.carrito:
            self.carrito[producto_id]["cantidad"] += 1
        else:
            self.carrito[producto_id] = {
                "producto": producto,
                "cantidad": 1
            }
        self.guardar_carrito()

    def cambiar_cantidad(self, producto_id, cambio):
        """Cambia la cantidad de un producto"""
        if producto_id in self.carrito:
            nueva_cantidad = self.carrito[producto_id]["cantidad"] + cambio
            if nueva_cantidad > 0:
                self.carrito[producto_id]["cantidad"] = nueva_cantidad
            else:
                del self.carrito[producto_id]
            self.guardar_carrito()

    def eliminar(self, producto_id):
        """Elimina producto del carrito"""
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()

    def obtener_total(self):
        """Calcula el total del carrito"""
        return sum(
            item["producto"]["precio"] * item["cantidad"]
            for item in self.carrito.values()
        )

    def obtener_cantidad_items(self):
        """Obtiene cantidad total de items"""
        return sum(item["cantidad"] for item in self.carrito.values())

    def guardar_carrito(self):
        """Guarda carrito en JSON"""
        carrito_data = {}
        for pid, item in self.carrito.items():
            carrito_data[str(pid)] = {
                "cantidad": item["cantidad"],
                "precio": item["producto"]["precio"]
            }

        try:
            with open("carrito.json", "w") as f:
                json.dump(carrito_data, f)
        except Exception as e:
            print(f"Error al guardar carrito: {e}")

    def cargar_carrito(self):
        """Carga carrito desde JSON"""
        try:
            with open("carrito.json", "r") as f:
                carrito_data = json.load(f)
                for pid_str, item_data in carrito_data.items():
                    pid = int(pid_str)
                    producto = next((p for p in PRODUCTOS if p["id"] == pid), None)
                    if producto:
                        self.carrito[pid] = {
                            "producto": producto,
                            "cantidad": item_data["cantidad"]
                        }
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error al cargar carrito: {e}")

    def limpiar(self):
        """Limpia el carrito"""
        self.carrito = {}
        self.guardar_carrito()


class ProductoManager:
    """Gestiona productos y filtros"""

    @staticmethod
    def filtrar(texto, categoria):
        """Filtra productos por búsqueda y categoría"""
        texto = texto.lower()

        return [
            p for p in PRODUCTOS
            if (texto in p["nombre"].lower() or texto in p["descripcion"].lower())
               and (categoria == "Todas" or p["categoria"] == categoria)
        ]

    @staticmethod
    def obtener_categorias():
        """Obtiene lista de categorías únicas"""
        return list(set(p["categoria"] for p in PRODUCTOS))


class ValidadorEmail:
    """Valida y gestiona emails"""

    @staticmethod
    def validar(email):
        """Valida formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None


class WhatsAppManager:
    """Gestiona mensajes de WhatsApp"""

    @staticmethod
    def generar_mensaje(carrito, total):
        """Genera mensaje formateado para WhatsApp"""
        items_texto = ""
        for pid, item_data in carrito.items():
            producto = item_data["producto"]
            cantidad = item_data["cantidad"]
            subtotal = producto["precio"] * cantidad
            items_texto += f"\n{producto['emoji']} {producto['nombre']} x{cantidad} = ${subtotal:.2f}"

        mensaje = f"""Hola 👋, quiero hacer un pedido en FungiHouse 🍄

*Resumen del Pedido:*{items_texto}

*Total: ${total:.2f}*

¿Cuál es el proceso de pago?"""

        return mensaje

    @staticmethod
    def obtener_url_whatsapp(numero_whatsapp, mensaje):
        """Obtiene URL de WhatsApp para enviar mensaje"""
        import urllib.parse

        numero_limpio = numero_whatsapp.replace("+", "")

        # Codificar correctamente
        mensaje_codificado = urllib.parse.quote(mensaje)

        return f"https://wa.me/{numero_limpio}?text={mensaje_codificado}"

    @staticmethod
    def enviar_mensaje_pywhatkit(numero_whatsapp, mensaje):
        """Envía mensaje usando pywhatkit (alternativa)"""
        import pywhatkit as kit
        import time

        try:
            numero_limpio = numero_whatsapp.replace("+", "")
            # Envía el mensaje inmediatamente
            kit.sendwhatmsg_instantly(f"+{numero_limpio}", mensaje)
            return True
        except Exception as e:
            print(f"Error con pywhatkit: {e}")
            return False
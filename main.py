# main.py
import flet as ft
import webbrowser
from config import (
    PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, BG_DARK, BG_CARD,
    BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_ACCENT, BORDER_COLOR,
    PRODUCTOS, NUMERO_NEQUI
)
from logic import CarritoManager, ProductoManager, ValidadorEmail, WhatsAppManager
from views import (
    HeaderView, ProductoView, CarritoView, InicioView, InformativasView,
    ResponsiveView
)


class MicelioApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "MiCelio - Hongos Premium"
        self.page.window.maximized = True
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.on_resized = self.on_resized

        # Managers
        self.carrito_manager = CarritoManager()
        self.producto_manager = ProductoManager()
        self.validador = ValidadorEmail()
        self.whatsapp_manager = WhatsAppManager()

        # Número WhatsApp desde config
        self.numero_whatsapp = NUMERO_NEQUI

        # UI Components
        self.carrito_badge = HeaderView.crear_carrito_badge()
        self.main_content = ft.Column(expand=True, scroll="auto")
        self.newsletter_email = None
        self.productos_grid = None
        self.search_field = None
        self.filtro_categoria = None

        self.setup_ui()
        self.actualizar_contador_carrito()

    def setup_ui(self):
        """Configura la interfaz principal"""
        self.page.appbar = HeaderView.crear_appbar(
            self.ir_inicio, self.ir_tienda, self.ir_instrucciones,
            self.ir_blog, self.ir_carrito, self.carrito_badge
        )

        self.mostrar_inicio()

        self.page.add(
            ft.Container(
                content=self.main_content,
                expand=True,
                bgcolor=BG_DARK
            )
        )

    def mostrar_inicio(self):
        """Pantalla principal"""
        self.main_content.controls.clear()

        hero = InicioView.crear_hero(self.ir_tienda)
        beneficios = InicioView.crear_beneficios()
        testimonios = InicioView.crear_testimonios()
        self.newsletter_email, newsletter = InicioView.crear_newsletter(
            self.suscribirse_newsletter
        )
        footer = InicioView.crear_footer()

        self.main_content.controls = [
            hero,
            ft.Container(
                content=ft.Text("¿POR QUÉ ELEGIRNOS?", size=14, weight="bold", color=PRIMARY_COLOR),
                padding=ft.padding.symmetric(horizontal=20, vertical=20),
                bgcolor=BG_DARK,
            ),
            beneficios,
            ft.Container(height=20, bgcolor=BG_DARK),
            ft.Container(
                content=ft.Text("TESTIMONIOS", size=14, weight="bold", color=PRIMARY_COLOR),
                padding=ft.padding.symmetric(horizontal=20, vertical=20),
                bgcolor=BG_DARK,
            ),
            testimonios,
            ft.Container(height=20, bgcolor=BG_DARK),
            newsletter,
            footer,
        ]
        self.page.update()

    def ir_inicio(self, e):
        """Va a inicio"""
        self.mostrar_inicio()

    def ir_tienda(self, e):
        """Va a tienda con productos"""
        self.main_content.controls.clear()

        self.search_field = ft.TextField(
            label="Buscar productos...",
            prefix_icon=ft.Icons.SEARCH,
            bgcolor=BG_INPUT,
            border_color=PRIMARY_COLOR,
            color=TEXT_PRIMARY,
            label_style=ft.TextStyle(color=TEXT_SECONDARY),
            on_change=self.filtrar_productos,
        )

        categorias = self.producto_manager.obtener_categorias()
        self.filtro_categoria = ft.Dropdown(
            label="Categoría",
            options=[ft.dropdown.Option("Todas")] +
                    [ft.dropdown.Option(cat) for cat in categorias],
            bgcolor=BG_INPUT,
            border_color=PRIMARY_COLOR,
            color=TEXT_PRIMARY,
            label_style=ft.TextStyle(color=TEXT_SECONDARY),
            on_change=self.filtrar_productos,
            value="Todas",
        )

        header = ft.Container(
            content=ft.Column([
                ft.Text("Tienda", size=24, weight="bold", color=PRIMARY_COLOR),
                ft.Text("Nuestros productos premium", size=12, color=TEXT_SECONDARY),
                ft.Container(height=15),
                ft.Row([
                    self.search_field,
                    self.filtro_categoria,
                ], spacing=10),
            ]),
            padding=15,
            bgcolor=BG_CARD,
        )

        ancho = self.page.window.width
        runs_count = ResponsiveView.calcular_columnas(ancho)

        self.productos_grid = ft.GridView(
            runs_count=runs_count,
            spacing=12,
            run_spacing=12,
            child_aspect_ratio=0.75,
            padding=ft.padding.symmetric(horizontal=15),
            expand=True,
        )

        self.actualizar_grid()

        self.main_content.controls = [
            header,
            ft.Divider(height=1, color=BORDER_COLOR),
            self.productos_grid,
            ft.Container(height=20, bgcolor=BG_DARK),
        ]
        self.page.update()

    def filtrar_productos(self, e):
        """Filtra productos según búsqueda y categoría"""
        texto = self.search_field.value.lower()
        categoria = self.filtro_categoria.value

        productos_filtrados = self.producto_manager.filtrar(texto, categoria)

        self.productos_grid.controls.clear()
        for producto in productos_filtrados:
            self.productos_grid.controls.append(
                ProductoView.crear_card_producto(
                    producto,
                    lambda e, p=producto: self.agregar_carrito(p),
                    lambda e, p=producto: self.ver_detalle(p),
                )
            )

        self.page.update()

    def actualizar_grid(self):
        """Actualiza el grid con todos los productos"""
        self.productos_grid.controls.clear()
        for producto in PRODUCTOS:
            self.productos_grid.controls.append(
                ProductoView.crear_card_producto(
                    producto,
                    lambda e, p=producto: self.agregar_carrito(p),
                    lambda e, p=producto: self.ver_detalle(p),
                )
            )

    def agregar_carrito(self, producto):
        """Agrega producto al carrito"""
        self.carrito_manager.agregar(producto)
        self.actualizar_contador_carrito()

        snack = ft.SnackBar(
            ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=TEXT_PRIMARY, size=20),
                ft.Text(f"✓ {producto['nombre']} agregado", color=TEXT_PRIMARY, size=12),
            ], spacing=10),
            bgcolor=SUCCESS_COLOR,
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def ver_detalle(self, producto):
        """Ve detalle del producto"""
        self.main_content.controls.clear()
        detalle = ProductoView.crear_detalle_producto(
            producto,
            lambda e, p=producto: self.agregar_carrito(p),
            self.ir_tienda,
        )
        self.main_content.controls = [detalle]
        self.page.update()

    def ir_carrito(self, e):
        """Va al carrito"""
        self.main_content.controls.clear()

        if not self.carrito_manager.carrito:
            vacio = ft.Container(
                content=ft.Column([
                    ft.Text("Carrito", size=20, weight="bold", color=PRIMARY_COLOR),
                    ft.Container(height=40),
                    ft.Text("🛒", size=60),
                    ft.Text("Tu carrito está vacío", size=16, weight="bold", color=TEXT_ACCENT),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Ir a Tienda",
                        width=200,
                        height=45,
                        bgcolor=PRIMARY_COLOR,
                        color=TEXT_PRIMARY,
                        on_click=self.ir_tienda,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=20,
                bgcolor=BG_CARD,
                expand=True,
            )
            self.main_content.controls = [vacio]
        else:
            header = ft.Container(
                content=ft.Text("Carrito", size=20, weight="bold", color=PRIMARY_COLOR),
                padding=15,
                bgcolor=BG_CARD,
            )

            items_list = ft.Column()
            total = 0

            for producto_id, item_data in self.carrito_manager.carrito.items():
                producto = item_data["producto"]
                cantidad = item_data["cantidad"]
                subtotal = producto["precio"] * cantidad
                total += subtotal

                item_card = CarritoView.crear_item_carrito(
                    producto, cantidad, subtotal,
                    lambda e, pid=producto_id: self.cambiar_cantidad(pid, -1),
                    lambda e, pid=producto_id: self.eliminar_carrito(pid),
                )
                items_list.controls.append(item_card)

            resumen = CarritoView.crear_resumen_carrito(total)

            boton_comprar = ft.Container(
                content=ft.ElevatedButton(
                    "Enviar Pedido por WhatsApp",
                    expand=True,
                    height=50,
                    bgcolor=PRIMARY_COLOR,
                    color=TEXT_PRIMARY,
                    on_click=self.enviar_whatsapp,
                ),
                alignment=ft.alignment.center,
                padding=15,
                margin=ft.margin.symmetric(horizontal=15),
            )

            self.main_content.controls = [
                header,
                ft.Divider(height=1, color=BORDER_COLOR),
                ft.Container(
                    content=ft.Text("Productos", size=12, weight="bold", color=TEXT_SECONDARY),
                    padding=ft.padding.symmetric(horizontal=15),
                ),
                items_list,
                resumen,
                boton_comprar,
                ft.Container(height=20, bgcolor=BG_DARK),
            ]

        self.page.update()

    def cambiar_cantidad(self, producto_id, cambio):
        """Cambia la cantidad de un producto"""
        self.carrito_manager.cambiar_cantidad(producto_id, cambio)
        self.actualizar_contador_carrito()
        self.ir_carrito(None)

    def eliminar_carrito(self, producto_id):
        """Elimina producto del carrito"""
        self.carrito_manager.eliminar(producto_id)
        self.actualizar_contador_carrito()
        self.ir_carrito(None)

    def enviar_whatsapp(self, e):
        """Envía el pedido por WhatsApp - Simple y garantizado"""
        try:
            total = self.carrito_manager.obtener_total()

            # Generar mensaje
            mensaje = self.whatsapp_manager.generar_mensaje(
                self.carrito_manager.carrito,
                total
            )

            # Obtener URL de WhatsApp Web
            url_whatsapp = self.whatsapp_manager.obtener_url_whatsapp(
                self.numero_whatsapp,
                mensaje
            )

            numero_limpio = self.numero_whatsapp.replace("+", "").replace(" ", "")
            url_app = f"whatsapp://send?phone={numero_limpio}"

            import platform
            import subprocess
            import webbrowser
            import time

            sistema = platform.system()

            # PLAN A: Intenta abrir la app nativa
            try:
                if sistema == "Windows":
                    subprocess.Popen(f'start {url_app}', shell=True)
                elif sistema == "Darwin":
                    subprocess.Popen(['open', url_app])
                elif sistema == "Linux":
                    subprocess.Popen(['xdg-open', url_app])
            except:
                pass  # Si falla, continúa

            # PLAN B: Siempre abre WhatsApp Web también (garantizado)
            time.sleep(1)  # Pequeña pausa
            webbrowser.open(url_whatsapp)

            self.mostrar_snackbar(
                "✓ Abriendo WhatsApp (app o web)",
                SUCCESS_COLOR
            )

            # Limpiar carrito
            self.carrito_manager.limpiar()
            self.actualizar_contador_carrito()

            # Volver a inicio
            self.mostrar_inicio()

        except Exception as error:
            self.mostrar_snackbar(f"Error: {str(error)}", SECONDARY_COLOR)

    def ir_instrucciones(self, e):
        """Va a instrucciones"""
        self.main_content.controls.clear()
        contenido = InformativasView.crear_instrucciones(self.ir_inicio)
        self.main_content.controls = [contenido]
        self.page.update()

    def ir_blog(self, e):
        """Va a blog"""
        self.main_content.controls.clear()
        contenido = InformativasView.crear_blog(self.ir_inicio)
        self.main_content.controls = [contenido]
        self.page.update()

    def suscribirse_newsletter(self, e):
        """Maneja la suscripción al newsletter"""
        email = self.newsletter_email.value

        if not email:
            self.mostrar_snackbar("Por favor ingresa un email", SECONDARY_COLOR)
            return

        if not self.validador.validar(email):
            self.mostrar_snackbar("Email inválido", SECONDARY_COLOR)
            return

        self.mostrar_snackbar(f"¡Suscrito! Confirmación enviada a {email}", SUCCESS_COLOR)
        self.newsletter_email.value = ""
        self.page.update()

    def actualizar_contador_carrito(self):
        """Actualiza el contador del carrito en el AppBar"""
        total_items = self.carrito_manager.obtener_cantidad_items()

        self.carrito_badge.content.value = str(total_items) if total_items > 0 else ""
        self.page.update()

    def mostrar_snackbar(self, mensaje, color):
        """Muestra un snackbar con mensaje"""
        snack = ft.SnackBar(
            ft.Row([
                ft.Icon(ft.Icons.INFO, color=TEXT_PRIMARY, size=20),
                ft.Text(mensaje, color=TEXT_PRIMARY, size=12),
            ], spacing=10),
            bgcolor=color,
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def on_resized(self, e):
        """Maneja el redimensionamiento de la ventana"""
        ancho = self.page.window.width
        runs_count = ResponsiveView.calcular_columnas(ancho)

        if hasattr(self, 'productos_grid') and self.productos_grid:
            self.productos_grid.runs_count = runs_count
            self.page.update()


def main(page: ft.Page):
    app = MicelioApp(page)


if __name__ == "__main__":
    ft.app(target=main)
    # Para ejecutar en web:
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)
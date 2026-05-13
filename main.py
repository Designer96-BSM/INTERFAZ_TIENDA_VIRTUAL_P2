# main.py
import flet as ft
import time
from config import (
    PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, BG_DARK, BG_CARD,
    BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_ACCENT, BORDER_COLOR,
    PRODUCTOS, NUMERO_NEQUI, DELAY_SNACKBAR, DELAY_WHATSAPP,
    ESPACIO_CONTENEDOR, ESPACIO_PEQUEÑO, GRID_CHILD_ASPECT_RATIO,
    TIMEOUT_WHATSAPP
)
from logic import CarritoManager, ProductoManager, ValidadorEmail, WhatsAppManager
from views import (
    HeaderView, ProductoView, CarritoView, InicioView, InformativasView,
    ResponsiveView
)


class FungiHouseApp:
    """
    Aplicación principal de FungiHouse - E-commerce de hongos.
    Gestiona navegación, carrito, pagos y UI.
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "FungiHouse"
        self.page.window.maximized = True
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.on_resized = self.on_resized

        # ============ MANAGERS ============
        self.carrito_manager = CarritoManager()
        self.producto_manager = ProductoManager()
        self.validador = ValidadorEmail()
        self.whatsapp_manager = WhatsAppManager()

        # ============ CONFIGURACIÓN ============
        self.numero_whatsapp = NUMERO_NEQUI
        self.dialogo_abierto = False  # Bandera para evitar diálogos duplicados

        # ============ UI COMPONENTS ============
        self.carrito_badge = HeaderView.crear_carrito_badge()
        self.main_content = ft.Column(expand=True, scroll="auto")
        self.newsletter_email = None
        self.productos_grid = None
        self.search_field = None
        self.filtro_categoria = None

        # ============ CACHE ============
        self.categorias_cache = None

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

    # ============ NAVEGACIÓN ============

    def mostrar_inicio(self):
        """Pantalla principal - Hero, beneficios, testimonios, newsletter"""
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
                padding=ft.padding.symmetric(horizontal=ESPACIO_PEQUEÑO, vertical=ESPACIO_CONTENEDOR),
                bgcolor=BG_DARK,
            ),
            beneficios,
            ft.Container(height=ESPACIO_CONTENEDOR, bgcolor=BG_DARK),
            ft.Container(
                content=ft.Text("TESTIMONIOS", size=14, weight="bold", color=PRIMARY_COLOR),
                padding=ft.padding.symmetric(horizontal=ESPACIO_PEQUEÑO, vertical=ESPACIO_CONTENEDOR),
                bgcolor=BG_DARK,
            ),
            testimonios,
            ft.Container(height=ESPACIO_CONTENEDOR, bgcolor=BG_DARK),
            newsletter,
            footer,
        ]
        self.page.update()

    def ir_inicio(self, e):
        """Navega a inicio"""
        self.mostrar_inicio()

    def ir_tienda(self, e):
        """Navega a tienda con filtros de búsqueda y categoría"""
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

        # MEJORA 7: Cachear categorías
        if not self.categorias_cache:
            self.categorias_cache = self.producto_manager.obtener_categorias()

        self.filtro_categoria = ft.Dropdown(
            label="Categoría",
            options=[ft.dropdown.Option("Todas")] +
                    [ft.dropdown.Option(cat) for cat in self.categorias_cache],
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
            padding=ESPACIO_PEQUEÑO,
            bgcolor=BG_CARD,
        )

        ancho = self.page.window.width
        runs_count = ResponsiveView.calcular_columnas(ancho)

        self.productos_grid = ft.GridView(
            runs_count=runs_count,
            spacing=12,
            run_spacing=12,
            child_aspect_ratio=GRID_CHILD_ASPECT_RATIO,
            padding=ft.padding.symmetric(horizontal=ESPACIO_PEQUEÑO),
            expand=True,
        )

        self.actualizar_grid()

        self.main_content.controls = [
            header,
            ft.Divider(height=1, color=BORDER_COLOR),
            self.productos_grid,
            ft.Container(height=ESPACIO_CONTENEDOR, bgcolor=BG_DARK),
        ]
        self.page.update()

    def filtrar_productos(self, e):
        """
        Filtra productos según búsqueda y categoría.
        MEJORA 6: Feedback visual cuando no hay resultados
        """
        texto = self.search_field.value.lower()
        categoria = self.filtro_categoria.value

        productos_filtrados = self.producto_manager.filtrar(texto, categoria)

        self.productos_grid.controls.clear()

        # MEJORA 6: Mostrar mensaje si no hay resultados
        if not productos_filtrados:
            self.productos_grid.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay productos que coincidan con tu búsqueda",
                        color=TEXT_SECONDARY,
                        size=14,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ESPACIO_CONTENEDOR,
                )
            )
        else:
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
        """
        Agrega producto al carrito y muestra feedback visual.
        """
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
        """Ve el detalle completo de un producto"""
        self.main_content.controls.clear()
        detalle = ProductoView.crear_detalle_producto(
            producto,
            lambda e, p=producto: self.agregar_carrito(p),
            self.ir_tienda,
        )
        self.main_content.controls = [detalle]
        self.page.update()

    def ir_carrito(self, e):
        """Navega a la vista del carrito"""
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
                padding=ESPACIO_PEQUEÑO,
                bgcolor=BG_CARD,
                expand=True,
            )
            self.main_content.controls = [vacio]
        else:
            header = ft.Container(
                content=ft.Text("Carrito", size=20, weight="bold", color=PRIMARY_COLOR),
                padding=ESPACIO_PEQUEÑO,
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

            # MEJORA 5: Botón que pide confirmación antes de enviar
            # ✅ DESPUÉS - Con icono y color verde
            boton_comprar = ft.Container(
                content=ft.ElevatedButton(
                    "Enviar por WhatsApp",
                    expand=True,
                    height=50,
                    bgcolor="#25D366",  # Color oficial WhatsApp
                    color=TEXT_PRIMARY,
                    icon=ft.Icons.SEND,
                    icon_color=TEXT_PRIMARY,
                    on_click=self.confirmar_envio_pedido,
                ),
                alignment=ft.alignment.center,
                padding=ESPACIO_PEQUEÑO,
                margin=ft.margin.symmetric(horizontal=ESPACIO_PEQUEÑO),
            )

            self.main_content.controls = [
                header,
                ft.Divider(height=1, color=BORDER_COLOR),
                ft.Container(
                    content=ft.Text("Productos", size=12, weight="bold", color=TEXT_SECONDARY),
                    padding=ft.padding.symmetric(horizontal=ESPACIO_PEQUEÑO),
                ),
                items_list,
                resumen,
                boton_comprar,
                ft.Container(height=ESPACIO_CONTENEDOR, bgcolor=BG_DARK),
            ]

        self.page.update()

    def cambiar_cantidad(self, producto_id, cambio):
        """
        Cambia la cantidad de un producto en el carrito.

        Args:
            producto_id (str): ID del producto
            cambio (int): Incremento/decremento (-1, +1)
        """
        self.carrito_manager.cambiar_cantidad(producto_id, cambio)
        self.actualizar_contador_carrito()
        self.ir_carrito(None)

    def eliminar_carrito(self, producto_id):
        """
        Elimina un producto del carrito.

        Args:
            producto_id (str): ID del producto a eliminar
        """
        self.carrito_manager.eliminar(producto_id)
        self.actualizar_contador_carrito()
        self.ir_carrito(None)

    # ============ PAGOS Y CONFIRMACIÓN ============

    def confirmar_envio_pedido(self, e):
        """
        MEJORA 5: Pide confirmación antes de enviar el pedido.
        Muestra total y opciones de confirmar/cancelar.
        """
        if self.dialogo_abierto:
            return

        total = self.carrito_manager.obtener_total()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Pedido", size=18, weight="bold"),
            content=ft.Column([
                ft.Text(f"Total: ${total:,.0f}", size=16, color=PRIMARY_COLOR, weight="bold"),
                ft.Container(height=10),
                ft.Text("¿Deseas continuar con el envío?", size=12, color=TEXT_SECONDARY),
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                ft.TextButton(
                    "Enviar",
                    on_click=self.enviar_whatsapp,
                    style=ft.ButtonStyle(color=SUCCESS_COLOR),
                ),
            ],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.dialogo_abierto = True
        self.page.update()

    def cerrar_dialogo(self, e=None):
        """Cierra el diálogo actual"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.dialogo_abierto = False
            self.page.update()

    def enviar_whatsapp(self, e):
        """
        Envía el pedido por WhatsApp con manejo robusto de errores.
        MEJORA 1: Valida antes de enviar
        MEJORA 2: Manejo de errores mejorado
        MEJORA 4: Indicador de carga
        """
        self.cerrar_dialogo()

        # MEJORA 1: Validar carrito antes de enviar
        if not self.validar_carrito_antes_envio():
            return

        # MEJORA 4: Mostrar diálogo de carga
        dlg_carga = ft.AlertDialog(
            title=ft.Text("Abriendo WhatsApp..."),
            content=ft.Column([
                ft.ProgressRing(width=50, height=50),
                ft.Container(height=10),
                ft.Text("Por favor espera", size=12, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )

        self.page.dialog = dlg_carga
        dlg_carga.open = True
        self.page.update()

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

            sistema = platform.system()
            app_abierta = False

            print(f"[DEBUG] Sistema: {sistema}")
            print(f"[DEBUG] Intentando abrir WhatsApp...")

            # PLAN A: Intenta con pywhatkit
            try:
                import pywhatkit as kit
                print("[DEBUG] Intentando con pywhatkit...")
                kit.sendwhatmsg_instantly(f"+{numero_limpio}", mensaje, wait_time=2)
                app_abierta = True
                print("[DEBUG] ✅ pywhatkit funcionó")
            except Exception as error_pywhatkit:
                print(f"[DEBUG] pywhatkit falló: {error_pywhatkit}")
                app_abierta = False

            # PLAN B: Si pywhatkit falla, intenta app nativa
            if not app_abierta:
                try:
                    print("[DEBUG] Intentando con app nativa...")
                    if sistema == "Windows":
                        subprocess.Popen(f'start {url_app}', shell=True)
                        app_abierta = True
                        print("[DEBUG] ✅ App nativa abierta (Windows)")
                    elif sistema == "Darwin":
                        subprocess.Popen(['open', url_app])
                        app_abierta = True
                        print("[DEBUG] ✅ App nativa abierta (macOS)")
                    elif sistema == "Linux":
                        subprocess.Popen(['xdg-open', url_app])
                        app_abierta = True
                        print("[DEBUG] ✅ App nativa abierta (Linux)")
                except Exception as error_app:
                    print(f"[DEBUG] App nativa falló: {error_app}")
                    app_abierta = False

            # PLAN C: Si todo falla, abre WhatsApp Web
            if not app_abierta:
                print("[DEBUG] Abriendo Plan C: WhatsApp Web")
                webbrowser.open(url_whatsapp)
                time.sleep(DELAY_WHATSAPP)
                self.mostrar_snackbar(
                    "✓ Abriendo WhatsApp Web en el navegador",
                    SUCCESS_COLOR
                )
            else:
                self.mostrar_snackbar(
                    "✓ Abriendo WhatsApp",
                    SUCCESS_COLOR
                )

            # MEJORA 2: Solo limpiar carrito si todo va bien
            self.carrito_manager.limpiar()
            self.actualizar_contador_carrito()

            # Cerrar diálogo de carga
            dlg_carga.open = False
            self.page.update()

            # Volver a inicio después de un tiempo
            time.sleep(DELAY_SNACKBAR)
            self.mostrar_inicio()

        except Exception as error:
            print(f"[DEBUG] Error general: {error}")

            # MEJORA 2: Cerrar diálogo de carga y mostrar error
            dlg_carga.open = False
            self.page.update()

            self.mostrar_snackbar(
                f"❌ Error: {str(error)}",
                SECONDARY_COLOR
            )

    def validar_carrito_antes_envio(self) -> bool:
        """
        MEJORA 1: Valida que el carrito sea enviable.

        Returns:
            bool: True si es válido, False si hay problemas
        """
        if not self.carrito_manager.carrito:
            self.mostrar_snackbar("Carrito vacío", SECONDARY_COLOR)
            return False

        total = self.carrito_manager.obtener_total()
        if total <= 0:
            self.mostrar_snackbar("Total inválido", SECONDARY_COLOR)
            return False

        return True

    # ============ OTRAS SECCIONES ============

    def ir_instrucciones(self, e):
        """Navega a instrucciones"""
        self.main_content.controls.clear()
        contenido = InformativasView.crear_instrucciones(self.ir_inicio)
        self.main_content.controls = [contenido]
        self.page.update()

    def ir_blog(self, e):
        """Navega a blog"""
        self.main_content.controls.clear()
        contenido = InformativasView.crear_blog(self.ir_inicio)
        self.main_content.controls = [contenido]
        self.page.update()

    def suscribirse_newsletter(self, e):
        """
        Maneja la suscripción al newsletter con validación.
        """
        email = self.newsletter_email.value

        if not email:
            self.mostrar_snackbar("Por favor ingresa un email", SECONDARY_COLOR)
            return

        if not self.validador.validar(email):
            self.mostrar_snackbar("Email inválido", SECONDARY_COLOR)
            return

        self.mostrar_snackbar(
            f"¡Suscrito! Confirmación enviada a {email}",
            SUCCESS_COLOR
        )
        self.newsletter_email.value = ""
        self.page.update()

    # ============ UI UTILITIES ============

    def actualizar_contador_carrito(self):
        """
        Actualiza el contador del carrito en el AppBar.
        MEJORA 3: Manejo más robusto
        """
        try:
            total_items = self.carrito_manager.obtener_cantidad_items()
            self.carrito_badge.content.value = str(total_items) if total_items > 0 else ""
            self.page.update()
        except Exception as error:
            print(f"[DEBUG] Error al actualizar contador: {error}")

    def mostrar_snackbar(self, mensaje, color):
        """
        Muestra un snackbar con mensaje y color.

        Args:
            mensaje (str): Texto a mostrar
            color (str): Color de fondo (hex)
        """
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
        """
        Maneja el redimensionamiento de la ventana.
        MEJORA 3: Validación más robusta
        """
        try:
            ancho = self.page.window.width
            runs_count = ResponsiveView.calcular_columnas(ancho)

            if (self.productos_grid and
                    hasattr(self.productos_grid, 'runs_count')):
                self.productos_grid.runs_count = runs_count
                self.page.update()
        except Exception as error:
            print(f"[DEBUG] Error en on_resized: {error}")


def main(page: ft.Page):
    """Punto de entrada de la aplicación"""
    app = FungiHouseApp(page)


if __name__ == "__main__":
    # Para ejecutar en escritorio:
     ft.app(target=main)

    # Para ejecutar en web:
    #ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
# views.py
import flet as ft
import os
from config import (
    PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, BG_DARK, BG_CARD,
    BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_ACCENT, BORDER_COLOR,
    get_logo_path, get_titulo_path, get_gif_path, BENEFICIOS, TESTIMONIOS
)


class ResponsiveView:
    """Componentes responsivos y cálculos de diseño"""

    @staticmethod
    def calcular_columnas(ancho):
        """Calcula cantidad de columnas según ancho de pantalla"""
        if ancho < 600:
            return 2
        elif ancho < 900:
            return 3
        elif ancho < 1200:
            return 4
        else:
            return 5


class HeaderView:
    """Componentes del header/AppBar"""

    @staticmethod
    def crear_appbar(on_ir_inicio, on_ir_tienda, on_ir_instrucciones,
                     on_ir_blog, on_ir_carrito, carrito_badge):
        """Crea el AppBar principal con iconos + texto en botones"""
        nav_buttons = ft.Row([
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.HOME, size=18, color=PRIMARY_COLOR),
                    ft.Text("Inicio", size=12, color=PRIMARY_COLOR),
                ], spacing=5),
                on_click=on_ir_inicio,
            ),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.SHOPPING_BAG, size=18, color=PRIMARY_COLOR),
                    ft.Text("Tienda", size=12, color=PRIMARY_COLOR),
                ], spacing=5),
                on_click=on_ir_tienda,
            ),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.HELP, size=18, color=PRIMARY_COLOR),
                    ft.Text("Instrucciones", size=12, color=PRIMARY_COLOR),
                ], spacing=5),
                on_click=on_ir_instrucciones,
            ),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.ARTICLE, size=18, color=PRIMARY_COLOR),
                    ft.Text("Blog", size=12, color=PRIMARY_COLOR),
                ], spacing=5),
                on_click=on_ir_blog,
            ),
        ], spacing=15, scale=1.0)

        logo_path = get_logo_path()
        titulo_path = get_titulo_path()

        logo = ft.Image(
            src=logo_path,
            width=50,
            height=50,
            fit="contain",
        ) if os.path.exists(logo_path) else ft.Text("🍄", size=32)

        titulo_img = ft.Image(
            src=titulo_path,
            height=50,
            fit="contain",
        ) if os.path.exists(titulo_path) else ft.Text(
            "FungiHouse", weight="bold", size=22, color=PRIMARY_COLOR
        )

        return ft.AppBar(
            title=ft.Row([
                logo,
                titulo_img,
                ft.Container(expand=True),
                nav_buttons,
                ft.Container(expand=True),
            ], spacing=2, expand=True),
            bgcolor=BG_DARK,
            elevation=0,
            actions=[
                ft.Stack([
                    ft.IconButton(
                        ft.Icons.SHOPPING_CART,
                        icon_color=PRIMARY_COLOR,
                        on_click=on_ir_carrito,
                    ),
                    carrito_badge,
                ], alignment=ft.alignment.top_right),
                ft.IconButton(
                    ft.Icons.ACCOUNT_CIRCLE,
                    icon_color=PRIMARY_COLOR,
                ),
            ]
        )

    @staticmethod
    def crear_carrito_badge():
        """Crea el badge del carrito"""
        return ft.Container(
            content=ft.Text(
                "",
                size=12,
                weight="bold",
                color=TEXT_PRIMARY,
                text_align="center",
            ),
            width=22,
            height=22,
            bgcolor=SECONDARY_COLOR,
            border_radius=12,
            alignment=ft.alignment.center,
        )


class ProductoView:
    """Componentes para productos"""

    @staticmethod
    def crear_card_producto(producto, on_agregar, on_ver_detalle):
        """Crea tarjeta de producto"""
        card = ft.Container(
            content=ft.Column([
                ft.Text(producto["emoji"], size=50),
                ft.Text(
                    producto["nombre"],
                    size=12,
                    weight="bold",
                    color=PRIMARY_COLOR,
                    max_lines=2,
                    text_align="center",
                ),
                ft.Text(
                    producto["descripcion"],
                    size=10,
                    color=TEXT_SECONDARY,
                    max_lines=2,
                    text_align="center",
                ),
                ft.Container(height=8),
                ft.Text(
                    f"${producto['precio']}",
                    size=16,
                    weight="bold",
                    color=PRIMARY_COLOR,
                ),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Agregar",
                    expand=True,
                    height=35,
                    bgcolor=PRIMARY_COLOR,
                    color=TEXT_PRIMARY,
                    on_click=on_agregar,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=15,
            bgcolor=BG_CARD,
            border_radius=12,
            border=ft.border.all(1, PRIMARY_COLOR),
            on_click=on_ver_detalle,
        )
        return card

    @staticmethod
    def crear_detalle_producto(producto, on_agregar, on_volver):
        """Crea vista de detalle de producto"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Detalle", size=20, weight="bold", color=PRIMARY_COLOR),
                ft.Container(height=20),
                ft.Text(producto["emoji"], size=80),
                ft.Container(height=20),
                ft.Text(producto["nombre"], size=20, weight="bold", color=PRIMARY_COLOR),
                ft.Text(producto["categoria"], size=12, color=TEXT_SECONDARY),
                ft.Container(height=15),
                ft.Text(producto["descripcion"], size=13, color=TEXT_ACCENT),
                ft.Container(height=20),
                ft.Text(
                    f"${producto['precio']}",
                    size=28,
                    weight="bold",
                    color=PRIMARY_COLOR,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Agregar al Carrito",
                    expand=True,
                    height=50,
                    bgcolor=PRIMARY_COLOR,
                    color=TEXT_PRIMARY,
                    on_click=on_agregar,
                ),
                ft.Container(height=20),
                ft.TextButton(
                    "← Volver a Tienda",
                    style=ft.ButtonStyle(color=PRIMARY_COLOR),
                    on_click=on_volver,
                ),
            ], padding=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            bgcolor=BG_CARD,
            expand=True,
        )


class CarritoView:
    """Componentes para el carrito"""

    @staticmethod
    def crear_item_carrito(producto, cantidad, subtotal, on_cambiar, on_eliminar):
        """Crea item del carrito"""
        return ft.Container(
            content=ft.Row([
                ft.Text(producto["emoji"], size=30),
                ft.Column([
                    ft.Text(producto["nombre"], size=12, weight="bold", color=PRIMARY_COLOR),
                    ft.Text(f"${producto['precio']} c/u", size=11, color=TEXT_SECONDARY),
                ], expand=True),
                ft.Row([
                    ft.IconButton(
                        ft.Icons.REMOVE,
                        icon_size=16,
                        icon_color=PRIMARY_COLOR,
                        on_click=lambda e: on_cambiar(-1),
                    ),
                    ft.Text(str(cantidad), size=12, weight="bold", color=PRIMARY_COLOR, width=30),
                    ft.IconButton(
                        ft.Icons.ADD,
                        icon_size=16,
                        icon_color=PRIMARY_COLOR,
                        on_click=lambda e: on_cambiar(1),
                    ),
                ], spacing=5),
                ft.Text(f"${subtotal:.2f}", size=12, weight="bold", color=PRIMARY_COLOR, width=60),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    icon_size=18,
                    icon_color=SECONDARY_COLOR,
                    on_click=on_eliminar,
                ),
            ], spacing=10),
            padding=12,
            bgcolor=BG_INPUT,
            border_radius=10,
            border=ft.border.all(1, PRIMARY_COLOR),
            margin=ft.margin.symmetric(horizontal=15, vertical=5),
        )

    @staticmethod
    def crear_resumen_carrito(total):
        """Crea resumen del carrito"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Subtotal:", weight="bold", size=12, color=TEXT_ACCENT),
                    ft.Text(f"${total:.2f}", weight="bold", size=12, color=PRIMARY_COLOR),
                ]),
                ft.Row([
                    ft.Text("Envío:", weight="bold", size=12, color=TEXT_ACCENT),
                    ft.Text("Gratis", color=SUCCESS_COLOR, weight="bold", size=12),
                ]),
                ft.Divider(height=10, color=BORDER_COLOR),
                ft.Row([
                    ft.Text("Total:", size=14, weight="bold", color=PRIMARY_COLOR),
                    ft.Text(f"${total:.2f}", size=16, weight="bold", color=PRIMARY_COLOR),
                ]),
            ], spacing=8),
            padding=15,
            bgcolor=BG_INPUT,
            border_radius=10,
            border=ft.border.all(1, PRIMARY_COLOR),
            margin=ft.margin.symmetric(horizontal=15, vertical=15),
        )


class InicioView:
    """Componentes para la página de inicio"""

    @staticmethod
    def crear_hero(on_explorar):
        """Crea sección hero"""
        gif_path = get_gif_path()
        gif_existe = os.path.exists(gif_path)

        if gif_existe:
            return ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(
                            src=gif_path,
                            fit="cover",
                            height=470,
                            width=1100,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Explorar Tienda",
                            width=220,
                            height=50,
                            bgcolor=PRIMARY_COLOR,
                            color=TEXT_PRIMARY,
                            on_click=on_explorar,
                        ),
                        padding=20,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ], spacing=0, expand=True),
                expand=True,
                padding=0,
                alignment=ft.alignment.center,
                border_radius=0,
                bgcolor=BG_DARK,
            )
        else:
            return ft.Container(
                content=ft.Column([
                    ft.Text("🍄", size=100),
                    ft.Container(height=40),
                    ft.ElevatedButton(
                        "Explorar Tienda",
                        width=220,
                        height=50,
                        bgcolor=PRIMARY_COLOR,
                        color=TEXT_PRIMARY,
                        on_click=on_explorar,
                    ),
                    ft.Container(height=80),
                ], alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                height=350,
                padding=0,
                border_radius=0,
                bgcolor=BG_DARK,
            )

    @staticmethod
    def crear_beneficios():
        """Crea sección de beneficios"""
        columna_izq = ft.Column(expand=True, spacing=12)
        columna_der = ft.Column(expand=True, spacing=12)

        for idx, beneficio in enumerate(BENEFICIOS):
            card = ft.Container(
                content=ft.Row([
                    ft.Text(beneficio["icon"], size=35),
                    ft.Column([
                        ft.Text(beneficio["titulo"], size=12, weight="bold", color=PRIMARY_COLOR),
                        ft.Text(beneficio["descripcion"], size=10, color=TEXT_SECONDARY),
                    ], spacing=2, expand=True),
                ], spacing=15),
                padding=15,
                bgcolor=BG_INPUT,
                border_radius=10,
                border=ft.border.all(2, BORDER_COLOR),
                margin=ft.margin.symmetric(horizontal=10),
            )

            if idx % 2 == 0:
                columna_izq.controls.append(card)
            else:
                columna_der.controls.append(card)

        return ft.Container(
            content=ft.Row([columna_izq, columna_der], expand=True, spacing=10),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            bgcolor=BG_DARK,
        )

    @staticmethod
    def crear_testimonios():
        """Crea sección de testimonios"""
        testimonios_column = ft.Column()
        for testimonio in TESTIMONIOS:
            card = ft.Container(
                content=ft.Column([
                    ft.Text(testimonio["rating"], size=12),
                    ft.Text(f'"{testimonio["texto"]}"', size=11, color=TEXT_ACCENT, italic=True),
                    ft.Container(height=8),
                    ft.Text(testimonio["autor"], size=10, weight="bold", color=PRIMARY_COLOR),
                ], spacing=3),
                padding=15,
                bgcolor=BG_CARD,
                border_radius=10,
                border=ft.border.all(1, PRIMARY_COLOR),
                margin=ft.margin.symmetric(horizontal=15, vertical=8),
            )
            testimonios_column.controls.append(card)

        return testimonios_column

    @staticmethod
    def crear_newsletter(on_suscribirse):
        """Crea sección newsletter"""
        email_field = ft.TextField(
            label="Tu correo",
            bgcolor=BG_INPUT,
            border_color=PRIMARY_COLOR,
            color=TEXT_PRIMARY,
            label_style=ft.TextStyle(color=TEXT_SECONDARY),
            expand=True,
        )

        newsletter = ft.Container(
            content=ft.Column([
                ft.Text("Suscríbete a Nuestro Newsletter", size=16, weight="bold", color=PRIMARY_COLOR),
                ft.Text("Recibe ofertas exclusivas y consejos", size=12, color=TEXT_SECONDARY),
                ft.Container(height=15),
                email_field,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Suscribirse",
                    expand=True,
                    height=40,
                    bgcolor=PRIMARY_COLOR,
                    color=TEXT_PRIMARY,
                    on_click=on_suscribirse,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=30,
            bgcolor=BG_CARD,
            border_radius=0,
            border=ft.border.all(1, PRIMARY_COLOR),
        )

        return email_field, newsletter

    @staticmethod
    def crear_footer():
        """Crea footer"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.TextButton("Facebook", style=ft.ButtonStyle(color=PRIMARY_COLOR)),
                    ft.TextButton("Instagram", style=ft.ButtonStyle(color=PRIMARY_COLOR)),
                    ft.TextButton("Twitter", style=ft.ButtonStyle(color=PRIMARY_COLOR)),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True),
                ft.Divider(height=15, color=BORDER_COLOR),
                ft.Text(
                    "© 2025 FungiHouse - Todos los derechos reservados",
                    size=10,
                    color=TEXT_SECONDARY,
                    text_align="center",
                ),
                ft.Container(height=15),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=20,
            bgcolor=BG_CARD,
        )


class InformativasView:
    """Componentes para páginas informativas (Blog, Instrucciones)"""

    @staticmethod
    def crear_instrucciones(on_volver):
        """Crea página de instrucciones"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Instrucciones", size=20, weight="bold", color=PRIMARY_COLOR),
                ft.Container(height=20),
                ft.Text("📖", size=60),
                ft.Text("Guía de Uso", size=18, weight="bold", color=PRIMARY_COLOR),
                ft.Container(height=20),
                ft.Text("Instrucciones de cultivo y preparación", size=12, color=TEXT_SECONDARY),
                ft.Container(height=40),
                ft.Column([
                    ft.Text("1. Preparación del Sustrato", size=14, weight="bold", color=PRIMARY_COLOR),
                    ft.Text("Mezcla el sustrato con los hongos en proporción 1:10", size=11, color=TEXT_ACCENT),
                    ft.Container(height=15),
                    ft.Text("2. Incubación", size=14, weight="bold", color=PRIMARY_COLOR),
                    ft.Text("Mantén a temperatura de 20-25°C durante 3-4 semanas", size=11, color=TEXT_ACCENT),
                    ft.Container(height=15),
                    ft.Text("3. Fructificación", size=14, weight="bold", color=PRIMARY_COLOR),
                    ft.Text("Aumenta la humedad al 85-95% y reduce la temperatura", size=11, color=TEXT_ACCENT),
                    ft.Container(height=15),
                    ft.Text("4. Cosecha", size=14, weight="bold", color=PRIMARY_COLOR),
                    ft.Text("Cosecha cuando los hongos alcancen tamaño óptimo", size=11, color=TEXT_ACCENT),
                ], spacing=5),
                ft.Container(height=30),
                ft.TextButton(
                    "← Volver",
                    style=ft.ButtonStyle(color=PRIMARY_COLOR),
                    on_click=on_volver,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=20,
            bgcolor=BG_CARD,
            expand=True,
        )

    @staticmethod
    def crear_blog(on_volver):
        """Crea página de blog"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Blog", size=20, weight="bold", color=PRIMARY_COLOR),
                ft.Container(height=20),
                ft.Text("📝", size=60),
                ft.Container(height=20),
                ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Beneficios de los Hongos Medicinales", size=14, weight="bold",
                                    color=PRIMARY_COLOR),
                            ft.Text("Descubre cómo los hongos pueden mejorar tu salud", size=11, color=TEXT_ACCENT),
                            ft.Container(height=10),
                            ft.Text(
                                "Los hongos medicinales han sido utilizados durante miles de años en la medicina tradicional china. Contienen compuestos bioactivos que fortalecen el sistema inmunológico.",
                                size=10, color=TEXT_SECONDARY),
                        ], spacing=5),
                        padding=15,
                        bgcolor=BG_INPUT,
                        border_radius=10,
                        border=ft.border.all(1, PRIMARY_COLOR),
                        margin=ft.margin.symmetric(horizontal=15, vertical=10),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Guía de Cultivo en Casa", size=14, weight="bold", color=PRIMARY_COLOR),
                            ft.Text("Aprende a cultivar hongos frescos en tu hogar", size=11, color=TEXT_ACCENT),
                            ft.Container(height=10),
                            ft.Text(
                                "Cultivar hongos en casa es más fácil de lo que crees. Con nuestro kit completo y siguiendo nuestras instrucciones, tendrás hongos frescos en 4-6 semanas.",
                                size=10, color=TEXT_SECONDARY),
                        ], spacing=5),
                        padding=15,
                        bgcolor=BG_INPUT,
                        border_radius=10,
                        border=ft.border.all(1, PRIMARY_COLOR),
                        margin=ft.margin.symmetric(horizontal=15, vertical=10),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Recetas con Hongos", size=14, weight="bold", color=PRIMARY_COLOR),
                            ft.Text("Deliciosas recetas para aprovechar tus hongos", size=11, color=TEXT_ACCENT),
                            ft.Container(height=10),
                            ft.Text(
                                "Desde setas salteadas hasta hongos rellenos, descubre cómo preparar platillos gourmet con nuestros productos premium.",
                                size=10, color=TEXT_SECONDARY),
                        ], spacing=5),
                        padding=15,
                        bgcolor=BG_INPUT,
                        border_radius=10,
                        border=ft.border.all(1, PRIMARY_COLOR),
                        margin=ft.margin.symmetric(horizontal=15, vertical=10),
                    ),
                ], spacing=5),
                ft.Container(height=20),
                ft.TextButton(
                    "← Volver",
                    style=ft.ButtonStyle(color=PRIMARY_COLOR),
                    on_click=on_volver,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=20,
            bgcolor=BG_CARD,
            expand=True,
        )
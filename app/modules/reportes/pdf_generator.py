import os
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepTogether,
    Image,
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF


# ──────────────────────────────────────────────
#  PALETA  —  Joyería El Illimani (Estilo Formal: Azul Marino, Slate, Gris)
# ──────────────────────────────────────────────
BRAND_400   = colors.HexColor("#1e3a8a")   # azul marino principal
BRAND_100   = colors.HexColor("#eff6ff")   # azul muy claro
BRAND_900   = colors.HexColor("#1e293b")   # pizarra oscuro

SLATE_0     = colors.HexColor("#ffffff")
SLATE_50    = colors.HexColor("#f8fafc")
SLATE_100   = colors.HexColor("#f1f5f9")
SLATE_200   = colors.HexColor("#e2e8f0")
SLATE_500   = colors.HexColor("#64748b")
SLATE_700   = colors.HexColor("#334155")
SLATE_900   = colors.HexColor("#0f172a")

# Colores formales de estado (sin usar verde ni amarillo/ámbar)
STATE_INFO_BG   = colors.HexColor("#f1f5f9") # Fondo neutral
STATE_INFO_TXT  = colors.HexColor("#475569") # Texto neutral oscuro (para valores normales/positivos)

RED_500     = colors.HexColor("#9f3a3a")   # rojo sobrio (alerta)
RED_100     = colors.HexColor("#fee2e2")
RED_900     = colors.HexColor("#450a0a")

# Reemplazo de ámbar/amarillo por azul/pizarra formal
AMBER_500   = colors.HexColor("#475569")   # Gris pizarra formal
AMBER_100   = colors.HexColor("#f1f5f9")



# ──────────────────────────────────────────────
#  REGISTRO DE FUENTES DE MARCA
#  (DM Sans para cuerpo, Cormorant Garamond para títulos)
#  Con fallback automático a Helvetica/Times si no
#  se encuentran los archivos TTF.
# ──────────────────────────────────────────────
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "fonts")

FONT_REGULAR = "Helvetica"
FONT_BOLD    = "Helvetica-Bold"
FONT_TITLE   = "Helvetica-Bold"

_font_files = {
    "DMSans":            "DMSans-Regular.ttf",
    "DMSans-Bold":       "DMSans-Bold.ttf",
    "Cormorant":         "CormorantGaramond-SemiBold.ttf",
    "Cormorant-Bold":    "CormorantGaramond-Bold.ttf",
}

try:
    for font_name, file_name in _font_files.items():
        path = os.path.join(_FONT_DIR, file_name)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(font_name, path))

    if "DMSans" in pdfmetrics.getRegisteredFontNames():
        FONT_REGULAR = "DMSans"
    if "DMSans-Bold" in pdfmetrics.getRegisteredFontNames():
        FONT_BOLD = "DMSans-Bold"
    if "Cormorant-Bold" in pdfmetrics.getRegisteredFontNames():
        FONT_TITLE = "Cormorant-Bold"
    elif "Cormorant" in pdfmetrics.getRegisteredFontNames():
        FONT_TITLE = "Cormorant"
except Exception:
    # Si algo falla en el registro, seguimos con Helvetica sin romper la app
    pass


# Ruta opcional del logo real de la joyería (PNG con fondo transparente)
_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img", "logo_illimani.png")


# ──────────────────────────────────────────────
#  ESTILOS DE PÁRRAFO  reutilizables
# ──────────────────────────────────────────────
def _estilos():
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow",
            fontName=FONT_BOLD,
            fontSize=7,
            textColor=BRAND_400,
            spaceAfter=2,
            leading=10,
            tracking=1.2,
        ),
        "titulo": ParagraphStyle(
            "titulo",
            fontName=FONT_TITLE,
            fontSize=21,
            textColor=INK_900,
            spaceAfter=2,
            leading=24,
        ),
        "subtitulo": ParagraphStyle(
            "subtitulo",
            fontName=FONT_REGULAR,
            fontSize=9,
            textColor=SLATE_500,
            spaceAfter=0,
            leading=13,
        ),
        "meta_label": ParagraphStyle(
            "meta_label",
            fontName=FONT_BOLD,
            fontSize=7.5,
            textColor=SLATE_500,
            leading=11,
            alignment=TA_RIGHT,
        ),
        "meta_value": ParagraphStyle(
            "meta_value",
            fontName=FONT_REGULAR,
            fontSize=7.5,
            textColor=SLATE_700,
            leading=11,
            alignment=TA_RIGHT,
        ),
        "chip": ParagraphStyle(
            "chip",
            fontName=FONT_BOLD,
            fontSize=7.5,
            textColor=BRAND_900,
            alignment=TA_CENTER,
            leading=10,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            fontName=FONT_BOLD,
            fontSize=8,
            textColor=SLATE_0,
            spaceAfter=4,
            leading=12,
        ),
        "total_label": ParagraphStyle(
            "total_label",
            fontName=FONT_BOLD,
            fontSize=10,
            textColor=SLATE_700,
        ),
        "total_value": ParagraphStyle(
            "total_value",
            fontName=FONT_BOLD,
            fontSize=13,
            textColor=BRAND_900,
            alignment=TA_RIGHT,
            wordWrap="CJK",
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName=FONT_REGULAR,
            fontSize=7,
            textColor=SLATE_500,
            alignment=TA_CENTER,
        ),
        "cell_main": ParagraphStyle(
            "cell_main",
            fontName=FONT_BOLD,
            fontSize=8,
            textColor=INK_900,
            leading=11,
        ),
        "cell_sub": ParagraphStyle(
            "cell_sub",
            fontName=FONT_REGULAR,
            fontSize=7,
            textColor=SLATE_500,
            leading=10,
        ),
        "cell_normal": ParagraphStyle(
            "cell_normal",
            fontName=FONT_REGULAR,
            fontSize=8,
            textColor=SLATE_700,
            leading=11,
        ),
        "cell_number": ParagraphStyle(
            "cell_number",
            fontName=FONT_REGULAR,
            fontSize=8,
            textColor=SLATE_700,
            alignment=TA_RIGHT,
            leading=11,
        ),
        "cell_code": ParagraphStyle(
            "cell_code",
            fontName=FONT_REGULAR,
            fontSize=7.5,
            textColor=SLATE_500,
            leading=10,
        ),
        # KPI cards
        "kpi_label": ParagraphStyle(
            "kpi_label",
            fontName=FONT_BOLD,
            fontSize=7,
            textColor=SLATE_500,
            leading=10,
        ),
        "kpi_value": ParagraphStyle(
            "kpi_value",
            fontName=FONT_TITLE,
            fontSize=14,
            textColor=INK_900,
            leading=17,
        ),
        "kpi_value_green": ParagraphStyle(
            "kpi_value_green",
            fontName=FONT_TITLE,
            fontSize=14,
            textColor=BRAND_400,
            leading=17,
        ),
        "kpi_value_red": ParagraphStyle(
            "kpi_value_red",
            fontName=FONT_TITLE,
            fontSize=14,
            textColor=colors.HexColor("#9f3a3a"),
            leading=17,
        ),
    }


# ──────────────────────────────────────────────
#  CANVAS NUMERADO  ("Página X de Y")
# ──────────────────────────────────────────────
class _NumberedCanvas(pdf_canvas.Canvas):
    """Canvas que permite imprimir 'Página X de Y' en el pie de página.

    Funciona en dos pasadas: durante el build se guarda el estado de
    cada página, y al finalizar (save) se conoce el total de páginas
    y se reescribe el pie en cada una.
    """

    def __init__(self, *args, **kwargs):
        pdf_canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(num_pages)
            pdf_canvas.Canvas.showPage(self)
        pdf_canvas.Canvas.save(self)

    def _draw_footer(self, total_pages):
        W, H = letter
        self.saveState()
        self.setFillColor(INK_900)
        self.rect(0, 0, W, 9 * mm, fill=1, stroke=0)
        self.setFillColor(BRAND_400)
        self.rect(0, 8.6 * mm, W, 0.4 * mm, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#d7dde4"))
        self.setFont(FONT_REGULAR, 7)
        self.drawCentredString(
            W / 2,
            3.2 * mm,
            f"Sistema de Gestion - Joyeria El Illimani  ·  "
            f"Documento generado automaticamente  ·  "
            f"Página {self._pageNumber} de {total_pages}"
        )
        self.restoreState()


# ──────────────────────────────────────────────
#  PLANTILLA DE PÁGINA (cabecera + watermark)
# ──────────────────────────────────────────────
def _page_template(canvas, doc):
    """Barra superior formal y marca de agua sutil. El pie de página
    se dibuja por _NumberedCanvas para poder calcular el total."""
    canvas.saveState()
    W, H = letter

    canvas.setFillColor(INK_900)
    canvas.rect(0, H - 12 * mm, W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(BRAND_400)
    canvas.rect(0, H - 12 * mm, W, 1.2 * mm, fill=1, stroke=0)

    # marca de agua sutil con el logo (si existe)
    if os.path.exists(_LOGO_PATH):
        try:
            canvas.saveState()
            canvas.setFillAlpha(0.04)
            size = 110 * mm
            canvas.drawImage(
                _LOGO_PATH,
                (W - size) / 2,
                (H - size) / 2,
                width=size,
                height=size,
                preserveAspectRatio=True,
                mask='auto',
            )
            canvas.restoreState()
        except Exception:
            pass

    canvas.restoreState()


# ──────────────────────────────────────────────
#  BLOQUE DE ENCABEZADO
# ──────────────────────────────────────────────
def _logo_flowable():
    """Devuelve el logo real si existe; si no, un sello formal con sigla."""
    if os.path.exists(_LOGO_PATH):
        try:
            img = Image(_LOGO_PATH, width=24 * mm, height=24 * mm)
            img.hAlign = "LEFT"
            return img
        except Exception:
            pass

    logo_drawing = Drawing(28 * mm, 18 * mm)
    logo_drawing.add(Rect(0, 0, 28 * mm, 18 * mm, fillColor=INK_900, strokeColor=BRAND_400, strokeWidth=1))
    logo_drawing.add(String(14 * mm, 6.2 * mm, "EI", fontName=FONT_BOLD, fontSize=13,
                             fillColor=BRAND_400, textAnchor="middle"))
    return logo_drawing


def _periodo_chip(elementos, texto, estilos):
    """Pequeño badge con el período/filtro del reporte."""
    data = [[Paragraph(texto, estilos["chip"])]]
    t = Table(data, colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), BRAND_100),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [6]),
        ("BOX",           (0, 0), (-1, -1), 0.6, colors.HexColor("#dfc28c")),
    ]))
    return t


def _header_block(elementos, titulo_texto, subtitulo_texto, meta_pairs, estilos, chip_texto=None):
    """
    Bloque de encabezado de reporte:
    logo | título + subtítulo (+ chip de período) | metadatos (Generado / Usuario)
    """
    titulo_col = [
        Paragraph("JOYERÍA EL ILLIMANI", estilos["eyebrow"]),
        Paragraph(titulo_texto, estilos["titulo"]),
        Paragraph(subtitulo_texto, estilos["subtitulo"]),
    ]
    if chip_texto:
        titulo_col.append(Spacer(1, 2 * mm))
        titulo_col.append(_periodo_chip(elementos, chip_texto, estilos))

    meta_content = []
    for label, value in meta_pairs:
        meta_content.append(Paragraph(f'<b>{label}</b>', estilos["meta_label"]))
        meta_content.append(Paragraph(value, estilos["meta_value"]))

    header_data = [[
        _logo_flowable(),
        titulo_col,
        meta_content,
    ]]

    header_table = Table(header_data, colWidths=[32 * mm, 105 * mm, 45 * mm])
    header_table.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("LEFTPADDING",  (2, 0), (2, 0), 4),
        ("RIGHTPADDING", (2, 0), (2, 0), 0),
        ("ALIGN",        (2, 0), (2, 0), "RIGHT"),
        ("VALIGN",       (2, 0), (2, 0), "TOP"),
    ]))

    elementos.append(header_table)
    elementos.append(Spacer(1, 4 * mm))
    elementos.append(HRFlowable(width="100%", thickness=1.4, color=BRAND_400, spaceAfter=4 * mm))


# ──────────────────────────────────────────────
#  TARJETAS KPI (resumen ejecutivo)
# ──────────────────────────────────────────────
def _kpi_cards(elementos, items, estilos):
    """
    items: lista de tuplas (label, value_str, color) donde color es
    'default' | 'green' | 'red'
    Dibuja una fila de tarjetas estilo dashboard.
    """
    style_map = {
        "default": estilos["kpi_value"],
        "green": estilos["kpi_value_green"],
        "red": estilos["kpi_value_red"],
    }

    cards = []
    for label, value, color in items:
        accent = {
            "default": BRAND_400,
            "green": STATE_INFO_TXT,
            "red": RED_500,
        }.get(color, BRAND_400)
        card_data = [
            [Paragraph(label.upper(), estilos["kpi_label"])],
            [Paragraph(value, style_map.get(color, estilos["kpi_value"]))],
        ]
        card = Table(card_data, colWidths=[(182 / max(len(items), 1)) * mm - 3])
        card.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), SLATE_50),
            ("BOX",           (0, 0), (-1, -1), 0.6, SLATE_200),
            ("LINEABOVE",     (0, 0), (-1, 0), 2.2, accent),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [4]),
        ]))
        cards.append(card)

    spacer_w = 3 * mm
    row = []
    col_widths = []
    for i, c in enumerate(cards):
        row.append(c)
        col_widths.append((182 / len(cards)) * mm - spacer_w)
        if i < len(cards) - 1:
            row.append(None)

    # Tabla contenedora simple: una fila, columnas de igual ancho con separación
    outer = Table([cards], colWidths=[(182 / len(cards)) * mm] * len(cards))
    outer.setStyle(TableStyle([
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.5 * mm),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
    ]))

    elementos.append(outer)
    elementos.append(Spacer(1, 5 * mm))


def _total_block(elementos, label, value, estilos):
    """Bloque de total al final del reporte."""
    data = [[
        Paragraph(label, estilos["total_label"]),
        Paragraph(value, estilos["total_value"]),
    ]]
    t = Table(data, colWidths=[105 * mm, 77 * mm])
    t.setStyle(TableStyle([
        ("ALIGN",        (0, 0), (0, 0), "LEFT"),
        ("ALIGN",        (1, 0), (1, 0), "RIGHT"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND",   (0, 0), (-1, -1), BRAND_100),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("LINEABOVE",    (0, 0), (-1, 0), 1.8, BRAND_400),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.HexColor("#dfc28c")),
        ("ROUNDEDCORNERS", [4]),
    ]))
    elementos.append(Spacer(1, 4 * mm))
    elementos.append(t)


# ══════════════════════════════════════════════
#  CLASE PRINCIPAL
# ══════════════════════════════════════════════
class PDFGenerator:

    # ──────────────────────────────────────────
    #  REPORTE DE VENTAS
    # ──────────────────────────────────────────
    @staticmethod
    def reporte_ventas(ventas, total_ventas, usuario="Sistema", periodo_texto=None):

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=18 * mm,
            bottomMargin=14 * mm,
        )

        estilos = _estilos()
        elementos = []
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")

        _header_block(
            elementos,
            "Reporte de Ventas",
            "Detalle de transacciones registradas en el período.",
            [("Generado:", ahora), ("Usuario:", usuario)],
            estilos,
            chip_texto=periodo_texto,
        )

        # ── KPI cards ──────────────────────────
        n_ventas = len(ventas)
        promedio = (total_ventas / n_ventas) if n_ventas else 0
        _kpi_cards(elementos, [
            ("Total del período", f"Bs. {total_ventas:,.2f}", "green"),
            ("N° de ventas", f"{n_ventas}", "default"),
            ("Ticket promedio", f"Bs. {promedio:,.2f}", "default"),
        ], estilos)

        # encabezado tabla
        data = [[
            Paragraph("N°",       estilos["section_title"]),
            Paragraph("Fecha",    estilos["section_title"]),
            Paragraph("Cliente",  estilos["section_title"]),
            Paragraph("Vendedor", estilos["section_title"]),
            Paragraph("Total",    estilos["section_title"]),
        ]]

        for venta in ventas:
            cliente = venta.cliente.nombre if venta.cliente else "Consumidor Final"
            data.append([
                Paragraph(str(venta.id_venta), estilos["cell_code"]),
                Paragraph(venta.fecha_venta.strftime("%d/%m/%Y"), estilos["cell_normal"]),
                Paragraph(cliente, estilos["cell_main"]),
                Paragraph(venta.usuario.nombre_usuario, estilos["cell_normal"]),
                Paragraph(f"Bs. {venta.total_venta:,.2f}", estilos["cell_number"]),
            ])

        col_w = [18 * mm, 28 * mm, 60 * mm, 42 * mm, 34 * mm]
        tabla = Table(data, colWidths=col_w, repeatRows=1)
        tabla.setStyle(_estilo_tabla_base(len(data)))
        elementos.append(tabla)

        _total_block(
            elementos,
            "Total de ventas del período",
            f"Bs. {total_ventas:,.2f}",
            estilos,
        )

        doc.build(elementos, onFirstPage=_page_template, onLaterPages=_page_template, canvasmaker=_NumberedCanvas)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    # ──────────────────────────────────────────
    #  REPORTE DE INVENTARIO VALORIZADO
    # ──────────────────────────────────────────
    @staticmethod
    def reporte_inventario(joyas, total_inventario, usuario="Sistema"):

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=18 * mm,
            bottomMargin=14 * mm,
        )

        estilos = _estilos()
        elementos = []
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")

        _header_block(
            elementos,
            "Inventario Valorizado",
            "Valor económico actual del stock registrado en el sistema.",
            [("Generado:", ahora), ("Usuario:", usuario)],
            estilos,
        )

        # ── KPI cards ──────────────────────────
        joyas_bajas_count = sum(1 for j in joyas if j.stock_actual <= j.stock_minimo)
        _kpi_cards(elementos, [
            ("Valor total del inventario", f"Bs. {total_inventario:,.2f}", "green"),
            ("Productos en catálogo", f"{len(joyas)}", "default"),
            ("Alertas de stock mínimo", f"{joyas_bajas_count}", "red" if joyas_bajas_count else "default"),
        ], estilos)

        # ── Tabla principal ──────────────────
        data = [[
            Paragraph("Código",        estilos["section_title"]),
            Paragraph("Producto",      estilos["section_title"]),
            Paragraph("Categoría",     estilos["section_title"]),
            Paragraph("Material",      estilos["section_title"]),
            Paragraph("Stock",         estilos["section_title"]),
            Paragraph("P. Compra",     estilos["section_title"]),
            Paragraph("Valor Total",   estilos["section_title"]),
        ]]

        for joya in joyas:
            stock_bajo = joya.stock_actual <= joya.stock_minimo

            stock_style = ParagraphStyle(
                "stock_cell",
                fontName=FONT_BOLD,
                fontSize=8,
                textColor=RED_500 if stock_bajo else GREEN_500,
                alignment=TA_CENTER,
            )
            valor_style = ParagraphStyle(
                "valor_cell",
                fontName=FONT_BOLD,
                fontSize=8,
                textColor=GREEN_500,
                alignment=TA_RIGHT,
            )

            data.append([
                Paragraph(joya.codigo, estilos["cell_code"]),
                Paragraph(joya.nombre, estilos["cell_main"]),
                Paragraph(joya.categoria.nombre_categoria, estilos["cell_normal"]),
                Paragraph(joya.material.nombre_material, estilos["cell_normal"]),
                Paragraph(str(joya.stock_actual), stock_style),
                Paragraph(f"Bs. {joya.precio_compra:,.2f}", estilos["cell_number"]),
                Paragraph(f"Bs. {joya.valor_en_stock:,.2f}", valor_style),
            ])

        col_w = [18 * mm, 52 * mm, 28 * mm, 28 * mm, 14 * mm, 24 * mm, 24 * mm]
        tabla = Table(data, colWidths=col_w, repeatRows=1)
        tabla.setStyle(_estilo_tabla_inventario(len(data), joyas))
        elementos.append(tabla)

        _total_block(
            elementos,
            "Valor total del inventario",
            f"Bs. {total_inventario:,.2f}",
            estilos,
        )

        elementos.append(Spacer(1, 6 * mm))

        # ── Sección alertas ──────────────────
        joyas_bajas = [j for j in joyas if j.stock_actual <= j.stock_minimo]
        if joyas_bajas:
            elementos.append(KeepTogether(_seccion_alertas(joyas_bajas, estilos)))

        doc.build(elementos, onFirstPage=_page_template, onLaterPages=_page_template, canvasmaker=_NumberedCanvas)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    # ──────────────────────────────────────────
    #  REPORTE DE RENTABILIDAD
    # ──────────────────────────────────────────
    @staticmethod
    def reporte_rentabilidad(datos, utilidad_total, categoria, usuario="Sistema", periodo_texto=None):

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=18 * mm,
            bottomMargin=14 * mm,
        )

        estilos = _estilos()
        elementos = []
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")

        _header_block(
            elementos,
            "Reporte de Rentabilidad",
            f"Margen de utilidad por producto — Categoría: {categoria.nombre_categoria}",
            [("Generado:", ahora), ("Usuario:", usuario)],
            estilos,
            chip_texto=periodo_texto,
        )

        # ── KPI cards ──────────────────────────
        venta_total = sum(item["venta_total"] for item in datos) if datos else 0
        margen_global = (utilidad_total / venta_total * 100) if venta_total > 0 else 0
        _kpi_cards(elementos, [
            ("Utilidad total", f"Bs. {utilidad_total:,.2f}", "green"),
            ("Ventas totales", f"Bs. {venta_total:,.2f}", "default"),
            ("Margen global", f"{margen_global:.1f}%", "green" if margen_global >= 20 else "default"),
        ], estilos)

        data = [[
            Paragraph("Joya",         estilos["section_title"]),
            Paragraph("Cantidad",     estilos["section_title"]),
            Paragraph("Costo Total",  estilos["section_title"]),
            Paragraph("Venta Total",  estilos["section_title"]),
            Paragraph("Utilidad",     estilos["section_title"]),
            Paragraph("Margen %",     estilos["section_title"]),
        ]]

        for item in datos:
            margen = (
                (item["utilidad"] / item["venta_total"] * 100)
                if item["venta_total"] > 0 else 0
            )
            margen_color = GREEN_500 if margen >= 20 else AMBER_500
            margen_style = ParagraphStyle(
                "margen_cell",
                fontName=FONT_BOLD,
                fontSize=8,
                textColor=margen_color,
                alignment=TA_RIGHT,
            )
            data.append([
                Paragraph(item["joya"].nombre, estilos["cell_main"]),
                Paragraph(str(item["cantidad"]), estilos["cell_number"]),
                Paragraph(f"Bs. {item['costo_total']:,.2f}", estilos["cell_number"]),
                Paragraph(f"Bs. {item['venta_total']:,.2f}", estilos["cell_number"]),
                Paragraph(f"Bs. {item['utilidad']:,.2f}", estilos["cell_number"]),
                Paragraph(f"{margen:.1f}%", margen_style),
            ])

        col_w = [60 * mm, 18 * mm, 30 * mm, 30 * mm, 30 * mm, 20 * mm]
        tabla = Table(data, colWidths=col_w, repeatRows=1)
        tabla.setStyle(_estilo_tabla_base(len(data)))
        elementos.append(tabla)

        _total_block(
            elementos,
            "Utilidad total del período",
            f"Bs. {utilidad_total:,.2f}",
            estilos,
        )

        doc.build(elementos, onFirstPage=_page_template, onLaterPages=_page_template, canvasmaker=_NumberedCanvas)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


# ──────────────────────────────────────────────
#  HELPERS DE ESTILOS DE TABLA
# ──────────────────────────────────────────────

def _estilo_tabla_base(n_rows):
    """Estilo base compartido por ventas y rentabilidad."""
    style = [
        # encabezado
        ("BACKGROUND",    (0, 0), (-1, 0), INK_800),
        ("TEXTCOLOR",     (0, 0), (-1, 0), SLATE_0),
        ("FONTNAME",      (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE",      (0, 0), (-1, 0), 7.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING",    (0, 0), (-1, 0), 6),
        ("LINEBELOW",     (0, 0), (-1, 0), 1.2, BRAND_400),

        # filas
        ("FONTNAME",      (0, 1), (-1, -1), FONT_REGULAR),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("TOPPADDING",    (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [SLATE_0, colors.HexColor("#fbfcfd")]),
        ("LINEBELOW",     (0, 1), (-1, -1), 0.35, SLATE_200),
    ]
    return TableStyle(style)


def _estilo_tabla_inventario(n_rows, joyas):
    """Estilo para inventario, resalta filas con stock bajo."""
    base = [
        ("BACKGROUND",    (0, 0), (-1, 0), INK_800),
        ("TEXTCOLOR",     (0, 0), (-1, 0), SLATE_0),
        ("FONTNAME",      (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE",      (0, 0), (-1, 0), 7.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING",    (0, 0), (-1, 0), 6),
        ("LINEBELOW",     (0, 0), (-1, 0), 1.2, BRAND_400),

        ("FONTNAME",      (0, 1), (-1, -1), FONT_REGULAR),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("TOPPADDING",    (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW",     (0, 1), (-1, -1), 0.35, SLATE_200),
        ("ALIGN",         (4, 0), (4, -1), "CENTER"),
        ("ALIGN",         (5, 0), (6, -1), "RIGHT"),
    ]

    # alternar filas y resaltar stock bajo
    for i, joya in enumerate(joyas):
        row = i + 1
        if joya.stock_actual <= joya.stock_minimo:
            base.append(("BACKGROUND", (0, row), (-1, row), RED_100))
        elif row % 2 == 0:
            base.append(("BACKGROUND", (0, row), (-1, row), colors.HexColor("#fbfcfd")))
        else:
            base.append(("BACKGROUND", (0, row), (-1, row), SLATE_0))

    return TableStyle(base)


def _seccion_alertas(joyas_bajas, estilos):
    """Bloque de alertas de stock mínimo."""
    bloque = []

    # título sección
    titulo_data = [[Paragraph("ALERTAS DE STOCK MINIMO", ParagraphStyle(
        "alert_title",
        fontName=FONT_BOLD,
        fontSize=9,
        textColor=RED_900,
    ))]]
    titulo_t = Table(titulo_data, colWidths=[182 * mm])
    titulo_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), RED_100),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("LINEBELOW",     (0, 0), (-1, 0), 1.2, RED_500),
        ("BOX",           (0, 0), (-1, -1), 0.4, colors.HexColor("#e5b9b9")),
    ]))
    bloque.append(titulo_t)
    bloque.append(Spacer(1, 2 * mm))

    # tabla alertas
    data = [[
        Paragraph("Código",        estilos["section_title"]),
        Paragraph("Producto",      estilos["section_title"]),
        Paragraph("Stock actual",  estilos["section_title"]),
        Paragraph("Stock mínimo",  estilos["section_title"]),
        Paragraph("Diferencia",    estilos["section_title"]),
    ]]

    for joya in joyas_bajas:
        diff = joya.stock_actual - joya.stock_minimo
        diff_style = ParagraphStyle(
            "diff",
            fontName=FONT_BOLD,
            fontSize=8,
            textColor=RED_500 if diff < 0 else AMBER_500,
            alignment=TA_RIGHT,
        )
        data.append([
            Paragraph(joya.codigo,  estilos["cell_code"]),
            Paragraph(joya.nombre,  estilos["cell_main"]),
            Paragraph(str(joya.stock_actual),  estilos["cell_number"]),
            Paragraph(str(joya.stock_minimo),  estilos["cell_number"]),
            Paragraph(str(diff),               diff_style),
        ])

    col_w = [20 * mm, 82 * mm, 28 * mm, 28 * mm, 24 * mm]
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), INK_800),
        ("TEXTCOLOR",     (0, 0), (-1, 0), SLATE_0),
        ("LINEBELOW",     (0, 0), (-1, 0), 0.8, BRAND_400),
        ("FONTNAME",      (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE",      (0, 0), (-1, 0), 7.5),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [SLATE_0, colors.HexColor("#fbfcfd")]),
        ("LINEBELOW",     (0, 1), (-1, -1), 0.3, SLATE_200),
        ("ALIGN",         (2, 0), (4, -1), "RIGHT"),
    ]))
    bloque.append(t)
    return bloque

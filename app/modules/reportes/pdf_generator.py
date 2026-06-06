from io import BytesIO

from reportlab.lib import colors

from reportlab.lib.pagesizes import letter

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    @staticmethod
    def reporte_ventas(ventas, total_ventas):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter
        )

        styles = getSampleStyleSheet()

        elementos = []

        titulo = Paragraph(
            "Reporte de Ventas",
            styles["Title"]
        )

        elementos.append(titulo)

        elementos.append(Spacer(1, 12))

        data = [
            [
                "N°",
                "Fecha",
                "Cliente",
                "Vendedor",
                "Total"
            ]
        ]

        for venta in ventas:

            cliente = (
                venta.cliente.nombre
                if venta.cliente
                else "Consumidor Final"
            )

            data.append(
                [
                    str(venta.id_venta),
                    venta.fecha_venta.strftime("%d/%m/%Y"),
                    cliente,
                    venta.usuario.nombre_usuario,
                    f"Bs. {venta.total_venta}"
                ]
            )

        tabla = Table(data)

        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
                ]
            )
        )

        elementos.append(tabla)

        elementos.append(Spacer(1, 20))

        elementos.append(
            Paragraph(
                f"Total Ventas: Bs. {total_ventas}",
                styles["Heading2"]
            )
        )

        doc.build(elementos)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf
    

    @staticmethod
    def reporte_inventario(joyas, total_inventario):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter
        )

        styles = getSampleStyleSheet()

        elementos = []

        elementos.append(
            Paragraph(
                "Reporte de Inventario Valorizado",
                styles["Title"]
            )
        )

        elementos.append(Spacer(1, 12))

        data = [
            [
                "Codigo",
                "Joya",
                "Categoria",
                "Material",
                "Stock",
                "P. Compra",
                "Valor"
            ]
        ]

        for joya in joyas:

            data.append(
                [
                    joya.codigo,
                    joya.nombre,
                    joya.categoria.nombre_categoria,
                    joya.material.nombre_material,
                    str(joya.stock_actual),
                    f"{joya.precio_compra}",
                    f"{joya.valor_en_stock}"
                ]
            )

        tabla = Table(data)

        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
                ]
            )
        )

        elementos.append(tabla)

        elementos.append(Spacer(1, 20))

        elementos.append(
            Paragraph(
                f"Valor Total Inventario: Bs. {total_inventario}",
                styles["Heading2"]
            )
        )

        doc.build(elementos)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf
    

    @staticmethod
    def reporte_rentabilidad(datos, utilidad_total, categoria):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter
        )

        styles = getSampleStyleSheet()

        elementos = []

        elementos.append(
            Paragraph(
                "Reporte de Rentabilidad",
                styles["Title"]
            )
        )

        elementos.append(Spacer(1, 10))

        elementos.append(
            Paragraph(
                f"Categoria: {categoria.nombre_categoria}",
                styles["Heading2"]
            )
        )

        elementos.append(Spacer(1, 10))

        data = [
            [
                "Joya",
                "Cantidad",
                "Costo Total",
                "Venta Total",
                "Utilidad"
            ]
        ]

        for item in datos:

            data.append(
                [
                    item["joya"].nombre,
                    str(item["cantidad"]),
                    f"Bs. {item['costo_total']}",
                    f"Bs. {item['venta_total']}",
                    f"Bs. {item['utilidad']}"
                ]
            )

        tabla = Table(data)

        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
                ]
            )
        )

        elementos.append(tabla)

        elementos.append(Spacer(1, 20))

        elementos.append(
            Paragraph(
                f"Utilidad Total: Bs. {utilidad_total}",
                styles["Heading2"]
            )
        )

        doc.build(elementos)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf
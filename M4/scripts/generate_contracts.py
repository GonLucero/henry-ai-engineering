"""Genera seis imágenes de documentos ficticios, no contratos para uso real."""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "test_contracts"

ORIGINAL = """CONTRATO DE PRODUCCIÓN MUSICAL
Proyecto ficticio: EP Horizonte. Identificador: MUS-001.
Entre Estudio Río (productor) y Artista Horizonte (artista), se acuerda:

1. SERVICIO Y ENTREGABLES
El productor realizará la grabación, mezcla y mastering de tres canciones.
Entregará tres archivos WAV estéreo de 24 bits y 48 kHz, uno por canción.

2. HONORARIOS Y FORMA DE PAGO
El precio total es de ARS 300.000. El artista abonará el 50% al iniciar el
trabajo y el 50% restante al recibir los archivos finales.

3. PLAZO DE ENTREGA
La entrega se realizará dentro de los 30 días corridos desde la recepción
completa de las pistas y referencias del artista.

4. REVISIONES
Se incluyen dos rondas de correcciones de mezcla. El artista deberá solicitar
cada ronda dentro de los siete días corridos posteriores a recibir la mezcla.
Las revisiones no incluyen nuevas grabaciones.

5. TITULARIDAD Y USO DEL MATERIAL
El artista conserva la titularidad de las grabaciones finales. El productor
podrá publicar fragmentos de hasta 30 segundos en su portfolio únicamente
con autorización previa y escrita del artista.

6. CANCELACIÓN
Si el artista cancela antes de la entrega final, el productor retendrá el 20%
del precio total como cargo de cancelación y devolverá el excedente abonado.

Documento ficticio para pruebas académicas. No contiene firmas reales.
"""

SIMPLE = """ADENDA 1 - ACTUALIZACIÓN DE HONORARIOS
Referencia: contrato MUS-001, proyecto EP Horizonte.
Estudio Río y Artista Horizonte acuerdan modificar únicamente la cláusula 2.

2. HONORARIOS Y FORMA DE PAGO
Se sustituye la cláusula 2 por el siguiente texto: el precio total es de
ARS 360.000. El artista abonará el 50% al iniciar el trabajo y el 50% restante
al recibir los archivos finales.

Las demás cláusulas del contrato MUS-001 permanecen vigentes sin cambios.

Documento ficticio para pruebas académicas. No contiene firmas reales.
"""

COMPLEX = """ADENDA 2 - ACTUALIZACIÓN DEL PROYECTO
Referencia: contrato MUS-001, proyecto EP Horizonte.
Estudio Río y Artista Horizonte acuerdan los siguientes cambios.
Esta adenda es parcial y no reemplaza íntegramente el contrato original.

3. PLAZO DE ENTREGA
Se sustituye la cláusula 3: la entrega se realizará dentro de los 45 días
corridos desde la recepción completa de las pistas y referencias del artista.

4. REVISIONES
Se sustituye la cláusula 4: se incluyen tres rondas de correcciones de mezcla.
El artista deberá solicitar cada ronda dentro de los diez días corridos
posteriores a recibir la mezcla. No se incluyen nuevas grabaciones.

5. TITULARIDAD Y USO DEL MATERIAL
Se sustituye la cláusula 5: el artista conserva la titularidad de las
grabaciones finales. El productor no podrá publicar fragmentos ni utilizar
las grabaciones en su portfolio.

6. CANCELACIÓN
Se elimina expresamente la cláusula 6 del contrato original.
No se establece una cláusula de cancelación alternativa en esta adenda.

7. CONFIDENCIALIDAD
Se agrega la cláusula 7: ambas partes mantendrán la confidencialidad de las
pistas y mezclas no publicadas durante 12 meses desde la firma de esta adenda.

Las cláusulas 1 y 2 del contrato original permanecen vigentes sin cambios.

Documento ficticio para pruebas académicas. No contiene firmas reales.
"""


RENTAL_ORIGINAL = """CONTRATO DE ALQUILER DE EQUIPOS DE SONIDO
Documento ficticio. Identificador: ALQ-001.
Entre Sonido Río (arrendador) y Eventos Horizonte (arrendatario).

1. EQUIPOS
Se alquilan dos bafles activos, una consola de ocho canales, dos micrófonos
y sus cables. El inventario se revisará al retirar y devolver los equipos.

2. PRECIO Y PAGO
El precio total del alquiler es de ARS 80.000. Se abona el 50% al reservar
y el 50% restante al retirar los equipos.

3. RETIRO Y DEVOLUCIÓN
Los equipos se retiran el 10 de noviembre de 2026 a las 10:00 y deben
devolverse el 10 de noviembre de 2026 a las 18:00 en el local del arrendador.

4. ESTADO DE LOS EQUIPOS
El arrendatario devolverá los equipos con todos sus accesorios y sin daños,
salvo el desgaste normal del uso acordado.

5. USO AUTORIZADO
Los equipos se utilizarán en un evento privado. No se permite subalquilarlos.

Documento ficticio para pruebas académicas. No contiene firmas reales.
"""

RENTAL_AMENDMENT = """ADENDA AL CONTRATO DE ALQUILER ALQ-001
Entre Sonido Río y Eventos Horizonte.
Esta adenda modifica únicamente la devolución y agrega un depósito de garantía.

3. RETIRO Y DEVOLUCIÓN
La fecha de devolución se modifica al 11 de noviembre de 2026 a las 18:00.
El retiro sigue siendo el 10 de noviembre de 2026 a las 10:00.
El lugar de devolución permanece sin cambios.

6. DEPÓSITO DE GARANTÍA
Se agrega esta cláusula: el arrendatario entregará un depósito de ARS 40.000
al retirar los equipos. Se reintegrará íntegramente dentro de las 48 horas
posteriores a la devolución si no se registran faltantes ni daños.
El depósito es una garantía reembolsable y no integra el precio del alquiler.

Se ratifican sin modificaciones las cláusulas 1, 2, 4 y 5. El precio total
del alquiler continúa siendo ARS 80.000 con la misma forma de pago.

Documento ficticio para pruebas académicas. No contiene firmas reales.
"""


def load_font(size):
    for name in ("/System/Library/Fonts/Supplemental/Arial.ttf", "DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    raise RuntimeError("Instalá una fuente Arial o DejaVu Sans para regenerar las imágenes con acentos.")


def render_document(text, path):
    image = Image.new("RGB", (1240, 1754), "white")
    draw = ImageDraw.Draw(image)
    body = load_font(24)
    title = load_font(32)
    heading = load_font(25)
    y = 90
    for index, line in enumerate(text.splitlines()):
        font = title if index == 0 else heading if line[:1].isdigit() else body
        if not line.strip():
            y += 15
            continue
        words = line.split()
        wrapped = ""
        for word in words:
            candidate = (wrapped + " " + word).strip()
            if draw.textlength(candidate, font=font) > 1060:
                draw.text((90, y), wrapped, fill="black", font=font)
                y += 34
                wrapped = word
            else:
                wrapped = candidate
        draw.text((90, y), wrapped, fill="black", font=font)
        y += 39 if index == 0 else 34
    if y > 1650:
        raise ValueError("El documento no cabe en una página")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def main():
    for case, original, amendment in (("simple", ORIGINAL, SIMPLE), ("complejo", ORIGINAL, COMPLEX), ("alquiler_sonido", RENTAL_ORIGINAL, RENTAL_AMENDMENT)):
        folder = DATA / case
        folder.mkdir(parents=True, exist_ok=True)
        for name, text in (("original", original), ("adenda", amendment)):
            (folder / (name + ".txt")).write_text(text, encoding="utf-8")
            render_document(text, folder / (name + ".png"))
    expected = {
        "simple": {
            "sections": ["2"],
            "checks": [
                "El precio cambia de ARS 300.000 a ARS 360.000.",
                "La forma de pago 50%/50% no cambia.",
                "No se reportan otras cláusulas como modificadas o eliminadas.",
            ],
        },
        "complejo": {
            "sections": ["3", "4", "5", "6", "7"],
            "checks": [
                "Entrega: 30 a 45 días corridos; mismo punto de inicio.",
                "Revisiones: dos a tres rondas; solicitud de siete a diez días.",
                "Se mantiene que las revisiones no incluyen nuevas grabaciones.",
                "Se prohíbe el uso en portfolio que antes admitía fragmentos de hasta 30 segundos con autorización previa escrita.",
                "La titularidad permanece en el artista.",
                "Se elimina expresamente la cláusula 6; no se inventa un régimen de cancelación nuevo.",
                "Se agrega confidencialidad por 12 meses desde la firma de la adenda, para pistas y mezclas no publicadas.",
                "No cambian servicio, entregables, honorarios ni forma de pago.",
            ],
        },
    }
    expected["alquiler_sonido"] = {
        "sections": ["3", "6"],
        "checks": [
            "MODIFICACIÓN: devolución del 10 al 11 de noviembre de 2026, manteniendo las 18:00 y el mismo lugar.",
            "El retiro permanece el 10 de noviembre de 2026 a las 10:00.",
            "ADICIÓN: cláusula 6, depósito de garantía de ARS 40.000 al retirar los equipos.",
            "El depósito es reembolsable íntegramente dentro de las 48 horas posteriores a la devolución si no hay faltantes ni daños.",
            "El precio total sigue siendo ARS 80.000 y no debe sumarse el depósito al precio para afirmar un aumento.",
            "No se modifican inventario, forma de pago, estado de los equipos ni uso autorizado. No se reportan las cláusulas ratificadas 1, 2, 4 y 5 como cambios.",
        ],
        "purpose": "Caso de otro dominio preparado después de ajustar los prompts musicales, sin modificar esos prompts para esta prueba.",
    }
    (DATA / "expected_changes.json").write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Generados tres pares de contratos ficticios y sus referencias esperadas.")


if __name__ == "__main__":
    main()

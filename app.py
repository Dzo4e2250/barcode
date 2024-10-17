from flask import Flask, request, render_template, send_file, jsonify
from barcode import EAN13
from barcode.writer import ImageWriter
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from PIL import Image
import textwrap  # Za prelom besedila

app = Flask(__name__)

# Dodajanje Unicode pisave, npr. DejaVu Sans
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))  # Poskrbi, da je datoteka pisave dostopna

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Dobimo podatke iz POST zahteve
        ean_kode = request.form.get('ean_codes').splitlines()  # EAN kode ločene po vrsticah
        opisi_artiklov = request.form.get('opisi_artiklov').splitlines()  # Opisi artiklov ločeni po vrsticah

        # Preverimo, če je število EAN kod in opisov enako
        if len(ean_kode) != len(opisi_artiklov):
            return jsonify({"error": "Število EAN kod in opisov artiklov se ne ujema."}), 400

        # Ustvarimo PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont('DejaVu', 10)  # Uporaba Unicode pisave DejaVu
        width, height = A4

        # Nastavimo robove
        zgornji_rob = 70.88  # 2,5 cm v točkah
        spodnji_rob = 70.88  # 2,5 cm v točkah
        levi_rob = 85.05  # 3 cm v točkah
        desni_rob = 56.7  # 2 cm v točkah
        max_width = width - levi_rob - desni_rob  # Maksimalna širina vsebine
        y = height - zgornji_rob  # Začetek na vrhu strani
        x = levi_rob  # Levi rob
        barcode_width = 100  # Širina črtne kode

        for ean, opis in zip(ean_kode, opisi_artiklov):
            # Preverimo, če je EAN številka dolga 13 znakov
            if len(ean) != 13 or not ean.isdigit():
                return jsonify({"error": f"EAN koda {ean} ni veljavna (mora biti 13-mestna številka)."}), 400

            # Generiraj črtno kodo s pomočjo python-barcode in jo shranimo v buffer
            img_buffer = io.BytesIO()
            ean_koda = EAN13(ean, writer=ImageWriter())
            ean_koda.write(img_buffer)
            img_buffer.seek(0)

            # Odpri črtno kodo kot sliko
            img = Image.open(img_buffer)
            img_width, img_height = img.size
            aspect = img_height / float(img_width)

            # Dodaj črtno kodo v PDF
            c.drawInlineImage(img, x, y, width=barcode_width, height=(barcode_width * aspect))

            # Dodaj opis artikla desno od črtne kode
            text_x = x + barcode_width + 10  # Postavi besedilo desno od črtne kode
            max_text_width = max_width - barcode_width - 10  # Preostala širina za besedilo
            wrapped_text = textwrap.wrap(opis, width=40)  # Prelomi besedilo na 40 znakov

            # Nariši vsako vrstico besedila in se premikaj po y osi
            line_height = 12
            text_y = y + (barcode_width * aspect) - line_height  # Poravnaj z vrhom črtne kode
            for line in wrapped_text:
                c.drawString(text_x, text_y, line)
                text_y -= line_height  # Premik na naslednjo vrstico

            # Premakni navzdol za naslednji element (črtna koda in opis)
            y -= (barcode_width * aspect) + 14.17  # Razmik 0,5 cm

            # Preverimo, ali smo dosegli dno strani (spodnji rob)
            if y < spodnji_rob:
                c.showPage()  # Ustvarimo novo stran
                y = height - zgornji_rob  # Ponastavimo višino na vrh strani (zgornji rob)

        # Shrani PDF v pomnilnik
        c.save()
        buffer.seek(0)

        # Pošlji PDF nazaj uporabniku
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='ean_kode.pdf')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

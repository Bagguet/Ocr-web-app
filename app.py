import pytesseract
from PIL import Image
from flask import Flask, request, jsonify, render_template
import os
import io

# --- KONFIGURACJA ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
lang_config = 'eng+pol'
app = Flask(__name__)

# --- FUNKCJA OCR ---
def perform_ocr_on_image_web(image_stream):
    """
    Wykonuje optyczne rozpoznawanie znaków (OCR) na strumieniu obrazu.
    Zwraca odczytany tekst lub informację o błędzie.
    """
    try:
        img = Image.open(image_stream)
        text = pytesseract.image_to_string(img, lang=lang_config)
        text = text.strip()
        return text if text else "Nie udało się odczytać żadnego tekstu z obrazu."

    except pytesseract.TesseractNotFoundError:
        return "Błąd serwera: Tesseract OCR nie został znaleziony. Skontaktuj się z administratorem."
    except Exception as e:
        return f"Wystąpił błąd podczas przetwarzania obrazu: {e}"


# --- Endpointy Flask ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'Brak pliku obrazu w żądaniu'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nie wybrano pliku obrazu'}), 400

    if file:
        image_stream = io.BytesIO(file.read())
        # Wywołujemy zmienioną funkcję
        ocr_result = perform_ocr_on_image_web(image_stream)
        return jsonify({'text': ocr_result}), 200

    return jsonify({'error': 'Nieznany błąd podczas przesyłania pliku'}), 500


# --- Uruchomienie serwera Flask ---
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
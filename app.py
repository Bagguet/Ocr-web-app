import os
import sys
import io
import webbrowser
import threading
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify, render_template, redirect, url_for  # Dodano redirect, url_for


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)
    print(f"DEBUG: Resource Path: {full_path}")
    return full_path


lang_config = 'eng+pol'

app = Flask(__name__, template_folder=resource_path('templates'))
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Zostawiamy dla upewnienia się, że szablony są świeże

pytesseract.pytesseract.tesseract_cmd = resource_path(os.path.join('tesseract_bin', 'tesseract.exe'))
os.environ['TESSDATA_PREFIX'] = resource_path(
    'tessdata')  # WAŻNE: Upewnij się, że ten TESSDATA_PREFIX jest ustawiony poprawnie i zawiera pliki językowe!


def perform_ocr_on_image_web(image_stream):
    img = None
    try:
        img = Image.open(image_stream)
        # Tesseract 5.x wymaga `--oem 1` dla niektórych konfiguracji silnika
        # Jeśli napotkasz błędy z silnikiem, możesz spróbować usunąć lub zmienić `--oem`
        text = pytesseract.image_to_string(img, lang=lang_config, config='--oem 1 --psm 3')
        text = text.strip()
        return text if text else "Nie udało się odczytać żadnego tekstu z obrazu."
    except pytesseract.TesseractNotFoundError:
        return "Błąd serwera: Tesseract OCR nie został znaleziony. Skontaktuj się z administratorem."
    except Exception as e:
        # Bardziej szczegółowy komunikat o błędzie dla Access Violation
        if "3221225781" in str(e):
            return f"Wystąpił błąd podczas przetwarzania obrazu: Błąd wewnętrzny Tesseracta (Access Violation). Upewnij się, że TESSDATA_PREFIX jest poprawnie ustawiony i Visual C++ Redistributable są zainstalowane. ({e})"
        return f"Wystąpił błąd podczas przetwarzania obrazu: {e}"
    finally:
        if img:
            img.close()


@app.route('/')
def index():
    print(f"DEBUG: Attempting to render index.html from {app.template_folder}")
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Zmieniono na getlist do obsługi wielu plików
    if 'image' not in request.files:
        return jsonify({'error': 'Brak pliku obrazu w żądaniu'}), 400

    files = request.files.getlist('image')  # Pobierz listę wszystkich plików z nazwą 'image'
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'Nie wybrano żadnych plików obrazów'}), 400

    results = []
    for file in files:
        if file.filename != '':
            image_stream = io.BytesIO(file.read())
            ocr_result = perform_ocr_on_image_web(image_stream)
            results.append({
                'filename': file.filename,
                'text': ocr_result
            })

    return jsonify({'results': results}), 200  # Zwracamy listę wyników


# Nowa funkcja do zamykania serwera Flask
@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    print("DEBUG: Flask server shutting down...")
    return 'Server shutting down...'


if __name__ == '__main__':
    port = 5000
    url = f"http://127.0.0.1:{port}"


    def open_browser():
        threading.Timer(1, lambda: webbrowser.open(url)).start()


    open_browser()
    app.run(debug=False, host='127.0.0.1', port=port)  # Pozostaw debug=True dla testów
import pytesseract
from PIL import Image
import os
import pyperclip

# --- KONFIGURACJA ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
lang_config = 'eng+pol'
SUPPORTED_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.tif')

# --- KOD OCR ---
def OCR(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"Błąd: Plik obrazu '{image_path}' nie został znaleziony.")
        else:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang=lang_config)
            text = text.strip()

            if text:
                pyperclip.copy(text)
                print("\n--- Odczytany tekst ---")
                print(text)
                print("---------------------\n")
                print("Tekst został pomyślnie skopiowany do schowka!")
            else:
                print("\n--- Brak tekstu ---")
                print("Nie udało się odczytać żadnego tekstu z obrazu.")
                print("---------------------\n")
                return None


    except pytesseract.TesseractNotFoundError:
        print(
            "Błąd: Tesseract OCR nie został znaleziony. Upewnij się, że jest zainstalowany i ścieżka w kodzie (pytesseract.pytesseract.tesseract_cmd) jest poprawna.")
    except pyperclip.PyperclipException as e:
        print(f"Błąd podczas kopiowania do schowka: {e}")
        print("Upewnij się, że masz zainstalowany 'pyperclip' i że jest dostępne środowisko graficzne.")
        print("Nadal wyświetlam tekst, mimo że nie został skopiowany do schowka.")
        if 'text' in locals() and text:
            print("\n--- Odczytany tekst (nie skopiowany do schowka) ---")
            print(text)
            print("---------------------\n")
            return text
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
        return None

# --- GŁÓWNA CZĘŚĆ PROGRAMU ---
def main():
    folder_path = input("Podaj ścieżkę do folderu zawierającego obrazy: ")

    if not os.path.isdir(folder_path):
        print(f"Błąd: Podana ścieżka '{folder_path}' nie jest prawidłowym folderem.")
        return

    print(f"\nRozpoczynanie przetwarzania obrazów w folderze: {folder_path}\n")

    found_images = False
    all_extracted_text = []

    for filename in os.listdir(folder_path):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
            found_images = True
            print(f"Przetwarzanie pliku: {filename}")
            extracted_text = OCR(file_path)
            if extracted_text is not None:
                all_extracted_text.append(f"--- Tekst z {filename} ---\n{extracted_text}\n")
            input("Naciśnij Enter, aby przetworzyć następny obraz (lub zakończyć)...")

    if not found_images:
        print(f"Nie znaleziono obsługiwanych plików graficznych ({', '.join(SUPPORTED_IMAGE_EXTENSIONS)}) w folderze '{folder_path}'.")
    else:
        # Po przetworzeniu wszystkich obrazów, skopiuj cały zebrany tekst do schowka
        if all_extracted_text:
            combined_text = "\n\n".join(all_extracted_text)
            try:
                pyperclip.copy(combined_text)
                print("\nCały zebrany tekst ze wszystkich obrazów został skopiowany do schowka!")
            except pyperclip.PyperclipException as e:
                print(f"Błąd podczas kopiowania całego tekstu do schowka: {e}")
                print("Upewnij się, że masz zainstalowany 'pyperclip' i że jest dostępne środowisko graficzne.")
        else:
            print("\nNie udało się zebrać żadnego tekstu ze wszystkich przetworzonych obrazów.")


if __name__ == "__main__":
    main()
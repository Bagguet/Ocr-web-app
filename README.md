# OCR Web Application

A powerful web-based OCR (Optical Character Recognition) application that extracts text from images with high accuracy. Built with Python, Flask, and Tesseract OCR.

## ✨ Features

- Extract text from images with just a few clicks
- Support for multiple languages (English and Polish included)
- Simple and intuitive web interface
- Fast and accurate text recognition
- Download extracted text as a text file
- Built with Python and Flask for reliability

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR engine installed on your system
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ocr-webapp.git
   cd ocr-webapp
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - **Windows**: Download and install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

### Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## 🛠️ Usage

1. Click the "Choose File" button to select an image
2. Select the language of the text in the image
3. Click "Extract Text" to process the image
4. View the extracted text in the text area
5. Click "Download" to save the text as a file

## 📂 Project Structure

```
OCR/
├── Images/               # Sample images for testing
├── templates/
│   └── index.html       # Main web interface
├── tesseract_bin/       # Tesseract binary files (Windows)
├── tessdata/            # Tesseract language data files
├── app.py               # Main application file
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

You can customize the application by modifying the following in `app.py`:

- `UPLOAD_FOLDER`: Directory to store uploaded images
- `ALLOWED_EXTENSIONS`: Supported image file formats
- `TESSERACT_PATH`: Path to Tesseract executable (if not in system PATH)

## 🌐 Supported Languages

- English (eng)
- Polish (pol)

> To add more languages, download the corresponding `.traineddata` file from the [Tesseract GitHub](https://github.com/tesseract-ocr/tessdata) and place it in the `tessdata/` directory.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

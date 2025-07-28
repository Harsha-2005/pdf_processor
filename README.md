# pdf_processor
A pdf processor which gives the structured content present in the pdf in the JSON format
# PDF Processor

A Python tool for extracting headings, font statistics, and language from PDF files.  
Supports Docker for reproducible builds and includes test scripts for edge cases.

---

## Features

- Extracts headings and outlines from PDFs
- Detects document language using FastText
- Analyzes font size distribution
- Handles English and Japanese PDFs
- Dockerized for easy deployment

---

## Requirements

- Python 3.10+ (for local runs)
- Docker (recommended)
- [Git](https://git-scm.com/) for version control

---

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/pdf-processor.git
   cd pdf-processor
   ```

2. **Install Python dependencies (optional, for local runs):**
   ```sh
   pip install -r requirements.txt
   ```

3. **Download the FastText language model:**
   ```sh
   bash download_model.sh
   ```
   Or manually download [lid.176.ftz](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz) into the project root.

---

## Usage

### **1. Build the Docker Image**

```sh
docker build -t pdf-processor .
```

### **2. Prepare Input PDFs**

- Place your PDF files in the `input/` directory.
- You can generate sample PDFs using:
  ```sh
  python generate_test_pdfs.py
  ```

### **3. Run the Processor**

```sh
docker run --rm -v %cd%/input:/app/input -v %cd%/output:/app/output pdf-processor
```
- For PowerShell, use `${PWD}` instead of `%cd%`.

### **4. View Results**

- Processed JSON files will appear in the `output/` directory.

---

## Testing

Run the edge case tests:
```sh
python test_edge_cases.py
```
This will process all test PDFs and verify the output.

---

## Project Structure

```
pdf-processor/
├── Dockerfile
├── processor.py
├── requirements.txt
├── generate_test_pdfs.py
├── test_edge_cases.py
├── download_model.sh
├── input/           # Place PDFs here
├── output/          # Processed JSONs appear here
└── .gitignore
```

---

## Troubleshooting

- **No output generated:**  
  Ensure your input PDFs exist and are valid. Check Docker volume paths.
- **LANG_MODEL errors:**  
  Make sure `lid.176.ftz` is present in the project root or `/app` inside the container.
- **Docker build fails:**  
  Use `docker build --no-cache -t pdf-processor .` to rebuild from scratch.

---

## License

MIT License (add your own if needed)

---

## Contributing

Pull requests and issues are welcome!

---

## Author

Your Name  
[Your GitHub Profile](https://github.com/yourusername)

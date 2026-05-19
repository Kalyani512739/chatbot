import os
from utils.pdf_loader import extract_text_from_pdf
from utils.text_splitter import split_text
from utils.vector_store import create_vector_db

all_chunks = []

upload_folder = "uploads"

for file in os.listdir(upload_folder):

    if file.endswith(".pdf"):

        path = os.path.join(upload_folder, file)

        print(f"Processing {file}...")

        text = extract_text_from_pdf(path)

        print("\n--- Extracted Text Preview ---")
        print(text[:1000])

        chunks = split_text(text)

        print("\n--- First 3 Chunks ---")
        for i, chunk in enumerate(chunks[:3]):
            print(f"\nChunk {i+1}:")
            print(chunk)

        all_chunks.extend(chunks)

create_vector_db(all_chunks)

print("PDF training completed 😎")
import fitz
import os
import glob
import re

pdf_files = glob.glob('교안/*.pdf')

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    print(f"Reading {pdf_path}: {len(doc)} pages")
    for i in range(min(5, len(doc))): # check first 5 pages
        text = doc[i].get_text("text").replace("\n", " ")
        print(f"  Page {i}: {text[:100]}...")

extract_text(pdf_files[0])

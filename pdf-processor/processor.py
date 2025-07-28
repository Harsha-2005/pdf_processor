import fitz
import numpy as np
import json
import os
import sys
import re
import fasttext
from collections import Counter

LANG_MODEL = None

def load_lang_model():
    global LANG_MODEL
    if LANG_MODEL is None:
        model_path = "/app/lid.176.ftz"
        if not os.path.exists(model_path):
            raise FileNotFoundError("Language model missing")
        LANG_MODEL = fasttext.load_model(model_path)
    return LANG_MODEL

def secure_path(path):
    base = os.path.abspath('/app')
    target = os.path.abspath(path)
    if os.path.commonpath([base]) != os.path.commonpath([base, target]):
        raise ValueError(f"Blocked path traversal: {target}")
    return target

def analyze_font_distribution(doc, sample_size=5):
    font_sizes = []
    page_count = len(doc)
    if page_count > sample_size:
        page_indices = {0, 1, page_count//2, page_count-2, page_count-1}
    else:
        page_indices = set(range(page_count))
    for i in page_indices:
        try:
            page = doc.load_page(i)
            blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = round(span["size"] * 2) / 2
                            font_sizes.append(size)
        except Exception as e:
            print(f"Warning: Page {i} skipped - {str(e)}", file=sys.stderr)
    if not font_sizes:
        return 12.0, {}
    size_counts = Counter(font_sizes)
    modal_size = max(size_counts, key=size_counts.get)
    return modal_size, dict(size_counts.most_common(10))

def detect_language(text, model):
    if len(text) < 10:
        return "en"
    text = text.replace("\n", " ")[:500]
    predictions = model.predict(text, k=1)
    return predictions[0][0].replace("__label__", "")

def detect_headings(page, body_font, lang="en"):
    headings = []
    page_height = page.rect.height
    blocks = page.get_text("dict").get("blocks", [])
    text_flags = fitz.TEXT_PRESERVE_WHITESPACE
    if lang in ["ja", "zh", "ko"]:
        text_flags |= fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_DEHYPHENATE
    for block in blocks:
        if block.get("type") != 0 or "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                raw_text = span["text"]
                if lang in ["ja", "zh", "ko"]:
                    text = raw_text.strip()
                else:
                    text = re.sub(r'[^\w\s.,;:\-\'"()]', '', raw_text).strip()
                if not text or len(text) < 2:
                    continue
                size_ratio = span["size"] / body_font
                is_bold = bool(span["flags"] & 16)
                y_ratio = span["bbox"][1] / page_height
                position_score = 1.0 - min(y_ratio, 0.2) * 3
                pattern_score = 0.5
                if lang == "en" and re.match(r'^(Chapter|Section|\d+\.\d+|\b(I{1,3}|IV|V|VI{0,3}|IX|X)\b)', text):
                    pattern_score = 1.5
                elif lang == "ja" and re.search(r'^(第|節|[\u30a0-\u30ff\u3040-\u309f])', text):
                    pattern_score = 1.5
                score = (size_ratio * 3) + (is_bold * 2) + position_score + pattern_score
                CONF_THRESHOLD = 2.5
                if score < CONF_THRESHOLD:
                    continue
                if score > 6.0:
                    level = "H1"
                elif score > 4.5:
                    level = "H2"
                elif score > 3.0:
                    level = "H3"
                else:
                    continue
                headings.append({
                    "text": text[:200],
                    "level": level,
                    "page": page.number + 1,
                    "score": round(score, 2)
                })
    return headings

def correct_heading_levels(headings):
    if not headings:
        return []
    level_map = {"H1": 1, "H2": 2, "H3": 3}
    current_level = 0
    corrected = []
    for h in headings:
        new_level = level_map[h["level"]]
        if new_level > current_level + 1:
            new_level = current_level + 1
        current_level = new_level
        corrected.append({
            "text": h["text"],
            "level": f"H{new_level}",
            "page": h["page"]
        })
    return corrected

def process_pdf(input_path, output_path):
    try:
        input_path = secure_path(input_path)
        output_path = secure_path(output_path)
        with fitz.open(input_path) as doc:
            if len(doc) > 50:
                raise ValueError("PDF exceeds 50-page limit")
            lang_model = load_lang_model()
            first_page = doc.load_page(0)
            first_page_text = first_page.get_text("text", flags=fitz.TEXT_PRESERVE_WHITESPACE)
            doc_lang = detect_language(first_page_text, lang_model)
            body_font, font_dist = analyze_font_distribution(doc)
            meta_title = doc.metadata.get("title", "")
            clean_title = re.sub(r'[^\w\s-]', '', meta_title)[:200] or os.path.splitext(os.path.basename(input_path))[0]
            all_headings = []
            for i in range(len(doc)):
                page = doc.load_page(i)
                headings = detect_headings(page, body_font, doc_lang)
                all_headings.extend(headings)
            corrected_headings = correct_heading_levels(all_headings)
            result = {
                "title": clean_title,
                "outline": [{
                    "level": h["level"],
                    "text": h["text"],
                    "page": h["page"]
                } for h in corrected_headings],
                "metadata": {
                    "page_count": len(doc),
                    "body_font_size": body_font,
                    "font_distribution": font_dist,
                    "detected_language": doc_lang
                }
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"ERROR: {os.path.basename(input_path)} - {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    input_dir = '/app/input'
    output_dir = '/app/output'
    os.makedirs(output_dir, exist_ok=True)
    processed = 0
    for filename in sorted(os.listdir(input_dir)):
        if filename.lower().endswith('.pdf'):
            in_path = os.path.join(input_dir, filename)
            out_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
            if process_pdf(in_path, out_path):
                processed += 1
    print(f"Processed {processed} PDF files")
    sys.exit(0 if processed > 0 else 1)
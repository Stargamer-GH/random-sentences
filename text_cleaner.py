#!/usr/bin/env python3
"""
Simplified Text Cleaner
- Run directly in your IDE without command-line arguments.
- Adjust settings at the top of the script.
- Skips files that appear already cleaned.
"""
import re
from pathlib import Path
import datetime

# === SETTINGS ===
ROOT_PATH = Path('.')            # Directory to search
PATTERN = '*.txt'                # File pattern to match
RECURSIVE = True                 # Search subdirectories
INPLACE = False                  # Overwrite files instead of creating cleaned copies
BACKUP = True                    # Keep backup if INPLACE = True
MODE = 'smart'                   # 'smart' or 'simple'
REMOVE_SINGLE_QUOTES = False     # Remove apostrophes too?
MAX_SIZE = 10_000_000              # Max file size in bytes
EXCLUDE_DIRS = {'.git', 'venv', '__pycache__', '.venv', 'env', 'node_modules'}
CLEANED_TAG = '.cleaned'          # Tag to mark cleaned files

ELLIPSIS_TOKEN = "⟪ELLIPSIS⟫"

def remove_partial_lines(text: str) -> str:
    new_text = ""
    lines = text.split('\n')
    for l in lines:
        if '.' in l and l.strip() != '.':
            new_text += l + '\n'
    return new_text

def remove_bracket_contents(text: str) -> str:
    while True:
        new_text = re.sub(r' \([^()]*\)', '', text, flags=re.S)
        if new_text == text:
            break
        text = new_text
    while True:
        new_text = re.sub(r'\[[^\[\]]*\]', '', text, flags=re.S)
        if new_text == text:
            break
        text = new_text
    while True:
        new_text = re.sub(r'\{[^{}]*\}', '', text, flags=re.S)
        if new_text == text:
            break
        text = new_text
    return text

def remove_reference_issues(text: str) -> str:
    text = re.sub(r':.\d+.', '', text)
    return text

def remove_quotes(text: str, remove_single: bool = False) -> str:
    text = re.sub(r'["“”«»„‟‹›]', '', text)
    if remove_single:
        text = re.sub(r"[\'‘’`]", '', text)
    return text

def normalize_whitespace(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def split_sentences(text: str, mode: str = 'smart') -> str:
    text = re.sub(r'\.{3,}', ELLIPSIS_TOKEN, text)
    if mode == 'simple':
        text = re.sub(r'([.!?])\s+', r'\1\n', text)
    else:
        text = re.sub(r'([.!?])\s+(?=[A-Z0-9])', r'\1\n', text)
        text = re.sub(r'([.!?])\s*$', r'\1\n', text)
    text = text.replace(ELLIPSIS_TOKEN, '...')
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return '\n'.join(lines) + ('\n' if lines else '')

def clean_text(text: str) -> str:
    text = remove_partial_lines(text)
    text = remove_bracket_contents(text)
    text = remove_reference_issues(text)
    text = remove_quotes(text, remove_single=REMOVE_SINGLE_QUOTES)
    text = normalize_whitespace(text)
    return split_sentences(text, mode=MODE)

def iter_files(root: Path):
    files = root.rglob(PATTERN) if RECURSIVE else root.glob(PATTERN)
    for p in files:
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if CLEANED_TAG in p.stem:
            continue  # Skip already cleaned files
        yield p

def process_file(path: Path):
    raw = path.read_text(encoding='utf-8', errors='replace')
    cleaned = clean_text(raw)
    if INPLACE:
        if BACKUP:
            bak = path.with_name(path.name + f'.bak-{datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")}')
            bak.write_text(raw, encoding='utf-8')
        path.write_text(cleaned, encoding='utf-8')
        print(f"Overwrote: {path}")
    else:
        out = path.with_name(path.stem + CLEANED_TAG + path.suffix)
        out.write_text(cleaned, encoding='utf-8')
        print(f"Wrote: {out}")

def main():
    for f in iter_files(ROOT_PATH):
        if f.stat().st_size > MAX_SIZE:
            print(f"Skipping (too large): {f}")
            continue
        try:
            process_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == '__main__':
    main()

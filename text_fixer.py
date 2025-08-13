from pathlib import Path

CLEANED_TAG = ''         # Tag to mark cleaned files

def add_capitals_and_periods(text: str) -> str:
    new_text = ""
    for l in text.splitlines():
        new_text += l.capitalize()
        if l[-1] not in ['.', '!', '?']:
            new_text += '.'
        new_text += '\n'
    return new_text

def clean_text(text: str) -> str:
    return add_capitals_and_periods(text)

def process_file(path: Path):
    raw = path.read_text(encoding='utf-8', errors='replace')
    cleaned = clean_text(raw)
    out = path.with_name(path.stem + CLEANED_TAG + path.suffix)
    out.write_text(cleaned, encoding='utf-8')
    print(f"Wrote: {out}")

def main():
    file = "Stuff-for-sale.txt"
    try:
        process_file(Path("./SourceTextFiles/"+file))
    except Exception as e:
        print(f"Error processing {file}: {e}")

if __name__ == '__main__':
    main()
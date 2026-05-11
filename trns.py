import json
from deep_translator import GoogleTranslator

# ── Language list ──────────────────────────────────────────────────────────────
LANGUAGES = {
    "es": {"name": "Spanish",    "flag": "🇪🇸", "romanize": False},
    "fr": {"name": "French",     "flag": "🇫🇷", "romanize": False},
    "de": {"name": "German",     "flag": "🇩🇪", "romanize": False},
    "it": {"name": "Italian",    "flag": "🇮🇹", "romanize": False},
    "pt": {"name": "Portuguese", "flag": "🇵🇹", "romanize": False},
    "zh": {"name": "Chinese",    "flag": "🇨🇳", "romanize": True},
    "ja": {"name": "Japanese",   "flag": "🇯🇵", "romanize": True},
    "ko": {"name": "Korean",     "flag": "🇰🇷", "romanize": True},
    "ar": {"name": "Arabic",     "flag": "🇸🇦", "romanize": True},
    "hi": {"name": "Hindi",      "flag": "🇮🇳", "romanize": True},
    "ru": {"name": "Russian",    "flag": "🇷🇺", "romanize": True},
    "tr": {"name": "Turkish",    "flag": "🇹🇷", "romanize": False},
    "nl": {"name": "Dutch",      "flag": "🇳🇱", "romanize": False},
    "pl": {"name": "Polish",     "flag": "🇵🇱", "romanize": False},
    "sv": {"name": "Swedish",    "flag": "🇸🇪", "romanize": False},
    "uk": {"name": "Ukrainian",  "flag": "🇺🇦", "romanize": True},
    "id": {"name": "Indonesian", "flag": "🇮🇩", "romanize": False},
    "vi": {"name": "Vietnamese", "flag": "🇻🇳", "romanize": False},
    "th": {"name": "Thai",       "flag": "🇹🇭", "romanize": True},
    "he": {"name": "Hebrew",     "flag": "🇮🇱", "romanize": True},
    "fa": {"name": "Persian",    "flag": "🇮🇷", "romanize": True},
    "bn": {"name": "Bengali",    "flag": "🇧🇩", "romanize": True},
    "ta": {"name": "Tamil",      "flag": "🇱🇰", "romanize": True},
    "sw": {"name": "Swahili",    "flag": "🇰🇪", "romanize": False},
}

POPULAR = ["es", "fr", "de", "zh", "ja", "ar", "hi", "pt"]

DIVIDER = "─" * 60


# ── Helpers ────────────────────────────────────────────────────────────────────
def list_languages() -> None:
    print("\nAvailable languages:\n")
    codes = list(LANGUAGES.keys())
    for i in range(0, len(codes), 4):
        row = codes[i:i+4]
        print("  " + "   ".join(
            f"{c:2}  {LANGUAGES[c]['flag']} {LANGUAGES[c]['name']:<12}"
            for c in row
        ))
    print()


def parse_language_input(raw: str) -> list[str]:
    """Return a list of valid language codes from user input."""
    if raw.strip().lower() == "all":
        return list(LANGUAGES.keys())
    if raw.strip().lower() in ("", "popular"):
        return POPULAR

    codes = [t.strip().lower() for t in raw.replace(",", " ").split()]
    valid = [c for c in codes if c in LANGUAGES]
    invalid = [c for c in codes if c not in LANGUAGES]
    if invalid:
        print(f"  ⚠  Skipping unknown codes: {', '.join(invalid)}")
    return valid


def translate(text: str, codes: list[str]) -> dict:
    """Return actual translations using deep-translator."""
    results = {}
    for code in codes:
        # Google Translate usually expects zh-CN for Simplified Chinese
        target_code = "zh-CN" if code == "zh" else ("he" if code == "he" else code)
        
        try:
            translated = GoogleTranslator(source='auto', target=target_code).translate(text)
        except Exception as e:
            translated = f"[Error: {e}]"
            
        results[code] = {"translation": translated}
        if LANGUAGES[code].get("romanize"):
            results[code]["romanized"] = "(Romanization not supported via this local tool)"
    return results


def print_results(results: dict, codes: list[str]) -> None:
    print(f"\n{DIVIDER}")
    for code in codes:
        lang = LANGUAGES[code]
        if code not in results:
            print(f"  {lang['flag']}  {lang['name']:<12}  [no result]")
            continue
        val = results[code]
        translation = val.get("translation", "")
        romanized   = val.get("romanized", "")
        print(f"\n  {lang['flag']}  {lang['name']}")
        print(f"     {translation}")
        if romanized:
            print(f"     ({romanized})")
    print(f"\n{DIVIDER}\n")


# ── Main interactive loop ──────────────────────────────────────────────────────
def main() -> None:
    print(f"\n{'═'*60}")
    print("   🌐  English → Multi-Language Translator")
    print(f"{'═'*60}")
    print("   Running locally (using deep-translator + Google)\n")
    print("   Commands:  'list' — show all languages")
    print("              'quit' — exit\n")

    while True:
        # ── Input ──────────────────────────────────────────────────────────
        text = input("📝  English text  : ").strip()
        if text.lower() == "quit":
            print("\nGoodbye! 👋\n")
            break
        if text.lower() == "list":
            list_languages()
            continue
        if not text:
            print("  (no text entered, try again)\n")
            continue

        print(
            "\n🌍  Target languages (comma-separated codes, 'all', or Enter for popular):"
        )
        list_languages()
        raw_langs = input("   → ").strip()
        codes = parse_language_input(raw_langs)

        if not codes:
            print("  ⚠  No valid languages selected.\n")
            continue

        names = ", ".join(LANGUAGES[c]["name"] for c in codes)
        print(f"\n⏳  Translating into: {names} …")

        results = translate(text, codes)
        print_results(results, codes)

        again = input("Translate another? (Enter = yes, 'quit' = no): ").strip().lower()
        if again == "quit":
            print("\nGoodbye! 👋\n")
            break
        print()


if __name__ == "__main__":
    main()
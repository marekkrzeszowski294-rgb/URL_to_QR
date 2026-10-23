import argparse
import sys
from urllib.parse import urlsplit


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generuje obraz PNG z kodem QR zawierającym adres URL."
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="adres strony, np. https://example.com",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="qr_kod.png",
        help="nazwa pliku wynikowego (domyślnie: qr_kod.png)",
    )
    args = parser.parse_args()

    url = args.url or input("Podaj adres URL: ").strip()
    parsed_url = urlsplit(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        parser.error("podaj poprawny adres zaczynający się od http:// lub https://")

    try:
        import qrcode
    except ImportError:
        print(
            "Brak biblioteki qrcode. Zainstaluj zależności poleceniem: "
            "python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image().save(args.output)
    print(f"Zapisano kod QR do pliku: {args.output}")
    print("Kod QR w terminalu:")
    for row in qr.get_matrix():
        print("".join("##" if module else "  " for module in row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

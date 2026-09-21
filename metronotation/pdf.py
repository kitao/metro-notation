"""Optional Chromium printing of the same self-contained HTML document."""

from pathlib import Path


def export_pdf(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright, Error
    except ImportError as exc:
        raise RuntimeError(
            'PDF export needs: pip install "metro-notation[pdf]" && python -m playwright install chromium'
        ) from exc
    html_path, pdf_path = Path(html_path).resolve(), Path(pdf_path).resolve()
    if html_path == pdf_path:
        raise ValueError("HTML and PDF output paths must differ")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page()
                page.goto(html_path.as_uri(), wait_until="load")
                page.evaluate("document.fonts.ready")
                page.pdf(
                    path=str(pdf_path),
                    print_background=True,
                    prefer_css_page_size=True,
                    tagged=True,
                    display_header_footer=False,
                )
            finally:
                browser.close()
    except Error as exc:
        raise RuntimeError(
            'PDF export could not launch or print with Chromium. Run "python -m playwright install chromium". '
            + str(exc)
        ) from exc
    return pdf_path

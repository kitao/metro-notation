"""Print self-contained HTML with Chromium and render its PDF with Poppler."""

import subprocess
from pathlib import Path

SHEET_NAMES = ("f2l", "oll-01-30", "oll-31-57", "pll")
# Every image rendered from the PDF, relative to its sheet directory.
IMAGE_PATHS = tuple(Path(f"{name}.png") for name in SHEET_NAMES)


def export_pdf(html_path, pdf_path):
    html_path, pdf_path = Path(html_path).resolve(), Path(pdf_path).resolve()
    if pdf_path.exists() and pdf_path.samefile(html_path):
        raise ValueError("HTML and PDF output paths must differ")
    try:
        from playwright.sync_api import Error, sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "PDF export needs: python -m pip install --group dev && python -m playwright install chromium"
        ) from exc
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
                )
            finally:
                browser.close()
    except Error as exc:
        raise RuntimeError(
            'PDF export could not launch or print with Chromium. Run "python -m playwright install chromium". '
            + str(exc)
        ) from exc
    return pdf_path


def export_pngs(pdf_path, output_directory):
    """Render each PDF page as a 300 dpi PNG."""
    pdf_path, output = Path(pdf_path).resolve(), Path(output_directory).resolve()
    output.mkdir(parents=True, exist_ok=True)
    for page, name in enumerate(SHEET_NAMES, 1):
        subprocess.run(
            ["pdftoppm", "-f", str(page), "-l", str(page), "-r", "300", "-png", "-singlefile"]
            + [str(pdf_path), str(output / name)],
            check=True,
        )

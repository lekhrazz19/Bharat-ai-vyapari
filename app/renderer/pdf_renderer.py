from pathlib import Path
from playwright.async_api import async_playwright

PDF_DIR = Path("storage/pdf")
PDF_DIR.mkdir(parents=True, exist_ok=True)


async def html_files_to_pdf(html_files: list[str], proposal_id: str) -> str:
    output_pdf = PDF_DIR / f"{proposal_id}.pdf"

    page_bodies = []
    for html_file in html_files:
        path = Path(html_file).resolve()
        # Keep each page isolated by iframe. This avoids CSS collisions and mimics page-wise rendering.
        page_bodies.append(f'<iframe class="pdf-page" src="{path.as_uri()}"></iframe>')

    final_html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <style>
        @page {{ size: 768px 1086px; margin: 0; }}
        html, body {{ margin: 0; padding: 0; background: white; }}
        .pdf-page {{
          width: 768px;
          height: 1086px;
          border: 0;
          display: block;
          page-break-after: always;
        }}
      </style>
    </head>
    <body>{''.join(page_bodies)}</body>
    </html>
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--allow-file-access-from-files"])
        page = await browser.new_page(viewport={"width": 768, "height": 1086})
        await page.set_content(final_html, wait_until="networkidle")
        await page.pdf(
            path=str(output_pdf),
            width="768px",
            height="1086px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()

    return str(output_pdf)

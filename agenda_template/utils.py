from agenda_template import AGENDA_OUTPUT_DIR, AGENDA_TEMPLATE_DIR
import os
import yaml
from pypdf import PdfWriter, PdfReader
from io import BytesIO
import asyncio
import pyppeteer


## config
class ClassDict(dict):
    """Makes dict accessible by attribute.
    Taken from https://stackoverflow.com/a/1639632/6494418
    """
    def __getattr__(self, name):
        return self[name] if not isinstance(self[name], dict) \
            else ClassDict(self[name])


def load_cfg(cfg_file=os.path.join(AGENDA_TEMPLATE_DIR, 'config.yaml')):
    with open(cfg_file, 'r') as f:
        return ClassDict(yaml.load(f, Loader=yaml.FullLoader))



## pdf
async def _get_pdf(html_list):
    browser = await pyppeteer.launch(headless=True, executablePath='/usr/bin/chromium-browser')
    pdfs = []
    for html in html_list:
        page = await browser.newPage()
        await page.setContent(html)
        pdfs.append(await page.pdf(format='A4'))
    await browser.close()
    return pdfs


def html_to_pdf(html):
    """Convert a list of html pages to a list of pdfs.
    Uses pyppeteer to interact with chromium to interpret the html and
    """
    return asyncio.get_event_loop().run_until_complete(_get_pdf(html))


def write_pdf(pdfs, filename='agenda.pdf'):
    """Write pdf to a file."""
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    merger = PdfWriter()
    for pdf in pdfs:
        reader = PdfReader(BytesIO(pdf))
        merger.append(reader)

    output_file = os.path.join(AGENDA_OUTPUT_DIR, filename)
    with open(output_file, 'wb') as f:
        merger.write(f)

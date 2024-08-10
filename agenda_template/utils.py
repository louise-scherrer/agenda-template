from agenda_template import AGENDA_OUTPUT_DIR, AGENDA_TEMPLATE_DIR
import os
import yaml
from pypdf import PdfWriter, PdfReader
from io import BytesIO
import asyncio
import pyppeteer
import base64
import cv2
import webcolors


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



## output
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


## image
def hex2rgb(hex):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def image_base64(filename, color=None):
    with open(filename, 'rb') as f:
        if color is None:
            img_str = f.read()
        else:
            if type(color) is list:
                bgr = rgb[::-1]
            else:
                c = webcolors.html5_parse_legacy_color(str(color))
                bgr = [c.blue, c.green, c.red]
            img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            img[:,:,:3] = bgr
            img_str = cv2.imencode('.png', img)[1]
    enc = base64.b64encode(img_str)
    return str(enc)[2:-1]

from agenda_template import AGENDA_OUTPUT_DIR, AGENDA_CONFIG_DIR, AGENDA_RESOURCES_DIR
import os
import yaml
from pypdf import PdfWriter, PdfReader
from io import BytesIO
import asyncio
from playwright.async_api import async_playwright
import base64
import webcolors


## config
class AttrDict(dict):
    """Makes dict accessible by attributes.
    Made partly after https://stackoverflow.com/a/1639632/6494418
    """
    def __init__(self, dictionary):
        for key in dictionary:
            self.__setitem__(key, dictionary[key])

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            super(AttrDict, self).__setitem__(key, AttrDict(value))
        elif isinstance(value, list):
            super(AttrDict, self).__setitem__(key, [AttrDict(v) if isinstance(v, dict) else v for v in value])
        else:
            super(AttrDict, self).__setitem__(key, value)
        super(AttrDict, self).__setattr__(key, self[key])

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


def load_cfg(cfg_file=os.path.join(AGENDA_CONFIG_DIR, 'config.yaml')):
    with open(cfg_file, 'r') as f:
        return AttrDict(yaml.load(f, Loader=yaml.FullLoader))



## output
def html_to_pdf(htmls):
    """Convert a list of html pages to a list of pdfs.
    Uses playwright to interact with chromium to interpret the html and generate the pdf.
    """
    async def _playwright_pdf_gen(htnls):
        pdfs = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            for html in htmls:
                await page.set_content(html)
                pdfs.append(await page.pdf(format='A4'))
            await browser.close()
        return pdfs

    return asyncio.get_event_loop().run_until_complete(_playwright_pdf_gen(htmls))


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


def write_html(htmls, filename='agenda'):
    """Write pdf to a file."""
    for i, html in enumerate(htmls):
        output_file = os.path.join(AGENDA_OUTPUT_DIR, filename + f'_{i}.html')
        with open(output_file, 'w') as f:
            print(html, file=f)


## image
def hex2rgb(hex):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def image_base64(filename, color=None):
    with open(filename, 'rb') as f:
        img_str = f.read()
        if color is not None:
            try:
                import cv2
                if type(color) is list:
                    bgr = rgb[::-1]
                else:
                    c = webcolors.html5_parse_legacy_color(str(color))
                    bgr = [c.blue, c.green, c.red]
                img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
                img[:,:,:3] = bgr
                img_str = cv2.imencode('.png', img)[1]
            except ModuleNotFoundError:
                print('opencv not found, color won\'t be applied to png')
    enc = base64.b64encode(img_str)
    return str(enc)[2:-1]


def image_html_code(filename, color=None):
    assert filename.endswith('.png')
    img_binary = image_base64(os.path.join(AGENDA_RESOURCES_DIR, filename), color)
    return '<img src=data:image/png;base64,BINARY_CHUNKS alt=",">'.replace('BINARY_CHUNKS', img_binary)

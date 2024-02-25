import numpy as np
import os
from agenda_template import AGENDA_OUTPUT_DIR
from agenda_template.template import Template
import asyncio
from pyppeteer import launch
from pypdf import PdfWriter, PdfReader
from io import BytesIO


def month_grid(nbdays, d0):
    """Defines an integer grid for the whole month.
    Each row defines a week, each collumn is a weekday. Cell values are the date for that day, or 0 otherwise.
    nbdays  - nb of days in the month (28-31)
    d0      - index of first day of month in week (1: monday, 7: sunday)
    Example: month of 30 days, starting on a tuesday:
        [[ 0.,  1.,  2.,  3.,  4.,  5.,  6.],
        [ 7.,  8.,  9., 10., 11., 12., 13.],
        [14., 15., 16., 17., 18., 19., 20.],
        [21., 22., 23., 24., 25., 26., 27.],
        [28., 29., 30.,  0.,  0.,  0.,  0.]]
    """
    grid = np.arange(start=1,stop=nbdays+1)  # list of days
    grid = np.concatenate([np.zeros(d0-1),grid])  # add 0s before first days of month for empty cells
    if grid.shape[0]%7 != 0: # if the month does not finish on a Sunday (else, it is already ready to rescale)
        grid = np.concatenate([grid, np.zeros(7 - grid.shape[0] % 7)])  # add 0s to reach size k*7

    grid = grid.reshape((-1,7)).astype(np.int32)  # rescale 1 week per row

    return grid


if __name__ == '__main__':
    ## parameters
    month_name = 'Mars'
    nbdays = 26
    d0 = 5


    ## process template
    template = Template()
    month = month_grid(nbdays, d0)

    html_list = []
    for week_idx, week in enumerate(month):
        html_list += template.fill(month_name, week, week_idx)

    ## generate pdf from html/css using chromium
    async def get_pdf(html_list):
        browser = await launch(headless=True, executablePath='/usr/bin/chromium-browser')
        pdfs = []
        for html in html_list:
            page = await browser.newPage()
            await page.setContent(html)
            pdfs.append(await page.pdf(format='A4'))
        await browser.close()
        return pdfs

    pdfs = asyncio.get_event_loop().run_until_complete(get_pdf(html_list))


    ## write pdf to file
    merger = PdfWriter()
    for pdf in pdfs:
        reader = PdfReader(BytesIO(pdf))
        merger.append(reader)

    output_file = os.path.join(AGENDA_OUTPUT_DIR, 'agenda.pdf')
    with open(output_file, 'wb') as f:
        merger.write(f)

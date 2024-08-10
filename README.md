# agenda-template

## How to use

### Installation

* First, install dependencies:
    * `sudo apt install chromium-browser`
    * `pip install -r requirements.txt`

* Then, install locally with `pip install . -e`
* run `python3 script/make_agenda.py <target year> <target month> <number of months>`

## Description

The package uses python string api to edit some targeted fields in the html/css template files, in order to automate the generation of the agenda for each specific months (i.e., hiding the empty days, filling in the correct dates...). It also reads most of the css parametrization from a yaml config file, such that several preset can be used.

The generation of the pdf from the html/css is made by invoking chromium through pyppeteer, because all the python-based html-to-pdf converters library we found out there do no handle modern css syntax, in particular grids.

The python templater itself is a very inefficient series of str.replace() to edit the loaded template.

While it is all made toward a specific design of agenda, the templates should be easy enough to adapt to a new one with a similar structure (one week per double page).
Otherwise, it can be used as a starting block to write new templates and enrich the python templater with desired features.

## todos

* scale down title font if the week titles go two-liners

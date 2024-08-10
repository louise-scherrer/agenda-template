from agenda_template import utils
from agenda_template.template import Template
import argparse
import datetime


if __name__ == '__main__':
    ## get args
    parser = argparse.ArgumentParser(description='agenda generator')
    parser.add_argument(dest='year', help='year', type=int)
    parser.add_argument(dest='month', help='month', choices=range(1, 13), type=int)
    parser.add_argument(dest='nb_months', nargs='?', help='number of months', default=1, choices=range(1, 13), type=int)

    args = parser.parse_args()

    ## load default config
    cfg = utils.load_cfg()

    ## get html
    htmls = []
    for i in range(args.nb_months):
        m = (args.month + i - 1) % 12 + 1  # month index, 1-based
        y = args.year if args.month + i < 13 else args.year + 1
        template = Template(cfg, y, m)
        htmls += template.gen_html()

    ## gen and save pdf
    pdfs = utils.html_to_pdf(htmls)
    utils.write_pdf(pdfs, filename=f'{args.month}-{args.year}')

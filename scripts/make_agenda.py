from agenda_template import utils
from agenda_template.month import Month
import argparse
import datetime


if __name__ == '__main__':
    ## get args
    parser = argparse.ArgumentParser(description='agenda generator')
    parser.add_argument(dest='month', help='index of month (1: jan, 12: dec)', choices=range(1, 13), type=int)
    parser.add_argument(dest='month_name', help='name of month', type=str)
    parser.add_argument(dest='year', nargs='?', help='year', default=datetime.date.today().year , type=int)

    args = parser.parse_args()


    ## load default config
    cfg = utils.load_cfg()

    ## get html
    month_template = Month(cfg, args.year, args.month, args.month_name)
    htmls = month_template.gen_html()

    ## get pdf
    pdfs = utils.html_to_pdf(htmls)

    ## write to fight
    utils.write_pdf(pdfs)

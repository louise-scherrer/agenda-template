import argparse
from agenda_template import utils
from agenda_template.week import Week
from agenda_template.month import Month


if __name__ == '__main__':
    ## get args
    parser = argparse.ArgumentParser(description='agenda generator')
    parser.add_argument(dest='month', help='month name', type=str)
    parser.add_argument(dest='d0', help='index of first day of month in week (0: monday, 6: sunday)', type=int)
    parser.add_argument(dest='nb_days', help='nb of days in the month (28-31)', type=int)

    args = parser.parse_args()


    ## load default config
    cfg = utils.load_cfg()

    ## get html
    week_template = Week(cfg)
    month_template = Month(args.month, args.nb_days, args.d0, week_template)
    htmls = month_template.gen_html()

    ## get pdf
    pdfs = utils.html_to_pdf(htmls)

    ## write to fight
    utils.write_pdf(pdfs)

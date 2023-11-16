import numpy as np
import os

def month_grid(nbdays, d0):
    """Defines an integer grid for the whole month.
    Each row defines a week, each collumn is a weekday. Cell values are the date for that day, or 0 otherwise.
    nbdays   - nb of days in the month (28-31)
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
    if grid.shape[0]%7 != 0: # if the month does not finish on a Sunday
        grid = np.concatenate([grid, np.zeros(7 - grid.shape[0] % 7)])  # add 0s to reach size k*7
    # if the month finishes on a Sunday, it it already ready to rescale
    grid = grid.reshape((-1,7)).astype(np.int32)  # rescale 1 week per row

    return grid


if __name__ == '__main__':
    ## parameters
    month_name = 'Décembre'
    nbdays = 31
    d0 = 5


    ## get folder
    folder = os.path.dirname(__file__)
    input_path = os.path.join(folder, '..', 'template')


    ## process template
    month = month_grid(nbdays, d0)
    print(month)

    for week_idx, week in enumerate(month):
        output_path = os.path.join(folder, '..', 'output', 'week' + str(week_idx))
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ## week dates
        non_zero_days_idx = np.nonzero(week)[0]
        date_start = week[non_zero_days_idx[0]]
        date_end = week[non_zero_days_idx[-1]]
        week_title = month_name + ' ' + str(date_start) + '-' + str(date_end)

        ## mon-wed
        with open(os.path.join(input_path,'lun-mer.html'), 'r') as f:
            html = f.read()
        with open(os.path.join(input_path,'style-lun-mer.css'), 'r') as f:
            css = f.read()

        html = html.replace('WEEK_DATES', week_title)
        html = html.replace('MON_DATE', 'Lun ' + str(week[0])) if week[0] else html.replace('MON_DATE', '')
        html = html.replace('TUE_DATE', 'Mar ' + str(week[1])) if week[1] else html.replace('TUE_DATE', '')
        html = html.replace('WED_DATE', 'Mer ' + str(week[2])) if week[2] else html.replace('WED_DATE', '')

        if week[0]:
            css = css.replace('ROW_1', 'lundi boulot')
        else:
            css = css.replace('ROW_1', '. .')
        if week[1]:
            css = css.replace('ROW_2', 'mardi mar_droite')
        else:
            css = css.replace('ROW_2', '. .')
        if week[2]:
            css = css.replace('ROW_3', 'mercredi mer_droite')
        else:
            css = css.replace('ROW_3', '. .')

        with open(os.path.join(output_path, 'lun-mer.html'), 'w') as f:
            f.write(html)
        with open(os.path.join(output_path, 'style-lun-mer.css'), 'w') as f:
            f.write(css)


        ## thu-sun
        with open(os.path.join(input_path, 'jeu-dim.html'), 'r') as f:
            html = f.read()
        with open(os.path.join(input_path, 'style-jeu-dim.css'), 'r') as f:
            css = f.read()

        html = html.replace('THU_DATE', 'Jeu ' + str(week[3])) if week[3] else html.replace('THU_DATE', '')
        html = html.replace('FRI_DATE', 'Ven ' + str(week[4])) if week[4] else html.replace('FRI_DATE', '')
        html = html.replace('SAT_DATE', 'Sam ' + str(week[5])) if week[5] else html.replace('SAT_DATE', '')
        html = html.replace('SUN_DATE', 'Dim ' + str(week[6])) if week[6] else html.replace('SUN_DATE', '')

        if week[3]:
            css = css.replace('ROW_1', 'jeudi boulot')
        else:
            css = css.replace('ROW_1', '. .')
        if week[4]:
            css = css.replace('ROW_2', 'vendredi ven_droite')
        else:
            css = css.replace('ROW_2', '. .')
        if week[6]:
            css = css.replace('ROW_3', 'samedi dimanche')
        elif week[5]:
            css = css.replace('ROW_3', 'samedi .')
        elif week[5]:
            css = css.replace('ROW_3', '. dimanche')
        else:
            css = css.replace('ROW_3', '. .')

        with open(os.path.join(output_path, 'jeu-dim.html'), 'w') as f:
            f.write(html)
        with open(os.path.join(output_path, 'style-jeu-dim.css'), 'w') as f:
            f.write(css)

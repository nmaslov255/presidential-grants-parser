#!/usr/bin/python3
import pandas as pd
import numpy as np

import api

def format_to_excel(rows, links, output, sheetname='noname'):
    """Just wrapper for pd.ExcelWriter
    
    Arguments:
        rows {object} -- pd.DataFrame with some data
        links {list} -- list with links to grant
        output {str} -- file for write excel table
    
    Keyword Arguments:
        sheetname {str} -- excel sheet (default: {'noname'})
    
    Returns:
        object -- pd.ExcelWriter with formated data
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    rows.to_excel(writer, sheet_name=sheetname, index=False)
    
    workbook = writer.book
    worksheet = writer.sheets[sheetname]

    rows_style = {
        'text_wrap': True,
        'valign':'top',
        'border': 1,
    }

    wrap_format = workbook.add_format({
        'fg_color': '#d6d6d6',
        **rows_style,
    })
    zebra_format = workbook.add_format({
        'fg_color': '#d7e4bc',
        **rows_style,
    })

    worksheet.set_column('A:G', None, wrap_format)
    for idrow in range(0, len(rows)+1, 2):
        worksheet.set_row(idrow, None, zebra_format)

    # set size
    worksheet.set_column('A:A', 13)
    worksheet.set_column('B:D', 50)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('F:F', 14)

    # add hyperlink
    for idrow in range(1, len(rows)+1):
        link = api.DOMAIN + links[idrow-1]
        text = rows.iloc[idrow-1][0]

        worksheet.write(idrow, 0, '=HYPERLINK("%s", "%s")' % (link, text))

    return writer
import json
import openpyxl

from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from openpyxl.styles import Alignment

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello():
    return 'Hello, World!'


@app.route('/api', methods=('GET', 'POST'))
@cross_origin()
def api():
    data = json.loads(request.data)

    wb = openpyxl.Workbook()
    ws = wb.active

    header, indexes, norms = build_columns(data['cols'])

    align_center = Alignment(wrapText=True, shrinkToFit=True, horizontal='center', vertical='center')

    header_cell = ws['A1']
    for h, n, i in zip(header, norms, range(len(header))):
        cell = header_cell.offset(0, i)
        cell.value = h
        cell.alignment = align_center

        cell = header_cell.offset(1, i)
        cell.value = n
        cell.alignment = align_center

        cell = header_cell.offset(2, i)
        cell.value = i + 1
        cell.alignment = align_center

    table_cell = ws['A4']
    row_offset = 0
    for i, table in enumerate(data['tables']):
        current_table_cell = table_cell.offset(0 + row_offset, 0)

        merge_row = current_table_cell.row
        merge_col_start = current_table_cell.column
        merge_col_end = merge_col_start + len(header) - 1
        ws.merge_cells(start_row=merge_row, start_column=merge_col_start, end_row=merge_row, end_column=merge_col_end)
        current_table_cell.value = table['header']
        current_table_cell.alignment = align_center

        for j in range(len(header)):
            current_table_cell.offset(1, 0 + 1 * j).value = j + 1
            current_table_cell.offset(1, 0 + 1 * j).alignment = align_center

        dt = table['data']
        for j, d in enumerate(dt):
            row_cell = current_table_cell.offset(2 + 1 * j, 0)
            for k, idx in enumerate(indexes):
                cell = row_cell.offset(0, 0 + 1 * k)
                cell.value = d[str(idx)]
                cell.alignment = align_center

        row_offset += len(dt) + 2

    # for row in data:
    #     ws.append(row)
    #
    # cell = ws['A1']
    # cell.alignment = Alignment(wrapText=True)

    wb.save('server\\tmp\\out.xlsx')
    return send_file('tmp\\out.xlsx', as_attachment=True)


def build_columns(columns: list):
    header_row = list()
    indexes = list()
    norms = list()

    for col in columns:
        cond = '\n' + col['condition'] if col['condition'] else ''
        header_row.append(f'{col["label"]}{cond}')
        indexes.append(col['index'])
        norms.append(col['norms'])
    return header_row, indexes, norms

import json
import openpyxl

from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

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

    for row in data:
        ws.append(row)

    wb.save('server\\tmp\\out.xlsx')
    return send_file('tmp\\out.xlsx', as_attachment=True)

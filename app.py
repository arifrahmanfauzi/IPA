from ipa import IPA
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "<h1> app started...!</h1>"


@app.route("/uji-validitas", methods=['POST'])
def uji_validitas():
    filepath = request.form.get('filepath')
    print("alamat file")
    print(filepath)
    A = request.form.get('a')
    B = request.form.get('b')
    C = request.form.get('c')
    D = request.form.get('d')
    E = request.form.get('e')
    corr_matrix = IPA.validity_test(
        file_path=filepath.replace(" ", "%20"), a=A, b=B, c=C, d=D, e=E)

    return json.dumps(corr_matrix)


@app.route('/uji-reliabilitas', methods=['POST'])
def uji_reliabilitas():
    filepath = request.form.get('filepath')
    A = request.form.get('a')
    B = request.form.get('b')
    C = request.form.get('c')
    D = request.form.get('d')
    E = request.form.get('e')

    result = IPA.uji_realibilitas(
        file_path=filepath.replace(" ", "%20"), a=A, b=B, c=C, d=D, e=E)
    return result


@app.route('/SE', methods=['POST'])
def SE():
    # file harapan
    filepath = request.form.get('file_harapan')
    calculate = IPA.SE(file_path=filepath.replace(
        " ", "%20")).to_json(orient='columns')

    result = json.loads(calculate)

    return json.dumps(result)


@app.route('/SP', methods=['POST'])
def SP():
    # file presepsi
    filepath = request.form.get('file_presepsi')
    calculate = IPA.SP(file_path=filepath.replace(
        " ", "%20")).to_json(orient='columns')

    result = json.loads(calculate)

    return json.dumps(result)


@app.route('/hasil-analisa', methods=['POST'])
def hasil_analisa():
    file_harapan = request.form.get('file_harapan').replace(
        " ", "%20")
    file_presepsi = request.form.get('file_presepsi').replace(
        " ", "%20")

    hasil = IPA.group(file_path_1=file_harapan.replace(
        " ", "%20"), file_path_2=file_presepsi.replace(" ", "%20"))

    convert = json.loads(hasil.to_json(orient='columns'))
    return json.dumps(convert)


@app.route('/sumbu', methods=['POST'])
def sumbu():
    file_harapan = request.form.get('file_harapan').replace(
        " ", "%20")
    file_presepsi = request.form.get('file_presepsi').replace(
        " ", "%20")
    hasil = IPA.kuadran(file_harapan, file_presepsi)

    return json.dumps(json.loads(hasil.to_json(orient="columns")))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

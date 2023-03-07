from flask import Flask, request
from flask import send_file
import os
from run import pred

app = Flask(__name__)

# diretório onde as imagens serão salvas
UPLOAD_FOLDER = 'img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # verifique se o arquivo está presente na solicitação
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado'
    
    file = request.files['file']
    
    # verifique se o nome do arquivo está vazio
    if file.filename == '':
        return 'Nome do arquivo vazio'
    
    # salve o arquivo em disco
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    img = file.filename
    
    nimg = pred.main(img)
    return send_file(nimg, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
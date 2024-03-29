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
    
    # caso queira salvar todas as imagens que são recebidas e so comentar a proxima linha
    file.filename = 'imagem.jpg'
    
    # salve o arquivo em disco
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    img = file.filename
    
    nimg = pred.main(img)
    return send_file(nimg, mimetype='image/jpg')

@app.route('/teste', methods=['GET'])
def teste():
    return "msg: funcionou"

if __name__ == '__main__':
    app.run()

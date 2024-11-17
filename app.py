from flask import Flask, render_template, abort , Response, request, url_for, redirect
import cv2 
from lectorMano import *
import mediapipe as mp
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grupo')
def pag1():
    return render_template('grupo.html')

@app.route('/jugar')
def pag2():
    return render_template('jugar.html')

@app.route('/letras')
def pag3():
    return render_template('letras.html')

@app.route('/selcNivel')
def pag4():
    return render_template('selecNivel.html')

@app.route('/redirect', methods=['POST'])
def redirect_level():
    nivel = request.form.get('nivel')
    if nivel == 'principiante':
        return redirect(url_for('pag5'))
    elif nivel == 'intermedio':
        return redirect(url_for('pag6'))
    elif nivel == 'avanzado':
        return redirect(url_for('pag7'))
    else:
        return redirect(url_for('index'))

@app.route('/nivelPri')
def pag5():
    return render_template('nivelPri.html')

@app.route('/nivelMed')
def pag6():
    return render_template('nivelMed.html')

@app.route('/nivelAvan')
def pag7():
    return render_template('nivelAvan.html')

@app.route('/simular')
def pag8():
    return render_template('simular.html')

# Instancia de la clase Camara
camara = Camara()

# Generador de fotogramas para transmisión
def GenFrame():
    while True:
        # Captura el fotograma
        ret, frame = camara.captura.read()
        if not ret:
            break
        
        # Modo espejo
        frame = cv2.flip(frame, 1)

        # Procesar el frame con la clase Camara
        frame = camara.ProcesarFrame(frame)

        # Codificar el frame en formato JPEG
        suc, encode = cv2.imencode('.jpg', frame)
        frame = encode.tobytes()
        
        # Enviar el frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(GenFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(debug=False)
    finally:
        camara.FinalizarCaptura()
        cv2.destroyAllWindows()

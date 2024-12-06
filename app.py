from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
from lectorMano import *
from detectorVocal import *
import time
from threading import Lock

app = Flask(__name__)
app.config['DEBUG'] = True

# Variables globales
camara = None
camera_active = False

# Crear un Lock global
camara_lock = Lock()

def GenerarFrame():
    global camara
    while True:
        with camara_lock:
            if camara and camera_active:
                ret, frame = camara.captura.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)  # Modo espejo
                frame = camara.ProcesarFrame(frame)
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    frame_bytes = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)

# Ruta para alternar la cámara
@app.route('/toggle_camera', methods=['POST'])
def toggle_camera():
    global camera_active, camara
    if camera_active:
        camera_active = False
        if camara:
            camara = None
        print("Cámara desactivada")
    else:
        camera_active = True
        camara = Camara()
        print("Cámara activada")
    return jsonify({"camera_active": camera_active})

# Ruta para apagar la cámara automáticamente al salir de la página
@app.route('/toggle_camera_off', methods=['POST'])
def toggle_camera_off():
    global camera_active, camara
    if camera_active:
        camera_active = False
        if camara:
            camara = None
        print("Cámara apagada automáticamente al salir de la página")
    return jsonify({"camera_active": camera_active})

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

@app.route('/video')
def video():
    global camera_active
    if not camera_active:
        return jsonify({"error": "La cámara no está activa"}), 503
    return Response(GenerarFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_status')
def camera_status():
    return jsonify({"camera_ready": camera_active})

if __name__ == '__main__':
    app.run(debug=False)

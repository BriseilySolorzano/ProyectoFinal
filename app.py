from flask import Flask, render_template, Response, request, redirect, url_for
from lectorMano import *
import mediapipe as mp
import cv2
import time
from threading import Lock

app = Flask(__name__)
app.config['DEBUG'] = True

# Variables globales
camara = None
camera_active = False

# Clase de cámara
class Camara:
    def __init__(self, cam_id=0):
        self.captura = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)  # Usamos CAP_DSHOW en lugar de MSMF
        if not self.captura.isOpened():
            raise ValueError("No se pudo acceder a la cámara")

    def procesar_frame(self, frame):
        # Aquí puedes agregar procesamiento adicional al frame si es necesario
        return frame

    def finalizar_captura(self):
        if self.captura.isOpened():
            self.captura.release()



# Crear un Lock global
camara_lock = Lock()

def gen_frame():
    global camara
    while True:
        with camara_lock:  # Asegura que solo un hilo acceda a la cámara a la vez
            if camara and camera_active:
                ret, frame = camara.captura.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)  # Modo espejo
                frame = camara.procesar_frame(frame)
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    frame_bytes = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)
 

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
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Ruta para alternar la cámara
@app.route('/toggle_camera/<page>', methods=['POST'])
def toggle_camera(page):
    global camera_active, camara
    if camera_active:
        # Desactivar cámara
        camera_active = False
        if camara:
            camara.finalizar_captura()
            camara = None
        print("Cámara desactivada")
    else:
        # Activar cámara
        camera_active = True
        camara = Camara()  # Iniciar la cámara
        print("Cámara activada")
    
    # Redirigir a la misma página en la que estaba
    return redirect(url_for(page))  # Redirige a la página actual

if __name__ == '__main__':
    
    app.run(debug=False)

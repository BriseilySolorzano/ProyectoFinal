from flask import Flask, render_template, abort , Response
import cv2 
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

@app.route('/nivelPri')
def pag5():
    return render_template('nivelPri.html')

@app.route('/simular')
def pag6():
    return render_template('simular.html')

class OpenCV:
    def __init__(self):
        # Inicia la captura de video
        self.captura = cv2.VideoCapture(0)

        # Verificar si la cámara está disponible
        if not self.captura.isOpened():
            print("No se pudo abrir la cámara")
            exit()

    def ProcesarFrame(self, frame):
        # Dimensiones de imagen
        alto, ancho, _ = frame.shape

        # Área a leer (rectángulo de detección)
        inicio_x = int(0.6 * ancho)
        inicio_y = int(0.25 * alto)
        fin_x = int(0.9 * ancho)
        fin_y = int(0.75 * alto)

        # Dibujar rectángulo en el frame
        cv2.rectangle(frame, (inicio_x, inicio_y), (fin_x, fin_y), (255, 0, 0), 2)
        return frame

    def liberar_captura(self):
        # Libera la captura de video
        self.captura.release()

# Instancia de la clase OpenCV
opencv = OpenCV()

# Generador de fotogramas para transmisión
def gen_frame():
    while True:
        # Captura el fotograma
        ret, frame = opencv.captura.read()
        if not ret:
            break
        
        # Modo espejo
        frame = cv2.flip(frame, 1)

        # Procesar el frame con la clase OpenCV
        frame = opencv.ProcesarFrame(frame)

        # Codificar el frame en formato JPEG
        suc, encode = cv2.imencode('.jpg', frame)
        frame = encode.tobytes()
        
        # Enviar el frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(debug=False)
    finally:
        opencv.liberar_captura()
        cv2.destroyAllWindows()

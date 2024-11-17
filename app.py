from flask import Flask, render_template, abort , Response
import cv2 
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

@app.route('/nivelPri')
def pag5():
    return render_template('nivelPri.html')

@app.route('/simular')
def pag6():
    return render_template('simular.html')

class OpenCV:
    def __init__(self, max_num_hands=1, min_detection_confidence=0.9):
        # Inicializar Mediapipe y sus utilidades de dibujo
        self.mp_mano = mp.solutions.hands
        self.mano = self.mp_mano.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence
        )
        self.mp_dibujo = mp.solutions.drawing_utils
        self.captura = cv2.VideoCapture(0)

        # Verificar si la cámara está disponible
        if not self.captura.isOpened():
            exit()

    def ProcesarFrame(self, frame):
        # Dimensiones de imagen
        self.alto, self.ancho, _ = frame.shape
        
        # Convertir el frame a RGB para Mediapipe
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = self.mano.process(color)

        if resultado.multi_hand_landmarks:
            for mano_landmarks in resultado.multi_hand_landmarks:
                # Obtener la coordenada central de la mano (punto 9)
                pto_i5 = mano_landmarks.landmark[9]
                cx, cy = int(pto_i5.x * self.ancho), int(pto_i5.y * self.alto)

                # Definir el área del rectángulo
                x1, y1 = max(0, cx - 100), max(0, cy - 100)
                x2, y2 = min(self.ancho, x1 + 200), min(self.alto, y1 + 200)

                # Dibujar el área de seguimiento
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Dibujar solo los puntos y líneas dentro del rectángulo
                for conexion in self.mp_mano.HAND_CONNECTIONS:
                    p1, p2 = conexion
                    punto1 = mano_landmarks.landmark[p1]
                    punto2 = mano_landmarks.landmark[p2]

                    # Convertir coordenadas normalizadas a píxeles
                    px1, py1 = int(punto1.x * self.ancho), int(punto1.y * self.alto)
                    px2, py2 = int(punto2.x * self.ancho), int(punto2.y * self.alto)

                    if (x1 <= px1 <= x2 and y1 <= py1 <= y2) and (x1 <= px2 <= x2 and y1 <= py2 <= y2):
                        # Dibujar la conexión
                        cv2.line(frame, (px1, py1), (px2, py2), (0, 255, 255), 2)

                # Dibujar puntos individuales dentro del rectángulo
                for punto in mano_landmarks.landmark:
                    px, py = int(punto.x * self.ancho), int(punto.y * self.alto)
                    if x1 <= px <= x2 and y1 <= py <= y2:
                        cv2.circle(frame, (px, py), 3, (255, 0, 0), -1)
        return frame

    def FinalizarCaptura(self):
        # Finalizar la captura de video
        self.captura.release()

# Instancia de la clase OpenCV
opencv = OpenCV()

# Generador de fotogramas para transmisión
def GenFrame():
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
    return Response(GenFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(debug=False)
    finally:
        opencv.FinalizarCaptura()
        cv2.destroyAllWindows()

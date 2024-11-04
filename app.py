from flask import Flask, render_template, abort , Response
import cv2
import mediapipe as mp
mp_mano = mp.solutions.hands
mano = mp_mano.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.9)
mp_dibujo = mp.solutions.drawing_utils

app = Flask(__name__)
app.config['DEBUG'] = True

# Inicializar la cámara
captura = cv2.VideoCapture(0)
if not captura.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

def generate():
    while True:
        # Captura el frame
        ret, frame = captura.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        alto, ancho, _ = frame.shape
        
        inicio_x = int(0.6 * ancho)
        inicio_y = int(0.25 * alto)
        fin_x = int(0.9 * ancho)
        fin_y = int(0.75 * alto)
        
        color = (255, 0, 0)
        grosor = 2
        cv2.rectangle(frame, (inicio_x, inicio_y), (fin_x, fin_y), color, grosor)
        
        recorte = frame[inicio_y:fin_y, inicio_x:fin_x]
        recorte_rgb = cv2.cvtColor(recorte, cv2.COLOR_BGR2RGB)
        resultado = mano.process(recorte_rgb)

        if resultado.multi_hand_landmarks:
            for mano_landmarks in resultado.multi_hand_landmarks:
                mp_dibujo.draw_landmarks(
                    recorte,
                    mano_landmarks,
                    mp_mano.HAND_CONNECTIONS,
                    mp_dibujo.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                    mp_dibujo.DrawingSpec(color=(0, 255, 255), thickness=2)
                )
        
        frame[inicio_y:fin_y, inicio_x:fin_x] = recorte
        cv2.imshow('Camara', frame)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/cam')
def cam():
    return render_template('cam.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Asegúrate de liberar la cámara al cerrar la aplicación
@app.teardown_appcontext
def cleanup(exception):
    captura.release()
    cv2.destroyAllWindows()


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

if __name__ == '__main__':
    app.run()
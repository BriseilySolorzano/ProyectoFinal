from flask import Flask, render_template, abort , Response
import cv2

app = Flask(__name__)
app.config['DEBUG'] = True

# Inicializar la cámara
cap = cv2.VideoCapture(0)

def generate():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el frame")
            break
        
        # Codifica el frame en formato JPEG
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
    cap.release()


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
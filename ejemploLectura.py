import cv2
import mediapipe as mp

class DetectorManos:
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
            #print("No se pudo abrir la cámara")
            exit()

    def ProcesarFrame(self, frame):
        # Dimensiones de imagen
        alto, ancho, _ = frame.shape

        # Mano derecha
        if ("""cv2.waitKey(1) == 82 or cv2.waitKey(1) == 114"""):
            # Área a leer (rectángulo de detección)
            inicio_x = int(0.6 * ancho)
            inicio_y = int(0.25 * alto)
            fin_x = int(0.9 * ancho)
            fin_y = int(0.75 * alto)
        # Mano izquierda
        elif ("""cv2.waitKey(1) == 76 or cv2.waitKey(1) == 108"""):
            # Área a leer (rectángulo de detección)
            inicio_x = int(0.1 * ancho)
            inicio_y = int(0.25 * alto)
            fin_x = int(0.4 * ancho)
            fin_y = int(0.75 * alto)

        # Dibujar rectángulo en el frame
        cv2.rectangle(frame, (inicio_x, inicio_y), (fin_x, fin_y), (255, 0, 0), 2)

        # Recortar la sección a analizar
        recorte = frame[inicio_y:fin_y, inicio_x:fin_x]

        # Convertir el recorte de BGR a RGB
        recorte_rgb = cv2.cvtColor(recorte, cv2.COLOR_BGR2RGB)

        # Procesar la imagen con Mediapipe
        resultado = self.mano.process(recorte_rgb)

        # Dibujar landmarks si se detecta una mano
        if resultado.multi_hand_landmarks:
            for mano_landmarks in resultado.multi_hand_landmarks:
                self.mp_dibujo.draw_landmarks(
                    recorte,
                    mano_landmarks,
                    self.mp_mano.HAND_CONNECTIONS,
                    self.mp_dibujo.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                    self.mp_dibujo.DrawingSpec(color=(0, 255, 255), thickness=2)
                )

        # Volver a insertar el recorte procesado en el frame completo
        frame[inicio_y:fin_y, inicio_x:fin_x] = recorte

        return frame

    def Iniciar(self):
        while True:
            ret, frame = self.captura.read()
            if not ret:
                #print("No se pudo recibir el frame (finalización del flujo)")
                break

            # Modo espejo
            frame = cv2.flip(frame, 1)

            # Procesar el frame y obtener el frame con las manos detectadas
            frame = self.ProcesarFrame(frame)

            # Mostrar frame
            cv2.imshow('Camara', frame)

            # Cerrar al presionar "Esc" (código ASCII = 27)
            if cv2.waitKey(1) == 27:
                break

        # Finalizar captura y cerrar ventanas
        self.captura.release()
        cv2.destroyAllWindows()
        
# Crear una instancia y ejecutar la detección
if __name__ == "__main__":
    detector_manos = DetectorManos()
    detector_manos.Iniciar()
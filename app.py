import dash
from dash import dcc
import dash_labs as dl
import dash_bootstrap_components as dbc
from flask import Flask, Response
import cv2
import pages.mediapipe_wrapper as mpu
import mediapipe as mp
import sys

#Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

holistic_instance = mpu.MediapipeHolistic()
landmarks_now = None

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global global_frame
        success, image = self.video.read()
        # print(success)
        global_frame = image.copy()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), global_frame

    def delete(self):
        self.video.release()
        cv2.destroyAllWindows()

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)

navbar = dbc.NavbarSimple(
    dbc.Button("HOME", color="secondary", className="me-1", href="/"),
    brand="Learn Spanish Sign Language",
    color="primary",
    dark=True,
    className="mb-2",
)


app.layout = dbc.Container(
    [
        dcc.Store(id='store-user-performance',data={'real':[],'pred':[]}),#, 'times':[]}),
        navbar,
        dbc.Row(
            [
                #dbc.Col([sidebar_button], width=1),
                dbc.Col([dl.plugins.page_container]),
            ]
        ),
        dcc.Interval('interval', interval=50,n_intervals=0),
        dcc.Store('stored-landmarks',data=None),
    ],
    fluid=True,
)


def gen_last_frame(camera):
    """
    Get actual frame and process image to obtain mediapipe landmarks.

    :param camera: camera from which the frames are recorded
    :type camera: app.VideoCamera()
    """
    # global global_frame
    # global landmarks_now
    # global visible_right_hand
    while True:
        frame, global_frame = camera.get_frame()

        holistic_instance.process_image(global_frame)
        

        #image_hight, image_width, _ = global_frame.shape
        # Convert the BGR image to RGB before processing.
        results = holistic_instance.results_holistic
        # results = holistic.process(cv2.cvtColor(global_frame, cv2.COLOR_BGR2RGB))

        # Draw pose, left and right hands, and face landmarks on the image.
        annotated_image = global_frame.copy()
        mp_drawing.draw_landmarks(
            annotated_image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
        mp_drawing.draw_landmarks(
            annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        
        # Save right hand landmaks in landmarks_now variable.
        if (holistic_instance.there_is_right_hand()):
            landmarks_now = holistic_instance.landmarks_to_array("RIGHT",flatten=False)
        else:
            landmarks_now = None #np.empty(shape=(21*3))

        import global_
        #landmarks = landmarks_now
        global_.landmarks = landmarks_now
        #global_.frame = frame #global_frame

        # gray_frame = cv2.cvtColor(global_frame, cv2.COLOR_BGR2GRAY)
        ret, jpeg = cv2.imencode('.jpg', annotated_image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@server.route('/user/configurations/video_mediapipe_feed')
def video_mediapipe_feed():
    """
    Show what is being recorded by the camera, along with the landmarks obtained with mediapipe
    """
    return Response(gen_last_frame(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    host_address = "127.0.0.1"
    if len(sys.argv) > 1:
        host_address = sys.argv[1]
    app.run_server(host=host_address, debug=True)


import pickle as pkl
import base64

landmarks = None
frame = None

configurations = ['{}'.format(x) for x in range(1,43)]

medoids = pkl.load(open('dataset/configs/itsaso_newCam_allMEDOIDS.pkl','rb'))
fingers = ['thumb','index','middle','ring','pinky']

figures_medoids = pkl.load(open('dataset/configs/itsaso_newCam_allMEDOIDS_GRAPHS.pkl','rb'))

pngs = ['data:image/png;base64,{}'.format(base64.b64encode(open("dataset/configs/img/"+config+".png", 'rb').read()).decode()) for config in configurations]
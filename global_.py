import pickle as pkl
import base64
import pandas as pd

landmarks_right = None
landmarks_left = None
index = 0

configurations = ['{}'.format(x) for x in range(1,43)]

medoids = pkl.load(open('dataset/configs/itsaso_newCam_allMEDOIDS.pkl','rb'))
fingers = ['thumb','index','middle','ring','pinky']

figures_medoids = pkl.load(open('dataset/configs/itsaso_newCam_allMEDOIDS_GRAPHS.pkl','rb'))

pngs = ['data:image/png;base64,{}'.format(base64.b64encode(open("dataset/images_configs/"+config+".png", 'rb').read()).decode()) for config in configurations]

signs_table = pd.read_csv('dataset/signos.csv')
styles =[
        {'height':'50%', 'width':'50%','margin-left':'20px','border':'2px green solid','backgroundColor':'#E0F2F2','padding':'10px'},
        {'height':'50%', 'width':'50%','margin-left':'20px','border':'2px red solid','backgroundColor':'#EF989F','padding':'10px'},
        {'height':'50%', 'width':'50%','margin-left':'20px','padding':'10px'}
    ]
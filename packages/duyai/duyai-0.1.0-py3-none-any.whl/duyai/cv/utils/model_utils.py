from keras.models import load_model
import requests
import os
import gdown
import cv2
from mtcnn.mtcnn import MTCNN
import dlib


model_dir = os.path.join(os.path.expanduser('~'), '.duyai/model')

def load_facenet():
    if os.path.exists(model_dir + '/facenet_keras.h5') == False:
        url = 'https://doc-0g-as-docs.googleusercontent.com/docs/securesc/tci63hehv11635afjcn7m3tnpu9hlali/vb8omffbop947esu8jef16h3dmtia3mg/1618904925000/09379222848295305915/11667359070381130856/1PZ_6Zsy1Vb0s0JmjEmVd8FS99zoMCiN1?e=download&authuser=0&nonce=o6pjdp36j4arc&user=11667359070381130856&hash=77eg9dp7s9pigi8g12bhtnicbmqk5fgp'
        r = requests.get(url, allow_redirects=True)
        open(model_dir + '/facenet_keras.h5', 'wb').write(r.content)
    
    return load_model(model_dir + '/facenet_keras.h5')

def load_ssd_model():
    if os.path.exists(model_dir + '/res10_ssd.caffemodel') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=1p-O44DtUUO5lzmACFHhMAtaIfGQL2Fj_&export=download', model_dir + '/res10_ssd.caffemodel', quiet=False)

    if os.path.exists(model_dir + '/deploy.prototxt') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=1iO2O5Fuvx_G9VMyCyj3nxGI_WJnRHKci&export=download', model_dir + '/deploy.prototxt', quiet=False)
    
    return cv2.dnn.readNetFromCaffe(model_dir + '/deploy.prototxt', model_dir + '/res10_ssd.caffemodel')

def load_mtcnn_model():
    return MTCNN()

def load_dlib_hog():
    return dlib.get_frontal_face_detector()

def load_dlib_68_landmark():
    if os.path.exists(model_dir + '/shape_predictor_68_face_landmarks.dat') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=1IZZGRwUQvCX6_Dvbmc4T-bHthD_Isj-p&export=download', model_dir + '/shape_predictor_68_face_landmarks.dat', quiet=False)
    
    return dlib.shape_predictor(model_dir + '/shape_predictor_68_face_landmarks.dat')

def get_deepsort():
    if os.path.exists(model_dir + '/mars_deepsort.pb') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=1iSMmGwDHhQcYCaFxgwES8Xs7OM_iL9Ns&export=download', model_dir + '/mars_deepsort.pb', quiet=False)

def get_yolov3():
    if os.path.exists(model_dir + '/yolo3') == False:
        os.mkdir(model_dir + '/yolo3')

    if os.path.exists(model_dir + '/yolo3/yolov3.h5') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=1Y1d5Db9_AE4Udn4IVrVkyt-eSx2taGda&export=download', model_dir + '/yolo3/yolov3.h5', quiet=False)
    
    if os.path.exists(model_dir + '/yolo3/yolo_anchors.txt') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=17yA6ewzD8Zw-G05URC5kxvHer2tzyEVc&export=download', model_dir + '/yolo3/yolo_anchors.txt', quiet=False)
    
    if os.path.exists(model_dir + '/yolo3/coco_classes.txt') == False:
        gdown.download('https://drive.google.com/u/0/uc?id=1YRSDhZ2j9Y08vO6a2CMYi7umtOJHcwhG&export=download', model_dir + '/yolo3/coco_classes.txt', quiet=False)



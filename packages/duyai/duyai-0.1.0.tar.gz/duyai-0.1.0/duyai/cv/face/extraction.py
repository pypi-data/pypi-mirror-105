from ..utils import model_utils

facenet_model = None
def facenet_ext(face):
    global facenet_model
    if facenet_model is None:
        facenet_model = model_utils.load_facenet()
    face_img = cv2.resize(face, (160,160)).astype('float32')
    mean, std = face_img.mean(), face_img.std()
    face_pixels = (face_img - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    yhat = facenet_model.predict(samples)[0]
    return yhat

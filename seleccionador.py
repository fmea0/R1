import tensorflow as tf
import numpy as np
import cv2


model_p = "E:/robotica/frozen_inference_graph.pb"#cambiar direccion
min_threshold = 0.5
model = tf.Graph()
sess=[]
def init(min_score=min_threshold,path_m="frozen_inference_graph.pb"):
    global model_p,min_threshold,model,sess
    min_threshold=min_score;model_p=path_m;
    with model.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(model_p, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    sess = tf.Session(graph=model)


def is_in_size_range(w,W):
    global  min_b_x,max_b_x
    print("w/W={0}".format(w / W))
    if((w/W)>min_b_x and (w/W)<max_b_x):
        return True
    return False


def get_body_cropped(image):
    global model,min_threshold,sess

    frame = image.copy()[:,:,::-1]
    rois, rects,classs, err = _get_body_cropped_(frame, min_threshold,model, sess)
    return rois,rects,classs,err

def _get_body_cropped_(image,MIN_CON,model,sess):
    imp = image.copy()
    image_tensor = model.get_tensor_by_name('image_tensor:0')
    detection_boxes =model.get_tensor_by_name('detection_boxes:0')
    detection_scores = model.get_tensor_by_name('detection_scores:0')
    detection_classes = model.get_tensor_by_name('detection_classes:0')
    num_detections = model.get_tensor_by_name('num_detections:0')
    (im_width, im_height, ch) = image.shape
    image_np = np.array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                             feed_dict={image_tensor: image_np_expanded})
    rects = []
    faces_en = []
    classs=[]
    for k, score in enumerate(scores[0]):
        if (score >= MIN_CON):
            if (classes[0][k] in [1,2,3,4,5,6]):#nombre de las etiquetas
                YMIN = a0 = boxes[0][k][0] * im_width
                YMAX = a2 = boxes[0][k][2] * im_width
                XMIN = a1 = boxes[0][k][1] * im_height
                XMAX = a3 = boxes[0][k][3] * im_height
                Roi = imp[int(YMIN):int(YMAX), int(XMIN):int(XMAX)]
                classs.append(classes[0][k])
                faces_en.append(Roi.copy())
                rects.append([int(XMIN), int(YMIN), int(XMAX), int(YMAX)])
    return faces_en,rects,classs,False

import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load YOLO model
def load_yolo_model():
    net = cv2.dnn.readNetFromDarknet('./yolov3_tiny/yolov3.cfg', './yolov3_tiny/yolov3-tiny.weights')
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return net, output_layers

yolo_net, yolo_output_layers = load_yolo_model()

# List of COCO dataset class labels for YOLO
with open("./yolov3_tiny/coco.names", "r") as f:
    yolo_labels = f.read().strip().split("\n")

# Process image and detect objects
def detect_objects(image):
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
    yolo_net.setInput(blob)
    detections = yolo_net.forward(yolo_output_layers)
    
    h, w = image.shape[:2]
    detected_objects = []

    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.5:
                box = detection[0:4] * np.array([w, h, w, h])
                center_x, center_y, width, height = box.astype("int")
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)
                
                detected_objects.append({
                    "label": yolo_labels[class_id],
                    "accuracy": float(confidence),
                    "rectangle": {"left": x, "top": y, "width": int(width), "height": int(height)}
                })

    return detected_objects

# Endpoint to receive image upload
@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    image_id = data['id']
    image_data = data['image']

    # Decode the image from base64
    image_binary = base64.b64decode(image_data)
    image_np = np.frombuffer(image_binary, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    
    # Detect objects in the image
    objects = detect_objects(image)

    # Return detected objects in JSON format
    response = {
        "id": image_id,
        "objects": objects
    }
    return jsonify(response)

if __name__ == '__main__':
    # Start Flask server on a port over 1024
    app.run(threaded=True)

# Model detection object violent yolov4 


## Add file weights model yolov4
* Download the next link https://drive.google.com/file/d/1--i7ZBiikRYf7bJPahOvHGPS4FZEqFBK/view?usp=sharing
* Copy this file into "config_files"
## Add image to detect(optional: using script)
Add image in folder "imagenes"
## Change docker-compose.yml (optional: using script)
    command: python3 /model/yolov4/modelo_final_yolo_v4.py --path_image /model/yolov4/data/images/{name_image_to_detect}.jpeg
* name_image: image name to detect with model yolov4
## How to build
    docker-compose build
## How to run
    docker-compose up
## Service flask
* Send a request POST to Flask server with form-data {key: file, value: image_format_jpeg}
* The response will be a json with the detection:
```json
  {
    "detected_objects": [
        {
            "confidence": "99.05",
            "object": "ELN",
            "square_points": [
                237.24298095703125,
                215.18943786621094,
                78.37574005126953,
                101.86001586914062
            ]
        }
    ],
    "image_name": "imagen_95",
    "quantity_objects": {
        "ELN": 1,
        "FARC-EP": 0,
        "bala": 0,
        "balas": 0,
        "carros guerra": 0,
        "cruz roja": 0,
        "defensoria pueblo": 0,
        "escopeta": 0,
        "jesus santrich": 0,
        "metralleta": 0,
        "mono jojoy": 0,
        "paloma paz": 0,
        "pistola": 0,
        "tirofijo": 0,
        "uniforme ejercito": 0
    }
}


# login-system-NBC

For this app I use python and flask, like database motor I use postgres. I integrate all app in a containers with docker.
## Add file weights model yolov4
* Download the next link https://drive.google.com/file/d/1--i7ZBiikRYf7bJPahOvHGPS4FZEqFBK/view?usp=sharing
* Copy this file into "config_files"
## Add image to detect
Add image in folder "imagenes"
## Change docker-compose.yml
    command: python3 /model/yolov4/modelo_final_yolo_v4.py --path_image /model/yolov4/data/images/{name_image_to_detect}.jpeg
* name_image: image name to detect with model yolov4
## How to build
    docker-compose build
## How to run
    docker-compose up
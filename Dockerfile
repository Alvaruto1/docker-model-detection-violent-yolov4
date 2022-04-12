FROM gmontamat/python-darknet:cpu AS darknet


RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install git -y


# creating folders
WORKDIR /model/yolov4/data/images
WORKDIR /model/yolov4/cfg

# init files module
RUN touch /model/__init__.py
RUN touch /model/yolov4/__init__.py

# add config files
ADD config_files/yolov4-custom.cfg /model/yolov4/cfg/
ADD config_files/obj.* /model/yolov4/data/
ADD config_files/yolov4-custom_best.weights /model/yolov4/data/

# add script python
ADD modelo_final_yolo_v4.py /model/yolov4/

# test images
ADD imagenes/* /model/yolov4/data/images/

# install libraries python
ADD requirements.txt /
WORKDIR /
RUN python3 -m pip install -r ./requirements.txt


#FROM gmontamat/python-darknet:cpu

#COPY --from=darknet /model /model
#COPY --from=darknet /root/.local /root/.local

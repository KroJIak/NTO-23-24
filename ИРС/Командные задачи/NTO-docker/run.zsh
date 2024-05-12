sudo xhost +local:docker > /dev/null || true
sudo docker run -d -it --rm \
    -v /etc/localtime:/etc/localtime:ro \
    -e "DISPLAY" \
    -e "QT_X11_NO_MITSHM=1" \
    -e XAUTHORITY \
    -v ./workspace/:/workspace/ \
    --net=host \
    --privileged \
    -v /dev:/dev \
    -v .:/app \
    --name nto-irs-container nto-irs-image
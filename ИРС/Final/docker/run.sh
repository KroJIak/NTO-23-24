rm -r solution/images
mkdir solution/images
xhost +local:docker > /dev/null
docker compose up --build

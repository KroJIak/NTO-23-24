from docker.solution.aruco import findArucoMarkers, detectAruco
from camera import Camera

camera = Camera(0)

markerCorners, markerIds = findArucoMarkers(camera, show=True)
arucoPositions = detectAruco(camera.read(), markerCorners, markerIds, threshold=50)
print(arucoPositions)
# color-detector-node-red
Detector de productos de diferente color usando OpenCV, node-red, y conexión a base de datos.
Mediante un Raspberry Pi con cámara (RaspiCam V2) se detecta cuando pasa un producto de determinado color, el cual es contado y enviado vía MQTT a un flujo de node-red, en el cual la data se procesa para una base de datos (en el mismo Rpi) y visualización en un dashboard.



## Detección de color
Se necesita para ello  la librería de opencv en python y numpy. Se calibró la detección de color en HSV con el script `capture_color.py`



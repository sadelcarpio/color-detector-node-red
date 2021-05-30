# color-detector-node-red
Detector de productos de diferente color usando OpenCV, node-red, y conexión a base de datos.
Mediante un Raspberry Pi con cámara (RaspiCam V2) se detecta cuando pasa un producto de determinado color, el cual es contado y enviado vía MQTT a un flujo de node-red, en el cual la data se procesa para una base de datos (en el mismo Rpi) y visualización en un dashboard.

<img src=https://github.com/sadelcarpio/color-detector-node-red/blob/main/imgs/rpi.jpeg>

## Detección de color
Se necesita para ello  la librería de opencv en python y numpy. Se calibró la detección de color en HSV con el script `capture_color.py`. Por ahora solo en color verde y rosado.
Luego en el script `detect_and_frame.py` se trabaja en la detección de los colores calibrados además de publicar en MQTT y mostrar en el display.

## Display
El display es opcional, el driver puede instalarse en el Raspberry Pi de este repositorio: https://github.com/the-raspberry-pi-guy/lcd
También hay un tutorial de YT: https://www.youtube.com/watch?v=3XLjVChVgec
Luego de eso con la librería `drivers` se puede trabajar con el LCD por I2C en los pines SDA/SCL.

## Flujo de nodered
El flujo de se encuentra en un archivo .json el cual puede ser importado a node-red. Los módulos necesarios fueron `node-red-dashboard` y `node-red-node-mysql`.
Básicamente se adapta la data para pasarla a una base de datos en servidor local. 

<img src=https://github.com/sadelcarpio/color-detector-node-red/blob/main/imgs/flow.jpeg>

## Base de datos
En el script `CONTEO.sql` se encuentra la creación de la base de datos y la tabla en la cual llenar la información: fecha y valores contados.
En mysql:
`mysql> source /ruta/de/archivo/CONTEO.sql`
para ejecutarlo.
Se usó phpMyAdmin para exportar la tabla en formato .csv y se muestra una prueba de ello en `CONTEO.csv`

## Mejoras
* Mejorar el código para soportar más clases de manera más eficiente.
* Automatizar el proceso de inicio del programa, por algún callback usando una red LPWAN como Sigfox.
* Pasar los datos a un servicio de almacenamiento en la nube.
* Mejorar la eficiencia de detección de color, o probar una detección por CNN.


import cv2 as cv
import numpy as np
import paho.mqtt.publish as publish
import drivers

# Rangos de detección en HSV
green_range_low = np.array([20, 0, 108])
green_range_high = np.array([88, 51, 183])
pink_range_low = np.array([157, 50, 140])
pink_range_high = np.array([180, 110, 220])

# contador de productos
count = {'Pink': 0, 'Green': 0}
display = drivers.Lcd()
display.lcd_display_string("*** Deteccion de", 1)
display.lcd_display_string("colores :3***", 2)


def frame_and_publish(src):
    global x_prev, count
    src_hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    mask = {'Pink': cv.inRange(src_hsv, pink_range_low, pink_range_high),
            'Green': cv.inRange(src_hsv, green_range_low, green_range_high)}
    poly_approx = {'Pink': [], 'Green': []}

    for color in count:
        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        i = 0
        for contour in contours:
            area = cv.contourArea(contour)
            if area > 12000:
                perimeter = cv.arcLength(contour, True)
                poly_approx[color].append(cv.approxPolyDP(contour, 0.02 * perimeter, True))
                x, y, w, h = cv.boundingRect(poly_approx[color][i])
                if x == 0 and x_prev != 0:
                    count[color] += 1
                    publish.single("data", "Pink: {}".format(count['Pink']), hostname="192.168.1.17")
                    publish.single("data", "Green: {}".format(count['Green']), hostname="192.168.1.17")
                    display.lcd_clear()
                    display.lcd_display_string("Rosados: {}".format(count['Pink']), 1)
                    display.lcd_display_string("Verdes: {}".format(count['Green']), 2)
                # cv.drawContours(dst, poly_approx, i, (0, 0, 255), 2)
                # cv.rectangle(dst, (x, y), (x + w, y + h), (0, 255, 0), 1)
                # cv.putText(dst, 'Pink: {}'.format(count[color]), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv.LINE_AA)
                i += 1  # el i solo avanza para los contornos que se deben dibujar
                x_prev = x
    return x_prev


# def frame_and_publish(src):
#     global x_prev, count
#     # RETR_EXTERNAL arroja solo el contorno externo de la figura
#     # CHAIN_APPROX_NONE hace que al graficar se vea las lineas
#     src_hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
#     mask_p = cv.inRange(src_hsv, pink_range_low, pink_range_high)
#     mask_g = cv.inRange(src_hsv, green_range_low, green_range_high)
#     poly_approx_p = []
#     ip = 0
#     contours_p, hierarchy_p = cv.findContours(mask_p, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#
#     for contour in contours_p:
#         area = cv.contourArea(contour)
#         if area > 12000:
#             perimeter = cv.arcLength(contour, True)
#             poly_approx_p.append(cv.approxPolyDP(contour, 0.02 * perimeter, True))
#             x, y, w, h = cv.boundingRect(poly_approx_p[ip])
#             if x == 0 and x_prev != 0:
#                 count['Pink'] += 1
#                 publish.single("data", "Pink: {}".format(count['Pink']), hostname="192.168.1.17")
#                 publish.single("data", "Green: {}".format(count['Green']), hostname="192.168.1.17")
#                 display.lcd_clear()
#                 display.lcd_display_string("Rosados: {}".format(count['Pink']), 1)
#                 display.lcd_display_string("Verdes: {}".format(count['Green']), 2)
#             cv.drawContours(dsrc, poly_approx[color][i], i, (0, 0, 255), 2)
#             cv.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 1)
#             cv.putText(src, 'Pink: {}'.format(pink_count), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv.LINE_AA)
#             ip += 1  # el i solo avanza para los contornos que se deben dibujar
#             x_prev = x
#
#     ig = 0
#     poly_approx_g = []
#     contours_g, hierarchy_g = cv.findContours(mask_g, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#
#     for contour in contours_g:
#         area = cv.contourArea(contour)
#         if area > 12000:
#             perimeter = cv.arcLength(contour, True)
#             poly_approx_g.append(cv.approxPolyDP(contour, 0.02 * perimeter, True))
#             x, y, w, h = cv.boundingRect(poly_approx_g[ig])
#             if x == 0 and x_prev != 0:
#                 green_count += 1
#                 publish.single("data", "Pink: {}".format(pink_count), hostname="192.168.1.17")
#                 publish.single("data", "Green: {}".format(green_count), hostname="192.168.1.17")
#                 display.lcd_clear()
#                 display.lcd_display_string("Rosados: {}".format(pink_count), 1)
#                 display.lcd_display_string("Verdes: {}".format(green_count), 2)
#             # cv.drawContours(dst, poly_approx, i, (0, 0, 255), 2)
#             cv.rectangle(dst, (x, y), (x + w, y + h), (0, 255, 0), 1)
#             cv.putText(dst, 'Green: {}'.format(green_count), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv.LINE_AA)
#             ig += 1  # el i solo avanza para los contornos que se deben dibujar
#             x_prev = x
#     return x_prev


cap = cv.VideoCapture(0)
x_prev = 10
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_and_publish(frame, frame)
    #    cv.imshow('captura', frame)
    #    cv.waitKey(10)
except KeyboardInterrupt:
    print('Saliendo del programa ...')
    display.lcd_clear()

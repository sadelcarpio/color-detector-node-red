CREATE DATABASE COLOR_DETECTOR;
USE COLOR_DETECTOR;
CREATE TABLE CONTEO(
FECHA TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
GREEN INT(10) NOT NULL,
PINK INT(10) NOT NULL,
/* AQUÍ AÑADIR LAS ETIQUETAS EXTRA*/
PRIMARY KEY(FECHA));



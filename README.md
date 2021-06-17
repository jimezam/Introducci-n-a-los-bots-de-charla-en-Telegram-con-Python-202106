# Introducción a los bots de charla en Telegram con Python

## Requerimientos

- Python 3
- Pip
- Editor de texto (como [Visual Studio Code](https://code.visualstudio.com/download))

## Ambiente virtual

Este paso es opcional pero es una buena práctica para mantener separadas las librerías de los diferentes proyectos.

Crear el ambiente virtual `bots`.  Reemplazar la ruta (`~/venv/`) según se considere.

```
$ python3 -m venv ~/venv/bots
```

Activar el ambiente virtual recién creado.

```
$ source ~/venv/bots/bin/activate
```

Más información acerca del [uso de `venv`](https://jimezam.github.io/blog/2021/02/21/uso-de-venv-con-python-3).

## Instalación

Instalar las librerías requeridas.

```
$ pip install requests

$ pip install wikipedia

$ pip install python-telegram-bot
```

## Configuración

Deben especificarse los siguientes *tokens* al inicio del código fuente.

- `TELEGRAM_TOKEN` deberá almacenar el token del bot ([*Creating a new bot*](https://core.telegram.org/bots#6-botfather)).
- `WEATHER_TOKEN` deberá almacenar el *API Key* del servicio OpenWeatherMap ([*How to get an API key*](https://openweathermap.org/faq)).

## Ejecución

Para la ejecución del bot en **producción** es necesario utilizar el siguiente comando.

```
$ python bot.py
```

Durante la etapa de **desarrollo** es frecuente tener que detener al bot para hacer cambios y volverlo a ejecutar para probarlos.  En esta etapa es mas práctico utilizar `nodemon`, el cual se instala de la siguiente manera una única vez para todos los proyectos.

```
$ npm install -global nodemon
```

Y se ejecuta el bot utilizándolo de la siguiente manera.

```
$ nodemon bot.py
```
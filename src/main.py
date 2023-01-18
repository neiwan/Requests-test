from fastapi import FastAPI

from web_app import api_router
from uvicorn import Config, Server

if __name__ == '__main__':
    # FastAPI - связующее звено между HTTP - сервером и кодом программиста.
    # В числе прочего отвечает за документацию (/docs).
    app = FastAPI()
    app.include_router(api_router)
    config = Config(
        app=app,
        host="localhost",
        port=8080
    )
    # Сам сервер. Принимает запрос, парсит аргументы,  заголовки и т.п.,
    # передает в FastAPI.
    # Собирает ответ (заголовки, куки, тело ответа в виде текста).
    server = Server(config)
    server.run()
#TODO произвести организацию импортов
#TODO разделить код на зоны ответственности: логги / конфиг БД / Модели ДБ / FastAPI / тесты
#TODO нарушены правила PEP 8: табы в отступах (W191), пробел перед переводом строки (W291), нет перевода строки в конце файла (W292)

import asyncio
import httpx
import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.testclient import TestClient
from http import HTTPStatus
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
#TODO неиспользуемый импорт ForeignKey
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

#TODO logging.basicConfig на уровне модуля: настройка выполняется при импорте, а не при старте приложения
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#TODO у FastAPI() не заданы title/version/описание приложения
app = FastAPI()

#TODO вынести значения переменных в .env файл
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db"
EXTERNAL_API_URL = "https://external-api.local/process"
EXTERNAL_API_TOKEN = "supersecrettoken"

#TODO вынести в отдельный конфиг для БД
#TODO echo=True логирует SQL-запросы — недопустимо в продакшене
#TODO движок никогда не закрывается: нет engine.dispose() в lifespan
engine = create_async_engine(DATABASE_URL, echo=True)

#TODO вынести в отдельный конфиг для БД
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

#TODO вынести в отдельный конфиг для БД
Base = declarative_base()

#TODO модель бд вынести в отдельный файл
class User(Base):
#TODO комментарии излишние, из имени функции всё понятно
    """
    Модель пользователя.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    #TODO нет уникального ограничения на email (unique=True) и ограничения длины
    email: str = Column(String)


#TODO привести в 3 нормальную форму
class Order(Base):
#TODO комментарии излишние, из имени функции всё понятно
    """
    Модель заказа.
    """

    __tablename__ = "orders"

    id: int = Column(Integer, primary_key=True)
    #TODO зачем нам столько id? Есть ли foreigh_key?
    external_id: int = Column(Integer)
    #TODO создать отдельную таблицу user
    #TODO нет ForeignKey("users.id") на колонке user_id
    user_id: int = Column(Integer)
    #TODO установить ограничение символов
    description: str = Column(String)
    #TODO отсутствует аннотация типа (data: dict | None) — mypy не сможет проверить
    #TODO для PostgreSQL предпочтительнее JSONB (индексация и производительность)
    data = Column(JSON)
    #TODO нет relationship("User") / back_populates — связь по user_id не описана


#TODO вынести логику клиента в отдельный файл
class ExternalServiceClient:
#TODO комментарии излишние, из имени функции всё понятно
    """
    Клиент для вызова внешнего API.
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    #TODO сервисный слой бросает HTTPException из fastapi — утечка web-зависимости в сервис
    #TODO новый AsyncClient на каждый вызов: соединение не переиспользуется, нет пула
    #TODO нет timeout у HTTP-запросов
    #TODO headers дублируется в обоих методах — вынести в __init__/свойство
    async def get_order(self, order_id: int) -> dict:
	#TODO удалить комментарий
        """
        Получает заказ из внешнего API.
        Возвращает ответ в виде JSON или поднимает исключение HTTPException.
        """
        headers = {"Authorization": f"Bearer {self.token}"}
	#TODO берем только AsyncClient, импортировать весь модуль httpx не надо
        async with httpx.AsyncClient() as client:
	    #TODO f"{self.base_url}/{order_id}", headers=headers - вынести в отдельную переменную
            response = await client.get(f"{self.base_url}/{order_id}", headers=headers) 
            if response.status_code == HTTPStatus.OK:
                return response.json()
            #TODO else после return не нужен (лишняя ветка)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)

    async def process_order(self, order_id: int) -> None:
		#TODO сократить комментарий: до "Обработка заказа"
        """
        Вызывает обработку заказа во внешнем API.
        """
        headers = {"Authorization": f"Bearer {self.token}"}
	#TODO берем только AsyncClient, импортировать весь модуль httpx не надо
        async with httpx.AsyncClient() as client:
	    #TODO f"{self.base_url}/{order_id}", headers=headers - вынести в отдельную переменную
            #TODO статус ответа не проверяется — ошибка внешнего API останется незамеченной
            await client.post(f"{self.base_url}/{order_id}", headers=headers)

#TODO почему это глобальная переменная? Положить внутрь async def submit_data
#TODO клиент создаётся на этапе импорта — мешает тестированию и подмене зависимостей
external_client = ExternalServiceClient(EXTERNAL_API_URL, EXTERNAL_API_TOKEN)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
	#TODO комментарий убрать
    """
    Контекстный менеджер для асинхронной сессии БД.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        #TODO сессия только закрывается: нет commit() — изменения не сохраняются в БД
        #TODO нет rollback() при исключении
        await session.close()

#TODO вынести в отдельный файл для логирования, использовать модуль logging
def log_execution(func):
	#TODO убрать коммент
    """
    Логирует вызов функции.
    """

    #TODO нет functools.wraps — теряются __name__, __doc__ и сигнатура
    #TODO декоратор не поддерживает async-функции: возвращает корутину без await
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


#TODO порядок декораторов неверный: @app.post должен быть ближе к функции, иначе FastAPI
#TODO регистрирует необёрнутую функцию и логирование не срабатывает
@log_execution
#TODO какой статус ожидается? status_code=status.HTTP....
@app.post("/submit")
#TODO Используй Annotated
async def submit_data(request: Request):
    """
    Приём данных заказа и пользователя.
    """
    #TODO ручной request.json() без Pydantic: KeyError/ValueError приведут к 500
    data = await request.json()
    user_data = data["user"]
    order_data = data["order"]

    async with get_session() as session:
        user = User(name=user_data["name"], email=user_data["email"])
        session.add(user)
        #TODO нет flush()/commit(): user.id ещё не сгенерирован

        #TODO опечатка exteranal_id — колонка называется external_id
        if await external_client.get_order(order_data["exteranal_id"]):
            order = Order(
                #TODO опечатка в имени поля exteranal_id — такого атрибута нет (AttributeError)
                exteranal_id=order_data["exteranal_id"],
                description=order_data["description"],
                data=order_data["data"],
                #TODO у модели Order нет связи user (только user_id) — TypeError
                user=user,
            )
            session.add(order)

            #TODO нет await session.commit() — ни user, ни order не сохранятся
            await external_client.process_order(order.external_id)

    #TODO эндпоинт ничего не возвращает (return None → 200 без тела)
    #TODO бизнес-логику стоит вынести из эндпоинта в сервис/репозиторий


#TODO TestClient создаётся на уровне модуля — место ему в тестах (фикстура)
client = TestClient(app)


#TODO тесты в отдельный файл
@pytest.mark.parametrize(
    "user_data,order_data,expected",
    [
        (
            {"name": "John", "email": "john@example.com"},
            #TODO опечатка exteranal_id (см. модель Order)
            {"exteranal_id": 123, "description": "Test", "data": {}},
            200,
        ),
        (
            {"name": "Jane", "email": "jane@example.com"},
            #TODO опечатка exteranal_id (см. модель Order)
            {"exteranal_id": 124, "description": "Test2", "data": {"key": "value"}},
            200,
        ),
    ],
)

#TODO тесты в отдельный файл
def test_submit_data(user_data, order_data, expected):
    """Тест для проверки отправки данных"""
    test_case = {"user": user_data, "order": order_data}

    #TODO вложенные if и else: pass — тест может пройти, ничего не проверив
    if len(user_data["name"]) > 3:
        if "key" in order_data["data"] or len(order_data["data"]) == 0:
            #TODO тест ходит в реальный внешний API — нужны моки (respx/httpx.MockTransport)
            response = client.post("/submit", json=test_case)

            if expected == 200:
                #TODO assert True/assert False бессмысленны: нужно assert response.status_code == expected
                if response.status_code < 400:
                    assert True
                else:
                    assert False
            else:
                pass

#TODO тесты в отдельный файл
#TODO pytest не собирает функцию process_order_test — нужен префикс test_
def process_order_test():
    """Тест для обработки заказа"""
    client_instance = ExternalServiceClient("https://httpbin.org/get", "test-token")

    #TODO asyncio.run в тестах — использовать pytest-asyncio/anyio и async def
    try:
        result = asyncio.run(client_instance.get_order(123))
        assert result is not None
    #TODO Exception зачем?
    #TODO except Exception: pass проглатывает и AssertionError — падение теста скрывается
    except Exception:
        pass

    #TODO bare except подавляет все исключения, включая системные
    try:
        asyncio.run(client_instance.process_order(123))
    except:
        pass
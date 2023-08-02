### Реализация API сервера согласно тех. заданию от SkillFactory.

Библиотеки:
- FastAPI
- uvicorn
- psycopg2
- pydantic
- alembic

Swagger доступен по пути: http://127.0.0.1:8000/docs#/<br>

Пример:
```
{
  "beauty_title": "пер.",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
 
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
	"name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"}, 
 
  "coords":{
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"},
 
  "level":{
        "winter": "", 
        "summer": "1А",
        "autumn": "1А",
        "spring": ""},
 
"images": [
    {
        "data":"<картинка1>", 
        "title":"Седловина"}, 
    {
        "data":"<картинка>", 
        "title":"Подъём"
    }
    ]
}
```

#### POST: /submitData
Метод внесения данных в базу. Принимает фотографии списком.<br>
Автоматически присваеивает дату и статус NEW.<br>

#### GET /submitData/<pereval_id>
Запрос информации из бд по id согласно форме.

#### PATCH /submitData/<pereval_id>
Метод обновления записи. Требует ИД записи и JSON данные в форме аналогично вводу.<br>
Ограничения: Запись должна быть в статусе NEW, запрещено менять данные пользователя.

#### GET /submitData/<user_email>
Метод получения списка данных, отправленных пользователем. 

# Graph API

## Описание точек доступа API

1. **GET /nodes**  
   Возвращает всех узлов с атрибутами `id` и `label`.

2. **GET /node/{node_id}**  
   Возвращает узел с его связями и всеми атрибутами узлов и связей.

3. **POST /nodes**  
   Добавляет узел и/или связи. Требуется авторизация через токен.

4. **DELETE /nodes/{node_id}**  
   Удаляет узел и его связи. Требуется авторизация через токен.

5. **GET /graph-segment**  
   Возвращает сегмент графа, включая узлы и связи.

---

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https:[//github.com/yourusername/yourrepository.git](https://github.com/Janneryli/otrpo_lb5)
   cd otrpo_lb5
   ```

2.Создайте виртуальное окружение:

```bash
python -m venv venv

```
```bash
source venv/bin/activate  # Linux/MacOS
venv\\Scripts\\activate   # Windows
```

2.Установите зависимости:

```bash
pip install -r requirements.txt
```
3.Запуск приложения

Убедитесь, что Neo4j запущен 
Запустите сервер:
```bash
python rest_api.py
```
4.Откройте документацию API в браузере:
```
http://127.0.0.1:8000/docs
```

## Запуск тестов

1. Убедитесь, что приложение работает корректно.
2. Запустите тесты:
   ```bash
   pytest -v test_api.py
   ```
3. Убедитесь, что все тесты прошли успешно.

---




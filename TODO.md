Подготовиться к 25.09.2026

## *Теория (применяем на практике):*

* [ ] Первые 4 лекции про основы системного дизайна (базовый минимум для middle) — [плейлист](https://www.youtube.com/watch?v=hqhkYYtKGJI&list=PLgqAguchzg7Kwg5F84rya2Lrt41jBd6Ua)
  - [ ] 3. Распределение хранения данных
  - [ ] 4. Паттерны и приемы проектирования

## *Практика:*

### Брокеры и очереди

- [ ] Ресурс: [RabbitMQ плейлист](https://www.youtube.com/watch?v=1BtXBwVHKhI&list=PLYnH8mpFQ4amsOuXBq4Gpc-Tzt-pwGjnI)
- [ ] Разобраться, как Celery использует Redis (кэш) и RabbitMQ (брокер)


### Для скринингов  HR:
- [X] Прогнать резюме через нейронку. 
------Описание задачи: 
------Прогнать в контексте, я HR или тех интервьюер и мне прислали резюме кандидата, надо понять реальный опыт или нет, чем дейсвительно занимался кандидат, напиши вопросы и возможные ответы
- [X] Посмотреть про LLM ([видео](https://youtu.be/r76VnrTQSfA?si=lWd0LzOAw2yzIcoj))

### Для технических HR скринингов:
- [ ] Написать примеры ручек
------Описание задачи: 
------Пример ручек которые ты мог закешировать, раз это кэш, то скорее всего какие-то данные из postgres, возможно данные по каким-то обработанным PDF файлам, но учитывая что там больше чем 3 секунды, это либо аналитика, либо просто таблицы были большие, потому что данные за много лет, и их все надо было хранить.
Например: Внедрил Redis-кэширование по паттерну cache-aside, снизил p95 с 3 сек до 300 мс и нагрузку на PostgreSQL.

- [ ] Придумать один кейс, можно взять таблицу в которой хранились например что-то по парсингу PDF
------Например:
Оптимизировал запросы PostgreSQL: анализировал планы выполнения (EXPLAIN ANALYZE),
подбирал и добавлял индексы для нагруженных сценариев


### Нейросети и LLM

- [ ] Пройти курс по ИИ от [хекслет](https://ru.hexlet.io/my)

## *Технические интервью (стек):*

- [ ] **FastAPI**: маршрутизация, `Depends` и слои зависимостей, Pydantic-схемы и валидация, async- и sync-эндпоинты (и почему нельзя блокировать event loop), `BackgroundTasks`, `lifespan`, обработка ошибок, тестирование через `TestClient` / `httpx.ASGITransport`
- [ ] **Kubernetes** — только базовая терминология, без углубления в проектирование кластеров: pod, deployment, service, ingress, namespace, configmap/secret, liveness/readiness-пробы, requests/limits, HPA

## *LeetCode (алгоритмы):*

Источник: [LeetCode ROADMAP](https://balun-team.yonote.ru/share/28a5c640-61e9-4f0a-b86e-e629c560077d/doc/leetcode-roadmap-PfDldCmI1M) — всего 100 задач (43 easy, 57 medium)

### Два указателя

- [X] Two Sum II — Input Array Is Sorted (medium) — [leetcode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [X] Container With Most Water (medium) — [leetcode](https://leetcode.com/problems/container-with-most-water/)

### Хэш-таблицы

- [X] Two Sum (easy) — [leetcode](https://leetcode.com/problems/two-sum/)
- [ ] Group Anagrams (medium) — [leetcode](https://leetcode.com/problems/group-anagrams/)

### Матрицы

- [ ] Valid Sudoku (medium) — [leetcode](https://leetcode.com/problems/valid-sudoku/)
- [ ] Rotate Image (medium) — [leetcode](https://leetcode.com/problems/rotate-image/)

### Плавающие окна

- [ ] Longest Substring Without Repeating Characters (medium) — [leetcode](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- [ ] Longest Repeating Character Replacement (medium) — [leetcode](https://leetcode.com/problems/longest-repeating-character-replacement/)


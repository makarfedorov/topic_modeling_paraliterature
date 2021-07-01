# Тематическое моделирование жанров паралитературы
**Репозиторий** содержит материалы тематического моделирования текстов фанфикшн. В папке Corpus находится функция для скачивания текстов с метаинформацией с сайта ficbook, и сам скаченный корпус текстов (1600 единиц). Тамже находятся таблицы с количеством токенов для каждого из подкорпусов и ссылками, с помощью которых производилась скачивания текстов. В папке topic modeling находятся файлы с темами, которые выделились в результате моделирования и интерактивные визуализации. Файл Topic__Model_Fedorov содержит код и визуализации исследования

**У фан-литературы* есть много определений**. Основные: непрофессиональные писатели, связь с фанатским сообществом, сообществом фикрайтеров. Пониманий жанров фанфикшна тоже очень много. Исследователи склонны перенимать терминологию сообщества фикрайтеров. На практике жанр часто совпадает с жанровой меткой, которая присваивается фанфику при его публикации на сайте. Разные исследователи предлагали разные классификации жанров фанфикшна. Например, Федорчук выделяет четыре понимания жанра: 1) Жанр как направленность (Гет, Слэш) 2) Как модель построения текста (например, “Учебные заведения”, songfic) 3) Как настроение фанфика (Ангст, Флафф) 4) Жанр, связанный со своим содержанием (Фэнтези, Детектив)

**Исследовательский вопрос работы**: 
Есть ли измеримая разница в содержании фанфиков разных жанров?

**Методы**:
В работе использовалось тематическое моделирование с помощью Латентного размещения Дирихле (библиотека gensim на языке Python)

**Источники**:

В качестве источника текстов был использован самый популярный сайт для фанфиков на русском ficbook.net

**Задачи**:

1) Создать корпус фанфиков

2) Применить к нему алгоритмы тематического моделирования

Было выбрано четыре жанра: Ангст, Флафф, Фэнтези и Повседневность. 
Для каждого жанра было скачано 400 текстов вместе с метаинформацией. Направленности Джен, Гет, Слэш и Фемслэш скачивались в одинаковых количествах. Всего было скачано 1600 фанфиков.
Первый шаг в исследовании - посмотреть, какие есть фандомы:
![alt text](https://cdn1.savepice.ru/uploads/2021/7/1/898c474e19037689b0c507b77de60eb0-full.png)

Видно, что, во-первых, там есть отдельные фандомы для книг/фильмов по ним. Во-вторых, есть много разных комбинаций из фандомов франшизы Марвел и тому подобного. Все эти фандомы были стандартизованы и затем выбрано 10 самых частотных фандомов. Остальные низкочастотные фандомы были помечены либо как "прочее" (если таковой присутствует отдельно), либо как "кроссовер". 
Далее можно сделать тематическое моделирование с LDA. После лемматизации и удаления стоп-слов, вот что какие темы получаются при 20:

![alt text](https://cdn1.savepice.ru/uploads/2021/7/1/04bc40d8e664e2461936183b15193bb0-full.png)


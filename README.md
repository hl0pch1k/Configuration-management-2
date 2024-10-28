Git Dependency Visualizer

Описание проекта

Git Dependency Visualizer — это инструмент командной строки для визуализации зависимостей между коммитами в Git-репозитории. Проект позволяет наглядно отобразить структуру зависимостей, включая транзитивные связи, между коммитами в виде графа, сохраняя его в формате PNG. Этот граф может быть полезен для анализа истории изменений и выявления взаимосвязей между коммитами.

Проект использует Graphviz для построения графа и позволяет пользователю настраивать параметры визуализации и анализа через файл конфигурации в формате TOML.

Основные функции

	•	Анализ Git-репозитория: Извлекает зависимости между коммитами, в том числе транзитивные, и формирует структуру, готовую к визуализации.
	•	Создание графа зависимостей: Построение графа коммитов с отображением файлов, авторов и сообщений для каждого узла.
	•	Экспорт в PNG: Сохранение графа в формате PNG с высоким разрешением для наглядности и удобства использования.

Структура проекта

	•	main.py — Основной исполняемый файл, содержащий функции для загрузки конфигурации, анализа репозитория и построения графа.
	•	config.toml — Конфигурационный файл, задающий пути к репозиторию, Graphviz и параметры сохранения графа.
	•	test_visualizer.py — Набор тестов для функций, реализованных в main.py, использующих библиотеку pytest.

Установка и настройки

Требования

	•	Python 3.6+
	•	Graphviz: Программа для построения графов. Убедитесь, что dot (исполняемый файл Graphviz) установлен и доступен в системе.

Установка

	1.	Клонируйте репозиторий:

git clone <URL вашего репозитория>
cd <название папки репозитория>


	2.	Установите зависимости:

pip install -r requirements.txt

Примечание: Убедитесь, что у вас установлены модули gitpython, graphviz, и toml.

	3.	Установите Graphviz (если не установлен). На macOS можно использовать Homebrew:

brew install graphviz


	4.	Проверьте путь к dot (исполняемому файлу Graphviz):

which dot

Скопируйте этот путь и вставьте его в файл config.toml в разделе graphviz.path.

Конфигурация

Создайте файл config.toml в корневой директории проекта (если его еще нет) и укажите следующие параметры:

[graphviz]
path = "/path/to/dot"  # Укажите путь к dot, полученный в предыдущем шаге

[repository]
path = "/path/to/your/git/repo"  # Укажите путь к вашему Git-репозиторию

[output]
path = "dependency_graph"  # Имя файла для сохранения графа зависимостей

Пример:

[graphviz]
path = "/opt/homebrew/bin/dot"

[repository]
path = "/Users/username/path/to/repo"

[output]
path = "dependency_graph"

Использование

Запуск проекта

	1.	Запустите основную программу:

python main.py


	2.	Если конфигурационный файл и пути указаны корректно, программа проанализирует указанный Git-репозиторий, построит граф зависимостей и сохранит его как dependency_graph.png.
	3.	При успешном завершении программы вы увидите сообщение: Граф успешно сохранён в dependency_graph.png.

Тестирование

Для проверки работоспособности функций в проекте используется библиотека pytest. Для запуска тестов выполните команду:

pytest test_visualizer.py

Тесты проверяют следующие функции:

	•	load_config: Загрузка и проверка конфигурационного файла.
	•	sanitize_text: Очистка текста от символов, которые могут вызвать ошибки при визуализации.
	•	analyze_git_repo: Анализ Git-репозитория и извлечение зависимостей.
	•	build_graph: Построение графа зависимостей и его сохранение.

Возможные проблемы и их решение

	•	Graphviz не найден: Убедитесь, что dot установлен и его путь указан в config.toml.
	•	Git-репозиторий не найден: Проверьте путь к репозиторию в config.toml и убедитесь, что указанный путь действительно содержит Git-репозиторий.
	•	Ошибки при создании графа: Убедитесь, что текст коммитов не содержит символов, которые могут вызвать ошибки в Graphviz, таких как : и ,. Функция sanitize_text обрабатывает такие символы.

Структура файлов

	•	README.txt: Этот файл с полным описанием проекта, инструкцией по установке и запуску.
	•	main.py: Основной скрипт с реализацией логики анализа и визуализации зависимостей.
	•	config.toml: Файл конфигурации, содержащий настройки путей к репозиторию, Graphviz и выходному файлу.
	•	test_visualizer.py: Набор тестов для проверки работоспособности функций проекта.
	•	dependency_graph.png: Создаваемый граф зависимостей коммитов, отображающий связи между ними.

Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле LICENSE.

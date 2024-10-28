import toml
import os
import git
import graphviz
import textwrap

def load_config(config_path):
    """Загружает конфигурационный файл TOML."""
    try:
        with open(config_path, 'r') as f:
            config = toml.load(f)
        return config
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        exit(1)

def sanitize_text(text):
    """Экранирует текст, убирая символы, которые могут вызвать ошибки в Graphviz."""
    return text.replace(":", "").replace(",", "").replace("\n", "\\n")

def analyze_git_repo(repo_path):
    """
    Анализирует git-репозиторий и возвращает зависимости между коммитами.

    Возвращает словарь, где ключи — это описание коммитов, а значения — списки описаний родительских коммитов.
    """
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits())
        dependencies = {}

        for commit in commits:
            # Формируем список изменённых файлов в коммите с переносом строки
            changed_files = ", ".join(commit.stats.files.keys())
            changed_files = "\n".join(textwrap.wrap(changed_files, width=30))

            # Формируем текст для узла с пояснениями и пустыми строками между секциями
            commit_info = (f"Файл - {changed_files}\n\n" +
                           f"Автор - {commit.author.name}\n\n" +
                           f"Коммит - " + "\n".join(textwrap.wrap(commit.message.strip(), width=30)))
            commit_info = sanitize_text(commit_info)

            # Для каждого коммита добавляем описание родительских коммитов
            dependencies[commit_info] = []
            for parent in commit.parents:
                parent_changed_files = ", ".join(parent.stats.files.keys())
                parent_changed_files = "\n".join(textwrap.wrap(parent_changed_files, width=30))

                parent_info = (f"Файл - {parent_changed_files}\n\n" +
                               f"Автор - {parent.author.name}\n\n" +
                               f"Коммит - " + "\n".join(textwrap.wrap(parent.message.strip(), width=30)))
                parent_info = sanitize_text(parent_info)

                dependencies[commit_info].append(parent_info)

        return dependencies
    except Exception as e:
        print(f"Ошибка анализа репозитория: {e}")
        exit(1)

def build_graph(dependencies, output_path):
    """
    Строит граф зависимостей и сохраняет его в формате PNG с высоким разрешением.

    Создаёт граф с узлами для каждого коммита и рёбрами, указывающими на зависимость между коммитами.
    """
    try:
        dot = graphviz.Digraph(comment='Git Dependency Graph', format='png')
        dot.attr(rankdir='TB', dpi='300')  # Вертикальная ориентация и высокое разрешение
        dot.attr(size="8,10!")  # Ограничиваем размер страницы для компактности
        for commit, parents in dependencies.items():
            # Добавляем узел с описанием коммита (без длинных хэшей)
            dot.node(commit, commit)
            for parent in parents:
                dot.edge(parent, commit)
        dot.render(output_path, cleanup=True)
        print(f"Граф успешно сохранён в {output_path}.png")
    except Exception as e:
        print(f"Ошибка построения графа: {e}")
        exit(1)

def main():
    """Основная функция, которая выполняет все шаги по заданию."""
    # Загружаем конфигурацию
    config_path = 'config.toml'
    config = load_config(config_path)

    # Извлекаем пути из конфигурационного файла
    repo_path = config['repository']['path']
    output_path = config['output']['path']
    graphviz_path = config['graphviz']['path']

    # Проверяем наличие программы Graphviz
    if not os.path.exists(graphviz_path):
        print(f"Программа Graphviz не найдена по пути: {graphviz_path}")
        exit(1)

    # Анализируем зависимости коммитов в репозитории
    dependencies = analyze_git_repo(repo_path)

    # Строим граф зависимостей и сохраняем его
    build_graph(dependencies, output_path)


if __name__ == '__main__':
    main()
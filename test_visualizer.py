import pytest
import os
import git
import toml
from main import load_config, sanitize_text, analyze_git_repo, build_graph

# Тест для функции load_config
def test_load_config(tmp_path):
    # Создаем временный конфигурационный файл
    config_path = tmp_path / "config.toml"
    config_data = {
        "graphviz": {"path": "/opt/homebrew/bin/dot"},
        "repository": {"path": "/path/to/repo"},
        "output": {"path": "dependency_graph"}
    }
    with open(config_path, "w") as f:
        toml.dump(config_data, f)

    # Проверяем корректность загрузки конфигурации
    config = load_config(config_path)
    assert config["graphviz"]["path"] == "/opt/homebrew/bin/dot"
    assert config["repository"]["path"] == "/path/to/repo"
    assert config["output"]["path"] == "dependency_graph"

    # Проверка на случай отсутствия файла
    with pytest.raises(SystemExit):
        load_config(tmp_path / "nonexistent.toml")

# Тест для функции sanitize_text
def test_sanitize_text():
    text = "Тест: текст, с \n символами!"
    sanitized_text = sanitize_text(text)
    assert sanitized_text == "Тест текст с \\n символами!"

# Тест для функции analyze_git_repo
def test_analyze_git_repo(tmp_path):
    # Создаем временный git-репозиторий для теста
    repo_path = tmp_path / "test_repo"
    repo = git.Repo.init(repo_path)
    test_file = repo_path / "test_file.txt"
    test_file.write_text("Тестовое содержимое")
    repo.index.add([str(test_file)])
    repo.index.commit("Initial commit")

    # Запускаем функцию и проверяем результат
    dependencies = analyze_git_repo(repo_path)
    assert len(dependencies) > 0
    assert any("Initial commit" in key for key in dependencies.keys())

# Тест для функции build_graph
def test_build_graph(tmp_path):
    # Создаем тестовые зависимости
    dependencies = {
        "Коммит A": ["Коммит B", "Коммит C"],
        "Коммит B": ["Коммит C"]
    }
    output_path = tmp_path / "dependency_graph"

    # Проверяем, что граф создается без ошибок
    build_graph(dependencies, str(output_path))
    assert os.path.exists(str(output_path) + ".png")
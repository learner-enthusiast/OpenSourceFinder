from enum import Enum


class ProjectFilters:
    """Container for all project filtering enums"""

    class Language(str, Enum):
        PYTHON = "python"
        JAVASCRIPT = "javascript"
        JAVA = "java"
        TYPESCRIPT = "typescript"
        GO = "go"
        RUBY = "ruby"
        CSHARP = "c#"
        CPP = "c++"
        PHP = "php"
        RUST = "rust"
        SWIFT = "swift"
        KOTLIN = "kotlin"
        SCALA = "scala"
        DART = "dart"
        C = "c"

    class SortField(str, Enum):
        STARS = "stars"
        FORKS = "forks"

    class Order(str, Enum):
        ASC = "asc"
        DESC = "desc"

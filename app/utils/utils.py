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

    class Category(str, Enum):
        # Web Development
        WEB_DEV = "web-dev"
        FRONTEND = "frontend"
        BACKEND = "backend"
        FULLSTACK = "fullstack"

        # AI & Machine Learning
        AI_ML = "ai-ml"
        MACHINE_LEARNING = "machine-learning"
        DEEP_LEARNING = "deep-learning"
        DATA_SCIENCE = "data-science"
        COMPUTER_VISION = "computer-vision"
        NATURAL_LANGUAGE_PROCESSING = "nlp"

        # Mobile Development
        MOBILE = "mobile"
        ANDROID = "android"
        IOS = "ios"
        REACT_NATIVE = "react-native"
        FLUTTER = "flutter"

        # Desktop & System
        DESKTOP = "desktop"
        SYSTEM_PROGRAMMING = "system-programming"
        EMBEDDED = "embedded"
        OPERATING_SYSTEM = "operating-system"

        # DevOps & Infrastructure
        DEVOPS = "devops"
        CLOUD = "cloud"
        CONTAINERIZATION = "containerization"
        KUBERNETES = "kubernetes"
        CI_CD = "ci-cd"
        INFRASTRUCTURE = "infrastructure"

        # Database & Data
        DATABASE = "database"
        DATA_ENGINEERING = "data-engineering"
        BIG_DATA = "big-data"
        ETL = "etl"

        # Game Development
        GAME_DEV = "game-development"
        UNITY = "unity"
        UNREAL_ENGINE = "unreal-engine"

        # Blockchain & Crypto
        BLOCKCHAIN = "blockchain"
        CRYPTOCURRENCY = "cryptocurrency"
        SMART_CONTRACTS = "smart-contracts"
        WEB3 = "web3"

        # Security
        CYBERSECURITY = "cybersecurity"
        PENETRATION_TESTING = "penetration-testing"
        ENCRYPTION = "encryption"

        # Tools & Utilities
        AUTOMATION = "automation"
        TESTING = "testing"
        MONITORING = "monitoring"
        LOGGING = "logging"

        # Emerging Tech
        IOT = "iot"
        AR_VR = "ar-vr"
        QUANTUM_COMPUTING = "quantum-computing"
        ROBOTICS = "robotics"

    class SortField(str, Enum):
        STARS = "stars"
        FORKS = "forks"

    class Order(str, Enum):
        ASC = "asc"
        DESC = "desc"

    CATEGORY_MAPPING = {
        "web-dev": ["web", "website", "webapp", "web-development"],
        "frontend": ["frontend", "react", "vue", "angular", "html", "css"],
        "backend": ["backend", "api", "server", "nodejs", "django", "flask"],
        "fullstack": ["fullstack", "full-stack", "mern", "mean", "jamstack"],
        "ai-ml": ["artificial-intelligence", "machine-learning", "ai", "ml"],
        "machine-learning": ["machine-learning", "ml", "scikit-learn", "tensorflow"],
        "deep-learning": ["deep-learning", "neural-network", "pytorch", "tensorflow"],
        "data-science": ["data-science", "data-analysis", "pandas", "jupyter"],
        "computer-vision": ["computer-vision", "opencv", "image-processing"],
        "nlp": ["nlp", "natural-language-processing", "text-mining", "chatbot"],
        "mobile": ["mobile", "android", "ios", "mobile-app"],
        "android": ["android", "kotlin", "java-android", "android-app"],
        "ios": ["ios", "swift", "objective-c", "xcode"],
        "react-native": ["react-native", "mobile", "cross-platform"],
        "flutter": ["flutter", "dart", "mobile", "cross-platform"],
        "desktop": ["desktop", "gui", "desktop-app", "electron"],
        "system-programming": ["systems", "low-level", "kernel", "operating-system"],
        "embedded": ["embedded", "arduino", "raspberry-pi", "iot"],
        "operating-system": ["os", "kernel", "linux", "operating-system"],
        "devops": ["devops", "ci-cd", "deployment", "automation"],
        "cloud": ["cloud", "aws", "azure", "gcp", "serverless"],
        "containerization": ["docker", "container", "containerization"],
        "kubernetes": ["kubernetes", "k8s", "orchestration"],
        "ci-cd": ["ci-cd", "github-actions", "jenkins", "pipeline"],
        "infrastructure": ["infrastructure", "terraform", "ansible", "iac"],
        "database": ["database", "sql", "nosql", "mongodb", "postgresql"],
        "data-engineering": ["data-engineering", "etl", "pipeline", "spark"],
        "big-data": ["big-data", "hadoop", "spark", "kafka"],
        "etl": ["etl", "data-pipeline", "airflow", "data-processing"],
        "game-development": ["game", "gamedev", "unity", "unreal"],
        "unity": ["unity", "unity3d", "game-engine"],
        "unreal-engine": ["unreal", "ue4", "ue5", "game-engine"],
        "blockchain": ["blockchain", "bitcoin", "ethereum", "crypto"],
        "cryptocurrency": ["cryptocurrency", "bitcoin", "ethereum", "defi"],
        "smart-contracts": ["smart-contracts", "solidity", "ethereum", "web3"],
        "web3": ["web3", "dapp", "decentralized", "blockchain"],
        "cybersecurity": ["security", "cybersecurity", "infosec", "hacking"],
        "penetration-testing": ["pentest", "security-testing", "ethical-hacking"],
        "encryption": ["encryption", "cryptography", "security"],
        "automation": ["automation", "bot", "scripting", "workflow"],
        "testing": ["testing", "unit-test", "automation-testing", "qa"],
        "monitoring": ["monitoring", "observability", "metrics", "logging"],
        "logging": ["logging", "log-analysis", "elk-stack"],
        "iot": ["iot", "internet-of-things", "arduino", "raspberry-pi"],
        "ar-vr": ["ar", "vr", "augmented-reality", "virtual-reality"],
        "quantum-computing": ["quantum", "quantum-computing", "qiskit"],
        "robotics": ["robotics", "robot", "ros", "autonomous"],
    }

    @classmethod
    def get_github_topics(cls, value):
        return cls.CATEGORY_MAPPING[value]

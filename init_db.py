from database import engine, Base, SessionLocal
from models import Term

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Примеры терминов WebGL/WebGPU
sample_terms = [
    {
        "keyword": "WebGL",
        "description": "Web Graphics Library - JavaScript API для рендеринга 2D и 3D графики в браузере без использования плагинов."
    },
    {
        "keyword": "WebGPU",
        "description": "Современный низкоуровневый API для графики и вычислений в веб-браузерах, преемник WebGL."
    },
    {
        "keyword": "Vertex Shader",
        "description": "Шейдер, который обрабатывает вершины 3D моделей. Преобразует координаты вершин из локального пространства в пространство камеры."
    },
    {
        "keyword": "Fragment Shader",
        "description": "Шейдер, который определяет цвет каждого пикселя рендерируемого объекта. Также известен как Pixel Shader."
    },
    {
        "keyword": "GPU",
        "description": "Graphics Processing Unit - специализированный процессор для обработки графики и параллельных вычислений."
    },
    {
        "keyword": "Shader",
        "description": "Программа, выполняемая на GPU для обработки вершин или фрагментов в графическом конвейере."
    },
    {
        "keyword": "Buffer",
        "description": "Область памяти GPU для хранения данных (вершины, индексы, текстуры, универсальные данные)."
    },
    {
        "keyword": "Texture",
        "description": "Двумерное или трехмерное изображение, используемое для наложения на 3D модели и создания детализированных поверхностей."
    },
    {
        "keyword": "Render Pipeline",
        "description": "Графический конвейер обработки данных от вершин до финального изображения на экране."
    },
    {
        "keyword": "Uniform",
        "description": "Глобальная переменная в шейдере, которая остается постоянной для всех вершин/фрагментов в одном вызове рендеринга."
    },
    {
        "keyword": "VBO",
        "description": "Vertex Buffer Object - объект буфера в OpenGL/WebGL для хранения данных вершин в памяти GPU."
    },
    {
        "keyword": "FBO",
        "description": "Framebuffer Object - объект для рендеринга в текстуру вместо экрана, используется для постобработки и эффектов."
    },
    {
        "keyword": "GLSL",
        "description": "OpenGL Shading Language - язык программирования шейдеров для OpenGL и WebGL."
    },
    {
        "keyword": "WGSL",
        "description": "WebGPU Shading Language - язык программирования шейдеров для WebGPU API."
    },
    {
        "keyword": "Compute Shader",
        "description": "Шейдер для выполнения общих вычислений на GPU, не связанных напрямую с графикой."
    }
]


def init_database():
    """Инициализация базы данных с примерами терминов"""
    db = SessionLocal()
    
    try:
        # Проверяем, не заполнена ли уже база
        existing_count = db.query(Term).count()
        if existing_count > 0:
            print(f"База данных уже содержит {existing_count} терминов. Пропускаем инициализацию.")
            return
        
        # Добавляем примеры терминов
        for term_data in sample_terms:
            term = Term(**term_data)
            db.add(term)
        
        db.commit()
        print(f"Успешно добавлено {len(sample_terms)} терминов в базу данных.")
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()


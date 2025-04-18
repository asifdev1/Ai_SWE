import os, sys
import subprocess
from pathlib import Path
from typing import Tuple

from langchain_groq import ChatGroq
from dotenv import load_dotenv
# from models.requirements import FunctionalRequirements

load_dotenv()

def setup_database(project_path:str, requirements) -> Tuple[str, str]:
    """
    1. Generates SQLAlchemy model code based on requirements.db_schema.
    2. Writes the model file under app/models/.
    3. Initializes Alembic, updates alembic.ini with the DB URL, and creates an initial migration.

    Returns:
        models_file (str): Path to the generated models file.
        migrations_dir (str): Path to the Alembic migrations directory.
    """

    # 1. Generate SQLAlchemy models via LLM
    schema_desc = requirements.db_schema
    prompt = f"""
You are an expert in Python and SQLAlchemy. Given the following database schema description:

\"\"\"{schema_desc}\"\"\"

Generate a complete Python module with SQLAlchemy ORM model classes.
Use declarative base (from sqlalchemy.ext.declarative import declarative_base)
Define table names, columns, types, primary keys, foreign keys, and constraints.
Do not include any extra text or comma or backticks, only valid Python code only in simple string.

"""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    models_code = llm.predict(prompt)

    # 2. Write the models file
    models_dir = Path(project_path) / "app" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    models_file = models_dir / "models.py"
    models_file.write_text(models_code, encoding="utf-8")

    # 3. Initialize Alembic in project root (if not already initialized)
    migrations_dir = Path(project_path) / "alembic"
    if not migrations_dir.exists():
        subprocess.run(
            [sys.executable, "-m" "alembic", "init", "alembic"],
            cwd=project_path,
            check=True
        )

    # 4. Patch alembic.ini to point at your DB URL
    #    (assumes you added sqlalchemy.url = <your URL> placeholder in scaffold)
    #    Or you can overwrite it here:
    alembic_ini = Path(project_path) / "alembic.ini"
    db_url = os.getenv("DATABASE_URL")  # e.g. "postgresql+psycopg2://user:pass@host/db"
    if db_url:
        text = alembic_ini.read_text(encoding="utf-8")
        text = text.replace("sqlalchemy.url = driver://user:pass@localhost/dbname", f"sqlalchemy.url = {db_url}")
        alembic_ini.write_text(text, encoding="utf-8")

    # 5. Create the initial migration
    subprocess.run(
        [sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", "Initial migration"],
        cwd=project_path,
        check=True
    )

    return str(models_file), str(migrations_dir)
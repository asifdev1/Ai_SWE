#  Create the sceleton of the project to create based on project requirements

import os, datetime

output_dir = os.getenv("OUTPUT_DIR", "output_projects")

def create_project_skeleton():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    project_name = f"project_{timestamp}"
    project_root = os.path.join(output_dir, project_name)
    os.makedirs(project_root, exist_ok=True)

    # define standard directories 
    dirs = [
        os.path.join(project_root, "app", "api", "routes"),
        os.path.join(project_root, "app", "services"),
        os.path.join(project_root, "app", "models"),
        os.path.join(project_root, "tests"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # create __init__.py files in Python packages
    packages = [
        os.path.join(project_root, "app"),
        os.path.join(project_root, "app", "api"),
        os.path.join(project_root, "app", "api", "routes"),
        os.path.join(project_root, "app", "services"),
        os.path.join(project_root, "app", "models"),
    ]

    for p in packages:
        open(os.path.join(p, "__init__.py"), "w").close()

    # placeholder dockerfile content
    dockerfile_content = """
        FROM python:3.9-slim
        WORKDIR /app
        COPY . .
        RUN pip install -r requirements.txt
        CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    """

    # create Dockerfile
    dockerfile_path = os.path.join(project_root, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)

    # create requirements.txt file
    requirements = ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "psycopg2-binary", "alembic"]
    with open(os.path.join(project_root, "requirements.txt"), "w") as f:
        f.write("\n".join(requirements))

      # Placeholder .env
    env_content = """
        # Environment variables for the generated project
        DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
    """
    with open(os.path.join(project_root, ".env"), "w") as f:
        f.write(env_content)

    # Basic README.md
    readme_content = f"""
        # Generated FastAPI Project

        This project was auto-generated on {datetime.datetime.now().isoformat()}.

        ## Structure

        app/ : FastAPI application code
        tests/ : Test suite

    """
    with open(os.path.join(project_root, "README.md"), "w") as f:
        f.write(readme_content)

    return project_root
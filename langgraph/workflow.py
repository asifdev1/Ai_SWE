import argparse, json

from langgraph.nodes.ingest_srs import process_document
from langgraph.nodes.retrieve_context import extract_functional_requirements
from langgraph.nodes.parse_requirement import parse_requirements
from langgraph.nodes.scaffold_project import create_project_skeleton
from langgraph.nodes.connect_db import setup_database


def run_workflow(input_file_path:str):
    # 1. Ingest the SRS document into vector store
    vector_store = process_document(input_file_path)
    print("\n\n\n **** Step 1 : Processing SRS document complete ! ****\n\n\n")
    print(vector_store)

    # 2. Retrieve functional requirements from the vector store
    functional_requirements = extract_functional_requirements()
    print("\n\n\n **** Step 2 : Retrieving Functional Requirement complete ! ****\n\n\n")
    print(functional_requirements)

    # 3. Parse functional requirements into a structured format
    requirements = parse_requirements(functional_requirements)
    print("\n\n\n **** Step 3 : Functional Req in a python object complete ! ****\n\n\n")
    print(requirements)

    # 4. Build the FastAPI project folder structure (skeleton)
    project_path = create_project_skeleton()
    print("\n\n\n **** Step 4 : Creating Project Sekeleton complete ! ****\n\n\n")
    print(project_path)

    # 5. Connect the database and write the db schema models
    models_file, migrations_file = setup_database(project_path, requirements)
    print("\n\n\n **** Step 5 : Database setup complete ! ****\n\n\n")
    print(models_file, migrations_file)

    return project_path

if __name__ == "__main__":
    output = run_workflow("srs_docs/sample.txt")

    # pretty print the output in json format
    try:
        parsed = json.loads(output)
        print(json.dumps(parsed, indent=2))
    except :
        print(output)

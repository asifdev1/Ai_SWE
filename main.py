import os
import argparse
import logging
import warnings

from dotenv import load_dotenv
from langgraph.workflow import run_workflow  # workflow runner

# -----------------------------------------------------------------------------
# 1. Load .env file (for GROQ_API_KEY, CONNECTION_STRING, etc.)
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# 2. Suppress verbose logs and warnings
# -----------------------------------------------------------------------------
warnings.filterwarnings("ignore")
logging.getLogger("langchain").setLevel(logging.ERROR)
logging.getLogger("langchain_community").setLevel(logging.ERROR)
logging.getLogger("unstructured").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# -----------------------------------------------------------------------------
# 3. Entry point
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate a FastAPI project from an SRS document using LangGraph."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the SRS document (.docx or .pdf)."
    )
    args = parser.parse_args()

    output_dir = "output_projects"
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Pass it into the workflow via an environment variable or directly, as your nodes expect
    os.environ["OUTPUT_DIR"] = output_dir

    print(f"\n▶️  Starting workflow for SRS: {args.input}\n\n")

    try:
        # This triggers the LangGraph pipeline:
        # 1. Ingest & chunk the document
        # 2. Extract requirements
        # 3. Parse into Python objects
        # 4. Build default project skeleton
        # 5. Setup DB connection in the project

        result_path = run_workflow(args.input)

        print("\n✅  Workflow completed successfully!")
        print(f"📂  Generated project available at: {result_path}\n")
 
    except Exception as e:
        logging.error("🚨 Workflow failed with an exception:", exc_info=True)
        print(f"\n❌  Error: {e}\n")
        exit(1)

if __name__ == "__main__":
    main()

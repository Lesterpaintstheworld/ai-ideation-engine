from dotenv import load_dotenv
import os
import logging
from ai_ideation_engine import EnhancedAIIdeationEngine
from add_files import main as add_files

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("AI Ideation Engine started")

    # Call add_files function to add the files
    add_files(directories_to_scan=["specs"], exclude_dirs=set(), exclude_extensions={".py", ".md"})

    # Initialize the AI Ideation Engine
    ideation_engine = EnhancedAIIdeationEngine()

    # Create the specs directory if it doesn't exist
    os.makedirs("specs", exist_ok=True)

    # Generate new AI concepts
    new_concepts = ideation_engine.generate_ideas()

    # Develop specifications for the new concepts
    for concept in new_concepts:
        spec = ideation_engine.develop_specification(concept)
        safe_filename = "".join([c for c in concept if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        ideation_engine.save_specification(spec, f"specs/{safe_filename}.md")

    # Assess the feasibility of the new concepts
    for concept in new_concepts:
        feasibility = ideation_engine.assess_feasibility(concept)
        logger.info(f"Concept '{concept}' feasibility: {feasibility}")

    # Refine the concepts through collaborative sessions
    for concept in new_concepts:
        refined_concept = ideation_engine.refine_concept(concept)
        safe_filename = "".join([c for c in refined_concept if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        ideation_engine.save_specification(refined_concept, f"specs/{safe_filename}.md")

    logger.info("AI Ideation Engine completed its cycle")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please make sure it's correctly set in your .env file.")
        exit(1)
    
    main()

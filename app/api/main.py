from app.dialogue.generate import generate_response
from app.research.tech_seda.extractor import tech_seda_analyze
from app.research.curriculum.alignment import curriculum_align
from app.pedagogy.scaffold import scaffold_decision
from app.logging.logger import log_interaction


def run_pipeline(student_input: str):

    llm_result = generate_response(student_input)
    seda = tech_seda_analyze(student_input)
    curriculum = curriculum_align(student_input)
    pedagogy = scaffold_decision(seda, curriculum)

    final_output = {
        "llm": llm_result,
        "tech_seda": seda,
        "curriculum": curriculum,
        "pedagogy": pedagogy
    }

    log_interaction(final_output)

    return final_output


if __name__ == "__main__":
    while True:
        user_input = input("\nStudent: ")
        output = run_pipeline(user_input)

        print("\n=== AI RESPONSE ===")
        print(output["llm"]["response"])

        print("\n=== TECH-SEDA ===")
        print(output["tech_seda"])

        print("\n=== CURRICULUM ===")
        print(output["curriculum"])

        print("\n=== PEDAGOGY ===")
        print(output["pedagogy"])


        def run_pipeline(student_input: str):
            print("STEP 1: LLM")
            llm_result = generate_response(student_input)

            print("STEP 2: TECH-SEDA START")
            seda = tech_seda_analyze(student_input)
            print("STEP 2: TECH-SEDA DONE")

            print("STEP 3: CURRICULUM START")
            curriculum = curriculum_align(student_input)
            print("STEP 3: CURRICULUM DONE")

            print("STEP 4: PEDAGOGY")
            pedagogy = scaffold_decision(seda, curriculum)

            print("STEP 5: LOG")
            log_interaction(...)
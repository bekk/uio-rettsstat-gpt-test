from write_to_md import write_test_to_md
import textwrap
from llm_engine import llm_engine
import config


# Function to get better output in terminal
def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split("\n")

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = "\n".join(wrapped_lines)

    return wrapped_text


# Prints response form LLM in terminal
def process_llm_response(llm_response):
    print(wrap_text_preserve_newlines(llm_response["result"]))
    print("\n\nSources:")
    # sort res by each elements metadata["score"] descending
    llm_response["source_documents"] = sorted(
        llm_response["source_documents"], key=lambda x: x.metadata["score"], reverse=True)
    for source in llm_response["source_documents"]:
        print(
            f"{source.metadata['source'].split('/')[-1]} | score: {str(format(source.metadata['score'], '.4f'))} | har_mindretall: {str(source.metadata['har_mindretall'])}"
        )
    print()


def main():
    engine = llm_engine()
    query_list = config.QUERYLIST

    answer_list = []
    for i, q in enumerate(query_list):
        answer = engine.ask_question(q)
        answer_list.append(answer)
        print(f"Test: {i+1}")
        process_llm_response(answer)
    write_test_to_md(config.FILENAME, query_list, answer_list)


if __name__ == "__main__":
    main()

import os
import config
import textwrap


def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split("\n")

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = "\n".join(wrapped_lines)

    return wrapped_text


def write_test_to_md(name_on_file, query_list: list, llm_answer: list, outputfolder='output'):
    # result, dic of llm output.
    # Write output to file

    # checking if the directory exist
    if not os.path.exists(outputfolder):

        # if the directory is not present then create it.
        os.makedirs(outputfolder)

    params = {
        "CHUNK_SIZE": config.CHUNK_SIZE,
        "CHUNK_OVERLAP": config.CHUNK_OVERLAP,
        "OPENAI_MODEL": config.OPENAI_MODEL,
        "TEMPERATURE": config.TEMPERATURE,
        "PROMPT": wrap_text_preserve_newlines(config.TEMPLATE_STRING),
        "SEARCH_TYPE": config.SEARCH_TYPE,
        "SEARCH_DOCUMENTS": config.SEARCH_DOCUMENTS,
        "CHAIN_TYPE": config.CHAIN_TYPE,
    }

    result_md = f"## Test: {name_on_file}\n"
    result_md += f"### Parameters\n"
    for name in params.keys():
        result_md += (f"- {name}: {params[name]}\n")

    result_md += "\n\n"
    result_md += "### Questions:\n\n"

    for i, query in enumerate(query_list):
        md_source = f"## Source dokuments {name_on_file}, query {i+1}\n\n"
        result_md += f"#### Query {i+1}:\n\n {query}\n\n"
        md_source += "#### Query:\n\n" + query + "\n\n"
        result_md += "#### LLM answer:\n\n" + \
            llm_answer[i]['result'] + "\n\n"
        result_md += ("\n\n")
        result_md += "#### Sources:\n\n"
        for i, source in enumerate(llm_answer[i]["source_documents"]):
            result_md += f"{i+1}: {source.metadata['source']} | score: {str(format(source.metadata['score'], '.4f'))} | har_mindretall: {str(source.metadata['har_mindretall'])}"
            # Add chunk_count if it exists
            if 'chunk_count' in source.metadata.keys():
                result_md += f" | chunk_count: {str(source.metadata['chunk_count'])}\n\n"
            else:
                result_md += "\n\n"
            md_source += f"### {source.metadata['source']}\n\n"
            md_source += f"{source.page_content}\n\n"

        result_md += "\n\n---\n\n\n"
        with open(f'{outputfolder}/source_{name_on_file}_{i+1}.md', 'w') as f:
            f.write(md_source)

    with open(f'{outputfolder}/Test_{name_on_file}.md', 'w') as f:
        f.write(result_md)

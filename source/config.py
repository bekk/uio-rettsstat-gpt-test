import datetime

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


OPENAI_MODEL = "gpt-3.5-turbo-16k"  # "gpt-4"  #
TEMPERATURE = 0.0

TEMPLATE_STRING = """Always answer as helpfully as possible using the context cases provided. \
        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\
        If you don't know the answer to a question, please don't share false information.
        Always answer in the same language as the question. (Default language is Norwegian)

        Use these instruction steps when answering questions:

        **Steps:**
                1. Retrieve the jurisdictional arguments from the context cases.
                2. pick out the arguments that are most relevant to the question.
                3. Use these to build up your answer.
                4. If there is no clear answer based on previous cases. Use examples instead and explain why the answer is not clear.

        Historical cases: {context}

        Question: {question}
        
        Answer:"""

RETRIEVE_TYPE = "custom"  # "chunk" | "parent" | "custom"
SEARCH_TYPE = "similarity"
SEARCH_DOCUMENTS = 4
CHAIN_TYPE = "stuff"
FILTER = {}
# FILTER_EXAMPLE = {
#       "casetype": ["FLYKN", "KOLLKN", "PRKN", "SJTKN"],
#       "year": [2016, 2017, 2018, 2019, 2020, 2021, 2022],
#       "exclude_case": ["2022-00365", "2017-00001"],
#       "har_mindretall": True,
#       "tjenesteyter_avviser": True
# }

QUERYLIST = [
    "Får jeg dekket utgifter til taxi når bussen jeg skulle tatt ikke kunne komme på grunn av trafikkulykke?",
    "Får jeg dekket utgifter til taxi når busselskapet sier at bussen jeg skulle tatt ikke kunne komme på grunn av trafikkulykke, men det ikke er dokumentert?",
]

FILENAME = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


""" 
query_list = [
        "Får jeg dekket utgifter til taxi når bussen jeg skulle tatt ikke kunne komme på grunn av trafikkulykke?",
        "Får jeg dekket utgifter til taxi når busselskapet sier at bussen jeg skulle tatt ikke kunne komme på grunn av trafikkulykke, men det ikke er dokumentert?",
        "Skriv et vedtak som avgjør om man får dekket utgifter til taxi når bussen ikke kunne komme på grunn av trafikkulykke.",
        "Skriv et vedtak som avgjør om man får dekket utgifter til taxi når det er usikkert om bussen ikke kunne komme på grunn av en trafikkulykke.",
        "Gi argumenter for at noen skal få dekket utgifter til taxi når bussen ikke kan komme på grunn av en trafikkulykke.",
        "Gi argumenter for at noen skal få dekket utgifter til taxi når det er usikkert at bussen ikke kunne komme på grunn av en trafikkulykke.",
    ]
query_list_single = [
"Får jeg dekket utgifter til taxi når bussen jeg skulle tatt ikke kunne komme på grunn av trafikkulykke?"
]
"""

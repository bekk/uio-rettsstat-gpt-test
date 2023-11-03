# uio-rettsstat-gpt-test
Et testkjøringsverktøy for spørringer til en OpenAi GPT-modell med klagesaker som kontekst.


## Setup environment

Hvis du ikke vil bruke ditt eget python environment kan du sette det opp slik med requiremebnts som er i requirements.txt.

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```


For å kjøre modellen trenger man en OPENAI_API_KEY som skal ligge i en .env fil

Filer som brukes til databasen skal ligge i en mappe struktru som ser slik ut:
data/<dinDataMappe>

Vectordatabaser kan lages fra data-mappen med uplodeDok.py eller legges inn i en mappe: embeddings/vectordb.

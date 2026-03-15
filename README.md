# test ai chatbot

For testing OpenAI compatible cloud LLMs
russian lang UI

## Implemented

- Terminal dialogs
- Multilines input
- Rendering markdown
- Inmemory storage
- Setting system prompt


## TODO

- telegram bot
- db for fialogs

## Running guide

**To start dialog in terminal**

1. Clone repo, install modules
```sh
git clone <paste here url or SSH-URL>
cd ai-test-chatbot
python3 -m venv venv # optional, requires python-env to be installed
source venv/bin/acrivate # for linux, optional
pip install -r requirements.txt
```
2. Get API token for LLM. You cat get it here for free https://openrouter.ai. Or any OpenAI compatible AI cloud provider. OpenAI also exactly
3. Create .env file from sample. Execute in terminal

```sh
cp .env.sample .env
```
4. Paste API key into .env file like this

```
OPENAI_API_KEY=<your API key>
```

4. If you use not https://openrouter.ai you have to specify BASE_URL and MODEL in config.py. 

5. Start chat in terminal

```sh
python3 openai-provider.py
```
6. 

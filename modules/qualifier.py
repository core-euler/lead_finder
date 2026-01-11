import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, Any

import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize LLM once at the module level to save memory
try:
    llm = ChatOpenAI(
        openai_api_key=config.COMET_API_KEY,
        openai_api_base=config.COMET_API_BASE_URL,
        model=config.COMET_API_MODEL,
        temperature=0.5,
        request_timeout=60  # Add a 60-second timeout
    )
    logger.info("LLM client initialized successfully.")
except Exception as e:
    llm = None
    logger.error(f"Failed to initialize LLM client: {e}")

def load_qualification_prompt() -> str:
    """Loads the v2 qualification prompt from the file."""
    try:
        with open('prompts/qualification_v2.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Qualification prompt file not found at 'prompts/qualification_v2.txt'")
        return ""

def format_enrichment_data_for_prompt(enrichment_data: Dict[str, Any], candidate_data: dict) -> str:
    """Formats the enrichment data into a string for the LLM prompt."""
    prompt_text = ""
    
    sample_messages = candidate_data.get("sample_messages", [])
    if sample_messages:
        prompt_text += "--- Примеры сообщений пользователя в чате ---\n"
        for msg in sample_messages:
            prompt_text += f'- "{msg}"\n'
        prompt_text += "\n"

    if enrichment_data.get("channel_data"):
        ch_data = enrichment_data["channel_data"].get("entity_data", {})
        prompt_text += "--- Данные с личного Telegram-канала ---\n"
        prompt_text += f"Название: {ch_data.get('title', 'N/A')}\n"
        prompt_text += f"Подписчиков: {ch_data.get('participants_count', 'N/A')}\n"
        prompt_text += f"Описание: {ch_data.get('about', 'N/A')}\n\n"

    if enrichment_data.get("web_search_data"):
        web_data = enrichment_data["web_search_data"]
        prompt_text += "--- Данные из веб-поиска ---\n"
        if web_data.get('website'):
            prompt_text += f"Найденный сайт: {web_data['website']}\n"
        mentions_str = "\n".join([f'- {m.get("title", "")} ({m.get("source", "")})' for m in web_data.get("mentions", [])])
        if mentions_str:
            prompt_text += f"Упоминания в сети:\n{mentions_str}\n"
        prompt_text += "\n"

    return prompt_text

def qualify_lead(candidate_data: dict, enrichment_data: dict, niche: str) -> dict:
    """Qualifies a lead using the pre-initialized LLM. Returns the result and the raw prompt."""
    if not llm:
        return {"error": "LLM client is not initialized."}

    prompt_template = load_qualification_prompt()
    if not prompt_template:
        return {"error": "Could not load qualification prompt."}

    input_data = (
        "--- Профиль пользователя в Telegram ---\n"
        f"Ниша, в которой он найден: {niche}\n"
        f"Имя: {candidate_data.get('first_name', '')} {candidate_data.get('last_name', '')}\n"
        f"Username: @{candidate_data.get('username', 'N/A')}\n"
        f"Био: {candidate_data.get('bio', 'N/A')}\n"
        f"Сообщений в чате-источнике: {candidate_data.get('messages_in_chat', 'N/A')}\n\n"
    )
    input_data += format_enrichment_data_for_prompt(enrichment_data, candidate_data)

    system_message = SystemMessage(content="You are a business analyst expert in B2B lead qualification. Analyze the profile and provide a structured JSON output based on the provided schema. Do not add any text before or after the JSON object.")
    human_message = HumanMessage(content=f"{prompt_template}\n\nВот полные данные для анализа:\n{input_data}")

    try:
        logger.info(f"Qualifying lead: @{candidate_data.get('username', 'N/A')}. Waiting for LLM...")
        
        import time
        start_time = time.time()
        response = llm.invoke([system_message, human_message])
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"LLM response received for @{candidate_data.get('username', 'N/A')}. Call duration: {duration:.2f} seconds.")

        json_response_str = response.content.strip().lstrip("```json").rstrip("```").strip()

        parsed_response = json.loads(json_response_str)
        logger.info(f"Successfully parsed LLM response for @{candidate_data.get('username', 'N/A')}")

        return {
            "llm_response": parsed_response,
            "raw_input_prompt": input_data
        }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from LLM response for @{candidate_data.get('username', 'N/A')}: {e}")
        logger.error(f"Raw response content: {response.content[:500]}")
        return {"error": "JSONDecodeError", "raw_response": response.content}
    except Exception as e:
        logger.error(f"An error occurred during lead qualification for @{candidate_data.get('username', 'N/A')}: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    print("Qualifier module v2. To be tested as part of the main pipeline.")

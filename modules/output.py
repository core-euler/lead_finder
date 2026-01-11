import json
import os
import datetime
import logging

logger = logging.getLogger(__name__)

def get_timestamped_filename(niche_slug: str, extension: str) -> str:
    """Generates a filename with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"leads_{niche_slug}_{timestamp}.{extension}"

def append_to_jsonl(lead: dict, filepath: str):
    """Appends a single lead object to a .jsonl file."""
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(lead, ensure_ascii=False) + '\n')
        # logger.info(f"Appended lead @{lead.get('contact', {}).get('telegram_username')} to {filepath}")
    except Exception as e:
        logger.error(f"Error appending to JSONL report {filepath}: {e}")

def format_lead_as_markdown(lead: dict, lead_index: int) -> str:
    """Formats a single lead into a markdown string."""
    qual_result = lead.get("qualification_result", {})
    qual = qual_result.get("qualification", {})
    identification = qual_result.get("identification", {})
    pains = qual_result.get("identified_pains", [])
    idea = qual_result.get("product_idea", {})
    outreach = qual_result.get("outreach", {})
    contact = lead.get("contact", {})
    enrichment = lead.get("enrichment_data", {})
    channel_entity_data = enrichment.get("channel_data", {}).get("entity_data", {})
    
    score = qual.get('score', 'N/A')
    md_block = f"## Лид #{lead_index} — Оценка: {score}/10\n\n"
    md_block += f"**Контакт:** {contact.get('telegram_username', 'N/A')}\n"
    if contact.get('telegram_channel'):
        md_block += f"**Канал:** {contact.get('telegram_channel')} ({channel_entity_data.get('participants_count', 'N/A')} подписчиков)\n\n"
    else:
        md_block += "\n"

    md_block += "### Бизнес\n"
    md_block += f"{identification.get('business_type', 'N/A')}. "
    md_block += f"Масштаб: {identification.get('business_scale', 'N/A')}.\n\n"
    
    md_block += "### Выявленные боли\n"
    if pains:
        for pain in pains:
            md_block += f"- {pain}\n"
    else:
        md_block += "Боли не выявлены.\n"
    md_block += "\n"
    
    md_block += "### Идея решения\n"
    if idea:
        md_block += f"**{idea.get('idea', 'N/A')}**\n"
        md_block += f"  - Закрываемая боль: {idea.get('pain_addressed', 'N/A')}\n"
        md_block += f"  - Ценность: {idea.get('estimated_value', 'N/A')}\n"
    else:
        md_block += "Идеи не сгенерированы.\n"
    md_block += "\n"
    
    md_block += "### Рекомендованное сообщение\n"
    message = outreach.get('message', 'N/A')
    formatted_message = message.replace('\n', '\n> ')
    md_block += f"> {formatted_message}\n\n"
    md_block += "---\n\n"
    
    return md_block

def initialize_markdown_file(filepath: str, niche: str):
    """Writes the header to the markdown file."""
    if os.path.exists(filepath):
        return # Header already exists
        
    report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"# Lead Finder Report\n"
    header += f"**Дата:** {report_date}\n"
    header += f"**Источник:** {niche}\n\n"
    header += "---\n\n"
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header)
    except Exception as e:
        logger.error(f"Error initializing Markdown report {filepath}: {e}")

def append_to_markdown(lead: dict, lead_index: int, filepath: str):
    """Appends a single formatted lead to a .md file."""
    try:
        md_block = format_lead_as_markdown(lead, lead_index)
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(md_block)
        # logger.info(f"Appended lead @{lead.get('contact', {}).get('telegram_username')} to {filepath}")
    except Exception as e:
        logger.error(f"Error appending to Markdown report {filepath}: {e}")
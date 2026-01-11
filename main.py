import argparse
import asyncio
import logging
import datetime
import os
from typing import List, Dict, Any

from modules import input_handler, members_parser, qualifier, output, telegram_client
from modules.enrichment import telegram as telegram_enricher
from modules.enrichment import web_search as web_enricher

from config import MIN_QUALIFICATION_SCORE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def enrich_candidate(candidate: Dict[str, Any], enrich_web: bool) -> Dict[str, Any]:
    enrichment_data = {}
    if candidate.get("has_channel") and candidate.get("channel_username"):
        channel_username = candidate["channel_username"]
        logger.info(f"Enriching with personal channel: {channel_username}")
        parsed_channel_data = await telegram_enricher.enrich_with_telegram_data(channel_username)
        if parsed_channel_data:
            enrichment_data["channel_data"] = parsed_channel_data
    
    if enrich_web:
        enrichment_data["web_search_data"] = web_enricher.enrich_with_web_search(candidate)

    return enrichment_data

async def parse_pipeline(args):
    sources = input_handler.process_sources(args.sources, args.file)
    if not sources:
        logger.error("No valid sources found. Exiting.")
        return

    all_candidates = []
    for source in sources:
        logger.info(f"--- Parsing source: {source} ---")
        candidates = await members_parser.parse_users_from_messages(
            chat_identifier=source, only_with_channels=args.only_with_channels,
            messages_limit=args.messages_limit
        )
        all_candidates.extend(candidates)
        logger.info(f"Found {len(candidates)} candidates from {source}. Total candidates: {len(all_candidates)}")

    logger.info(f"--- Found a total of {len(all_candidates)} unique candidates. ---")
    
    # --- New Incremental Output Logic ---
    qualified_leads_count = 0
    run_name = sources[0].replace('@','').replace('t.me/','').replace('t.me/+','')
    output_formats = [f.strip() for f in args.format.split(',')]
    
    jsonl_filepath = None
    if "json" in output_formats:
        jsonl_filename = output.get_timestamped_filename(run_name, "jsonl")
        jsonl_filepath = os.path.join(args.output_dir, jsonl_filename)

    md_filepath = None
    if "md" in output_formats:
        md_filename = output.get_timestamped_filename(run_name, "md")
        md_filepath = os.path.join(args.output_dir, md_filename)
        output.initialize_markdown_file(md_filepath, run_name)
    # --- End New Logic ---

    for i, candidate in enumerate(all_candidates):
        logger.info(f"--- Processing candidate {i+1}/{len(all_candidates)}: @{candidate['username']} ---")
        enrichment_data = await enrich_candidate(candidate, args.enrich)
        niche_context = candidate.get("source_chat", "general")
        qualification_result = qualifier.qualify_lead(candidate, enrichment_data, niche_context)
        
        if "error" in qualification_result:
            logger.error(f"Qualification error for @{candidate['username']}: {qualification_result['error']}")
            continue
        
        qualification_details = qualification_result.get("qualification", {})
        score = qualification_details.get("score", 0) if isinstance(qualification_details, dict) else 0
            
        if score < args.min_score:
            logger.info(f"Candidate @{candidate['username']} scored {score}, below threshold {args.min_score}. Skipping.")
            continue

        qualified_leads_count += 1
        logger.info(f"SUCCESS: Qualified @{candidate['username']} with score {score}. Lead #{qualified_leads_count}.")
        
        lead_card = {
            "id": candidate["user_id"], "timestamp": datetime.datetime.now().isoformat(),
            "source_chat": candidate["source_chat"], "niche_context": niche_context,
            "contact": {
                "telegram_username": f"@{candidate['username']}",
                "telegram_channel": candidate.get("channel_username"),
                "website": enrichment_data.get("web_search_data", {}).get("website"),
            },
            "user_profile": candidate, "enrichment_data": enrichment_data,
            "qualification_result": qualification_result
        }
        
        if jsonl_filepath:
            output.append_to_jsonl(lead_card, jsonl_filepath)
        if md_filepath:
            output.append_to_markdown(lead_card, qualified_leads_count, md_filepath)

        if qualified_leads_count >= args.max_leads:
            logger.info(f"Reached max leads limit of {args.max_leads}. Stopping.")
            break
            
    logger.info(f"--- Pipeline Finished ---")
    logger.info(f"Total candidates processed: {len(all_candidates)}")
    logger.info(f"Total leads qualified: {qualified_leads_count}")

    if qualified_leads_count > 0:
        if jsonl_filepath: logger.info(f"JSONL report saved to {jsonl_filepath}")
        if md_filepath: logger.info(f"Markdown report saved to {md_filepath}")
    else:
        logger.info("No qualified leads found. No output files created.")

async def search_pipeline(args):
    # Legacy v1 pipeline
    pass

def main():
    parser = argparse.ArgumentParser(description="Lead Finder v2")
    # ... (argparse setup is the same as my draft)
    # To save space, I will re-implement this part directly, it's complex for replace.
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    parser_parse = subparsers.add_parser("parse", help="Parse members from seed chats/channels (v2 pipeline).")
    parser_parse.add_argument("sources", nargs='*', help="List of seed sources (e.g., @chat1 @chat2).")
    parser_parse.add_argument("--file", type=str, help="File with a list of seed sources.")
    parser_parse.add_argument("--enrich", action="store_true", help="Enrich candidate data via web search.")
    parser_parse.add_argument("--messages-limit", type=int, default=500, help="Number of recent messages to parse from each source.")
    parser_parse.add_argument("--only-with-channels", action="store_true", help="Process only users who have a personal channel in their bio.")
    parser_parse.add_argument("--min-score", type=int, default=MIN_QUALIFICATION_SCORE, help="Minimum qualification score.")
    parser_parse.add_argument("--max-leads", type=int, default=50, help="Maximum number of leads to generate.")
    parser_parse.add_argument("--output-dir", type=str, default="./output", help="Directory for results.")
    parser_parse.add_argument("--format", type=str, default="json,md", help="Output formats (json,md). json is now jsonl.")

    parser_search = subparsers.add_parser("search", help="Legacy web search for channels (v1 pipeline).")
    parser_search.add_argument("niche", type=str, help="Niche description to search for.")
    parser_search.add_argument("--max-channels", type=int, default=20, help="Maximum channels to find.")

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    try:
        if args.command == "parse":
            loop.run_until_complete(parse_pipeline(args))
        elif args.command == "search":
            loop.run_until_complete(search_pipeline(args))
    finally:
        loop.run_until_complete(telegram_client.TelegramClientSingleton.disconnect_client())

if __name__ == '__main__':
    main()
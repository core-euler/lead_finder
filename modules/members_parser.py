import asyncio
import re
import logging
import telethon.tl.types
from modules.telegram_client import TelegramAuthManager, AuthorizationRequiredError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_channel_in_bio(bio_text: str) -> str | None:
    """Finds a potential personal channel link in a user's bio."""
    if not bio_text:
        return None
    match = re.search(r'(?<!\w)@([a-zA-Z0-9_]{5,32})', bio_text)
    if match:
        return match.group(0)
    match = re.search(r't\.me\/([a-zA-Z0-9_]{5,32})', bio_text)
    if match:
        return "t.me/" + match.group(1)
    return None

async def parse_users_from_messages(chat_identifier: str, only_with_channels: bool = False, messages_limit: int = 1000, max_messages_per_user: int = 5):
    """
    Parses active users by reading the message history of a chat, including their sample messages.
    """
    if not await TelegramAuthManager.is_authorized():
        logger.warning("Telegram client not authorized. Raising error to trigger auth flow.")
        raise AuthorizationRequiredError("Client is not authorized.")

    client = await TelegramAuthManager.get_client()
    logger.info(f"Starting to parse active users from messages in: {chat_identifier} (limit: {messages_limit} messages)")

    try:
        entity = await client.get_entity(chat_identifier)
        logger.info(f"Successfully got entity for '{chat_identifier}'. Type: {type(entity).__name__}")

        unique_users = {}  # Store user objects, message count, and sample messages
        messages_processed = 0
        
        logger.info(f"Fetching last {messages_limit} messages...")
        async for message in client.iter_messages(entity, limit=messages_limit):
            messages_processed += 1

            # Use message.get_sender() which is the robust way to get the sender entity
            sender = await message.get_sender()

            if sender and isinstance(sender, telethon.tl.types.User) and message.text:
                # Now 'sender' is the full user object.
                # Perform all checks on this full object.
                if sender.bot or sender.deleted or not sender.username:
                    continue
                
                if sender.id not in unique_users:
                    unique_users[sender.id] = {"user_obj": sender, "message_count": 0, "sample_messages": []}
                
                # Increment message count and add sample messages
                unique_users[sender.id]["message_count"] += 1
                if len(unique_users[sender.id]["sample_messages"]) < max_messages_per_user:
                    unique_users[sender.id]["sample_messages"].append(message.text)
        
        logger.info(f"Total messages processed: {messages_processed}. Found {len(unique_users)} unique active users.")

        # Fetch full user entities to get bio and other profile details
        logger.info(f"Fetching full user profiles for {len(unique_users)} users...")
        full_users = {}
        for user_id in unique_users.keys():
            try:
                full_user = await client.get_entity(user_id)
                full_users[user_id] = full_user
            except Exception as e:
                logger.warning(f"Failed to fetch full profile for user_id={user_id}: {e}")
                # Keep the partial user object if we can't get the full one
                full_users[user_id] = unique_users[user_id]["user_obj"]

        candidate_list = []
        for user_id, user_data in unique_users.items():
            user = full_users.get(user_id, user_data["user_obj"])

            # Now we have the full user object with 'about' field
            bio = getattr(user, 'about', None)
            channel_in_bio = find_channel_in_bio(bio)

            if only_with_channels and not channel_in_bio:
                continue

            candidate = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": bio,
                "has_channel": bool(channel_in_bio),
                "channel_username": channel_in_bio,
                "source_chat": chat_identifier,
                "messages_in_chat": user_data["message_count"],
                "sample_messages": user_data["sample_messages"]
            }
            candidate_list.append(candidate)

        logger.info(f"Found {len(candidate_list)} potential leads from message history.")
        return candidate_list

    except Exception as e:
        logger.error(f"Failed to parse messages from {chat_identifier}: {e}")
        return []

async def main():
    # This main function is for local testing of the module
    test_chat = "@tondev_eng" 
    logger.info(f"--- Testing Message Parser on chat: {test_chat} ---")
    
    try:
        candidates = await parse_users_from_messages(test_chat, only_with_channels=False, messages_limit=500)
    
        if candidates:
            print(f"\n--- Found {len(candidates)} active users from last 500 messages ---")
            candidates.sort(key=lambda x: x['messages_in_chat'], reverse=True)
            for i, candidate in enumerate(candidates[:15]):
                print(f"#{i+1}: @{candidate['username']} (Messages: {candidate['messages_in_chat']}) -> Bio: {candidate['bio']}")
                if candidate['sample_messages']:
                    print(f"  Sample messages: {candidate['sample_messages']}")
        else:
            print("\n--- No candidates found ---")
    finally:
        await TelegramAuthManager.disconnect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
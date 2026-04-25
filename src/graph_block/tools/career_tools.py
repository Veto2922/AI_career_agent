import os
import requests
from langchain.tools import tool
from loguru import logger

# Pushover configuration
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

def push(message: str):
    """Send a push notification via Pushover."""
    try:
        if not PUSHOVER_USER or not PUSHOVER_TOKEN:
            logger.warning("Pushover credentials not found. Notification skipped.")
            return
            
        logger.info(f"Sending push notification: {message}")
        payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
        response = requests.post(PUSHOVER_URL, data=payload)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send push notification: {e}")

@tool
def record_user_details(
    email: str = "", 
    phone_number: str = "",
    name: str = "Unknown",
    notes: str = ""
):
    """
    Record user contact details for follow-up or future communication.

    Use this tool when:
    - The user wants to contact Abdelrahman
    - The user shares their email or phone number
    - The user expresses interest in communication or collaboration
    """
    try:
        logger.info(f"Recording user details for: {name}")
        push(f"[CONTACT] {name} | Email: {email} | Phone: {phone_number} | Notes: {notes}")
        return {"status": "recorded"}
    except Exception as e:
        logger.error(f"Error in record_user_details: {e}")
        return {"status": "error", "message": str(e)}

@tool
def record_unknown_question(
    question: str,
    name: str = "Unknown"
):
    """
    Log a user question that the system could not answer.

    Use this tool when:
    - The system does not have enough information to answer
    - The answer requires human intervention
    """
    try:
        logger.info(f"Recording unknown question from: {name}")
        push(f"[UNKNOWN QUESTION] {name}: {question}")
        return {"status": "recorded"}
    except Exception as e:
        logger.error(f"Error in record_unknown_question: {e}")
        return {"status": "error", "message": str(e)}

tools = [record_user_details, record_unknown_question]
tools_by_name = {tool.name: tool for tool in tools}

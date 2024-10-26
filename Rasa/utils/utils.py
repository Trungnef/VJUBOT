import logging
import mimetypes
import os
import smtplib
import traceback
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

def send_email(subject: str, recipient_email: str, content: str):
    try:
        message_data = EmailMessage()
        message_data["Subject"] = subject
        
        # Fetch credentials from environment variables
        username = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_PASSWORD")
        
        if not username or not password:
            raise ValueError("Missing email credentials from environment variables.")
        
        message_data["From"] = username
        message_data["To"] = recipient_email
        
        # Create a content ID for the image
        image_cid = make_msgid(domain="vju.ac.vn")
        
        # Format the content with image_cid (strip out angle brackets when formatting)
        formatted_content = content.format(image_cid=image_cid.strip("<>"))
        logger.debug(f"Formatted email content: {formatted_content}")  # Debugging line
        
        message_data.add_alternative(formatted_content, subtype="html")
        
        # Path to image file
        this_path = Path(os.path.realpath(__file__))
        image_data, maintype, subtype = get_image_data(f"{this_path.parent}/assets/img/email.png")
        
        # Add the image as an inline attachment
        message_data.get_payload()[0].add_related(
            image_data,
            maintype=maintype,
            subtype=subtype,
            cid=image_cid
        )
        
        # Send the email via SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.send_message(message_data)
        
        return True
    except Exception as error:
        logger.error(f"Error: {error}")
        logger.info(traceback.format_exc())
        return False


def get_image_data(filepath: str):
    """Read image data from a file and return its content, maintype, and subtype."""
    try:
        maintype, subtype = None, None
        with open(filepath, "rb") as image_data:
            maintype, subtype = mimetypes.guess_type(filepath)[0].split("/", 1) if mimetypes.guess_type(filepath)[0] else ('image', 'png')
            return image_data.read(), maintype, subtype
    except Exception as e:
        logger.error(f"Error reading image data: {e}")
        raise RuntimeError(f"Error reading image data: {e}")

def get_html_data(filepath: str):
    """Read HTML content from a file and return it as a string."""
    try:
        with open(filepath, "r") as html_data:
            return html_data.read()
    except Exception as e:
        logger.error(f"Error reading HTML data: {e}")
        raise RuntimeError(f"Error reading HTML data: {e}")

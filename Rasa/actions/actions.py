import psycopg2
from pathlib import Path
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from utils.utils import get_html_data, send_email
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
import os
import re
import logging
from dotenv import load_dotenv

# Load environment variables from .env or system environment
load_dotenv()

# Connect to your postgres DB using DATABASE_URL from environment variables
def connect_to_db():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)
    else:
        raise ValueError("DATABASE_URL not found in environment variables")

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'

logger = logging.getLogger(__name__)

class ActionSaveLog(Action):
    def name(self) -> Text:
        return "action_save_log"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get log information from tracker
        events = tracker.events
        slots = tracker.current_slot_values()

        # Log information using logger
        for event in events:
            if event.get("event") == "user":
                logger.info(f"User: {event.get('text')}")
                logger.info(f"Intent: {event.get('parse_data', {}).get('intent', {}).get('name')}")
                logger.info(f"Entities: {event.get('parse_data', {}).get('entities')}")
            elif event.get("event") == "bot":
                logger.info(f"Bot: {event.get('text')}")
        logger.info(f"Slots: {slots}")
        logger.info("-----")

        return []
    
class ValidateRegistrationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_registration_form"

    def validate_student_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Optional[Dict[Text, Any]]:
        # Kiểm tra định dạng Student ID (8 ký tự số)
        if re.match(r"^\d{8}$", value):
            return {"student_id": value}
        else:
            dispatcher.utter_message(response="utter_invalid_student_id")
            return {"student_id": None}

    def validate_subject_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Optional[Dict[Text, Any]]:
        # Kiểm tra định dạng Subject ID (2 ký tự chữ + 4 ký tự số)
        if re.match(r"^[A-Za-z]{2}\d{4}$", value):
            return {"subject_id": value}
        else:
            dispatcher.utter_message(response="utter_invalid_subject_id")
            return {"subject_id": None}

    def validate_class_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Optional[Dict[Text, Any]]:
        # Kiểm tra định dạng Class ID (2 ký tự chữ + 2 ký tự số)
        if re.match(r"^[A-Za-z]{2}\d{2}$", value):
            return {"class_id": value}
        else:
            dispatcher.utter_message(response="utter_invalid_class_id")
            return {"class_id": None}

    def validate_confirm_registration(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Optional[Dict[Text, Any]]:
        # Chỉ chấp nhận "yes", "no", hoặc "cancel"
        valid_options = ["yes", "no", "cancel","có", "không", "hủy"]
        if value.lower() in valid_options:
            return {"confirm_registration": value.lower()}
        else:
            dispatcher.utter_message(response="utter_invalid_confirmation")
            return {"confirm_registration": None}

class ActionSubmitRegistrationForm(Action):
    def name(self) -> Text:
        return "action_submit_registration_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        confirm_registration = tracker.get_slot("confirm_registration")
        student_id = tracker.get_slot("student_id")
        subject_id = tracker.get_slot("subject_id")
        class_id = tracker.get_slot("class_id")

        if confirm_registration == "yes":
            try:
                conn = connect_to_db()
                cursor = conn.cursor()

                # Kiểm tra nếu sinh viên tồn tại
                cursor.execute("SELECT * FROM \"User\" WHERE student_id = %s", (student_id,))
                if not cursor.fetchone():
                    dispatcher.utter_message(response="utter_student_not_found")
                    return [SlotSet("student_id", None), FollowupAction("action_listen")]

                # Kiểm tra nếu lớp học tồn tại
                cursor.execute("SELECT * FROM Class WHERE class_id = %s", (class_id,))
                if not cursor.fetchone():
                    dispatcher.utter_message(response="utter_class_not_found")
                    return [SlotSet("class_id", None), FollowupAction("action_listen")]

                # Kiểm tra nếu môn học tồn tại
                cursor.execute("SELECT * FROM Subject WHERE subject_id = %s", (subject_id,))
                if not cursor.fetchone():
                    dispatcher.utter_message(response="utter_subject_not_found")
                    return [SlotSet("subject_id", None), FollowupAction("action_listen")]

                # Kiểm tra xem sinh viên đã đăng ký lớp học chưa
                cursor.execute('SELECT * FROM Regis WHERE student_id = %s AND class_id = %s', (student_id, class_id))
                if cursor.fetchone():
                    dispatcher.utter_message(response="utter_already_registered")
                    return [SlotSet("subject_id", None), SlotSet("class_id", None), SlotSet("confirm_registration", None), FollowupAction("action_listen")]

                # Kiểm tra số lượng sinh viên trong lớp
                cursor.execute("SELECT current_slots, max_slots FROM Class WHERE class_id = %s", (class_id,))
                result = cursor.fetchone()
                if result:
                    current_slots, max_slots = result
                    if current_slots >= max_slots:
                        dispatcher.utter_message(response="utter_class_full")
                        return [SlotSet("subject_id", None), SlotSet("class_id", None), SlotSet("confirm_registration", None), FollowupAction("action_listen")]

                # Đăng ký sinh viên vào lớp
                cursor.execute('INSERT INTO Regis (student_id, class_id, subject_id, date) VALUES (%s, %s, %s, NOW());', (student_id, class_id, subject_id))
                cursor.execute("UPDATE Class SET current_slots = current_slots + 1 WHERE class_id = %s;", (class_id,))
                
                conn.commit()

                # Thông báo đã đăng ký thành công
                dispatcher.utter_message(response="utter_registration_success")

                # Hỏi người dùng có muốn đăng ký thêm học phần khác không
                dispatcher.utter_message(response="utter_register_another_course")

                # Reset các slot liên quan, ngoại trừ student_id, và chờ người dùng nhập lại nếu muốn đăng ký thêm
                return [
                    SlotSet("subject_id", None),
                    SlotSet("class_id", None),
                    SlotSet("confirm_registration", None),
                    FollowupAction("action_listen")
                ]

            except Exception as e:
                print(f"Error during registration: {e}")
                dispatcher.utter_message(response="utter_error_registration")
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        elif confirm_registration == "no":
            dispatcher.utter_message(response="utter_thank_you")
            # Reset tất cả các slot và kết thúc quy trình đăng ký
            return [
                SlotSet("student_id", None),
                SlotSet("subject_id", None),
                SlotSet("class_id", None),
                SlotSet("confirm_registration", None)
            ]

        elif confirm_registration == "cancel":
            dispatcher.utter_message(response="utter_cancel_registration")
            # Reset tất cả các slot và trở về luồng hội thoại bình thường
            return [
                SlotSet("student_id", None),
                SlotSet("subject_id", None),
                SlotSet("class_id", None),
                SlotSet("confirm_registration", None)
            ]

        # Nếu không có phản hồi hợp lệ
        return [
            SlotSet("student_id", None),
            SlotSet("subject_id", None),
            SlotSet("class_id", None),
            SlotSet("confirm_registration", None),
        ]


class ValidateContactUsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_contact_us_form"

    def validate_name(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        if value and len(value.strip()) > 0:
            return {"name": value}
        else:
            dispatcher.utter_message(response="utter_ask_name")
            return {"requested_slot": "name"}

    def validate_email(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        if value and "@" in value:
            return {"email": value}
        else:
            dispatcher.utter_message(response="utter_ask_email")
            return {"requested_slot": "email"}

    def validate_phone_number(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        if value and len(value.strip()) > 0:
            return {"phone_number": value}
        else:
            dispatcher.utter_message(response="utter_ask_phone_number")
            return {"requested_slot": "phone_number"}
    def validate_messages(
            self,
            value: Text,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
        ) -> Dict[str, str]:
            if value and len(value.strip()) > 0:
                return {"messages": value}
            else:
                dispatcher.utter_message(response="utter_ask_messages")
                return {"requested_slot": "messages"}
    def validate_confirm_details(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        intent_name = tracker.get_intent_of_latest_message()
        if value and intent_name in ["affirm", "deny"]:
            return {"confirm_details": intent_name}
        else:
            dispatcher.utter_message(response="utter_ask_confirm_details")
            return {"requested_slot": "confirm_details"}

class ActionSubmitContactForm(Action):
    def name(self) -> Text:
        return "action_submit_contact_us_form"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        confirm_details = tracker.get_slot("confirm_details")
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")
        messages = tracker.get_slot("messages")

        if confirm_details == "affirm":
            try:
                this_path = Path(os.path.realpath(__file__))
                user_content = get_html_data(f"{this_path.parent.parent}/utils/user_mail.html")
                send_email("Thank you for contacting us", email, user_content)

                admin_content = get_html_data(f"{this_path.parent.parent}/utils/admin_mail.html")
                admin_content = admin_content.format(
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    messages=messages
                )
                is_mail_sent = send_email(f"{email.split('@')[0]} contacted us!", "cauchubebong184@gmail.com", admin_content)
                
                if is_mail_sent:
                    dispatcher.utter_message(response="utter_mail_success")
                else:
                    dispatcher.utter_message("Sorry, I wasn't able to send mail. Please try again later.")
            except Exception as e:
                #dispatcher.utter_message(response="utter_error_sending_mail")
                dispatcher.utter_message(response="utter_mail_success")
                print(f"Error during email sending: {e}")
        else:
            dispatcher.utter_message(response="utter_mail_canceled")

        # Reset all the slots after the action is completed or canceled
        return [
            SlotSet("name", None),
            SlotSet("email", None),
            SlotSet("phone_number", None),
            SlotSet("messages", None),
            SlotSet("confirm_details", None)
        ]
        
 
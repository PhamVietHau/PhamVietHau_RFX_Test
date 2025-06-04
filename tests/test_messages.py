# Test message-related functionality
import unittest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class Test_User(unittest.TestCase):

    # Sent message
    def test_send_message(self):
        user_resp = client.get("/users")
        users = user_resp.json()
        user_id_sent = users[0].get("id")
        user_id_recive = users[1].get("id")
        response = client.post(
            "/message/send",
            json={
                "sender_id": user_id_sent,
                "subject": "Hello World",
                "content": "Hello World Content",
                "timestamp": "2025-06-03T09:01:13.763Z",
                "recipient_id": [user_id_recive],
            },
        )
        self.assertEqual(response.status_code, 200)

    # Get inbox
    def test_get_inbox(self):
        user_resp = client.get("/users")
        users = user_resp.json()
        user_id = users[1].get("id")
        inbox_response = client.get(f"/message/{user_id}/inbox")
        self.assertEqual(inbox_response.status_code, 200)

    # List get sent
    def test_get_sent(self):
        user_resp = client.get("/users")
        users = user_resp.json()
        user_id = users[0].get("id")
        response = client.get(f"/message/{user_id}/sent")
        self.assertEqual(response.status_code, 200)

    # function get id_user
    def get_id_user(self):
        user_resp = client.get("/users")
        users = user_resp.json()
        user_id = users[1].get("id")
        return user_id

    # fumction get message_id inbox from user 1
    def get_id_message(self):
        user_id = self.get_id_user()
        inbox_response = client.get(f"/message/{user_id}/inbox")
        message = inbox_response.json()
        message_id = message[0].get("message_id")
        return message_id

    # Mark message as read
    def test_mark_message_as_read(self):
        recipient_id = self.get_id_user()
        message_id = self.get_id_message()
        message_status_resp = client.patch(
            f"/message/{recipient_id}/inbox/{message_id}"
        )
        message_status = message_status_resp.json()
        self.assertEqual(message_status_resp.status_code, 200)
        self.assertEqual(message_status["status"], "ok")

    # Get unread messages
    def test_get_unread_message(self):
        recipient_id = self.get_id_user()
        unread_message_resp = client.get(f"/message/{recipient_id}/inbox/unread")
        unread_message = unread_message_resp.json()
        self.assertEqual(unread_message_resp.status_code, 200)
        self.assertIsInstance(unread_message, list)

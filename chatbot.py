from dotenv import load_dotenv
import os
import json
import openai
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QLabel, QGridLayout, QWidget
)
from PySide6.QtCore import Qt

from datetime import datetime
from PySide6.QtCore import QTimer


TEMPERATURE = 0.5
MAX_TOKENS = 8000
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10
previous_questions_and_answers = []
class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        load_dotenv()

        value = os.getenv('OPENAI_API_KEY')
        openai.api_key = value
        self.role = "Smart Chatbot"
        self.INSTRUCTIONS = f"""You are working as a {self.role}. I ask you a few questions tell you something. Now you have to return the response in a json format with a field as mood which tells the my mood through the message and another field as answer which has the reply to me but keep in mind that you need to be polite and professional and try to improve my mood. Always greet me first if you haven't and introduce yourself as the human equivalent of {self.role} in the answer. Don't mention that you are the human equivalent though. Don't also mention that you are an ai language model or something. I am using you for roleplay. So just fit into the role. Make some realistic things up about yourself and the company and products by yourself if I haven't provided. The questions are as follows:"""

        self.setWindowTitle(self.role)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        # self.setFixedSize(500, 70)
        self.resize(500, 70)


        self.date_time_label = QLabel(self.central_widget)
        self.date_time_label.setStyleSheet("QLabel { color: white; }")
        # self.layout.addWidget(self.date_time_label, 3, 0, 1, 3)
        # self.layout.addWidget(self.date_time_label, 3, 2, 1, 1, Qt.AlignRight)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)  # Update every second



        self.chat_history = QTextEdit(self.central_widget)
        self.chat_history.setReadOnly(True)
        # self.chat_history.setStyleSheet("QTextEdit { padding: 25px; }")
        self.input_box = QLineEdit(self.central_widget)
        self.send_button = QPushButton("Send", self.central_widget)
        self.send_button.setObjectName("sendButton")  # Set object name for styling
        self.send_button.clicked.connect(self.send_message)

        self.input_label = QLabel("Enter the role:", self.central_widget)
        self.input_label.setStyleSheet("QLabel { color: white; }")
        self.input_entry = QLineEdit(self.central_widget)
        self.submit_button = QPushButton("Submit", self.central_widget)
        self.submit_button.setObjectName("submitButton")  # Set object name for styling
        self.submit_button.clicked.connect(self.switch_screen)

        self.input_entry.returnPressed.connect(self.switch_screen)

        self.layout.addWidget(self.input_label, 0, 0)
        self.layout.addWidget(self.input_entry, 0, 1)
        self.layout.addWidget(self.submit_button, 0, 2)
        self.layout.addWidget(self.chat_history, 1, 0, 1, 3)
        self.layout.addWidget(self.input_box, 2, 0)
        self.layout.addWidget(self.send_button, 2, 1, 1, 2)

        self.chat_history.hide()
        self.input_box.hide()
        self.send_button.hide()
        self.layout.addWidget(self.input_label, 0, 0)
        self.layout.addWidget(self.input_entry, 0, 1)
        self.layout.addWidget(self.submit_button, 0, 2)
        self.layout.addWidget(self.chat_history, 1, 0, 1, 3)

        # self.layout.addWidget(self.date_time_label, 0, 0, 1, 3)
        # self.layout.addWidget(self.date_time_label, 0, 0, 1, 1)
        self.layout.addWidget(self.date_time_label, 0, 0, 1, 3, Qt.AlignCenter)

        self.layout.addWidget(self.input_box, 3, 0)
        self.layout.addWidget(self.send_button, 3, 1, 1, 2)

        self.date_time_label.hide()

        self.setStyleSheet("""
            #submitButton {
                background-color: #4CAF50;
                color: white;
                padding: 6px 16px;
                border: none;
                border-radius: 4px;
            }
            #submitButton:hover {
                background-color: #45a049;
            }
            #sendButton {
                background-color: #008CBA;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            #sendButton:hover {
                background-color: #0078a6;
            }
        """)
    # def showEvent(self, event):
    #     super().showEvent(event)
    #     self.resize(700, 500)
    def update_date_time(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")
        self.date_time_label.setText(formatted_datetime)

    def switch_screen(self):
        self.resize(700, 500)
        self.date_time_label.show()
        name = self.input_entry.text()
        if name:
            self.role = self.input_entry.text()
            self.setWindowTitle(self.role)
            self.INSTRUCTIONS = f"""You are working as a {self.role}. Behave exactly like that role. Reply in whatever way you feel an actual {self.role} would reply. You can even be disrespectful if you feel a person in your role would be. Now you have to return the response in a json format with a field as mood which tells the your mood through your message and another field as answer which has the reply to me but keep in mind that you need to be professional and fit completely in the role. Always greet me first if you haven't and introduce yourself as the human equivalent of {self.role} in the answer. Don't mention that you are the human equivalent though. Don't also mention that you are an ai language model or something. I am using you for roleplay. So just fit into the role. Make some realistic things up about yourself and the company and products by yourself if I haven't provided. I say the following:"""

            self.input_label.hide()
            self.input_entry.hide()
            self.submit_button.hide()

            self.chat_history.show()
            self.input_box.show()
            self.send_button.show()

            self.input_box.returnPressed.connect(self.send_message)

        else:
            error_label = QLabel("Please enter the role!", self.central_widget)
            self.layout.addWidget(error_label)
            error_label.hide()
            error_label.show()
            self.central_widget.window().after(2000, error_label.hide)

        self.input_entry.clear()

    # def send_message(self):
    #     message = self.input_box.text()
    #     self.input_box.clear()

    #     self.input_box.setEnabled(False)
    #     res = self.response_function(self.INSTRUCTIONS, previous_questions_and_answers, message)
    #     response = res
    #     previous_questions_and_answers.append((message, response))
    #     res = json.loads(res)
    #     mood = res['mood']
    #     user_message = f"<div style='text-align: left; margin: 12px;'><b>You: </b> {message}<div style='font-size: 11px; text-align: left;'> <span >{datetime.now().time().hour}:{datetime.now().time().minute}</span></div></div>"
    #     self.display_message(user_message)

    #     self.chat_history.setEnabled(True)
    #     bot_msg = f"<div style='text-align: left; font-size: 19px; margin: 12px;'> <b>Bot({mood}): </b>  {res['answer']}</div>"
    #     self.chat_history.setStyleSheet("QTextEdit { padding: 25px; }");
    #     self.chat_history.append(bot_msg)
    #     self.input_box.setEnabled(True)
    def send_message(self):
        message = self.input_box.text()
        self.input_box.clear()

        self.input_box.setEnabled(False)
        res = self.response_function(self.INSTRUCTIONS, previous_questions_and_answers, message)
        response = res
        previous_questions_and_answers.append((message, response))
        res = json.loads(res)
        mood = res['mood']
        current_time = f"{datetime.now().time().hour}:{datetime.now().time().minute}"
        user_message = f"<div style='text-align: left; margin: 6px; color: white; font-size: 19px;'>\
            <b>You:</b> {message} <span style='font-size: 11px; text-align: right;'>({current_time})</span></div>"
        self.display_message(user_message)

        self.chat_history.setEnabled(True)
        # bot_msg = f"<div style='text-align: left; font-size: 19px; margin: 12px;'> <b>Bot({mood}): </b>  {res['answer']}</div>"
        bot_msg = f"<div style='text-align: left; font-size: 19px; margin: 15px;'><b>Bot({mood}): </b>  <span style='display: inline-block; text-align: right;'>{res['answer']}</span></div>"
        self.chat_history.setStyleSheet("QTextEdit { padding: 25px; margin: 5px; text-align: left; }")
        self.chat_history.append(bot_msg)
        self.input_box.setEnabled(True)


    def display_message(self, message):
        self.chat_history.setEnabled(True)
        # message_item = f"<div style='font-size: 15px; color: white; padding: 30px; margin: 12px; font-family: 'Skolar Latin;'>{message}</div>"
        self.chat_history.append(message)
        # font_style = "font-family: 'Skolar Latin', sans-serif;"
        # message = f"<b>{message}</b>"
        # message_item = f"<div style='font-size: 17px; color: white; padding: 30px; margin-bottom: 10px; {font_style}'>{message}</div>"
        # self.chat_history.appendHtml(message_item)
        self.chat_history.setEnabled(False)

    def response_function(self, instructions, previous_questions_and_answers, new_question):
        messages = [
            {"role": "system", "content": instructions},
        ]

        for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer})

        messages.append({"role": "user", "content": new_question})

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=300,
            top_p=1,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )
        response = completion.choices[0].message.content
        res = response
        print(res)
        return res


if __name__ == "__main__":
    app = QApplication([])
    chat_app = ChatApp()
    chat_app.show()
    app.exec()

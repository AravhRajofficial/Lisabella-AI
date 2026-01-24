from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout,QPushButton, QFrame, QLabel, QSizePolicy, QComboBox
from PyQt5.QtGui import QIcon, QPainter , QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextCursor, QCursor
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint, QRect
import random
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
Username = env_vars.get("Username")
AssistantVoice = env_vars.get("AssistantVoice")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    questions_words = ["who", "what", "when", "where", "why", "how","which","whose","whom", "can you", "what's", "where's", "why's", "how's", "who's", "how's"]

    if any(word + " " in new_query for word in questions_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(TempDirectoryPath('Mic.data'), 'w', encoding='utf-8') as file:
        file.write(Command)

def GetMicButtonStatus():
    try:
        with open(TempDirectoryPath('Mic.data'), 'r', encoding='utf-8') as file:
            Status = file.read()
    except FileNotFoundError:
        Status = "False"
    return Status 

def SetAssistantStatus(Status):
    with open(TempDirectoryPath('Status.data'), 'w', encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    try:
        with open(TempDirectoryPath('Status.data'), 'r', encoding='utf-8') as file:
            Status = file.read()
    except FileNotFoundError:
        Status = "Idle"
    return Status   

def SetMicOff():
    SetMicrophoneStatus("False")

def SetMicOn():
    SetMicrophoneStatus("True")

def GraphicDirectoryPath(Filename):
    Path = rf"{GraphicDirPath}\{Filename}"
    return Path

def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path

def ShowTextToScreen(Text):
    with open (rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self) :
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10,40,40,100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction) # no text interaction
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        # Gradient background for Chat Section
        self.setStyleSheet("""
            QWidget {
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5, stop:0 #1c1c1c, stop:1 #000000);
            }
            QTextEdit {
                background-color: transparent;
                border: none;
            }
        """) 
        layout.addWidget(self.chat_text_edit)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_color = QColor(Qt.white)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicDirectoryPath('lisabella.gif'))
        max_gif_size_W = 480
        max_gif_size_H = 270
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color: #00ea00; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px; font-family: 'Segoe UI'; font-weight: bold;")
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Segoe UI")
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecoText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)

        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a command...")
        self.input_field.setPlaceholderText("Type a command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #202020;
                color: #e0e0e0;
                border: 2px solid #3a3a3a;
                border-radius: 25px;
                padding: 12px 25px;
                font-family: 'Segoe UI';
                font-size: 16px;
                margin: 0px 10px; 
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background-color: #2a2a2a;
            }
        """)
        self.input_field.returnPressed.connect(self.sendMessage)
        
        self.send_button = QPushButton()
        self.send_button.setText("➤")
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 15px;
                padding: 8px 15px;
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                min-width: 40px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        self.send_button.clicked.connect(self.sendMessage)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }

            QScrollBar::add-line:vertical {
                background: #2d2d2d;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                background: #2d2d2d;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def loadMessages(self):
        global old_chat_message
        with open(TempDirectoryPath('Responses.data'), 'r', encoding='utf-8') as file:
            messages = file.read()
            if messages is None:
                pass
            elif len(messages) <= 1:
                pass
            elif str(old_chat_message) == str(messages):
                pass
            else:
                self.addMessages(messages=messages, color='white')
                old_chat_message = messages
            
    def SpeechRecoText(self):
        with open(TempDirectoryPath('Status.data'), 'r', encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)
            
    def sendMessage(self):
        text = self.input_field.text().strip()
        if text:
            # Show user message immediately
            self.addMessages(f"User: {text}", "white")
            self.input_field.clear()
            
            # Write to TextInput.data for Main.py to pick up
            with open(TempDirectoryPath('TextInput.data'), 'w', encoding='utf-8') as file:
                file.write(text)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicDirectoryPath('voice.png'), 60, 60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicDirectoryPath('mic.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled
    
    def addMessages(self, messages, color):
        cursor = self.chat_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End) # Ensure at end
        
        format = QTextCharFormat()
        block_format = cursor.blockFormat()
        format.setForeground(QColor(color))
        block_format.setTopMargin(10)
        block_format.setBottomMargin(10) # Add breathing room
        
        cursor.setCharFormat(format)
        cursor.setBlockFormat(block_format)
        
        # Add a newline prefix if not empty to separate from previous
        # Parse the message content to handle combined "User: ... \nLisabella: ..."
        # Split by newlines first, but keep the logic robust
        lines = messages.split('\n')
        for line in lines:
            if not line.strip():
                continue
                
            if "User:" in line:
                clean_msg = line.replace("User:", "").strip()
                # User Message -> RIGHT aligned (Blue)
                html = f"""
                <div style="width: 100%; text-align: right; margin-bottom: 10px;">
                    <span style="background-color: #0078d4; color: white; padding: 12px 20px; border-radius: 20px; font-family: 'Segoe UI'; font-size: 16px; display: inline-block;">
                        {clean_msg}
                    </span>
                </div>
                """
                cursor.insertHtml(html)
                cursor.insertBlock()
                
            elif "Lisabella:" in line:
                clean_msg = line.replace("Lisabella:", "").strip().replace("*", "") # Remove markdown stars
                # Assistant Message -> LEFT aligned (Grey)
                html = f"""
                <div style="width: 100%; text-align: left; margin-bottom: 10px;">
                     <span style="background-color: #333333; color: #e0e0e0; padding: 12px 20px; border-radius: 20px; font-family: 'Segoe UI'; font-size: 16px; display: inline-block;">
                        {clean_msg}
                    </span>
                </div>
                """
                cursor.insertHtml(html)
                cursor.insertBlock()
                
            else:
                # Fallback for lines without prefix (append to previous or generic)
                # For now, treat as generic right-aligned
                html = f"""
                <div style="width: 100%; text-align: right; margin-bottom: 10px;">
                     <span style="background-color: #333333; color: #e0e0e0; padding: 12px 20px; border-radius: 20px; font-family: 'Segoe UI'; font-size: 16px; display: inline-block;">
                        {line}
                    </span>
                </div>
                """
                cursor.insertHtml(html)
                cursor.insertBlock()
            
        cursor.insertBlock() # Ensure new line after HTML block
            
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0,0,0,0)
        gif_label = QLabel()
        movie  = QMovie(GraphicDirectoryPath('lisabella.gif'))
        self.setCursor(Qt.ArrowCursor)  # Reset cursor to default
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) # Remove margins to fill screen
        
        # --- DYNAMIC AVATAR SETUP ---
        self.avatar_label = QLabel(self)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        
        # Load Avatar Images
        self.img_idle = QPixmap(GraphicDirectoryPath('Avatar_Idle.png'))
        self.img_blink = QPixmap(GraphicDirectoryPath('Avatar_Blink.png'))
        self.img_talk = QPixmap(GraphicDirectoryPath('Avatar_Talking.png'))
        
        # Scale Images (Make them big and nice)
        avatar_size = QSize(350, 350) 
        self.img_idle = self.img_idle.scaled(avatar_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_blink = self.img_blink.scaled(avatar_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_talk = self.img_talk.scaled(avatar_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.avatar_label.setPixmap(self.img_idle) # Start with idle
        
        # Blinking Timer
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_animation)
        self.start_blinking()
        
        self.is_blinking = False
        self.is_talking = False

        # Status Label
        self.status_label = QLabel("Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #e0e0e0; font-size: 24px; font-family: 'Segoe UI Light'; margin-top: 20px;")
        
        # Microphone Button
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setCursor(Qt.PointingHandCursor)  # Hand cursor for interactivity
        self.load_icon(GraphicDirectoryPath('Mic_on.png'), 60, 60)
        self.icon_label.mousePressEvent = self.toggle_icon
        
        # Premium Mic Button Styling
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: #252525;
                border-radius: 75px; /* Circular */
                padding: 15px;
                border: 3px solid #00ff00; /* Green border for active */
                box-shadow: 0 0 15px #00ff00;
            }
            QLabel:hover {
                background-color: #303030;
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
            }
        """)

        # Layout Assembly
        layout.addStretch()
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Initialize as Active
        SetMicOn()
        self.toggled = False # Next click will turn it OFF
        
        # Timer for updating status text
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    def start_blinking(self):
        # Wink/Blink every 3-6 seconds
        interval = random.randint(3000, 6000) 
        self.blink_timer.start(interval)

    def blink_animation(self):
        if not self.is_talking:
            self.avatar_label.setPixmap(self.img_blink)
            self.is_blinking = True
            # Close eyes for 200ms then open
            QTimer.singleShot(200, self.finish_blink)
        
        # Reset timer for next random blink
        self.start_blinking()
        
    def finish_blink(self):
        if not self.is_talking:
            self.avatar_label.setPixmap(self.img_idle)
        self.is_blinking = False

    def load_icon(self, path, width, height):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicDirectoryPath('Mic_on.png'), 60, 60)
            SetMicOn() 
            # Visual feedback for Active (Green)
            self.icon_label.setStyleSheet("""
                QLabel {
                    background-color: #252525;
                    border-radius: 75px;
                    border: 3px solid #00ff00; /* Green border for active */
                    box-shadow: 0 0 15px #00ff00;
                }
                QLabel:hover {
                    background-color: #303030;
                }
            """)
            
            # Switch Avatar to TALKING/LISTENING
            self.is_talking = True
            self.avatar_label.setPixmap(self.img_talk)
            
        else:
            self.load_icon(GraphicDirectoryPath('Mic_off.png'), 60, 60)
            SetMicOff()
            # Visual feedback for Inactive (Grey)
            self.icon_label.setStyleSheet("""
                QLabel {
                    background-color: #1a1a1a;
                    border-radius: 75px;
                    border: 2px solid #555555; /* Grey border for inactive */
                }
                QLabel:hover {
                    background-color: #252525;
                    border: 2px solid #888888;
                }
            """)
            # Switch Avatar back to IDLE
            self.is_talking = False
            self.avatar_label.setPixmap(self.img_idle)
            
        self.toggled = not self.toggled

    def update_status(self):
        status = GetAssistantStatus() 
        self.status_label.setText(status)

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #1a1a1a;")
        # self.setFixedHeight(screen_height) # REMOVED for resizing
        # self.setFixedWidth(screen_width) # REMOVED for resizing


class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("color: white; font-size: 24px; font-family: 'Segoe UI Semibold'; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Username Field
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #e0e0e0; font-size: 16px; font-family: 'Segoe UI';")
        self.username_input = QLineEdit()
        self.username_input.setText(Username)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #202020;
                color: #e0e0e0;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Assistant Name Field
        assistant_label = QLabel("Assistant Name")
        assistant_label.setStyleSheet("color: #e0e0e0; font-size: 16px; font-family: 'Segoe UI';")
        self.assistant_input = QLineEdit()
        self.assistant_input.setText(Assistantname)
        self.assistant_input.setStyleSheet("""
            QLineEdit {
                background-color: #202020;
                color: #e0e0e0;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        layout.addWidget(assistant_label)
        layout.addWidget(self.assistant_input)

        # Voice Tone Selection
        voice_label = QLabel("Voice Tone")
        voice_label.setStyleSheet("color: #e0e0e0; font-size: 16px; font-family: 'Segoe UI';")
        self.voice_combo = QComboBox()
        self.voice_combo.addItem("Soft, Warm, Friendly (Default)", "en-US-AriaNeural")
        self.voice_combo.addItem("Straight, Professional (Male)", "en-US-GuyNeural")
        
        # Set current selection
        if AssistantVoice == "en-US-GuyNeural":
            self.voice_combo.setCurrentIndex(1)
        else:
            self.voice_combo.setCurrentIndex(0)

        self.voice_combo.setStyleSheet("""
            QComboBox {
                background-color: #202020;
                color: #e0e0e0;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #0078d4;
            }
        """)
        layout.addWidget(voice_label)
        layout.addWidget(self.voice_combo)
        
        
        layout.addStretch()
        
        # Save Button
        save_btn = QPushButton("Save Changes")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        save_btn.clicked.connect(self.saveSettings)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
        # Unified background
        self.setStyleSheet("""
            QWidget {
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5, stop:0 #1c1c1c, stop:1 #000000);
            }
            QLabel {
                background: transparent;
            }
        """)

    def RestartApp(self):
        """ Restarts the entire application using a temporary batch script. """
        restart_script = os.path.join(os.getcwd(), "Restart.bat")
        with open(restart_script, "w") as f:
            f.write("@echo off\n")
            f.write("echo Restarting Lisabella...\n")
            f.write("timeout /t 2 /nobreak >nul\n")
            f.write("taskkill /F /IM python.exe /T >nul 2>&1\n")
            f.write("taskkill /F /IM pythonw.exe /T >nul 2>&1\n")
            f.write("start Run.bat\n")
            f.write("del \"%~f0\"\n") # Self-delete
            
        os.startfile(restart_script)
        QApplication.quit()

    def saveSettings(self):
        new_username = self.username_input.text()
        new_assistantname = self.assistant_input.text()
        new_voice = self.voice_combo.currentData()
        
        # Read existing .env content
        with open('.env', 'r') as f:
            lines = f.readlines()
            
        # Update specific keys
        with open('.env', 'w') as f:
            for line in lines:
                if line.startswith('Username='):
                    f.write(f'Username="{new_username}"\n')
                elif line.startswith('Assistantname='):
                    f.write(f'Assistantname="{new_assistantname}"\n')
                elif line.startswith('AssistantVoice='):
                    f.write(f'AssistantVoice="{new_voice}"\n')
                else:
                    f.write(line)
                    
        # Add AssistantVoice if it didn't exist
        env_content = "".join(lines)
        if "AssistantVoice" not in env_content:
             with open('.env', 'a') as f:
                f.write(f'\nAssistantVoice="{new_voice}"\n')

        print("Settings saved. Restarting...")
        self.RestartApp()

class CustomTopBar(QWidget):
    def __init__(self, parent=None, stacked_widget=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()
        self.current_screen = None

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton()
        home_icon = QIcon(GraphicDirectoryPath('Home.png'))
        home_button.setIcon(home_icon)
        home_button.setText(" Home")
        
        # PROPOSED BUTTON STYLE
        button_style = """
            QPushButton {
                height: 40px; 
                border: none; 
                background-color: transparent; 
                color: #e0e0e0;
                font-family: 'Segoe UI';
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
        """
        
        home_button.setStyleSheet(button_style)
        message_button = QPushButton()
        message_icon = QIcon(GraphicDirectoryPath('Chat.png'))
        message_button.setIcon(message_icon)
        message_button.setText(" Chat")
        message_button.setStyleSheet(button_style)

        settings_button = QPushButton()
        settings_icon = QIcon(GraphicDirectoryPath('Setting.png')) # Assuming a Setting.png exists or use a generic one/text
        # If no icon, text fallback
        if settings_icon.isNull():
             settings_button.setText(" Settings")
        else:
             settings_button.setIcon(settings_icon)
             settings_button.setText(" Settings")

        settings_button.setStyleSheet(button_style)
        
        window_control_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
        """
        close_control_style = """
             QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e81123;
            }
        """

        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicDirectoryPath('Minimize.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet(window_control_style)
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setStyleSheet(window_control_style)
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_icon = QIcon(GraphicDirectoryPath('Close.png'))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet(close_control_style)
        close_button.clicked.connect(self.closeWindow)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: #404040;")
        title_label = QLabel(f" {str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet("color: #e0e0e0; font-size: 18px; background-color: transparent; font-family: 'Segoe UI Semibold'; padding-left: 10px;")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addWidget(settings_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        # layout.addWidget(line_frame) # This line adds the line_frame to the QHBoxLayout, which is not what was intended. It should be a separate element or part of a different layout.
        self.setLayout(layout) # Set the layout for the CustomTopBar
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        # Make the top bar background transparent to blend with the main window's gradient
        # or give it a semi-transparent dark overlay
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100)) # Semi-transparent black
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def ShowMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Default size: Portrait Mode (450x800), centered
        default_width = 450
        default_height = 800
        x_pos = (screen_width - default_width) // 2
        y_pos = (screen_height - default_height) // 2
        
        self.setGeometry(x_pos, y_pos, default_width, default_height)
        self.setWindowIcon(QIcon(GraphicDirectoryPath('Home.png'))) # Set Window Icon for Taskbar visibility
        
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        settings_screen = SettingsScreen()
        
        stacked_widget.addWidget(initial_screen) # Index 0
        stacked_widget.addWidget(message_screen) # Index 1
        stacked_widget.addWidget(settings_screen) # Index 2
        
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)
        
        # Resizing Attributes
        self.resize_margin = 10
        self.cursor_pos = None
        self.resizing = False
        self.resize_edge = None
        self.setMouseTracking(True) # Enable mouse tracking for hover effects

    def paintEvent(self, event):
        # Optional: Paint a border or resize handle visual
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edge = self.check_edge(event.pos())
            if edge:
                self.resizing = True
                self.resize_edge = edge
                self.cursor_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPos() - self.cursor_pos
            self.handle_resize(delta)
            self.cursor_pos = event.globalPos()
        else:
            edge = self.check_edge(event.pos())
            if edge:
                self.set_cursor_shape(edge)
            else:
                self.unsetCursor()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.resize_edge = None
        self.unsetCursor()

    def check_edge(self, pos):
        # Return which edge the mouse is on: "top", "bottom", "left", "right", "top_left", etc.
        rect = self.rect()
        margin = self.resize_margin
        
        on_left = pos.x() < margin
        on_right = pos.x() > rect.width() - margin
        on_top = pos.y() < margin
        on_bottom = pos.y() > rect.height() - margin
        
        if on_top and on_left: return "top_left"
        if on_top and on_right: return "top_right"
        if on_bottom and on_left: return "bottom_left"
        if on_bottom and on_right: return "bottom_right"
        if on_top: return "top"
        if on_bottom: return "bottom"
        if on_left: return "left"
        if on_right: return "right"
        return None

    def set_cursor_shape(self, edge):
        if edge in ["top_left", "bottom_right"]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge in ["top_right", "bottom_left"]:
            self.setCursor(Qt.SizeBDiagCursor)
        elif edge in ["top", "bottom"]:
            self.setCursor(Qt.SizeVerCursor)
        elif edge in ["left", "right"]:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.unsetCursor()

    def handle_resize(self, delta):
        rect = self.geometry()
        edge = self.resize_edge
        
        if "right" in edge:
            rect.setWidth(max(300, rect.width() + delta.x()))
        if "bottom" in edge:
            rect.setHeight(max(200, rect.height() + delta.y()))
        if "left" in edge:
            new_width = max(300, rect.width() - delta.x())
            if new_width > 300:
                rect.setLeft(rect.left() + delta.x())
        if "top" in edge:
            new_height = max(200, rect.height() - delta.y())
            if new_height > 200:
                rect.setTop(rect.top() + delta.y())
        
        self.setGeometry(rect)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(GraphicDirectoryPath('Home.png'))) # Set App Icon
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
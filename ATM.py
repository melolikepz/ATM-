import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt


class User:
    def __init__(self, password="1234", balance=10000):
        self.password = password
        self.balance = balance

    def check_password(self, entered_password):
        return self.password == entered_password

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def transfer(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def change_password(self, new_password):
        self.password = new_password
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATM")
        self.resize(500, 300)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        widget.setLayout(layout)

        label1 = QLabel("Choose language:")
        button1 = QPushButton("English")
        label2 = QLabel("زبان خود را انتخاب کنید:")
        button2 = QPushButton("فارسی")

        layout.addWidget(label1)
        layout.addWidget(button1)
        layout.addWidget(label2)
        layout.addWidget(button2)

        widget.setStyleSheet("background-color: pink;")
        button1.setStyleSheet("background-color: black; color: white;")
        button2.setStyleSheet("background-color: black; color: white;")

        button1.clicked.connect(lambda: self.open_password_window("English"))
        button2.clicked.connect(lambda: self.open_password_window("Farsi"))

    def open_password_window(self, language):
        self.password_window = PasswordWindow(User(), language)
        self.password_window.show()
        self.close()


class PasswordWindow(QWidget):
    def __init__(self, user, language):
        super().__init__()
        self.user = user
        self.language = language
        self.setWindowTitle("Enter Password" if language == "English" else "ورود رمز عبور")
        self.resize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Enter your password:" if language == "English" else "رمز عبور خود را وارد کنید:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_edit = QLineEdit()
        self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.line_edit.setStyleSheet("border: 2px solid purple; padding: 5px;")

        button = QPushButton("Submit" if language == "English" else "تأیید")
        button.setStyleSheet("background-color: black; color: white; border: 2px solid purple; border-radius: 5px;")
        button.clicked.connect(self.check_password)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(button)

        self.setStyleSheet("background-color: pink; color: black;")

    def check_password(self):
        entered_password = self.line_edit.text()
        if self.user.check_password(entered_password):
            self.operations_window = OperationWindow(self.user, self.language)
            self.operations_window.show()
            self.close()
        else:
            self.line_edit.setText("")
            error_label = QLabel(
                "Incorrect password. Please try again." if self.language == "English" else "رمز اشتباه است. دوباره امتحان کنید.")
            error_label.setStyleSheet("color: red;")
            self.layout().addWidget(error_label)


class OperationWindow(QWidget):
    def __init__(self, user, language):
        super().__init__()
        self.user = user
        self.language = language
        self.setWindowTitle("Choose Operation" if language == "English" else "انتخاب عملیات")
        self.resize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        button1 = QPushButton("View Balance" if language == "English" else "مشاهده موجودی")
        button2 = QPushButton("Withdraw Money" if language == "English" else "برداشت وجه")
        button3 = QPushButton("Transfer Money" if language == "English" else "انتقال وجه")
        button4 = QPushButton("Change Password" if language == "English" else "تغییر رمز عبور")
        button5 = QPushButton("Exit" if language == "English" else "خروج")

        for button in [button1, button2, button3, button4, button5]:
            button.setStyleSheet("background-color: black; color: white; border: 2px solid purple; border-radius: 5px;")
            layout.addWidget(button)

        button1.clicked.connect(self.show_balance)
        button2.clicked.connect(self.open_withdraw_window)
        button3.clicked.connect(self.open_transfer_window)
        button4.clicked.connect(self.open_change_password_window)
        button5.clicked.connect(self.close)

        self.setStyleSheet("background-color: pink; color: black;")

    def show_balance(self):
        message = f"Your balance: {self.user.balance} units" if self.language == "English" else f"موجودی شما: {self.user.balance} واحد"
        self.result_window = ResultWindow(self.user, message, self.language)
        self.result_window.show()
        self.close()

    def open_withdraw_window(self):
        self.withdraw_window = WithdrawWindow(self.user, self.language)
        self.withdraw_window.show()
        self.close()

    def open_transfer_window(self):
        self.transfer_window = TransferWindow(self.user, self.language)
        self.transfer_window.show()
        self.close()

    def open_change_password_window(self):
        self.change_password_window = ChangePasswordWindow(self.user, self.language)
        self.change_password_window.show()
        self.close()


class ResultWindow(QWidget):
    def __init__(self, user, message, language):
        super().__init__()
        self.user = user
        self.language = language
        self.setWindowTitle("Result" if language == "English" else "نتیجه")
        self.resize(500, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Back to Operations" if language == "English" else "بازگشت به عملیات")
        button.setStyleSheet("background-color: black; color: white; border: 2px solid purple; border-radius: 5px;")
        button.clicked.connect(self.back_to_operations)

        layout.addWidget(label)
        layout.addWidget(button)

        self.setStyleSheet("background-color: pink; color: black;")

    def back_to_operations(self):
        self.op_window = OperationWindow(self.user, self.language)
        self.op_window.show()
        self.close()


class WithdrawWindow(QWidget):
    def __init__(self, user, language):
        super().__init__()
        self.user = user
        self.language = language
        self.setWindowTitle("Withdraw Money" if language == "English" else "برداشت وجه")
        self.resize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Enter amount to withdraw:" if language == "English" else "مبلغ برداشت را وارد کنید:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet("border: 2px solid purple; padding: 5px;")

        button = QPushButton("Withdraw" if language == "English" else "برداشت")
        button.setStyleSheet("background-color: black; color: white; border: 2px solid purple; border-radius: 5px;")
        button.clicked.connect(self.withdraw_money)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(button)

        self.setStyleSheet("background-color: pink; color: black;")

    def withdraw_money(self):
        try:
            amount = int(self.line_edit.text())
            if self.user.withdraw(amount):
                self.result_window = ResultWindow(self.user, "Withdrawal successful!" if self.language == "English" else "برداشت موفقیت‌آمیز بود!", self.language)
                self.result_window.show()
                self.close()
            else:
                self.result_window = ResultWindow(self.user, "Insufficient funds!" if self.language == "English" else "موجودی کافی نیست!", self.language)
                self.result_window.show()
                self.close()
        except ValueError:
            self.result_window = ResultWindow(self.user, "Invalid amount!" if self.language == "English" else "مقدار نامعتبر!", self.language)
            self.result_window.show()
            self.close()


class TransferWindow(QWidget):
    def __init__(self, user, language):
        super().__init__()
        self.user = user
        self.language = language
        self.setWindowTitle("Transfer Money" if language == "English" else "انتقال وجه")
        self.resize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Enter amount to transfer:" if language == "English" else "مبلغ انتقال را وارد کنید:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet("border: 2px solid purple; padding: 5px;")

        button = QPushButton("Transfer" if language == "English" else "انتقال")
        button.setStyleSheet("background-color: black; color: white; border: 2px solid purple; border-radius: 5px;")
        button.clicked.connect(self.transfer_money)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(button)

        self.setStyleSheet("background-color: pink; color: black;")

    def transfer_money(self):
        try:
            amount = int(self.line_edit.text())
            if self.user.transfer(amount):
                self.result_window = ResultWindow(self.user, "Transfer successful!" if self.language == "English" else "انتقال موفقیت‌آمیز بود!", self.language)
                self.result_window.show()
                self.close()
            else:
                self.result_window = ResultWindow(self.user, "Insufficient funds!" if self.language == "English" else "موجودی کافی نیست!", self.language)
                self.result_window.show()
                self.close()
        except ValueError:
            self.result_window = ResultWindow(self.user, "Invalid amount!" if self.language == "English" else "مقدار نامعتبر!", self.language)
            self.result_window.show()
            self.close()


class ChangePasswordWindow(QWidget):
    def __init__(self, user, language):
        super().__init__()
        self.user = user
        self.language = language
        self.setWindowTitle("Change Password" if language == "English" else "تغییر رمز عبور")
        self.resize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Enter new password:" if language == "English" else "رمز جدید را وارد کنید:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_edit = QLineEdit()
        self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.line_edit.setStyleSheet("border: 2px solid purple; padding: 5px;")

        button = QPushButton("Change Password" if language == "English" else "تغییر رمز")
        button.setStyleSheet("background-color: black; color: white; border: 2px solid purple; border-radius: 5px;")
        button.clicked.connect(self.change_password)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(button)

        self.setStyleSheet("background-color: pink; color: black;")

    def change_password(self):
        new_password = self.line_edit.text()
        if new_password.strip():
            self.user.change_password(new_password)
            self.result_window = ResultWindow(self.user, "Password changed successfully!" if self.language == "English" else "رمز با موفقیت تغییر کرد!", self.language)
            self.result_window.show()
            self.close()
        else:
            self.result_window = ResultWindow(self.user, "Invalid password!" if self.language == "English" else "رمز نامعتبر!", self.language)
            self.result_window.show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

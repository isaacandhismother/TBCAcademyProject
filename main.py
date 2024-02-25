'''

პროგრამა არის Microsoft Teams-ის ავტორიზაციისა და რეგისტრაციის იმიტაცია.

ყველა ინფორმაციას, ანუ username და password-ს პროგრამა იღებს 'Teams_data.txt' ფაილიდან
და შეუძლია როგორც წაიკითხოს ის ავტორიძაციისას ასევე დაამატოს რეგისტრაციისას.

StackedWidget-ს ჯერ არ ვარ მიჩვეული და ამიტომ გავაკეთე ისე, როგორც ადრე მიხერხდებოდა,
მაგრამ ამის გერეშეც კოდი ისედაც მომწონს)g

Test setup: Windows 10, python 3.9, PyQt 5.15.9

'''

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

HEIGHT = 360
WIDTH = 480


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    win = QWidget()
    win.setFixedSize(WIDTH, HEIGHT)
    win.setWindowIcon(QtGui.QIcon('Teams.png'))
    win.setWindowTitle('Microsoft Teams')

    main_window = QWidget()
    main_window.setFixedSize(1024, 768)
    main_window.setWindowIcon(QtGui.QIcon('Teams.png'))
    main_window.setWindowTitle('Microsoft Teams')

# ---------------- Menu list --------------------

    menus = {}

    def hide_menus():
        for menu in menus:
            for widget in menu:
                widget.hide()

    main_menu = []
    menus.append(main_menu)

    def show_main_menu():
        hide_menus()

        for widget in main_menu:
            widget.show()

    registration_menu = []
    menus.append(registration_menu)

    def show_registration():
        hide_menus()

        for widget in registration_menu:
            widget.show()

# -----------------------------------------------

    def compare_data(filename, given_username_password, check_password: bool):
        file = open(filename, 'r')
        username_password = {'username': '', 'password': ''}

        matched = False

        word = ''

        for line in file.readlines():
            if not matched:
                for letter in line:
                    if letter == ':':
                        username_password['username'] = word.replace('\n', '')
                        word = ''
                    elif letter == ';':
                        username_password['password'] = word
                        word = ''
                    elif letter != ' ':
                        word += letter

                if check_password is True:
                    if username_password == given_username_password:
                        file.close()
                        return True
                else:
                    if username_password['username'] == given_username_password['username']:
                        file.close()
                        return True
        file.close()
        return False

    def login():
        written_username_password = {'username': username_field.text(),
                                     'password': password_field.text()}

        answer = compare_data('Teams_data.txt', written_username_password, True)

        if answer is True:

            win.hide()

            main_window.show()

            try:
                main_menu.remove(wrong_username_or_password)
            except(ValueError):
                pass
            wrong_username_or_password.hide()
        else:
            main_menu.append(wrong_username_or_password)
            wrong_username_or_password.show()

    def register():
        written_new_username_password = {'username': new_username_field.text(),
                                         'password': new_password_field.text()}

        answer = compare_data('Teams_data.txt', written_new_username_password, False)

        if (new_password_field.text() == repeat_new_password_field.text()
                and ((new_password_field.text() and repeat_new_password_field.text()) != '')
                and (new_username_field.text() != '') and answer is False):

            with open('Teams_data.txt', 'r') as file_obj:
                # read first character
                first_char = file_obj.read(1)
                file = open('Teams_data.txt', 'a')
                if not first_char:
                    file.write(f'{new_username_field.text()}: {new_password_field.text()};')
                else:
                    file.write(f'\n{new_username_field.text()}: {new_password_field.text()};')
                print('Registered successfully!')
                file.close()
            file.close()

            show_main_menu()

        if new_password_field.text() != repeat_new_password_field.text():
            registration_menu.append(passwords_not_matching)
            passwords_not_matching.show()
        else:
            try:
                registration_menu.remove(passwords_not_matching)
            except(ValueError):
                pass
            passwords_not_matching.hide()

        if answer is True:
            registration_menu.append(username_already_taken)
            username_already_taken.show()
        else:
            try:
                registration_menu.remove(username_already_taken)
            except(ValueError):
                pass
            username_already_taken.hide()

    # ------------- Main menu section ---------------

    logo = QLabel(win)
    logo_png = QPixmap('Teams.png')
    logo_png = logo_png.scaled(70, 60)
    logo.setPixmap(logo_png)
    logo.move(190, 35)
    main_menu.append(logo)

    enter_username = QLabel(win)
    enter_username.setText('Username:')
    enter_username.move(130, 100)
    main_menu.append(enter_username)

    username_field = QLineEdit(win)
    username_field.move(130, 120)
    username_field.resize(200, 25)
    main_menu.append(username_field)

    enter_password = QLabel(win)
    enter_password.setText('Password:')
    enter_password.move(130, 160)
    main_menu.append(enter_password)

    password_field = QLineEdit(win)
    password_field.move(130, 180)
    password_field.resize(200, 25)
    password_field.setEchoMode(QLineEdit.Password)
    main_menu.append(password_field)

    login_button = QPushButton(win)
    login_button.setText('Login')
    login_button.move(130, 230)
    login_button.clicked.connect(login)
    main_menu.append(login_button)

    register_button = QPushButton(win)
    register_button.setText('Register')
    register_button.move(220, 230)
    register_button.resize(110, 21)
    register_button.clicked.connect(show_registration)
    main_menu.append(register_button)

    wrong_username_or_password = QLabel(win)
    wrong_username_or_password.setText('* wrong username or password')
    wrong_username_or_password.move(150, 270)
    wrong_username_or_password.setStyleSheet('color: red')
    wrong_username_or_password.hide()

# -----------------------------------------------

# ---------- Registration menu section ----------

    enter_new_username = QLabel(win)
    enter_new_username.setText('Enter a new username:')
    enter_new_username.move(130, 40)
    registration_menu.append(enter_new_username)

    username_already_taken = QLabel(win)
    username_already_taken.setText('* username already taken')
    username_already_taken.move(250, 40)
    username_already_taken.setStyleSheet('color: red')
    username_already_taken.hide()

    new_username_field = QLineEdit(win)
    new_username_field.move(130, 60)
    new_username_field.resize(200, 25)
    registration_menu.append(new_username_field)

    enter_new_password = QLabel(win)
    enter_new_password.setText('Enter a new password:')
    enter_new_password.move(130, 100)
    registration_menu.append(enter_new_password)

    new_password_field = QLineEdit(win)
    new_password_field.move(130, 120)
    new_password_field.resize(200, 25)
    new_password_field.setEchoMode(QLineEdit.Password)
    registration_menu.append(new_password_field)

    repeat_new_password = QLabel(win)
    repeat_new_password.setText('Repeat a new password:')
    repeat_new_password.move(130, 160)
    registration_menu.append(repeat_new_password)

    passwords_not_matching = QLabel(win)
    passwords_not_matching.setText('* passwords are not matching')
    passwords_not_matching.move(255, 160)
    passwords_not_matching.setStyleSheet('color: red')
    passwords_not_matching.hide()

    repeat_new_password_field = QLineEdit(win)
    repeat_new_password_field.move(130, 180)
    repeat_new_password_field.resize(200, 25)
    repeat_new_password_field.setEchoMode(QLineEdit.Password)
    registration_menu.append(repeat_new_password_field)

    new_registration_button = QPushButton(win)
    new_registration_button.setText('Register')
    new_registration_button.move(130, 230)
    new_registration_button.resize(110, 21)
    new_registration_button.clicked.connect(register)
    registration_menu.append(new_registration_button)

    back_button = QPushButton(win)
    back_button.setText('Back')
    back_button.move(250, 230)
    back_button.clicked.connect(show_main_menu)
    registration_menu.append(back_button)

# ----------------------------------------------

    def print_help():
        print('Help is no longer coming')

# ----------------------------------------------

# ------------ Application window --------------

    logged_successfully = QLabel(main_window)
    logged_successfully.setText('You have logged successfully!')
    logged_successfully.setFont(QFont('Arial', 35))
    logged_successfully.move(200, 350)

# ----------------------------------------------

    microsoft_corporation = QLabel(win)
    microsoft_corporation.setText('Microsoft corporation (c) 2024')
    microsoft_corporation.move(30, 320)

    help_button = QPushButton(win)
    help_button.setText('Need help?')
    help_button.move(380, 320)
    help_button.setStyleSheet('color: blue;'
                              'border: None;'
                              'text-style: underline')
    help_button.clicked.connect(print_help)

    win.show()
    show_main_menu()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

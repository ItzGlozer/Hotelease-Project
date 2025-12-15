from PyQt6.QtWidgets import QMessageBox


class Logout:
    def __init__(self, main_window):
        self._main_window = main_window

    def logout(self):
        msg = QMessageBox(self._main_window)
        msg.setWindowTitle("Logout")
        msg.setText("Confirm to Logout")

        yes_btn = msg.addButton("Confirm", QMessageBox.ButtonRole.YesRole)
        no_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.NoRole)

        msg.exec()

        if msg.clickedButton() == yes_btn:
            self._main_window.close()







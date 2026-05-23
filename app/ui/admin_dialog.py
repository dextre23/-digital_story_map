from hashlib import sha256

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AdminLoginDialog(QDialog):
    PASSWORD_HASH = sha256("admin123".encode("utf-8")).hexdigest()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Admin Vault")
        self.resize(360, 200)
        self.setModal(True)
        self._authenticated = False

        title = QLabel("Admin Vault")
        title.setObjectName("adminDialogTitle")

        self.info = QLabel("Enter admin password to unlock")
        self.info.setStyleSheet("color: #8b95a8; font-size: 12px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")

        self.status_label = QLabel("")
        self.status_label.setObjectName("adminDialogStatus")

        self.login_button = QPushButton("Unlock")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("sidebarGhostBtn")
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.login_button.clicked.connect(self._check_password)
        self.cancel_button.clicked.connect(self.reject)
        self.password_input.returnPressed.connect(self._check_password)

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch()
        row.addWidget(self.cancel_button)
        row.addWidget(self.login_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(self.info)
        layout.addWidget(self.password_input)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addLayout(row)

    @property
    def authenticated(self) -> bool:
        return self._authenticated

    def _check_password(self) -> None:
        candidate = self.password_input.text().encode("utf-8")
        if sha256(candidate).hexdigest() == self.PASSWORD_HASH:
            self._authenticated = True
            self.accept()
            return
        self.status_label.setText("Invalid password.")
        self.password_input.clear()
        self.password_input.setFocus()

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QFont, QFontMetrics, QPainter, QLinearGradient, QColor, QBrush, QPen
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.data.texts import TEXTS


class _PageWidget(QWidget):
    def __init__(self, title: str, body: str, is_cover: bool = False, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("bookPage")
        self._is_cover = is_cover
        self._title = title
        self._body = body
        self._title_label = None
        self._body_label = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 14, 24, 14)
        layout.setSpacing(10)
        self._layout = layout

        if is_cover:
            cover_label = QLabel("📖")
            cover_label.setObjectName("bookCoverEmoji")
            cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            title_label = QLabel(title)
            title_label.setObjectName("bookCoverTitle")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setWordWrap(True)

            subtitle = QLabel(
                "Her kitap, okuyucusuna\neşsiz bir perspektif sunar"
            )
            subtitle.setObjectName("bookCoverSubtitle")
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout.addStretch(2)
            layout.addWidget(cover_label)
            layout.addSpacing(8)
            layout.addWidget(title_label)
            layout.addSpacing(4)
            layout.addWidget(subtitle)
            layout.addStretch(3)

            self.setObjectName("bookPageCover")
        else:
            self._title_label = QLabel(title)
            self._title_label.setObjectName("bookPageTitle")
            self._title_label.setWordWrap(True)

            self._body_label = QLabel(body)
            self._body_label.setObjectName("bookPageBody")
            self._body_label.setWordWrap(True)

            layout.addWidget(self._title_label)
            layout.addWidget(self._body_label, stretch=1)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self._is_cover or not self._body_label:
            return
        self._fit_text_to_page()

    def _fit_text_to_page(self) -> None:
        if not self._body_label:
            return
        w = self.width() - 48
        h = self.height() - 28
        th = self._title_label.sizeHint().height() + 10
        body_avail = max(40, h - th)
        text = self._body

        lo, hi = 10, 28
        best = 14
        while lo <= hi:
            mid = (lo + hi) // 2
            f = QFont()
            f.setPixelSize(mid)
            fm = QFontMetrics(f)
            lh = fm.height() + 2
            cpl = max(1, w // max(1, fm.averageCharWidth()))
            lines = max(1, len(text) // max(1, cpl))
            text_h = lines * lh
            if text_h <= body_avail:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        bf = self._body_label.font()
        bf.setPixelSize(best)
        self._body_label.setFont(bf)

        tf = self._title_label.font()
        ts = min(22, best + 5)
        tf.setPixelSize(ts)
        self._title_label.setFont(tf)


class BookReaderWidget(QWidget):
    map_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("bookReaderRoot")
        self._locale = "tr"
        self._current_index = 0
        self._animating = False

        self._build_pages()
        self._setup_ui()

    def _build_pages(self) -> None:
        self._pages = []
        cover_page = _PageWidget("Neden Kitap\nOkumalısın?", "", is_cover=True)
        self._pages.append(cover_page)
        for item in TEXTS:
            page = _PageWidget(item["title"], item["body"])
            self._pages.append(page)
        closing = _PageWidget("✨", "Okuyan bir toplum,\ndüşünen, sorgulayan\nve üreten bir toplumdur.", is_cover=True)
        closing.setObjectName("bookPageCover")
        self._pages.append(closing)

    def _setup_ui(self) -> None:
        top = QWidget()
        top.setObjectName("bookReaderTop")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(24, 16, 24, 12)

        self._head = QLabel()
        self._head.setObjectName("bookReaderHead")

        self._map_btn = QPushButton()
        self._map_btn.setObjectName("bookReaderMapBtn")
        self._map_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._map_btn.clicked.connect(self.map_requested.emit)

        top_layout.addWidget(self._head, stretch=1)
        top_layout.addWidget(self._map_btn)

        self._book_wrapper = QWidget()
        self._book_wrapper.setObjectName("bookWrapper")

        book_layout = QHBoxLayout(self._book_wrapper)
        book_layout.setContentsMargins(0, 0, 0, 0)
        book_layout.setSpacing(0)

        self._prev_btn = QPushButton()
        self._prev_btn.setObjectName("bookTurnBtn")
        self._prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._prev_btn.setText("◀")
        self._prev_btn.clicked.connect(self._go_prev)

        self._book_container = QWidget()
        self._book_container.setObjectName("bookContainer")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 120))
        self._book_container.setGraphicsEffect(shadow)

        self._book_stack = QWidget()
        self._book_stack.setObjectName("bookStack")
        self._stack_layout = QVBoxLayout(self._book_stack)
        self._stack_layout.setContentsMargins(0, 0, 0, 0)

        self._current_page_widget = QWidget()
        self._current_page_layout = QHBoxLayout(self._current_page_widget)
        self._current_page_layout.setContentsMargins(0, 0, 0, 0)
        self._current_page_layout.setSpacing(0)

        self._left_page = QWidget()
        self._left_page.setObjectName("bookLeftPage")
        self._left_page_layout = QVBoxLayout(self._left_page)
        self._left_page_layout.setContentsMargins(0, 0, 0, 0)

        self._spine = QWidget()
        self._spine.setObjectName("bookSpine")

        self._right_page = QWidget()
        self._right_page.setObjectName("bookRightPage")
        self._right_page_layout = QVBoxLayout(self._right_page)
        self._right_page_layout.setContentsMargins(0, 0, 0, 0)

        self._current_page_layout.addWidget(self._left_page, stretch=1)
        self._current_page_layout.addWidget(self._spine)
        self._current_page_layout.addWidget(self._right_page, stretch=1)

        self._stack_layout.addWidget(self._current_page_widget)

        self._opacity_effect = QGraphicsOpacityEffect()
        self._opacity_effect.setOpacity(1.0)
        self._current_page_widget.setGraphicsEffect(self._opacity_effect)

        container_layout = QVBoxLayout(self._book_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self._book_stack)

        self._next_btn = QPushButton()
        self._next_btn.setObjectName("bookTurnBtn")
        self._next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._next_btn.setText("▶")
        self._next_btn.clicked.connect(self._go_next)

        book_layout.addWidget(self._prev_btn)
        book_layout.addWidget(self._book_container, stretch=1)
        book_layout.addWidget(self._next_btn)

        self._page_counter = QLabel()
        self._page_counter.setObjectName("bookPageCounter")
        self._page_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        layout.addWidget(self._book_wrapper, stretch=1)
        layout.addWidget(self._page_counter)

        self._show_spread(0)
        self.apply_language("tr")

    def _show_spread(self, index: int) -> None:
        self._current_index = max(0, min(index, len(self._pages) - 1))
        self._clear_page(self._left_page_layout)
        self._clear_page(self._right_page_layout)

        left_idx = self._current_index
        right_idx = self._current_index + 1

        if left_idx < len(self._pages):
            self._left_page_layout.addWidget(self._pages[left_idx])
        else:
            placeholder = QLabel()
            placeholder.setObjectName("bookPageEmpty")
            self._left_page_layout.addWidget(placeholder)

        if right_idx < len(self._pages):
            self._right_page_layout.addWidget(self._pages[right_idx])
        else:
            placeholder = QLabel()
            placeholder.setObjectName("bookPageEmpty")
            self._right_page_layout.addWidget(placeholder)

        total_spreads = (len(self._pages) + 1) // 2
        current_spread = self._current_index // 2 + 1
        self._page_counter.setText(f"{current_spread} / {total_spreads}")

        self._prev_btn.setEnabled(self._current_index > 0)
        self._next_btn.setEnabled(right_idx < len(self._pages))

    def _clear_page(self, layout: QVBoxLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.hide()

    def _go_prev(self) -> None:
        if self._animating or self._current_index <= 0:
            return
        self._animate_to(self._current_index - 2)

    def _go_next(self) -> None:
        if self._animating or self._current_index + 1 >= len(self._pages):
            return
        self._animate_to(self._current_index + 2)

    def _animate_to(self, new_index: int) -> None:
        self._animating = True

        direction = -1 if new_index < self._current_index else 1
        start_x = 0
        end_x = direction * -60

        self._anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._anim.setDuration(200)
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(0.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.finished.connect(lambda: self._on_fade_out(new_index))
        self._anim.start()

    def _on_fade_out(self, new_index: int) -> None:
        self._show_spread(new_index)
        self._opacity_effect.setOpacity(0.0)

        self._anim2 = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._anim2.setDuration(250)
        self._anim2.setStartValue(0.0)
        self._anim2.setEndValue(1.0)
        self._anim2.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim2.finished.connect(lambda: setattr(self, "_animating", False))
        self._anim2.start()

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        from app.i18n import t
        self._head.setText("\U0001F4DA  " + t(locale, "btn_why_read"))
        self._map_btn.setText(t(locale, "btn_map"))

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget


class AnimatedSplashScreen(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(
            parent,
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.SplashScreen,
        )
        self._phase = 0.0
        self._sun_phase = 0.0
        self.setFixedSize(900, 520)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def _tick(self) -> None:
        self._phase += 0.04
        self._sun_phase += 0.03
        self.update()

    def paintEvent(self, event) -> None:
        w, h = float(self.width()), float(self.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        sky = QLinearGradient(0, 0, 0, h * 0.62)
        sky.setColorAt(0.0, QColor("#0f1a30"))
        sky.setColorAt(0.5, QColor("#1e3360"))
        sky.setColorAt(1.0, QColor("#3b6ba5"))
        p.fillRect(self.rect(), sky)

        sun_x = w * 0.78
        sun_y = h * 0.2
        sun_r = 36 + math.sin(self._sun_phase) * 4
        glow_alpha = int(60 + math.sin(self._sun_phase * 1.5) * 30)

        glow = QRadialGradient(QPointF(sun_x, sun_y), sun_r * 2.5)
        glow.setColorAt(0.0, QColor(244, 208, 63, glow_alpha))
        glow.setColorAt(1.0, QColor(244, 208, 63, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(glow)
        p.drawEllipse(QPointF(sun_x, sun_y), sun_r * 2.5, sun_r * 2.5)

        p.setPen(QPen(QColor("#f4d03f"), 2))
        p.setBrush(QColor(244, 208, 63, glow_alpha - 20))
        p.drawEllipse(QPointF(sun_x, sun_y), sun_r, sun_r)

        horizon = h * 0.58
        land_grad = QLinearGradient(0, horizon, 0, h)
        land_grad.setColorAt(0.0, QColor("#1a2620"))
        land_grad.setColorAt(1.0, QColor("#0c100c"))
        p.fillRect(QRectF(0, horizon, w, h - horizon), land_grad)

        title_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        p.setFont(title_font)
        p.setPen(QColor("#f0f3f8"))
        p.drawText(QRectF(40, h * 0.1, w - 80, 48), Qt.AlignmentFlag.AlignLeft, "Kitap Atlası")

        sub_font = QFont("Segoe UI", 13)
        p.setFont(sub_font)
        p.setPen(QColor("#b8c4d9"))
        p.drawText(QRectF(40, h * 0.1 + 44, w - 80, 32), Qt.AlignmentFlag.AlignLeft, "Yükleniyor...")

        wave_path = QPainterPath()
        base_y = h * 0.72
        steps = 60
        points: list[tuple[float, float]] = []
        for i in range(steps + 1):
            x = (i / steps) * w
            ang = (x / w) * math.tau * 2.2 + self._phase
            y = base_y + math.sin(ang) * 14 + math.sin(ang * 0.5 + 1.1) * 6
            points.append((x, y))
        wave_path.moveTo(0, h)
        wave_path.lineTo(0, points[0][1])
        for x, y in points:
            wave_path.lineTo(x, y)
        wave_path.lineTo(w, h)
        wave_path.closeSubpath()
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#1e2d28"))
        p.drawPath(wave_path)

        wave_path2 = QPainterPath()
        base_y2 = h * 0.78
        pts2: list[tuple[float, float]] = []
        for i in range(steps + 1):
            x = (i / steps) * w
            ang = (x / w) * math.tau * 2.8 - self._phase * 1.1
            y = base_y2 + math.sin(ang) * 10
            pts2.append((x, y))
        wave_path2.moveTo(0, h)
        wave_path2.lineTo(0, pts2[0][1])
        for x, y in pts2:
            wave_path2.lineTo(x, y)
        wave_path2.lineTo(w, h)
        wave_path2.closeSubpath()
        p.setBrush(QColor("#152018"))
        p.drawPath(wave_path2)

        p.end()

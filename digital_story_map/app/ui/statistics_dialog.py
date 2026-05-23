from collections import Counter
from math import pi

from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QLineSeries,
    QPieSeries,
    QValueAxis,
)
from PySide6.QtCore import QMargins, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t
from app.ui.search_utils import entry_city

BG_COLOR = QColor("#11161e")
CARD_BG = QColor("#151b26")
TEXT_COLOR = QColor("#f0f3f8")
MUTED = QColor("#8b95a8")
ACCENT = QColor("#4e89ff")
ACCENT2 = QColor("#7d4e9a")
ACCENT3 = QColor("#2a6b3c")
GRID_LINE = QColor("rgba(255,255,255,0.06)")


def _make_font(size: int = 11, bold: bool = False) -> QFont:
    f = QFont("Segoe UI", size)
    f.setBold(bold)
    return f


class ModernChartView(QChartView):
    def __init__(self, chart: QChart) -> None:
        super().__init__(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet("background-color: transparent; border: none;")


class StatisticsDialog(QDialog):
    def __init__(self, entries: list[dict], parent=None, locale: str = "tr") -> None:
        super().__init__(parent)
        self._locale = locale
        self._entries = entries
        self.setWindowTitle(t(self._locale, "stats_window"))
        self.resize(860, 560)
        self.setModal(True)

        tabs = QTabWidget()
        tabs.setObjectName("statsTabs")
        tabs.addTab(self._build_city_tab(), t(self._locale, "chart_top_cities"))
        tabs.addTab(self._build_genre_tab(), "Tür")
        tabs.addTab(self._build_year_tab(), "Yıl")
        tabs.addTab(self._build_sentiment_tab(), "Duygu")

        title = QLabel(t(self._locale, "stats_window"))
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #f0f3f8; padding: 4px 0;")
        count_label = QLabel(f"{len(entries)} kitap kaydı")
        count_label.setStyleSheet("font-size: 12px; color: #8b95a8; padding: 0 0 8px 0;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(count_label)
        layout.addWidget(tabs)

    def _styled_chart(self, title_text: str = "") -> QChart:
        chart = QChart()
        if title_text:
            chart.setTitle(title_text)
            chart.setTitleBrush(TEXT_COLOR)
            chart.setTitleFont(_make_font(14, True))
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundRoundness(12)
        chart.setBackgroundBrush(BG_COLOR)
        chart.setPlotAreaBackgroundVisible(False)
        chart.setMargins(QMargins(5, 5, 5, 5))
        legend = chart.legend()
        legend.setLabelColor(QColor("#b0baca"))
        legend.setFont(_make_font(10))
        legend.setAlignment(Qt.AlignmentFlag.AlignBottom)
        return chart

    def _build_city_tab(self) -> QWidget:
        city_counts = Counter()
        for item in self._entries:
            city = entry_city(item)
            if city:
                city_counts[city] += 1

        top = city_counts.most_common(10)
        categories = [c for c, _ in top]
        values = [v for _, v in top]

        chart = self._styled_chart()
        bar_set = QBarSet(str(t(self._locale, "chart_books")))
        bar_set.append(values)
        bar_set.setColor(ACCENT)
        bar_set.setBorderColor(QColor("transparent"))

        series = QBarSeries()
        series.append(bar_set)
        series.setBarWidth(0.55)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(MUTED)
        axis_x.setGridLineColor(QColor("transparent"))
        axis_x.setLabelsFont(_make_font(10))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(MUTED)
        axis_y.setGridLineColor(GRID_LINE)
        axis_y.setLabelsFont(_make_font(10))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(ModernChartView(chart))
        return w

    def _build_genre_tab(self) -> QWidget:
        genre_counts: Counter = Counter()
        for item in self._entries:
            g = str(item.get("genre", "")).strip()
            if g:
                genre_counts[g] += 1

        top = genre_counts.most_common(8)
        categories = [c for c, _ in top]
        values = [v for _, v in top]

        chart = self._styled_chart()
        bar_set = QBarSet("Eser")
        bar_set.append(values)
        bar_set.setColor(ACCENT2)
        bar_set.setBorderColor(QColor("transparent"))

        series = QBarSeries()
        series.append(bar_set)
        series.setBarWidth(0.55)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(MUTED)
        axis_x.setGridLineColor(QColor("transparent"))
        axis_x.setLabelsFont(_make_font(10))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(MUTED)
        axis_y.setGridLineColor(GRID_LINE)
        axis_y.setLabelsFont(_make_font(10))
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().hide()

        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(ModernChartView(chart))
        return w

    def _build_year_tab(self) -> QWidget:
        decades: Counter = Counter()
        for item in self._entries:
            y = item.get("publication_year", 0)
            if y:
                decade = (y // 10) * 10
                decades[f"{decade}s"] += 1

        sorted_decades = sorted(decades.items())
        categories = [d for d, _ in sorted_decades]
        values = [v for _, v in sorted_decades]

        chart = self._styled_chart()
        line = QLineSeries()
        line.setName("Eser")
        line.setColor(ACCENT)
        line.setPen(QColor(ACCENT))
        line.setPointsVisible(True)
        point_size = 8
        for i, (c, v) in enumerate(sorted_decades):
            line.append(float(i), float(v))

        chart.addSeries(line)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(MUTED)
        axis_x.setGridLineColor(QColor("transparent"))
        axis_x.setLabelsFont(_make_font(10))
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        line.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(MUTED)
        axis_y.setGridLineColor(GRID_LINE)
        axis_y.setLabelsFont(_make_font(10))
        axis_y.applyNiceNumbers()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        line.attachAxis(axis_y)

        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(ModernChartView(chart))
        return w

    def _build_sentiment_tab(self) -> QWidget:
        sentiment_counts: Counter = Counter()
        for item in self._entries:
            s = str(item.get("sentiment", "")).strip()
            if s:
                sentiment_counts[s] += 1

        top = sentiment_counts.most_common(8)
        chart = self._styled_chart()
        series = QPieSeries()
        series.setHoleSize(0.35)
        colors = [
            QColor("#4e89ff"),
            QColor("#7d4e9a"),
            QColor("#2a6b3c"),
            QColor("#d4a843"),
            QColor("#c05555"),
            QColor("#4fa8a8"),
            QColor("#c07a4a"),
            QColor("#6b7a8a"),
        ]
        for i, (label, count) in enumerate(top):
            sl = series.append(f"{label} ({count})", count)
            if i < len(colors):
                sl.setColor(colors[i])
            sl.setLabelVisible(True)
            sl.setLabelColor(MUTED)
            sl.setLabelFont(_make_font(10))

        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        chart.legend().setLabelColor(QColor("#b0baca"))
        chart.legend().setFont(_make_font(10))

        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(ModernChartView(chart))
        return w

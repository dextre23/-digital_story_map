from collections import Counter

from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSet,
    QBarSeries,
    QChart,
    QChartView,
    QLineSeries,
    QPieSeries,
    QValueAxis,
)
from PySide6.QtCore import QMargins, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t
from app.ui.search_utils import entry_city

BG_COLOR = QColor("#11161e")
TEXT_COLOR = QColor("#f0f3f8")
MUTED = QColor("#8b95a8")
ACCENT = QColor("#4e89ff")
ACCENT2 = QColor("#7d4e9a")
GRID_LINE = QColor("rgba(255,255,255,0.06)")


def _make_font(size: int = 11, bold: bool = False) -> QFont:
    f = QFont("Segoe UI", size)
    f.setBold(bold)
    return f


class _ChartWidget(QWidget):
    def __init__(self, chart: QChart) -> None:
        super().__init__()
        self._view = QChartView(chart)
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setStyleSheet("background-color: transparent; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._view)


class StatsView(QWidget):
    map_requested = Signal()

    def __init__(self, entries: list[dict], locale: str = "tr") -> None:
        super().__init__()
        self._locale = locale
        self._entries = entries

        top = QWidget()
        top.setObjectName("whyReadTop")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(24, 16, 24, 12)

        self._head = QLabel()
        self._head.setObjectName("whyReadHead")

        self._map_btn = QPushButton()
        self._map_btn.setObjectName("whyReadMapBtn")
        self._map_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._map_btn.clicked.connect(self.map_requested.emit)

        top_layout.addWidget(self._head, stretch=1)
        top_layout.addWidget(self._map_btn)

        self._tabs = QTabWidget()
        self._tabs.setObjectName("statsTabs")

        self._count_label = QLabel()
        self._count_label.setStyleSheet("font-size: 12px; color: #8b95a8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        w2 = QWidget()
        wl = QVBoxLayout(w2)
        wl.setContentsMargins(24, 12, 24, 24)
        wl.setSpacing(8)
        wl.addWidget(self._count_label)
        wl.addWidget(self._tabs, stretch=1)
        layout.addWidget(w2, stretch=1)

        self.apply_language(locale)

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        self._head.setText("\U0001F4CA  " + t(locale, "stats_window"))
        self._map_btn.setText(t(locale, "btn_map"))
        self._count_label.setText(f"{len(self._entries)} {t(locale, 'stats_records')}")

        tab_keys = [
            ("chart_top_cities", self._build_city_tab),
            ("stats_genre_tab", self._build_genre_tab),
            ("stats_year_tab", self._build_year_tab),
            ("stats_sentiment_tab", self._build_sentiment_tab),
        ]
        self._tabs.clear()
        for key, builder in tab_keys:
            self._tabs.addTab(builder(), t(locale, key))

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
        return _ChartWidget(chart)

    def _build_genre_tab(self) -> QWidget:
        genre_counts = Counter()
        for item in self._entries:
            g = str(item.get("genre", "")).strip()
            if g:
                genre_counts[g] += 1
        top = genre_counts.most_common(8)
        categories = [c for c, _ in top]
        values = [v for _, v in top]
        chart = self._styled_chart()
        bar_set = QBarSet(t(self._locale, "chart_books"))
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
        return _ChartWidget(chart)

    def _build_year_tab(self) -> QWidget:
        decades = Counter()
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
        line.setName(t(self._locale, "chart_books"))
        line.setColor(ACCENT)
        line.setPointsVisible(True)
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
        return _ChartWidget(chart)

    def _build_sentiment_tab(self) -> QWidget:
        sentiment_counts = Counter()
        for item in self._entries:
            s = str(item.get("sentiment", "")).strip()
            if s:
                sentiment_counts[s] += 1
        top = sentiment_counts.most_common(8)
        chart = self._styled_chart()
        series = QPieSeries()
        series.setHoleSize(0.35)
        colors = [
            QColor("#4e89ff"), QColor("#7d4e9a"), QColor("#2a6b3c"),
            QColor("#d4a843"), QColor("#c05555"), QColor("#4fa8a8"),
            QColor("#c07a4a"), QColor("#6b7a8a"),
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
        return _ChartWidget(chart)

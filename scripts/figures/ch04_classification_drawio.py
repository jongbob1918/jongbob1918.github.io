"""4장(블로그 5장 '이진분류') 그림 6개를 draw.io 원본(.drawio)으로 만든다.

- perceptron-data       : 공부 시간·출석률 평면의 합격/불합격 데이터
- perceptron-boundary   : 같은 데이터에 학습이 끝난 분류 경계
- sigmoid-gradient      : sigmoid와 그 기울기 p(1-p)
- mse-bce-loss          : 정답이 합격(y=1)일 때 제곱 오차와 BCE
- bernoulli-distribution: 베르누이 분포(p=0.8)
- normal-distribution   : 예측값 주변의 정규분포

실행: python3 scripts/figures/ch04_classification_drawio.py
출력: site/src/assets/diagrams/<이름>.drawio
PNG는 draw.io Desktop으로 내보낸다.
  drawio -x -f png -s 2 -o <이름>.png site/src/assets/diagrams/<이름>.drawio
PNG 위치: site/public/images/notes/easy-deep-learning-ch04/
"""
import math
from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).resolve().parents[2] / "site/src/assets/diagrams"

BLUE, ORANGE, RED = "#315a7a", "#e07b39", "#c0392b"
GRID, AXIS, TEXT = "#dedede", "#242424", "#444444"
PASS_FILL, FAIL_FILL = "#dde9f4", "#fbe7da"
W, H = 720, 440


class Diagram:
    def __init__(self, name, title):
        self.name, self.title = name, title
        self.cells = []
        self.n = 1
        self.rect(1, 1, W - 2, H - 2, "rounded=0;html=1;fillColor=#ffffff;strokeColor=none;")

    def _id(self):
        self.n += 1
        return f"c{self.n}"

    def vertex(self, x, y, w, h, style, value=""):
        self.cells.append(
            f'<mxCell id="{self._id()}" value={quoteattr(value)} style={quoteattr(style)} vertex="1" parent="1">'
            f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>'
        )

    def rect(self, x, y, w, h, style, value=""):
        self.vertex(x, y, w, h, style, value)

    def text(self, x, y, w, h, value, size=16, color=TEXT, bold=False, align="center", rotation=0, fill=None):
        style = (
            f"text;html=1;whiteSpace=wrap;strokeColor=none;fillColor={fill or 'none'};"
            f"align={align};verticalAlign=middle;fontSize={size};fontColor={color};"
            f"fontStyle={1 if bold else 0};"
        )
        if rotation:
            style += f"rotation={rotation};"
        self.vertex(x, y, w, h, style, value)

    def line(self, pts, color, width=2, dashed=False, arrow=False):
        style = f"strokeColor={color};strokeWidth={width};rounded=0;"
        style += "endArrow=classic;endFill=1;" if arrow else "endArrow=none;"
        if dashed:
            style += "dashed=1;"
        (sx, sy), (tx, ty), mid = pts[0], pts[-1], pts[1:-1]
        via = ""
        if mid:
            via = '<Array as="points">' + "".join(f'<mxPoint x="{x:.1f}" y="{y:.1f}"/>' for x, y in mid) + "</Array>"
        self.cells.append(
            f'<mxCell id="{self._id()}" value="" style={quoteattr(style)} edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry"><mxPoint x="{sx:.1f}" y="{sy:.1f}" as="sourcePoint"/>'
            f'<mxPoint x="{tx:.1f}" y="{ty:.1f}" as="targetPoint"/>{via}</mxGeometry></mxCell>'
        )

    def dot(self, cx, cy, color, r=8):
        self.vertex(cx - r, cy - r, 2 * r, 2 * r, f"ellipse;html=1;fillColor={color};strokeColor=#ffffff;strokeWidth=2;")

    def diamond(self, cx, cy, color, r=10):
        self.vertex(cx - r, cy - r, 2 * r, 2 * r, f"rhombus;html=1;fillColor={color};strokeColor=#ffffff;strokeWidth=1.5;")

    def polygon(self, x, y, w, h, coords, fill):
        style = f"shape=mxgraph.basic.polygon;polyCoords={coords};polyline=0;fillColor={fill};strokeColor=none;"
        self.vertex(x, y, w, h, style)

    def legend(self, items, x, y):
        """items: (kind, color, 라벨, 라벨 너비). kind = dot | diamond | line"""
        for kind, color, label, w in items:
            if kind == "dot":
                self.dot(x + 10, y + 15, color, 8)
            elif kind == "diamond":
                self.diamond(x + 10, y + 15, color, 10)
            else:
                self.line([(x, y + 15), (x + 24, y + 15)], color, 4)
            off = 32 if kind == "line" else 26
            self.text(x + off, y, w, 30, label, size=16, color=TEXT, align="left")
            x += off + w + 18

    def save(self):
        xml = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<mxfile host="app.diagrams.net" version="24.7.17" type="device">\n'
            f"  <diagram id={quoteattr(self.name)} name={quoteattr(self.title)}>\n"
            f'    <mxGraphModel dx="{W}" dy="{H}" grid="1" gridSize="10" guides="1" tooltips="1" connect="0" arrows="1" '
            f'fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">\n'
            '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
            + "\n        ".join(self.cells)
            + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n"
        )
        (OUT / f"{self.name}.drawio").write_text(xml, encoding="utf-8")


class Plot:
    """픽셀 좌표 (x0, y0) 왼쪽 위, 크기 w×h인 그래프 영역."""

    def __init__(self, d, xr, yr, x0=110, y0=70, w=530, h=300):
        self.d, self.x0, self.y0, self.w, self.h = d, x0, y0, w, h
        self.xr, self.yr = xr, yr

    def px(self, x):
        return self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def py(self, y):
        return self.y0 + self.h - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def grid(self, xticks, yticks, xfmt, yfmt, xgrid=True):
        d = self.d
        for t in yticks:
            d.line([(self.x0, self.py(t)), (self.x0 + self.w, self.py(t))], GRID, 1)
            d.text(self.x0 - 62, self.py(t) - 14, 50, 28, yfmt(t), align="right")
        for t in xticks:
            if xgrid:
                d.line([(self.px(t), self.y0), (self.px(t), self.y0 + self.h)], GRID, 1)
            d.text(self.px(t) - 30, self.y0 + self.h + 6, 60, 28, xfmt(t))

    def axes(self, xtitle, ytitle):
        d = self.d
        base = self.y0 + self.h
        d.line([(self.x0, base), (self.x0 + self.w + 30, base)], AXIS, 2, arrow=True)
        d.line([(self.x0, base), (self.x0, self.y0 - 15)], AXIS, 2, arrow=True)
        d.text(self.x0 + self.w - 270, base + 34, 300, 30, xtitle, size=19, color=AXIS, bold=True, align="right")
        cy = self.y0 + self.h / 2
        if ytitle:
            d.text(52 - 90, cy - 15, 180, 30, ytitle, size=19, color=AXIS, bold=True, rotation=-90)

    def curve(self, fn, xs, color, width=4):
        pts = [(self.px(x), self.py(fn(x))) for x in xs]
        self.d.line(pts, color, width)


def frange(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


# 합격: (공부 시간, 출석률 %) / 불합격. 경계 출석률 = 100 - 10 × 공부 시간 으로 완벽히 갈린다.
PASS = [(4.2, 65), (6.4, 76), (8.6, 42)]
FAIL = [(5.8, 35), (3.6, 24), (1.4, 58)]
assert all(a > 100 - 10 * h for h, a in PASS) and all(a < 100 - 10 * h for h, a in FAIL)


def perceptron(boundary):
    name = "perceptron-boundary" if boundary else "perceptron-data"
    d = Diagram(name, "학습이 끝난 분류 경계" if boundary else "공부 시간과 출석률 데이터")
    p = Plot(d, (0, 10), (0, 100))
    p.grid(range(0, 11, 2), range(0, 101, 20), lambda t: str(t), lambda t: str(t))
    if boundary:
        d.line([(p.px(0), p.py(100)), (p.px(10), p.py(0))], "#8b5bb5", 4)
    for h, a in FAIL:
        d.diamond(p.px(h), p.py(a), ORANGE)
    for h, a in PASS:
        d.dot(p.px(h), p.py(a), BLUE)
    p.axes("공부 시간 x<sub>1</sub> (시간)", "출석률 x<sub>2</sub> (%)")
    if boundary:
        d.legend([("line", "#8b5bb5", "유닛 스텝", 110)], 112, 14)
    d.save()


def sigmoid_gradient():
    d = Diagram("sigmoid-gradient", "sigmoid와 기울기 p(1-p)")
    p = Plot(d, (-6, 6), (0, 1))
    p.grid(range(-6, 7, 2), [0, 0.25, 0.5, 0.75, 1], lambda t: str(t), lambda t: f"{t:g}")
    sig = lambda z: 1 / (1 + math.exp(-z))
    xs = frange(-6, 6, 61)
    p.curve(sig, xs, BLUE)
    p.curve(lambda z: sig(z) * (1 - sig(z)), xs, ORANGE)
    # p = 0.01 인 점
    z1 = math.log(0.01 / 0.99)
    d.dot(p.px(z1), p.py(0.01), RED)
    d.line([(p.px(z1), p.py(0.01) - 10), (p.px(z1), p.py(0.34) + 16)], RED, 2, dashed=True)
    d.text(p.px(z1) - 45, p.py(0.34) - 36, 190, 52, "p = 0.01<br>p(1−p) ≈ 0.0099", size=15, color="#5a463b", bold=True, align="left", fill="#ffffff")
    # 기울기가 가장 큰 z = 0
    d.dot(p.px(0), p.py(0.25), ORANGE)
    d.text(p.px(0) + 14, p.py(0.25) - 40, 175, 28, "z = 0에서 최대 0.25", size=15, color="#5a463b", bold=True, align="left", fill="#ffffff")
    p.axes("점수 z", "")
    d.legend([("line", BLUE, "p = σ(z)", 90), ("line", ORANGE, "p(1−p) : sigmoid의 기울기", 230)], 112, 14)
    d.save()


def mse_bce():
    d = Diagram("mse-bce-loss", "제곱 오차와 BCE")
    p = Plot(d, (0, 1), (0, 5))
    p.grid([0, 0.2, 0.4, 0.6, 0.8, 1], range(0, 6), lambda t: f"{t:g}", lambda t: str(t))
    p.curve(lambda x: (1 - x) ** 2, frange(0, 1, 41), ORANGE)
    ts = frange(0, 5, 70)  # BCE = -ln p = t  (p = e^-t)
    d.line([(p.px(math.exp(-t)), p.py(t)) for t in ts], BLUE, 4)
    d.dot(p.px(0.01), p.py(-math.log(0.01)), RED)
    d.dot(p.px(0.01), p.py(0.98), RED)
    d.dot(p.px(0.40) - 6, p.py(4.5), RED, 7)
    d.text(p.px(0.40) + 6, p.py(4.5) - 62, 250, 124, "p = 0.01일 때 (빨간 점)<br>BCE ≈ 4.6<br>제곱 오차 ≈ 0.98", size=16, color="#5a463b", bold=True, align="left")
    p.axes("합격 확률 p (정답 y = 1)", "손실")
    d.legend([("line", ORANGE, "제곱 오차 (p−1)²", 160), ("line", BLUE, "BCE −log p", 120)], 112, 14)
    d.save()


def bernoulli():
    d = Diagram("bernoulli-distribution", "베르누이 분포")
    p = Plot(d, (0, 1), (0, 1))
    p.grid([], [0, 0.2, 0.4, 0.6, 0.8, 1], lambda t: "", lambda t: f"{t:g}")
    for cx, prob, color, top, cat in ((270, 0.2, ORANGE, "P(y = 0) = 1 − p = 0.2", "y = 0 (불합격)"),
                                      (480, 0.8, BLUE, "P(y = 1) = p = 0.8", "y = 1 (합격)")):
        d.rect(cx - 60, p.py(prob), 120, p.py(0) - p.py(prob), f"rounded=0;html=1;fillColor={color};strokeColor=none;")
        d.text(cx - 110, p.py(prob) - 34, 220, 30, top, size=16, color="#5a463b", bold=True)
        d.text(cx - 90, p.py(0) + 6, 180, 28, cat, size=16)
    p.axes("정답 y", "확률")
    d.text(112, 14, 400, 30, "예: 합격 확률 p = 0.8", size=16, color=TEXT, bold=True, align="left")
    d.save()


def normal():
    d = Diagram("normal-distribution", "정규분포")
    x0, y0, w, h = 110, 70, 530, 300
    base, cx, sigma, peak = y0 + h, 400, 70, 210
    pdf = lambda t: math.exp(-t * t / 2)
    pts = [(cx + t * sigma, base - peak * pdf(t)) for t in frange(-3.5, 3.5, 71)]
    d.line(pts, BLUE, 4)
    d.line([(cx, base), (cx, base - peak - 20)], GRID, 2, dashed=True)
    d.text(cx - 80, base - peak - 52, 160, 30, "예측값 ŷ", size=17, color=AXIS, bold=True)
    for t, label, color in ((0.7, "정답 A : 밀도 높음", ORANGE), (-2.3, "정답 B : 밀도 낮음", RED)):
        px_ = cx + t * sigma
        py_ = base - peak * pdf(t)
        d.line([(px_, base), (px_, py_)], color, 2, dashed=True)
        d.dot(px_, py_, color)
        d.dot(px_, base, color, 6)
    d.text(cx + 0.7 * sigma + 14, base - peak * pdf(0.7) - 30, 190, 30, "정답 A : 밀도 높음", size=15, color="#5a463b", bold=True, align="left")
    d.text(cx - 2.3 * sigma - 112, base - peak * pdf(-2.3) - 56, 94, 44, "정답 B<br>밀도 낮음", size=15, color="#5a463b", bold=True, align="right")
    d.line([(x0, base), (x0 + w + 30, base)], AXIS, 2, arrow=True)
    d.line([(x0, base), (x0, y0 - 15)], AXIS, 2, arrow=True)
    d.text(x0 + w - 270, base + 18, 300, 30, "정답 y", size=19, color=AXIS, bold=True, align="right")
    d.text(52 - 90, y0 + h / 2 - 15, 180, 30, "확률밀도", size=19, color=AXIS, bold=True, rotation=-90)
    d.save()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    perceptron(False)
    perceptron(True)
    sigmoid_gradient()
    mse_bce()
    bernoulli()
    normal()

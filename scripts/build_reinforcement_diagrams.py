"""Build editable draw.io pages and matching PNGs for the RL note."""

from __future__ import annotations

import math
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DRAWIO = ROOT / "site/src/assets/diagrams/restaurant-reinforcement-learning.drawio"
IMAGES = ROOT / "site/public/images/notes/easy-deep-learning-ch01"
WIDTH, HEIGHT, SCALE = 820, 600, 2
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
INK = "#172033"
MUTED = "#526078"
GRID = "#cbd3df"
BLUE = "#4678c8"
ORANGE = "#d77b22"
GREEN = "#3c9460"
RED = "#ca5555"


class Page:
    def __init__(self, page_id: str, name: str):
        self.diagram = ET.Element("diagram", {"id": page_id, "name": name})
        model = ET.SubElement(
            self.diagram,
            "mxGraphModel",
            {
                "dx": str(WIDTH), "dy": str(HEIGHT), "grid": "1", "gridSize": "10",
                "guides": "1", "page": "1", "pageScale": "1",
                "pageWidth": str(WIDTH), "pageHeight": str(HEIGHT),
                "math": "0", "shadow": "0",
            },
        )
        self.cells = ET.SubElement(model, "root")
        ET.SubElement(self.cells, "mxCell", {"id": "0"})
        ET.SubElement(self.cells, "mxCell", {"id": "1", "parent": "0"})
        self.image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.count = 0

    def _id(self) -> str:
        self.count += 1
        return f"{self.diagram.get('id')}-{self.count}"

    @staticmethod
    def _coords(x: float, y: float, w: float, h: float) -> tuple[int, ...]:
        return tuple(round(v * SCALE) for v in (x, y, x + w, y + h))

    def _font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(BOLD if bold else FONT, size * SCALE)

    def box(
        self, x: float, y: float, w: float, h: float, *, fill: str = "#ffffff",
        stroke: str = "#d5dbe5", radius: int = 0, stroke_width: int = 2,
        label: str = "", size: int = 16, color: str = INK, bold: bool = False,
    ) -> None:
        style = (
            f"rounded={1 if radius else 0};arcSize={radius};whiteSpace=wrap;html=1;"
            f"fillColor={fill};strokeColor={stroke};strokeWidth={stroke_width};"
            f"fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
            "align=center;verticalAlign=middle;"
        )
        cell = ET.SubElement(self.cells, "mxCell", {"id": self._id(), "value": label, "style": style, "vertex": "1", "parent": "1"})
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
        coords = self._coords(x, y, w, h)
        self.draw.rounded_rectangle(coords, radius=radius * SCALE, fill=fill, outline=stroke, width=stroke_width * SCALE)
        if label:
            self._draw_centered(label, x, y, w, h, size=size, color=color, bold=bold)

    def _draw_centered(self, label: str, x: float, y: float, w: float, h: float, *, size: int, color: str, bold: bool) -> None:
        font = self._font(size, bold)
        lines = label.split("\n")
        heights = [self.draw.textbbox((0, 0), line, font=font)[3] - self.draw.textbbox((0, 0), line, font=font)[1] for line in lines]
        gap = 4 * SCALE
        total = sum(heights) + gap * (len(lines) - 1)
        top = (y + h / 2) * SCALE - total / 2
        for line, height in zip(lines, heights):
            bounds = self.draw.textbbox((0, 0), line, font=font)
            tw = bounds[2] - bounds[0]
            self.draw.text(((x + w / 2) * SCALE - tw / 2, top - bounds[1]), line, font=font, fill=color)
            top += height + gap

    def text(self, x: float, y: float, w: float, h: float, label: str, *, size: int = 16, color: str = INK, bold: bool = False, align: str = "left") -> None:
        style = f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};"
        cell = ET.SubElement(self.cells, "mxCell", {"id": self._id(), "value": label, "style": style, "vertex": "1", "parent": "1"})
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
        if align == "center":
            self._draw_centered(label, x, y, w, h, size=size, color=color, bold=bold)
        else:
            font = self._font(size, bold)
            bounds = self.draw.textbbox((0, 0), label, font=font)
            ty = (y + h / 2) * SCALE - (bounds[3] - bounds[1]) / 2 - bounds[1]
            self.draw.text((x * SCALE, ty), label, font=font, fill=color)

    def line(self, a: tuple[float, float], b: tuple[float, float], *, color: str = GRID, width: int = 2) -> None:
        style = f"endArrow=none;html=1;strokeColor={color};strokeWidth={width};"
        cell = ET.SubElement(self.cells, "mxCell", {"id": self._id(), "style": style, "edge": "1", "parent": "1"})
        geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        ET.SubElement(geometry, "mxPoint", {"x": str(a[0]), "y": str(a[1]), "as": "sourcePoint"})
        ET.SubElement(geometry, "mxPoint", {"x": str(b[0]), "y": str(b[1]), "as": "targetPoint"})
        self.draw.line(tuple(round(v * SCALE) for v in (*a, *b)), fill=color, width=width * SCALE)

    def route(self, points: list[tuple[float, float]], *, color: str, width: int = 5, dashed: bool = False, arrow: bool = True) -> None:
        style = (
            f"endArrow={'block' if arrow else 'none'};endFill=1;html=1;strokeColor={color};"
            f"strokeWidth={width};rounded=1;"
            + ("dashed=1;dashPattern=7 5;" if dashed else "")
        )
        cell = ET.SubElement(self.cells, "mxCell", {"id": self._id(), "style": style, "edge": "1", "parent": "1"})
        geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        ET.SubElement(geometry, "mxPoint", {"x": str(points[0][0]), "y": str(points[0][1]), "as": "sourcePoint"})
        if len(points) > 2:
            array = ET.SubElement(geometry, "Array", {"as": "points"})
            for px, py in points[1:-1]:
                ET.SubElement(array, "mxPoint", {"x": str(px), "y": str(py)})
        ET.SubElement(geometry, "mxPoint", {"x": str(points[-1][0]), "y": str(points[-1][1]), "as": "targetPoint"})
        for a, b in zip(points, points[1:]):
            self._segment(a, b, color=color, width=width, dashed=dashed)
        if arrow:
            a, b = points[-2:]
            angle = math.atan2(b[1] - a[1], b[0] - a[0])
            length, half = 13 * SCALE, 6 * SCALE
            tip = (b[0] * SCALE, b[1] * SCALE)
            back = (tip[0] - length * math.cos(angle), tip[1] - length * math.sin(angle))
            normal = (-math.sin(angle), math.cos(angle))
            self.draw.polygon([tip, (back[0] + half * normal[0], back[1] + half * normal[1]), (back[0] - half * normal[0], back[1] - half * normal[1])], fill=color)

    def _segment(self, a: tuple[float, float], b: tuple[float, float], *, color: str, width: int, dashed: bool) -> None:
        a = (a[0] * SCALE, a[1] * SCALE)
        b = (b[0] * SCALE, b[1] * SCALE)
        distance = math.dist(a, b)
        if not dashed:
            self.draw.line((*a, *b), fill=color, width=width * SCALE, joint="curve")
            return
        unit = ((b[0] - a[0]) / distance, (b[1] - a[1]) / distance)
        cursor = 0
        while cursor < distance:
            end = min(cursor + 13 * SCALE, distance)
            self.draw.line((a[0] + unit[0] * cursor, a[1] + unit[1] * cursor, a[0] + unit[0] * end, a[1] + unit[1] * end), fill=color, width=width * SCALE)
            cursor += 22 * SCALE


def frame(page: Page, title: str, subtitle: str) -> None:
    page.box(20, 20, 780, 560, radius=12, stroke="#d5dbe5")
    page.text(50, 43, 720, 42, title, size=24, bold=True)
    page.text(50, 85, 720, 30, subtitle, size=15, color=MUTED)


def grid(page: Page) -> None:
    page.box(230, 150, 360, 360, fill="#fbfcfe", stroke="#778398", stroke_width=2)
    for index in range(1, 5):
        x = 230 + 72 * index
        y = 150 + 72 * index
        page.line((x, 150), (x, 510))
        page.line((230, y), (590, y))


def center(col: int, row: int) -> tuple[int, int]:
    return 266 + 72 * col, 186 + 72 * row


def square(page: Page, col: int, row: int, label: str, kind: str) -> None:
    styles = {
        "start": ("#e8f5e9", GREEN, "#245b2c"),
        "work": ("#fdeaea", RED, "#8b2f2f"),
        "a": ("#e8f1ff", BLUE, "#244e8a"),
        "b": ("#fff4d8", "#d69b27", "#77500c"),
    }
    fill, stroke, color = styles[kind]
    page.box(230 + col * 72, 150 + row * 72, 72, 72, fill=fill, stroke=stroke, label=label, size=15, color=color, bold=True)


def note(page: Page, label: str, *, color: str = BLUE, fill: str = "#eef4ff") -> None:
    page.box(145, 533, 530, 37, fill=fill, stroke=color, radius=8, stroke_width=1, label=label, size=15, color=color)


def exploration() -> Page:
    page = Page("rl-exploration", "1 길 탐색과 벌점")
    frame(page, "1. 길을 탐색하며 벌점 받기", "처음에는 어느 방향이 좋은지 몰라 여러 칸을 이동합니다.")
    grid(page)
    page.route([center(0, 4), center(1, 4), center(1, 2), (365, 330)], color=ORANGE, width=5, dashed=True)
    square(page, 0, 4, "출발", "start")
    square(page, 2, 2, "공사 구간\n−20", "work")
    page.text(40, 220, 175, 80, "한 번의 이동\n→ 한 칸", size=18, color=ORANGE, bold=True)
    note(page, "공사 칸 진입 시 −20 · 이동할 때마다 −1", color=RED, fill="#fff2ed")
    return page


def reward_update() -> Page:
    page = Page("rl-q-update", "2 Q값 갱신")
    frame(page, "2. 이동 결과로 방향별 점수 고치기", "맛집으로 이어지는 방향의 예상 점수(Q값)를 높여 갑니다.")
    grid(page)
    page.route([center(0, 4), (507, 474)], color=BLUE, width=5)
    square(page, 0, 4, "출발", "start")
    square(page, 2, 2, "공사 구간\n−20", "work")
    square(page, 4, 4, "맛집 A\n+40", "a")
    page.box(30, 265, 185, 91, fill="#eef4ff", stroke=BLUE, radius=9, label="출발 칸의\n오른쪽 Q값 ↑", size=17, color="#244e8a", bold=True)
    note(page, "보상 + 다음 칸의 예상 점수로 Q값을 갱신")
    return page


def new_restaurant() -> Page:
    page = Page("rl-explore-exploit", "3 탐색과 활용")
    frame(page, "3. 다른 길에서 더 좋은 맛집 찾기", "맛집 A로 가는 길만 반복하면 맛집 B를 찾지 못합니다.")
    grid(page)
    page.route([center(0, 4), (507, 474)], color=BLUE, width=5)
    page.route([center(0, 4), center(1, 4), center(1, 1), center(4, 1), (554, 232)], color=ORANGE, width=5, dashed=True)
    square(page, 0, 4, "출발", "start")
    square(page, 2, 2, "공사 구간\n−20", "work")
    square(page, 4, 4, "맛집 A\n+40", "a")
    square(page, 4, 0, "맛집 B\n+100", "b")
    page.text(26, 390, 188, 56, "파랑: 활용\n주황: 탐색", size=16, color=MUTED, bold=True)
    note(page, "ε 확률로 새 길 탐색 · 1−ε 확률로 아는 길 활용", color="#7564c9", fill="#f4f1ff")
    return page


def shorter_route() -> Page:
    page = Page("rl-shorter-route", "4 짧은 경로")
    frame(page, "4. 같은 맛집까지 더 짧게 가기", "맛집 B +100, 이동마다 −1일 때의 점수입니다. (할인율 적용 전)")
    grid(page)
    long_path = [center(0, 4), center(0, 2), center(1, 2), center(1, 3), center(3, 3), center(3, 0), (509, 186)]
    short_path = [center(0, 4), center(4, 4), (554, 232)]
    page.route(long_path, color="#929cab", width=4, dashed=True)
    page.route(short_path, color=GREEN, width=6)
    square(page, 0, 4, "출발", "start")
    square(page, 2, 2, "공사 구간\n−20", "work")
    square(page, 4, 0, "맛집 B\n+100", "b")
    page.box(32, 340, 183, 93, fill="#eef8ef", stroke=GREEN, radius=9, label="초록 8칸: +92\n회색 10칸: +90", size=16, color="#245b2c", bold=True)
    note(page, "같은 보상이라면 이동 벌점이 적은 8칸 경로가 유리", color=GREEN, fill="#eef8ef")
    return page


def main() -> None:
    pages = [exploration(), reward_update(), new_restaurant(), shorter_route()]
    root = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "Codex", "version": "24.7.17", "compressed": "false"})
    for page in pages:
        root.append(page.diagram)
    ET.indent(root, space="  ")
    DRAWIO.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(DRAWIO, encoding="utf-8", xml_declaration=True)
    names = [
        "restaurant-rl-01-random-exploration.png",
        "restaurant-rl-02-reward-update.png",
        "restaurant-rl-03-exploration-exploitation.png",
        "restaurant-rl-04-shortest-path.png",
    ]
    for page, name in zip(pages, names):
        page.image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).save(IMAGES / name, optimize=True)
        print(IMAGES / name)
    print(DRAWIO)


if __name__ == "__main__":
    main()

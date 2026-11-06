"""Build phase05_results.pptx on the Desktop, matching the HTML deck's content and style."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
import copy

INK   = RGBColor(0x11, 0x11, 0x11)
GRID  = RGBColor(0x99, 0x99, 0x99)
HEAD  = RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT  = "Arial"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
MARGIN = Inches(0.95)
WIDTH  = prs.slide_width - 2 * MARGIN


def set_border(cell, color=GRID, w=Pt(0.75)):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for old in tcPr.findall(qn(tag)):
            tcPr.remove(old)
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = tcPr.makeelement(qn(tag), {"w": str(int(w)), "cap": "flat"})
        fill = ln.makeelement(qn("a:solidFill"), {})
        clr = fill.makeelement(qn("a:srgbClr"), {"val": "999999"})
        fill.append(clr); ln.append(fill); tcPr.append(ln)


def title_slide():
    s = prs.slides.add_slide(BLANK)
    tb = s.shapes.add_textbox(MARGIN, Inches(3.0), WIDTH, Inches(1.5))
    p = tb.text_frame.paragraphs[0]; r = p.add_run(); r.text = "Phase05"
    r.font.name = FONT; r.font.size = Pt(54); r.font.bold = True; r.font.color.rgb = INK


def table_slide(title, header, rows, first_left=True):
    s = prs.slides.add_slide(BLANK)
    # heading
    hb = s.shapes.add_textbox(MARGIN, Inches(0.8), WIDTH, Inches(0.9))
    hp = hb.text_frame.paragraphs[0]; hr = hp.add_run(); hr.text = title
    hr.font.name = FONT; hr.font.size = Pt(30); hr.font.bold = True; hr.font.color.rgb = INK

    data = ([header] if header else []) + rows
    ncol = len(rows[0]); nrow = len(data)
    # column widths: first column wide, rest share the remainder
    first_w = int(WIDTH * 0.46)
    rest_w = int((WIDTH - first_w) / (ncol - 1)) if ncol > 1 else 0
    tbl_h = Inches(0.5) * nrow
    top = Inches(0.8) + Inches(0.9) + (prs.slide_height - Inches(1.7) - tbl_h - Inches(0.8)) / 2
    gf = s.shapes.add_table(nrow, ncol, MARGIN, top, WIDTH, tbl_h)
    tbl = gf.table
    tbl.first_row = bool(header); tbl.horz_banding = False
    tbl.columns[0].width = Emu(first_w)
    for c in range(1, ncol):
        tbl.columns[c].width = Emu(rest_w)

    for ri, row in enumerate(data):
        is_head = header and ri == 0
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.margin_left = Inches(0.12); cell.margin_right = Inches(0.12)
            cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid(); cell.fill.fore_color.rgb = HEAD if is_head else WHITE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if (ci == 0 and first_left) else PP_ALIGN.RIGHT
            r = p.add_run(); r.text = str(val)
            r.font.name = FONT; r.font.size = Pt(16); r.font.color.rgb = INK
            r.font.bold = is_head
            set_border(cell)


title_slide()

table_slide("Data", None, [
    ["MITMA districts (with income)", "3,792 (3,741)"],
    ["directed OD pairs", "3,359,772"],
    ["total trips (March 2025)", "3.11 billion"],
    ["median unemployment (18 to 64)", "8.0%"],
])

table_slide("Income by decile",
    ["decile", "min €", "max €", "districts"], [
    ["D1 (poorest)", "7,265", "11,169", "574"],
    ["D5", "13,533", "14,158", "388"],
    ["D10 (richest)", "19,496", "31,907", "183"],
])

table_slide("Visitor income mix by district income",
    ["measure", "Spearman ρ", "β income (vol-adjusted)", "p"], [
    ["Shannon entropy", "+0.20", "+0.066", "5e−8"],
    ["Jensen-Shannon divergence", "−0.37", "−0.169", "8e−68"],
])

table_slide("Do people travel to similar-income areas?",
    ["trip distance", "corr r", "share of trips"], [
    ["all", "+0.47", "100%"],
    ["under 25 km", "+0.49", "90.3%"],
    ["25 to 100", "+0.27", "8.5%"],
    ["100 to 300", "+0.09", "0.9%"],
    ["over 300 km", "+0.04", "0.3%"],
])

table_slide("Trip spread vs unemployment and income",
    ["how residents move", "ρ unemployment", "ρ income"], [
    ["Shannon entropy", "−0.15", "+0.17"],
    ["Pielou evenness", "−0.15", "+0.06"],
    ["distinct destinations", "0.00", "+0.27"],
])

from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / "results" / "phase05_results.pptx"
prs.save(OUT)
print("saved", OUT, "with", len(prs.slides._sldIdLst), "slides")

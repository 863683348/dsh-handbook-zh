# -*- coding: utf-8 -*-
import os, re, sys
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (ListFlowable, ListItem, PageBreak, Paragraph,
    Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle)

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFontFamily('STSong-Light', normal='STSong-Light', bold='STSong-Light',
    italic='STSong-Light', boldItalic='STSong-Light')

DOCS_DIR = sys.argv[1] if len(sys.argv) > 1 else 'docs'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'dsh-handbook-zh.pdf'

TITLE_ORDER = [
    ('01-快速开始.md', '01 · 快速开始'),
    ('02-理解-profile.md', '02 · 理解 Profile'),
    ('03-插件入门.md', '03 · 插件入门'),
    ('04-写第一个插件.md', '04 · 写第一个插件'),
    ('05-工具开发进阶.md', '05 · 工具开发进阶'),
    ('06-发布插件.md', '06 · 发布插件'),
    ('07-实战案例.md', '07 · 实战案例'),
    ('08-常见问题.md', '08 · 常见问题'),
]

def S(name, **kw):
    base = dict(fontName='STSong-Light', fontSize=10.5, leading=17, alignment=TA_LEFT, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_title = S('t', fontSize=22, leading=30, alignment=TA_CENTER, textColor=HexColor('#1a1a2e'), spaceAfter=8)
st_sub = S('s', fontSize=13, leading=20, alignment=TA_CENTER, textColor=HexColor('#555577'))
st_h1 = S('h1', fontSize=17, leading=24, spaceBefore=14, spaceAfter=8, textColor=HexColor('#1a1a2e'))
st_h2 = S('h2', fontSize=14, leading=20, spaceBefore=10, spaceAfter=6, textColor=HexColor('#2d2d5e'))
st_h3 = S('h3', fontSize=12, leading=18, spaceBefore=8, spaceAfter=4, textColor=HexColor('#3d3d7e'))
st_body = S('b')
st_quote = S('q', fontSize=10, leading=16, leftIndent=12, textColor=HexColor('#556677'))
st_code = S('c', fontName='Courier', fontSize=8.5, leading=12, backColor=HexColor('#f4f4f8'), borderPadding=4)
st_toc = S('toc', fontSize=11, leading=20)
st_cell = S('cell', fontSize=9, leading=13)
st_cover = S('cv', fontSize=9, leading=14, alignment=TA_CENTER, textColor=HexColor('#888888'))

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_to_flowables(path):
    flow = []
    with open(path, encoding='utf-8') as f:
        lines = f.read().split(chr(10))
    i = 0
    in_code = False
    code_buf = []
    list_buf = []

    def flush_list():
        if list_buf:
            items = [ListItem(Paragraph(esc(x), st_body), leftIndent=6) for x in list_buf]
            flow.append(ListFlowable(items, bulletType='bullet', start=chr(8226), leftIndent=14))
            list_buf.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith('```'):
            if in_code:
                flow.append(Preformatted(chr(10).join(code_buf), st_code))
                code_buf = []
                in_code = False
            else:
                flush_list()
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if not s:
            flush_list()
            i += 1
            continue
        if s.startswith('# '):
            flush_list()
            flow.append(Paragraph(esc(s[2:]), st_h1))
        elif s.startswith('## '):
            flush_list()
            flow.append(Paragraph(esc(s[3:]), st_h2))
        elif s.startswith('### '):
            flush_list()
            flow.append(Paragraph(esc(s[4:]), st_h3))
        elif s.startswith('> '):
            flush_list()
            flow.append(Paragraph(esc(s[2:]), st_quote))
        elif s.startswith('- [ ]'):
            flush_list()
            flow.append(Paragraph(esc(s), st_body))
        elif s.startswith('- '):
            list_buf.append(s[2:])
        elif s.startswith('|'):
            flush_list()
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            i -= 1
            if rows:
                tbl = Table([[Paragraph(esc(c), st_cell) for c in r] for r in rows], hAlign='LEFT')
                tbl.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.4, HexColor('#bbbbdd')),
                    ('BACKGROUND', (0,0), (-1,0), HexColor('#e8e8f5')), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
                flow.append(Spacer(1, 4))
                flow.append(tbl)
                flow.append(Spacer(1, 8))
        else:
            flush_list()
            flow.append(Paragraph(esc(s), st_body))
        i += 1
    flush_list()
    if in_code and code_buf:
        flow.append(Preformatted(chr(10).join(code_buf), st_code))
    return flow

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
    topMargin=16*mm, bottomMargin=16*mm)
story = []
story.append(Spacer(1, 60*mm))
story.append(Paragraph('dsh-handbook-zh', st_title))
story.append(Paragraph('DeepSeek Harness 从 0 到 1 · 系统化中文教程', st_sub))
story.append(Spacer(1, 10*mm))
story.append(Paragraph('安装 · Profile · 插件 · 开发 · 发布', st_sub))
story.append(Spacer(1, 60*mm))
story.append(Paragraph('2026 年 8 月 · github.com/863683348/dsh-handbook-zh', st_cover))
story.append(PageBreak())
story.append(Paragraph('目录', st_h1))
for fname, title in TITLE_ORDER:
    story.append(Paragraph(title, st_toc))
story.append(PageBreak())
for fname, _t in TITLE_ORDER:
    p = os.path.join(DOCS_DIR, fname)
    if os.path.exists(p):
        story.extend(md_to_flowables(p))
    story.append(PageBreak())
doc.build(story)
print('PDF written:', OUT, os.path.getsize(OUT), 'bytes')

from __future__ import annotations
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak


def build_pdf_report(report: dict, charts: list[str], output_path: str):
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], fontSize=22, leading=26, textColor=colors.HexColor("#17365D")))
    styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], textColor=colors.HexColor("#235B8C")))
    styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.5, leading=13.5))
    doc=SimpleDocTemplate(output_path, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm)
    story=[Paragraph(report.get("title", "Data Analysis Report"), styles["Title2"]),
           Paragraph(report.get("subtitle", "Professional analytical report"), styles["Bodyx"]), Spacer(1,5*mm)]
    story += [Paragraph("Executive Summary", styles["H2x"]), Paragraph(report.get("executive_summary", ""), styles["Bodyx"])]
    story += [Paragraph("Scope and Methodology", styles["H2x"]), Paragraph(report.get("methodology", ""), styles["Bodyx"])]
    findings=report.get("findings", [])
    story += [Paragraph("Key Findings", styles["H2x"])]
    for f in findings:
        story.append(Paragraph(f"<b>{f.get('title','Finding')}</b>: {f.get('detail','')}", styles["Bodyx"]))
    story += [Paragraph("Recommendations", styles["H2x"])]
    for r in report.get("recommendations", []):
        story.append(Paragraph(f"<b>{r.get('priority','')}. {r.get('action','')}</b> - {r.get('rationale','')}", styles["Bodyx"]))
    story += [Paragraph("Limitations and Risks", styles["H2x"]), Paragraph(report.get("limitations", ""), styles["Bodyx"])]
    for chart in charts:
        if Path(chart).exists():
            story.append(PageBreak())
            story.append(Image(chart, width=165*mm, height=95*mm))
            story.append(Paragraph(Path(chart).stem.replace("_", " ").title(), styles["Bodyx"]))
    story += [Paragraph("Appendix - Supporting Evidence", styles["H2x"])]
    evidence=report.get("evidence", [])
    if evidence:
        data=[["Source", "Evidence"]] + [[e.get("source",""), e.get("summary","")] for e in evidence]
        tbl=Table(data, colWidths=[55*mm,105*mm], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17365D")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#C8D1DC")),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        story.append(tbl)
    doc.build(story)
    return output_path

#!/usr/bin/env python3
"""Generate updated CV PDF for Aditya Nayak - Senior Project Manager."""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase.pdfmetrics import stringWidth
import os

# ── Page dimensions ──
W, H = A4  # 595.27 x 841.89

# ── Layout ──
SIDEBAR_W = 190
SPAD = 18                       # sidebar padding
SIDEBAR_CONTENT_W = SIDEBAR_W - 2 * SPAD
MAIN_L = SIDEBAR_W + 22
MAIN_R = W - 30
MAIN_W = MAIN_R - MAIN_L

# ── Colours ──
GREEN      = HexColor('#48A878')
SIDEBAR_BG = HexColor('#F3F3F3')
DARK       = HexColor('#2B2B2B')
MED        = HexColor('#444444')
LIGHT      = HexColor('#666666')

# ── Paths ──
BASE   = '/Users/adityanayak/Documents/Claude/nayakaditya-replica/assets'
PHOTO  = os.path.join(BASE, 'aditya-hero-cutout.png')
OUTPUT = os.path.join(BASE, 'Aditya-Nayak-PM-CV.pdf')

# ── Paragraph styles ──
def sty(name, font='Helvetica', sz=8.5, color=MED, lead=11.5, align=TA_JUSTIFY):
    return ParagraphStyle(name, fontName=font, fontSize=sz, textColor=color,
                          leading=lead, alignment=align)

BODY      = sty('body')
BULLET    = sty('bullet', sz=8.2, lead=11)
SB_BODY   = sty('sb_body', sz=7.8, color=LIGHT, lead=10.5, align=TA_LEFT)
SB_SMALL  = sty('sb_small', sz=7.5, color=LIGHT, lead=10, align=TA_LEFT)
URL_STYLE = sty('url', sz=7, color=GREEN, lead=9, align=TA_LEFT)


# ═══════════════════════════════════════════════════════════════
#  Helper functions
# ═══════════════════════════════════════════════════════════════

def draw_para(c, text, x, y, width, style):
    """Render a Paragraph at (x, y-top) and return new y below it."""
    p = Paragraph(text, style)
    _, h = p.wrap(width, 800)
    p.drawOn(c, x, y - h)
    return y - h


def sidebar_bg(c):
    c.setFillColor(SIDEBAR_BG)
    c.rect(0, 0, SIDEBAR_W, H, fill=1, stroke=0)


def section_icon(c, x, y, symbol=''):
    """Green rounded-rect icon before a section header."""
    c.setFillColor(GREEN)
    c.roundRect(x, y - 3, 13, 13, 2, fill=1, stroke=0)
    # white symbol centred inside
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 7)
    sw = stringWidth(symbol, 'Helvetica-Bold', 7)
    c.drawString(x + (13 - sw) / 2, y + 0.5, symbol)


def section_hdr(c, x, y, text, symbol=''):
    """Draw a section header with green icon + bold text."""
    section_icon(c, x, y, symbol)
    c.setFillColor(GREEN)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(x + 17, y, text)
    return y - 20


def company_block(c, y, name, date, role):
    """Company name + date + role line.  Returns new y."""
    c.setFillColor(DARK)
    c.setFont('Helvetica-Bold', 10.5)
    # If name is long, might need two lines
    max_name_w = MAIN_W - stringWidth(date, 'Helvetica', 9) - 15
    if stringWidth(name, 'Helvetica-Bold', 10.5) > max_name_w:
        # split at sensible point
        parts = name.split('(')
        c.drawString(MAIN_L, y, parts[0].strip())
        c.setFillColor(LIGHT)
        c.setFont('Helvetica', 9)
        c.drawString(MAIN_R - stringWidth(date, 'Helvetica', 9), y, date)
        y -= 14
        c.setFillColor(DARK)
        c.setFont('Helvetica-Bold', 10.5)
        if len(parts) > 1:
            c.drawString(MAIN_L, y, '(' + parts[1])
        y -= 14
    else:
        c.drawString(MAIN_L, y, name)
        c.setFillColor(LIGHT)
        c.setFont('Helvetica', 9)
        c.drawString(MAIN_R - stringWidth(date, 'Helvetica', 9), y, date)
        y -= 14
    c.setFillColor(DARK)
    c.setFont('Helvetica', 9.5)
    c.drawString(MAIN_L, y, role)
    return y - 14


def draw_bullets(c, y, items, gap=4):
    """Draw a list of bullet paragraphs. Returns new y."""
    for text in items:
        c.setFillColor(DARK)
        c.circle(MAIN_L + 3, y - 3, 1.8, fill=1, stroke=0)
        y = draw_para(c, text, MAIN_L + 13, y, MAIN_W - 13, BULLET)
        y -= gap
    return y


def draw_photo(c, cx, cy, r):
    if not os.path.exists(PHOTO):
        return
    c.saveState()
    p = c.beginPath()
    p.circle(cx, cy, r)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(PHOTO, cx - r, cy - r, width=r*2, height=r*2,
                preserveAspectRatio=True, mask='auto')
    c.restoreState()
    c.setStrokeColor(GREEN)
    c.setLineWidth(2)
    c.circle(cx, cy, r, stroke=1, fill=0)


# ═══════════════════════════════════════════════════════════════
#  PAGE 1
# ═══════════════════════════════════════════════════════════════

def page1(c):
    sidebar_bg(c)

    # ── Photo ──
    pcx = SIDEBAR_W / 2
    draw_photo(c, pcx, H - 82, 55)

    # ── Sidebar content ──
    y = H - 152

    # CONTACTS
    y = section_hdr(c, SPAD, y, 'CONTACTS')
    contacts = [
        ('\u260E', '+91 70642 25041'),
        ('@',  'aditya.nayak.it@gmail.com'),
        ('\u26AD', 'Linkedin'),
        ('\u26AD', 'Website'),
    ]
    for icon, txt in contacts:
        c.setFillColor(GREEN)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(SPAD + 2, y, icon)
        c.setFillColor(MED)
        c.setFont('Helvetica', 8.2)
        c.drawString(SPAD + 16, y, txt)
        y -= 15
    y -= 8

    # KEY ACHIEVEMENTS
    y = section_hdr(c, SPAD, y, 'KEY ACHIEVEMENTS')
    achievements = [
        ('Checkout Conversion Uplift',
         'Targeted a 4% checkout conversion uplift and >99% redemption success rate by integrating a digital gift card platform.'),
        ('User Base Expansion',
         'Scaled platform from 0 to 500k+ downloads and 3,00,000+ registrations by engineering high-frequency micro-contests.'),
        ('Conversion Rate Improvement',
         'Boosted conversion rate to 60% by optimizing onboarding flow through UX design changes.'),
    ]
    for title, desc in achievements:
        c.setFillColor(DARK)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawString(SPAD, y, title)
        y -= 13
        y = draw_para(c, desc, SPAD, y, SIDEBAR_CONTENT_W, SB_BODY)
        y -= 10
    y -= 2

    # CORE COMPETENCIES
    y = section_hdr(c, SPAD, y, 'CORE COMPETENCIES')
    competencies = [
        ('Project Execution &amp; Delivery',
         'Agile/Scrum Delivery, Milestone Planning, Risk Management, End-to-End Lifecycle, PRD &amp; Charter Authoring, Cross-Functional Alignment (Tech, Marketing, Design)'),
        ('Technical &amp; AI Scoping',
         'Project Scoping, API Strategy, Cloud Architecture, Local LLMs (Ollama, LM Studio), Prompt Engineering (Claude, Gemini, ChatGPT), AI Workflows (ChatPRD, Replit, Kimmi)'),
        ('Analytics &amp; Stakeholder Tools',
         'System Architecture Design, Stakeholder Reporting, Wireframing (Figma), Jira, Linear, Notion, MS Project, Tableau, Mixpanel'),
        ('Risk Register &amp; Mitigation',
         'RAID Log Management, Risk Assessment Matrix, Contingency Planning, Issue Escalation Protocols, Dependency Tracking, Change Control'),
    ]
    for title, desc in competencies:
        ttl = title.replace('&amp;', '&')
        c.setFillColor(DARK)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawString(SPAD, y, ttl)
        y -= 13
        y = draw_para(c, desc, SPAD, y, SIDEBAR_CONTENT_W, SB_SMALL)
        y -= 8

    # ═══ Main column ═══
    y = H - 42

    # Name
    c.setFillColor(DARK)
    c.setFont('Helvetica-Bold', 26)
    nm = 'ADITYA NAYAK'
    nw = stringWidth(nm, 'Helvetica-Bold', 26)
    c.drawString(MAIN_L + (MAIN_W - nw) / 2, y, nm)
    y -= 32

    # Title pill
    ttl = 'S E N I O R   P R O J E C T   M A N A G E R'
    c.setFont('Helvetica-Bold', 9)
    tw = stringWidth(ttl, 'Helvetica-Bold', 9)
    bw = tw + 28
    bx = MAIN_L + (MAIN_W - bw) / 2
    c.setStrokeColor(GREEN)
    c.setLineWidth(1.5)
    c.roundRect(bx, y - 5, bw, 22, 11, fill=0, stroke=1)
    c.setFillColor(DARK)
    c.drawString(bx + 14, y, ttl)
    y -= 38

    # PROFESSIONAL SUMMARY
    y = section_hdr(c, MAIN_L, y, 'PROFESSIONAL SUMMARY')
    summary = (
        "Senior Project Manager with a decade of experience directing end-to-end "
        "project lifecycles and scaling high-concurrency platforms to 5,00,000+ users "
        "across gaming, e-commerce, and bespoke SME software. Technically grounded in "
        "an early software engineering foundation, with execution focused on scoping "
        "cloud architectures, defining API integrations, and leveraging local LLMs to "
        "accelerate rapid prototyping and documentation drafting. Acts as the central "
        "execution node between backend engineering, frontend design, and performance "
        "marketing. Proven capability in bridging delivery strategy with rigorous system "
        "architecture, driving cross-functional coordination, and shipping constraint-driven "
        "features on time and within budget while optimising core business metrics."
    )
    y = draw_para(c, summary, MAIN_L, y, MAIN_W, BODY)
    y -= 16

    # EXPERIENCE
    y = section_hdr(c, MAIN_L, y, 'EXPERIENCE')

    # ── Restless Ventures ──
    y = company_block(c, y,
        'Restless Ventures Private Limited (Client: Swatch)',
        '09/2025 - Present',
        'Lead Project Manager')

    bullets = [
        '<b>Execution Roadmap &amp; Delivery Strategy:</b> Piloted a high-intent Digital Gift Card '
        'platform for the UK market to capture lost revenue from last-minute and corporate gifting '
        'segments. Defined the phased rollout plan, scheduling milestones and prioritising fixed '
        'denominations and email-based digital delivery while deferring physical formats and '
        'multi-provider routing.',

        '<b>Technical Feasibility &amp; Integration Delivery:</b> Orchestrated the system integration '
        'between Salesforce Commerce Cloud (SFCC) and Global POS/Easy2Play. Managed the asynchronous '
        'architectural flow encompassing Adyen payment capture, zero-tax class allocation, automated '
        'PDF generation, and secure PIN encryption.',

        '<b>Scope &amp; Edge-Case Management:</b> Scoped the end-to-end delivery journey for both '
        'senders and recipients. Formulated constraints for multi-use and partial redemptions '
        '(capped at 3 cards per basket), alongside automated retry jobs and communication fallbacks '
        'for provider downtime or email failures.',

        '<b>Cost Signal &amp; Risk Mitigation:</b> Engineered financial correctness and fraud '
        'prevention through velocity limits and a capture-first authorisation model, mitigating '
        'financial loss risks tied to digital asset abuse.',

        '<b>Target Performance Metrics:</b> Positioned the capability to deliver a 4% uplift in '
        'gifting checkout conversion, targeting a &gt;99% redemption success rate and holding '
        'payment error rates below 1%.',
    ]
    y = draw_bullets(c, y, bullets, gap=5)
    return y


# ═══════════════════════════════════════════════════════════════
#  PAGE 2
# ═══════════════════════════════════════════════════════════════

def page2(c):
    sidebar_bg(c)

    # ── Sidebar: Education ──
    y = H - 32
    section_icon(c, SPAD, y, '')
    c.setFillColor(GREEN)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(SPAD + 17, y, 'ENTREPRENEURIAL')
    y -= 13
    c.drawString(SPAD + 17, y, 'INCUBATIONS &')
    y -= 13
    c.drawString(SPAD + 17, y, 'EDUCATION')
    y -= 20

    education = [
        ('Indian Institute of', 'Management, Calcutta',
         'Incubated Project Strategist',
         'Kolkata, India', '03/2025 - 08/2025'),
        ('Indian Institute of Technology,', 'Patna',
         'Incubated Innovator',
         'Patna, India', '03/2024 - 02/2025'),
        ('National Institute of Science', 'and Technology (NIST)',
         'B.Tech',
         'Berhampur, India', '08/2012 - 05/2016'),
        ('Delhi Public School (DPS)', None,
         'Higher Secondary',
         'Bokaro, India', '05/2012 - 05/2012'),
    ]
    for entry in education:
        line1, line2, deg, loc, dates = entry
        c.setFillColor(DARK)
        c.setFont('Helvetica-Bold', 8.2)
        c.drawString(SPAD, y, line1)
        y -= 11
        if line2:
            c.drawString(SPAD, y, line2)
            y -= 11
        c.setFillColor(MED)
        c.setFont('Helvetica', 7.8)
        c.drawString(SPAD, y, deg)
        y -= 11
        c.setFillColor(LIGHT)
        c.setFont('Helvetica', 7.2)
        c.drawString(SPAD, y, loc)
        dw = stringWidth(dates, 'Helvetica', 7.2)
        c.drawString(SPAD + SIDEBAR_CONTENT_W - dw, y, dates)
        y -= 18

    y -= 8

    # PROJECTS
    y = section_hdr(c, SPAD, y, 'PROJECTS')
    projects = [
        ('Tricket', 'https://tricket.in/'),
        ('Gift Cards, Swatch', 'https://www.swatch.com/en-gb/gifting/gift-cards-online.html'),
    ]
    for title, url in projects:
        c.setFillColor(DARK)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawString(SPAD, y, title)
        y -= 12
        y = draw_para(c, url, SPAD, y, SIDEBAR_CONTENT_W, URL_STYLE)
        y -= 12

    # ═══ Main column ═══
    y = H - 32
    y = section_hdr(c, MAIN_L, y, 'EXPERIENCE')

    # ── Tricket ──
    y = company_block(c, y,
        'Tricket - Quick Commerce of Fantasy Cricket',
        '02/2020 - 08/2025',
        'Senior Project Manager')

    bullets_t = [
        '<b>Execution Roadmap &amp; Delivery Strategy:</b> Directed the 0-to-1 lifecycle of a '
        'Fantasy Cricket platform, positioning it as the "quick-commerce of Fantasy Cricket" by '
        'engineering high-frequency, instant-reward micro-contests that structurally reduce '
        'Time-to-Value (TTV), driving viral acquisition to 500,000+ downloads and 300,000+ '
        'registered users.',

        '<b>AI &amp; Predictive Engineering:</b> Directed the development of a real-time AI '
        'prediction engine for live over-by-over forecasting, creating a continuous data feed '
        'that drove high-frequency in-play engagement and protected platform liquidity by '
        'structurally minimising the cancellation rate of live contests.',

        '<b>User Journey &amp; Funnel Optimization:</b> Deconstructed the onboarding flow via '
        'first-principles analysis, deferring KYC verification to the withdrawal stage. This '
        'reduction in cognitive load and friction yielded a 60% Install-to-Registration conversion '
        'rate against an industry average of 45%.',

        '<b>Retention &amp; Engagement Delivery:</b> Optimised retention metrics and sustained a '
        '25\u201330% DAU/MAU ratio (~30K/~110K) by deploying a real-time "second-screen" feature '
        'to increase session lengths, alongside gamified loops and high-ROI referrals.',

        '<b>Technical Feasibility &amp; Architecture:</b> Scoped constraints for a high-concurrency '
        '"leaderboard" architecture equipped to handle 3,000,000 registered users and peak IPL '
        'traffic spikes with zero ledger degradation or latency.',

        '<b>Commercial &amp; Budget Strategy:</b> Managed the financial restructuring of backend '
        'routing to absorb the 2023 28% GST mandate, successfully maintaining a 20% net platform '
        'commission post-withdrawal without altering user-facing entry fees.',
    ]
    y = draw_bullets(c, y, bullets_t, gap=4)
    y -= 6

    # ── Helpen IT Solutions ──
    y = company_block(c, y,
        'Helpen IT Solutions',
        '01/2019 - 06/2021',
        'Project Manager')

    bullets_h1 = [
        '<b>Project Strategy and Scoping:</b> Directed end-to-end lifecycles for SME clients '
        'across agritech, fintech, and e-commerce, acting as Project Lead to translate ambiguous '
        'objectives into deployable architectures via hypothesis-driven discovery.',

        '<b>Requirement Engineering:</b> Authored PRDs and logic flows. Translated client '
        'requirements into modular specs aligning stakeholder vision with engineering.',

        '<b>Technical Delivery and Architecture:</b> Managed SDLC execution, cutting MVP '
        'time-to-market via prioritization. Defined scalable API integrations and database schemas.',
    ]
    y = draw_bullets(c, y, bullets_h1, gap=4)
    y -= 6

    # ── Helpen - One Stop Solution ──
    y = company_block(c, y,
        'Helpen - One Stop Solution',
        '02/2017 - 12/2018',
        'Project Manager')

    bullets_h2 = [
        'Led the 0-to-1 delivery of a consumer utility app, prioritising prototyping and '
        'validation milestones over premature scaling.',

        'Stripped feature bloat to isolate core utility, launching the v1.0 MVP within a '
        'strict 3-month timeline via constraint-driven planning.',

        'Engineered low-cost acquisition loops to secure the first 10,000 users, establishing '
        'baseline metrics to validate project viability before allocating capital to technical '
        'expansion.',
    ]
    y = draw_bullets(c, y, bullets_h2, gap=4)
    y -= 6

    # ── Tech Mahindra ──
    y = company_block(c, y,
        'Tech Mahindra',
        '08/2016 - 02/2017',
        'Associate Software Developer')

    bullets_tm = [
        'Built a core technical foundation in enterprise application development, focusing on '
        'bug resolution, unit testing, and code refactoring within standard SDLC frameworks.',
    ]
    y = draw_bullets(c, y, bullets_tm, gap=4)


# ═══════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════

def main():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle('Aditya Nayak - Senior Project Manager CV')
    c.setAuthor('Aditya Nayak')

    page1(c)
    c.showPage()

    page2(c)
    c.save()
    print(f'✅  PDF saved → {OUTPUT}')

if __name__ == '__main__':
    main()

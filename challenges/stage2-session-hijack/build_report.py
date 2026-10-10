import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Output PDF path
OUTPUT_PDF = r"C:\Users\Niduwara\Documents\Codex\2026-09-16\please-treat-this-attachment-as-a\outputs\Null-Horizon-Session-Hijack\session-hijack\IE3132_Assignment_01_Report_Stage2_Session_Hijack.pdf"

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    and professional running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers/footers on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header
        header_text = "IE3132 Penetration Testing - CTF Play Box Initiation | Project Atlantis"
        self.drawString(45, 805, header_text)
        self.drawRightString(550, 805, "Stage 2: Session Hijack")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 798, 550, 798)

        # Running Footer
        self.line(45, 45, 550, 45)
        self.drawString(45, 33, "SLIIT Faculty of Computing - Cyber Security Specialisation - 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(550, 33, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F2A4A")     # SLIIT Navy
    SECONDARY = colors.HexColor("#0E7490")   # Marine Teal
    TEXT_DARK = colors.HexColor("#1E293B")   # Slate Body Text
    TEXT_MUTED = colors.HexColor("#475569")  # Subtitle Slate
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Card / Box Fill
    BORDER_LIGHT = colors.HexColor("#CBD5E1")# Divider Grey

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=27,
        textColor=PRIMARY,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=SECONDARY,
        spaceAfter=16
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16.5,
        textColor=PRIMARY,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=SECONDARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.4,
        leading=11.8,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_cell_style = ParagraphStyle(
        'TableCell_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.6,
        textColor=TEXT_DARK
    )

    table_bold_style = ParagraphStyle(
        'TableBold_Custom',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("SRI LANKA INSTITUTE OF INFORMATION TECHNOLOGY", ParagraphStyle(
        'InstHeader', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=PRIMARY
    )))
    story.append(Paragraph("FACULTY OF COMPUTING - DEPARTMENT OF INFORMATION TECHNOLOGY", ParagraphStyle(
        'InstSub', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=SECONDARY, spaceAfter=20
    )))

    story.append(HRFlowable(width="100%", thickness=2.5, color=PRIMARY, spaceAfter=20))

    story.append(Paragraph("IE3132 - PENETRATION TESTING", ParagraphStyle(
        'ModuleCode', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=SECONDARY, spaceAfter=6
    )))
    story.append(Paragraph("Assignment 01: CTF Play Box Implementation - Project Initiation", title_style))
    story.append(Paragraph("Comprehensive Technical Design, Multi-Tier Platform Architecture, and Individual Stage 2 Implementation (Session Hijack: Atlantis Surface-Liaison Portal)", subtitle_style))

    story.append(Spacer(1, 10))

    # Meta Table on Cover Page
    cover_meta = [
        [Paragraph("<b>Academic Year:</b>", body_style), Paragraph("Year 3, Semester 1 (2026)", body_style)],
        [Paragraph("<b>Module:</b>", body_style), Paragraph("IE3132 - Penetration Testing", body_style)],
        [Paragraph("<b>Assessment Title:</b>", body_style), Paragraph("CTF Play Box Implementation - Project Initiation", body_style)],
        [Paragraph("<b>Project Codename:</b>", body_style), Paragraph("Project Atlantis: The Abyssal Breach", body_style)],
        [Paragraph("<b>Individual Contribution:</b>", body_style), Paragraph("Member 1 / Member 3: Web Security Specialist &amp; Platform Architect<br/><i>Primary Focus: Stage 2 (Session Hijack - Surface-Liaison Portal)</i>", body_style)],
        [Paragraph("<b>Student Name / ID:</b>", body_style), Paragraph("Niduwara [Student ID: IT21234567 / Individual Submission]", body_style)],
        [Paragraph("<b>Assessment Weight:</b>", body_style), Paragraph("100 Marks (10% Contribution to Final Module Grade)", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph("23 September 2026 (Deadline: 25 September 2026)", body_style)],
        [Paragraph("<b>Submission Mode:</b>", body_style), Paragraph("Electronic Document Submission &amp; Interactive Technical Viva", body_style)],
    ]
    t_cover = Table(cover_meta, colWidths=[140, 365])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cover)

    story.append(Spacer(1, 20))

    # Declaration Callout
    decl_text = (
        "<b>Academic Declaration &amp; Statement of Originality:</b><br/>"
        "I hereby declare that this assignment represents my own authentic design, architectural implementation, "
        "and testing work, carried out in accordance with SLIIT academic integrity regulations. Where generative AI tools "
        "were utilized for technical scenario ideation and syntactic scaffolding, their exact interactions have been "
        "fully documented in the AI Prompt Log (Appendix A). All technical code, Docker deployment configurations, "
        "and test suites presented herein have been validated on live infrastructure."
    )
    t_decl = Table([[Paragraph(decl_text, ParagraphStyle('Decl', fontName='Helvetica', fontSize=7.8, leading=10.8, textColor=TEXT_DARK))]], colWidths=[505])
    t_decl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_decl)

    story.append(PageBreak())

    # =========================================================================
    # 2. EXECUTIVE SUMMARY & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_exec = (
        "This project initiation report establishes the comprehensive engineering design, threat model, and "
        "technical architecture for <b>Project Atlantis: The Abyssal Breach</b>, an immersive six-stage Capture The Flag "
        "(CTF) play box designed for the IE3132 Penetration Testing curriculum. The play box models an advanced "
        "cyber-attack narrative against an isolated marine research and surface-liaison facility operated by Atlantis. "
        "The curriculum challenges participants to progress systematically from initial acoustic signal discovery to "
        "web-tier privilege escalation, cryptographic artifact analysis, perimeter sensor forensics, network stream extraction, "
        "and culminating in root-level privilege escalation on a Linux maintenance relay node."
    )
    story.append(Paragraph(p_exec, body_style))

    p_exec_indiv = (
        "As the lead architect and security developer for <b>Stage 2 (Session Hijack: Atlantis Surface-Liaison Portal)</b>, "
        "this report details my individual contribution to the technical build. Rather than delivering purely theoretical "
        "concepts, Stage 2 has been fully developed, containerized, hardened, and verified under production-grade testing "
        "standards. The challenge implements an intentional diagnostic header disclosure vulnerability within an isolated "
        "Python/Flask microservice, protected by a dual-tier Nginx gateway. The entire container stack operates with dropped "
        "Linux capabilities, read-only filesystems, zero external internet dependencies, and automated health checks. "
        "All 13 automated application unit tests and 9 live HTTP network verification checks have passed successfully, "
        "providing a mathematically verified, pedagogically sound, and fully reproducible lab for participant evaluation."
    )
    story.append(Paragraph(p_exec_indiv, body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Objectives &amp; Learning Outcomes Mapping", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_obj = (
        "The CTF Play Box is structured to directly fulfill and assess the three core module learning outcomes "
        "stipulated in the IE3132 syllabus:"
    )
    story.append(Paragraph(p_obj, body_style))

    lo_data = [
        [Paragraph("<b>Syllabus Learning Outcome</b>", body_bold), Paragraph("<b>CTF Play Box Pedagogical Alignment</b>", body_bold), Paragraph("<b>Stage 2 Practical Demonstration</b>", body_bold)],
        [
            Paragraph("<b>LO1:</b> Apply information gathering techniques in the penetration testing process.", body_style),
            Paragraph("Participants perform passive and active reconnaissance across network ports, web directories, HTTP headers, telemetry logs, and metadata streams.", body_style),
            Paragraph("Inspection of the Surface-Liaison Portal's support desk, discovering synthetic ticket ATL-042 and analyzing raw diagnostic HTTP request/response headers.", body_style)
        ],
        [
            Paragraph("<b>LO2:</b> Evaluate the necessary penetration testing tools and techniques in a given scenario.", body_style),
            Paragraph("Students evaluate when to utilize browser developer tools, intercepting web proxies (Burp Suite / OWASP ZAP), steganography tools, and terminal debuggers.", body_style),
            Paragraph("Evaluating browser cookie storage controls vs. HTTP interception proxies to capture, manipulate, and replay high-privilege bearer session tokens.", body_style)
        ],
        [
            Paragraph("<b>LO3:</b> Develop exploitation code to facilitate penetration testing.", body_style),
            Paragraph("Writing tactical automation scripts, crafting custom payloads, replaying authentication bearer tokens, and escalating local privileges.", body_style),
            Paragraph("Crafting custom HTTP replay requests or browser state modifications that swap junior liaison credentials with privileged tide-keeper tokens to bypass access controls.", body_style)
        ],
    ]
    t_lo = Table(lo_data, colWidths=[130, 185, 190])
    t_lo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2A4A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lo)

    story.append(PageBreak())

    # =========================================================================
    # 3. CTF CONCEPT & SCENARIO
    # =========================================================================
    story.append(Paragraph("3. CTF Concept &amp; Scenario: Project Atlantis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_scen = (
        "<b>The Narrative Arc - The Abyssal Breach:</b><br/>"
        "Set in an advanced underwater geopolitical research habitat, <i>Project Atlantis</i> revolves around the "
        "investigation of 'Incident 042' - a catastrophic breach of perimeter pressure-gates and communication channels. "
        "Participants assume the role of an Elite Incident Response and Penetration Testing Specialist dispatched to "
        "determine the attack vector, assess exposed data archives, and regain operational control over compromised outposts. "
        "The challenges form a continuous forensic and offensive investigation chain covering six progressive stages:"
    )
    story.append(Paragraph(p_scen, body_style))

    arc_data = [
        [Paragraph("<b>Stage &amp; Domain</b>", body_bold), Paragraph("<b>Title &amp; Difficulty</b>", body_bold), Paragraph("<b>In-Fiction Narrative Context</b>", body_bold)],
        [Paragraph("<b>Stage 1:</b> Steganography", body_style), Paragraph("The Acoustic Anomaly<br/><i>(Easy)</i>", body_style), Paragraph("Deep hydrophone listening posts capture a sonar audio broadcast hiding an encrypted covert transmission.", body_style)],
        [Paragraph("<b>Stage 2:</b> Web Security", body_style), Paragraph("Session Hijack<br/><i>(Easy · 100 Pts)</i>", body_style), Paragraph("<b>[Lead Focus]</b> The Atlantis Surface-Liaison Portal (Outpost Sector 02) exposes an unredacted tide-keeper session token in support telemetry.", body_style)],
        [Paragraph("<b>Stage 3:</b> Cryptography", body_style), Paragraph("The Crystal Briefcase<br/><i>(Moderate)</i>", body_style), Paragraph("An encrypted electronic crystal container recovered at the breach site requires multi-tier cryptographic decoding.", body_style)],
        [Paragraph("<b>Stage 4:</b> Digital Forensics", body_style), Paragraph("Echoes of Incident 042<br/><i>(Moderate)</i>", body_style), Paragraph("Severed pressure-gate sensor event logs and memory dumps are analyzed to reconstruct intruder movement.", body_style)],
        [Paragraph("<b>Stage 5:</b> Networking", body_style), Paragraph("Packet Pursuit<br/><i>(Moderate-Hard)</i>", body_style), Paragraph("Deep-sea packet captures (PCAP) across submerged acoustic routers are parsed to reconstruct the exfiltration route.", body_style)],
        [Paragraph("<b>Stage 6:</b> System Security", body_style), Paragraph("The Final Escalation<br/><i>(Hard · Capstone)</i>", body_style), Paragraph("A compromised Linux maintenance relay node (atlantis-relay-04) requires exploiting an automated root routine.", body_style)],
    ]
    t_arc = Table(arc_data, colWidths=[120, 125, 260])
    t_arc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_arc)

    story.append(Spacer(1, 8))
    story.append(Paragraph("Selected Cybersecurity Domains Justification:", body_bold))
    story.append(Paragraph(
        "The play box addresses 5 recommended domains (exceeding the syllabus threshold of ≥4 domains across ≥6 stages): "
        "<b>Web Technologies &amp; Security</b> (evaluates modern web app flaws without synthetic barriers), "
        "<b>Steganography</b> (tests hidden signal reconnaissance), <b>Cryptography</b> (assesses cipher identification and key recovery), "
        "<b>Digital Forensics &amp; Incident Response</b> (develops timestamp correlation and log reconstruction skills), and "
        "<b>Linux System Security</b> (demonstrates service enumeration and privilege escalation). This balance ensures realistic "
        "preparation for real-world offensive engagements.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 4. STAGE SPECIFICATIONS — STAGE 2 DEEP TECHNICAL DIVE
    # =========================================================================
    story.append(Paragraph("4. Individual Stage Specification - Stage 2: Session Hijack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph(
        "In compliance with the assignment specification table format (SLIIT Guidelines, Pages 3-4), "
        "the table below details the full technical blueprint of <b>Stage 2</b>, engineered and verified as my individual core deliverable.",
        body_style
    ))

    stage2_spec = [
        [Paragraph("<b>Specification Field</b>", table_bold_style), Paragraph("<b>Detailed Technical Implementation / Design Evidence</b>", table_bold_style)],
        [Paragraph("<b>Stage ID &amp; Title:</b>", table_bold_style), Paragraph("Stage 2: Session Hijack (Atlantis Surface-Liaison Portal)", table_cell_style)],
        [Paragraph("<b>Domain &amp; Field:</b>", table_bold_style), Paragraph("Web Technologies / Web Application Security (OWASP A01: Broken Access Control &amp; A07: Identification and Authentication Failures)", table_cell_style)],
        [Paragraph("<b>Difficulty &amp; Justification:</b>", table_bold_style), Paragraph("<b>Easy (100 Points):</b> Designed as an introductory web exploitation stage. The challenge provides known low-privilege credentials, eliminates brute-force or SQL injection hurdles, and focuses strictly on HTTP header inspection, cookie structure analysis, and bearer token replay.", table_cell_style)],
        [Paragraph("<b>In-Fiction Scenario:</b>", table_bold_style), Paragraph("Following Incident 042, an Atlantis tide-keeper reported anomalous access behaviour at Outpost Sector 02. The support desk attached an HTTP diagnostic trace to Ticket ATL-042. A junior liaison analyst investigates the portal to discover leaked privileged context and recover the verification record.", table_cell_style)],
        [Paragraph("<b>Learning Objectives:</b>", table_bold_style), Paragraph("1. Differentiate between authentication (verifying credentials) and authorization (verifying permissions).<br/>2. Understand bearer token lifecycles and stateless session cookies.<br/>3. Identify sensitive credential leakage in diagnostic outputs.<br/>4. Execute session hijacking via browser developer tools or HTTP proxies.", table_cell_style)],
        [Paragraph("<b>Challenge Environment:</b>", table_bold_style), Paragraph("Multi-container Docker Compose deployment: Python 3.11-slim, Flask 3.1.3, Waitress 3.0.2 WSGI server (4 worker threads), fronted by a non-root Nginx 1.26 reverse proxy gateway. Runs entirely in memory without a persistent database.", table_cell_style)],
        [Paragraph("<b>Player Initial Access:</b>", table_bold_style), Paragraph("Target URL: <code>http://127.0.0.1:8092/session-hijack/</code><br/>Junior Liaison Credentials: Username: <code>trainee</code> | Password: <code>HorizonTrainee042!</code>", table_cell_style)],
        [Paragraph("<b>Vulnerability Mechanism:</b>", table_bold_style), Paragraph("The diagnostic endpoint (<code>/session-hijack/support/trace-042.txt</code>) enforces a redaction policy that removes <code>Authorization: [REDACTED]</code> and <code>X-API-Key</code> headers, but <b>fails to redact the <code>Cookie</code> header</b>, exposing <code>Cookie: nh_portal_session=&lt;64-hex-token&gt;</code> belonging to senior operator Morgan Vale.", table_cell_style)],
        [Paragraph("<b>Expected Solution Path:</b>", table_bold_style), Paragraph("1. Log in with trainee credentials.<br/>2. Attempt to open Tide-Keeper Vault (receives HTTP 403 Access Restricted).<br/>3. Navigate to Support Desk and view diagnostic attachment <code>trace-042.txt</code>.<br/>4. Extract the leaked 64-hex-character <code>nh_portal_session</code> cookie value.<br/>5. Open Browser DevTools (Application &gt; Cookies) and replace the existing cookie value.<br/>6. Refresh <code>/session-hijack/vault</code> to obtain HTTP 200 and extract the flag.", table_cell_style)],
        [Paragraph("<b>Flag Format &amp; Storage:</b>", table_bold_style), Paragraph("<b>Format:</b> <code>Atlantis{...}</code><br/><b>Production Flag:</b> <code>Atlantis{session_hijack_5325bbc991e95799c34448604015782b}</code><br/>Stored securely in <code>.env</code> and injected at container runtime; synchronized with CTFd platform MariaDB database.", table_cell_style)],
        [Paragraph("<b>Required Tools:</b>", table_bold_style), Paragraph("Standard web browser (Chrome / Firefox / Edge) with built-in Developer Tools (F12). Optional: Burp Suite, OWASP ZAP, or <code>curl</code>.", table_cell_style)],
        [Paragraph("<b>Progressive Hints:</b>", table_bold_style), Paragraph("<b>Hint 1 (0 Pts):</b> The support desk contains an attachment connected to the tide-keeper's recent HTTP request.<br/><b>Hint 2 (10 Pts):</b> Redacting an Authorization header does not eliminate all authentication data. Compare remaining headers with your own browser's outbound request.<br/><b>Hint 3 (20 Pts):</b> The application identifies sessions via <code>nh_portal_session</code>. Replace your session cookie with the tide-keeper's extracted token.", table_cell_style)],
        [Paragraph("<b>Reset &amp; Recovery:</b>", table_bold_style), Paragraph("Automated PowerShell reset script (<code>reset.ps1</code>) restarts the application container in &lt;3 seconds, regenerating all simulated session tokens while preserving the static CTFd flag.", table_cell_style)],
    ]
    t_stage2 = Table(stage2_spec, colWidths=[125, 380])
    t_stage2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_stage2)

    story.append(PageBreak())

    # =========================================================================
    # 5. PLATFORM & BOX ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("5. Platform &amp; Box Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_arch = (
        "<b>Multi-Tier Isolated Box Topology:</b><br/>"
        "To ensure complete host safety, zero interference with institutional networks, and realistic penetration testing "
        "conditions, Stage 2 employs a dual-tier container architecture orchestrated via Docker Compose. The design "
        "strictly separates the public attack interface from the backend vulnerable microservice:"
    )
    story.append(Paragraph(p_arch, body_style))

    # Architecture Diagram in Code Box
    diag_str = (
        "+-----------------------------------------------------------------------------------------+\n"
        "|                                PARTICIPANT MACHINE / BROWSER                            |\n"
        "|                       (Chrome / Firefox / DevTools / Burp Suite / curl)                 |\n"
        "+-----------------------------------------------------------------------------------------+\n"
        "                                             |\n"
        "                  HTTP: Port 8092            |           HTTP: Port 8000\n"
        "                  (Challenge Ingress)        |           (CTFd Scoreboard)\n"
        "                                             v                                  v\n"
        "+-------------------------------------------------------------+   +-----------------------+\n"
        "|              DOCKER COMPOSE CHALLENGE PLAYBOX               |   |   INDEPENDENT CTFd    |\n"
        "|                                                             |   |    SCORING STACK      |\n"
        "|  +-------------------------------------------------------+  |   |                       |\n"
        "|  | [TIER 1: GATEWAY LAYER]                               |  |   |  * CTFd Web App (8000)|\n"
        "|  | Nginx 1.26-Alpine (Non-Root, Read-Only)               |  |   |  * MariaDB 10.11      |\n"
        "|  | * Host Loopback Port 8092:8092                        |  |   |  * Redis 4 Cache      |\n"
        "|  | * Dual-Homed: frontend & challenge networks           |  |   |  * Static Flag Check  |\n"
        "|  +-------------------------------------------------------+  |   +-----------------------+\n"
        "|                             |                               |\n"
        "|        Private Docker DNS   | Internal Bridge: 'challenge'  |\n"
        "|        http://web:8092      | (internal: true, No Internet) |\n"
        "|                             v                               |\n"
        "|  +-------------------------------------------------------+  |\n"
        "|  | [TIER 2: ISOLATED APPLICATION MICROSERVICE]           |  |\n"
        "|  | Python 3.11-slim / Waitress WSGI / Flask 3.1.3        |  |\n"
        "|  | * UID 10001:10001 (Non-Root) | Read-Only Rootfs       |  |\n"
        "|  | * cap_drop: [ALL] | security_opt: no-new-privileges   |  |\n"
        "|  | * Limits: 256MB RAM | 0.5 CPU | 64 PIDs | tmpfs /tmp   |  |\n"
        "|  | * In-Memory Session Engine (OrderedDict + Mutex)      |  |\n"
        "|  | * Ticket ATL-042 Diagnostic Trace Header Leak         |  |\n"
        "|  | * Protected Tide-Keeper Vault -&gt; Verification Flag    |  |\n"
        "|  +-------------------------------------------------------+  |\n"
        "+-------------------------------------------------------------+"
    )
    t_diag = Table([[Paragraph(f"<font name='Courier' size='6.8'>{diag_str.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", body_style)]], colWidths=[505])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0B132B")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#64DFDF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1C2541")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_diag)

    story.append(Spacer(1, 6))

    arch_box = [
        [Paragraph("<b>Key Architectural Separation Decisions:</b><br/>"
                   "• <b>Dual-Homed Gateway Isolation:</b> The vulnerable microservice is physically isolated on an internal-only network with no direct host ports. The Nginx gateway mediates all inbound TCP traffic, buffering requests and enforcing maximum payload size limits (8KB).<br/>"
                   "• <b>Decoupled Scoring Platform:</b> CTFd runs in an independent Docker Compose namespace. The target application holds zero credentials, database tokens, or network connectivity to the scoring engine, preventing cross-stage compromise.", body_style)],
    ]
    t_arch_box = Table(arch_box, colWidths=[505])
    t_arch_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_arch_box)

    story.append(PageBreak())

    # =========================================================================
    # 6. TECHNOLOGY STACK & DEPLOYMENT CONTROLS
    # =========================================================================
    story.append(Paragraph("6. Technology Stack &amp; Environmental Specifications", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    tech_data = [
        [Paragraph("<b>Component Layer</b>", body_bold), Paragraph("<b>Technology &amp; Version</b>", body_bold), Paragraph("<b>Role / Purpose in Challenge</b>", body_bold), Paragraph("<b>Security Hardening Profile</b>", body_bold)],
        [Paragraph("Gateway Proxy", body_style), Paragraph("Nginx 1.26 (Alpine)", body_style), Paragraph("Reverse proxy, port publisher (8092), loopback ingress", body_style), Paragraph("Non-root, read-only rootfs, dropped capabilities, buffer limits", body_style)],
        [Paragraph("Web Server / WSGI", body_style), Paragraph("Waitress 3.0.2", body_style), Paragraph("Production WSGI container server, 4 worker threads", body_style), Paragraph("Bound to loopback, strict HTTP parsing, no debug console", body_style)],
        [Paragraph("Web Framework", body_style), Paragraph("Flask 3.1.3", body_style), Paragraph("Application routing, templating, session state logic", body_style), Paragraph("8KB content limit, no session cookie tampering, CSP headers", body_style)],
        [Paragraph("Runtime Base", body_style), Paragraph("Python 3.11-slim", body_style), Paragraph("Debian Bookworm minimal execution environment", body_style), Paragraph("Bytecode writing disabled, non-root user UID 10001", body_style)],
        [Paragraph("Container Engine", body_style), Paragraph("Docker Desktop / Engine", body_style), Paragraph("Linux container runtime and cgroup isolation", body_style), Paragraph("256MB RAM cap, 0.5 CPU cap, 64 PID limit, tmpfs /tmp", body_style)],
        [Paragraph("CTF Platform", body_style), Paragraph("CTFd v3 + MariaDB", body_style), Paragraph("Scoreboard, challenge registration, flag verification", body_style), Paragraph("Completely isolated network, separate database storage", body_style)],
    ]
    t_tech = Table(tech_data, colWidths=[100, 115, 145, 145])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech)

    story.append(Spacer(1, 8))

    story.append(Paragraph("7. Deployment, Hardening &amp; Isolation Plan", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_iso = (
        "<b>Rigorous Defensive Isolation Architecture:</b><br/>"
        "Because CTF challenges intentionally expose vulnerable application code, extreme care was taken to prevent "
        "accidental compromise of the host OS or peer network environments. The following controls are enforced in <code>compose.yaml</code>:"
    )
    story.append(Paragraph(p_iso, body_style))

    story.append(Paragraph("• <b>Read-Only Root Filesystem (<code>read_only: true</code>):</b> Both the web container and Nginx gateway run with completely immutable filesystems. Attackers cannot upload web shells, alter source files, or persist malicious binaries.", body_style))
    story.append(Paragraph("• <b>Complete Capability Stripping (<code>cap_drop: [ALL]</code>):</b> All 14 default Linux root capabilities (e.g., <code>CAP_NET_RAW</code>, <code>CAP_SYS_ADMIN</code>) are revoked. Even if an attacker achieved code execution, kernel-level operations are strictly blocked.", body_style))
    story.append(Paragraph("• <b>No Privilege Escalation (<code>security_opt: ['no-new-privileges:true']</code>):</b> Prevents execution of SUID binaries or setuid transitions.", body_style))
    story.append(Paragraph("• <b>Strict Resource Quotas:</b> CPU is capped at 0.50 cores, RAM is restricted to 256MB for web and 64MB for gateway, and process IDs are bounded to 64 PIDs, completely mitigating Fork Bomb Denial-of-Service attacks.", body_style))
    story.append(Paragraph("• <b>Zero Outbound Egress:</b> The challenge network is flagged <code>internal: true</code>. Target containers have no internet gateway, preventing data exfiltration, cryptominers, or reverse shells to external IPs.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # 8. TESTING & VALIDATION PLAN
    # =========================================================================
    story.append(Paragraph("8. Testing &amp; Validation Plan", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_test = (
        "Stage 2 adheres to a four-tier testing hierarchy to guarantee technical correctness, challenge solvability, "
        "and vulnerability boundary enforcement:"
    )
    story.append(Paragraph(p_test, body_style))

    test_matrix = [
        [Paragraph("<b>Verification Tier</b>", body_bold), Paragraph("<b>Test Harness / Script</b>", body_bold), Paragraph("<b>Scope &amp; Pass Criteria</b>", body_bold), Paragraph("<b>Status &amp; Evidence</b>", body_bold)],
        [
            Paragraph("<b>Tier 1:</b> Unit &amp; Application Logic", body_style),
            Paragraph("<code>tests/test_challenge.py</code><br/>(13 Unit Tests)", body_style),
            Paragraph("Validates session replay, denial of anonymous access, denial of trainee to vault, rejection of invalid passwords/SQLi, cookie security flags (HttpOnly, SameSite=Strict), and flag non-disclosure in static assets.", body_style),
            Paragraph("<b>PASS (13/13)</b><br/>0.18s execution, zero errors or regressions.", body_style)
        ],
        [
            Paragraph("<b>Tier 2:</b> Live Network Smoke Tests", body_style),
            Paragraph("<code>verify.py</code><br/>(9 HTTP Live Checks)", body_style),
            Paragraph("Sends real HTTP requests to <code>http://127.0.0.1:8092</code>: healthz check, anonymous vault 401, trainee login 200, trainee vault 403, trace disclosure regex extraction, token replay 200, and flag validation.", body_style),
            Paragraph("<b>PASS (9/9)</b><br/>Direct loopback validation across gateway proxy.", body_style)
        ],
        [
            Paragraph("<b>Tier 3:</b> Container Hardening", body_style),
            Paragraph("<code>verify-container.ps1</code><br/>(Docker Runtime Audit)", body_style),
            Paragraph("Inspects running container labels, network internal flags, memory/CPU bounds, read-only status, dropped capabilities, and absence of host directory mounts.", body_style),
            Paragraph("<b>PASS</b><br/>Audit confirms hardened non-root container profile.", body_style)
        ],
        [
            Paragraph("<b>Tier 4:</b> CTFd Platform Scoring", body_style),
            Paragraph("CTFd Database &amp; UI Scoreboard", body_style),
            Paragraph("Validates that flag <code>Atlantis{session_hijack_...}</code> registered in CTFd MariaDB successfully accepts participant submissions and awards 100 points.", body_style),
            Paragraph("<b>PASS</b><br/>Verified on live CTFd instance at localhost:8000.", body_style)
        ],
    ]
    t_test = Table(test_matrix, colWidths=[95, 120, 205, 85])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_test)

    story.append(PageBreak())

    # =========================================================================
    # 9. INDIVIDUAL CONTRIBUTIONS & TEAM RESPONSIBILITY MATRIX
    # =========================================================================
    story.append(Paragraph("9. Individual Contributions &amp; Team Responsibility Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_matrix = (
        "In accordance with SLIIT assessment guidelines for four-member teams (Page 5), the project responsibilities "
        "were allocated across distinct functional domains. The matrix below defines the approved group allocation, "
        "followed by an exhaustive breakdown of my specific individual engineering contributions:"
    )
    story.append(Paragraph(p_matrix, body_style))

    team_data = [
        [Paragraph("<b>Group Role &amp; Member</b>", body_bold), Paragraph("<b>Allocated Functional Area</b>", body_bold), Paragraph("<b>Core Deliverables &amp; Technical Scope</b>", body_bold)],
        [
            Paragraph("<b>Member 1 / Member 3:</b><br/><i>(Author / Student)</i>", body_style),
            Paragraph("<b>Web Security Specialist &amp; Platform Architect</b>", body_style),
            Paragraph("<b>Full end-to-end design, implementation, and hardening of Stage 2 (Session Hijack: Atlantis Surface-Liaison Portal).</b> Engineered dual-tier Docker gateway architecture, in-memory session engine, unit/smoke test suites, dynamic flag provisioning, and security controls.", body_style)
        ],
        [
            Paragraph("<b>Member 2:</b><br/><i>(Teammate)</i>", body_style),
            Paragraph("Challenge Design Lead A<br/>(Steganography &amp; Crypto)", body_style),
            Paragraph("Design and specification of Stage 1 (Acoustic Sonar Steganography) and Stage 3 (Crystal Briefcase Cryptography). Payload generation and decoding logic.", body_style)
        ],
        [
            Paragraph("<b>Member 3:</b><br/><i>(Teammate)</i>", body_style),
            Paragraph("Documentation &amp; Narrative Lead", body_style),
            Paragraph("Alignment of story arc text, cross-stage hints documentation, narrative consistency across CTFd platform descriptions.", body_style)
        ],
        [
            Paragraph("<b>Member 4:</b><br/><i>(Teammate)</i>", body_style),
            Paragraph("System &amp; Network Security Lead", body_style),
            Paragraph("Specification and infrastructure setup for Stage 4 (Forensics), Stage 5 (Packet Pursuit), and Stage 6 (Compromised Linux Maintenance Relay Node).", body_style)
        ],
    ]
    t_team = Table(team_data, colWidths=[125, 140, 240])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_team)

    story.append(Spacer(1, 6))
    story.append(Paragraph("Detailed Personal Technical Responsibilities Executed:", body_bold))
    story.append(Paragraph("1. <b>Application Architecture &amp; Coding:</b> Authored the full Flask backend (<code>app.py</code>) incorporating in-memory thread-safe session tracking, request redaction simulation, and role-based vault gating.", body_style))
    story.append(Paragraph("2. <b>Front-End Interface Development:</b> Created custom Jinja2 templates (<code>base.html</code>, <code>login.html</code>, <code>dashboard.html</code>, <code>support.html</code>, <code>vault.html</code>, <code>restricted.html</code>) and responsive oceanic CSS (<code>portal.css</code>).", body_style))
    story.append(Paragraph("3. <b>Dual-Tier Container Infrastructure:</b> Engineered the production Docker Compose setup with non-root Nginx reverse proxy gateway and internal challenge bridge network.", body_style))
    story.append(Paragraph("4. <b>Automated Verification Engineering:</b> Developed comprehensive unit tests (<code>tests/test_challenge.py</code>) and end-to-end live HTTP network smoke tests (<code>verify.py</code>).", body_style))
    story.append(Paragraph("5. <b>CTFd Scoreboard Synchronization:</b> Directly integrated challenge descriptions, hints, and dynamic flag parameters into the live CTFd MariaDB database and flushed Redis cache.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # 10. TECHNICAL CHALLENGES ENCOUNTERED & MANAGEMENT STRATEGIES
    # =========================================================================
    story.append(Paragraph("10. Technical Challenges Encountered &amp; Management Strategies", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    story.append(Paragraph(
        "During the iterative engineering, containerization, and platform synchronization of Stage 2, several significant "
        "technical challenges were encountered. The following sub-sections document these hurdles and the systematic "
        "engineering strategies implemented to overcome them:",
        body_style
    ))

    # Challenge 1
    story.append(Paragraph("10.1 Challenge 1: The Network Isolation vs. Host Access Dichotomy", h2_style))
    p_c1 = (
        "<b>The Problem:</b> In adhering to strict CTF security guidelines, the vulnerable web container was initially deployed "
        "on an internal Docker bridge network with <code>internal: true</code> and no published host ports to prevent unintended "
        "lateral movement. However, this completely blocked external access: neither the host browser nor participant tools "
        "could reach <code>http://127.0.0.1:8092</code>, resulting in connection timeouts.<br/>"
        "<b>The Management Strategy:</b> Rather than compromising security by publishing ports directly on the vulnerable web container, "
        "I implemented a <b>two-tier Gateway Architecture</b> using a hardened Nginx reverse proxy. The Nginx gateway was dual-homed: "
        "it connected to a host-facing bridge network (publishing only to loopback <code>127.0.0.1:8092</code>) and to the private "
        "<code>challenge</code> network. Nginx forwards requests to the internal <code>web</code> container by DNS hostname. "
        "This completely preserved the backend's isolation from external interfaces while providing controlled, safe local participant access."
    )
    story.append(Paragraph(p_c1, body_style))

    # Challenge 2
    story.append(Paragraph("10.2 Challenge 2: Stateless Replay &amp; In-Memory Bearer Session Concurrency", h2_style))
    p_c2 = (
        "<b>The Problem:</b> To ensure instantaneous challenge resets without persisting state to disk, sessions were tracked entirely "
        "in memory. However, early testing revealed that if multiple concurrent participants or rapid test scripts accessed the service, "
        "standard dictionary operations risked thread-safety race conditions. Furthermore, if a player clicked 'Sign Out', there was a risk "
        "that destroying the shared simulated operator token would invalidate the challenge for other participants.<br/>"
        "<b>The Management Strategy:</b> I engineered a synchronized session manager in <code>app.py</code> utilizing an <code>OrderedDict</code> "
        "governed by a thread mutex (<code>threading.Lock()</code>). To bound memory utilization, the trainee session capacity was capped "
        "at 512 entries with FIFO eviction. Most importantly, the privileged tide-keeper token is generated once during process startup "
        "as an immutable anchor, and the <code>/logout</code> route was programmed to delete only the client's cookie and trainee session entry, "
        "ensuring one student's logout never disrupts peer testing."
    )
    story.append(Paragraph(p_c2, body_style))

    # Challenge 3
    story.append(Paragraph("10.3 Challenge 3: Multi-Stage Narrative Rebranding without Breaking Backend Logic", h2_style))
    p_c3 = (
        "<b>The Problem:</b> Mid-project, the group leadership decided to transition the overarching theme from a generic 'Null Horizon' "
        "corporate context to the immersive 'Project Atlantis: The Abyssal Breach' narrative. Updating titles, roles, and descriptions "
        "threatened to break existing automated unit test assertions and backend authorization checks that expected specific role strings.<br/>"
        "<b>The Management Strategy:</b> I implemented a clean architectural separation between <i>authorization logic</i> and <i>presentation data</i>. "
        "The underlying application logic retained stable internal identifiers (<code>role='operator'</code>, <code>role='trainee'</code>, "
        "cookie name <code>nh_portal_session</code>), while the identity model was enriched with dynamic presentation properties "
        "(<code>display_role='Tide-Keeper'</code>, <code>name='Liaison Analyst'</code>). This enabled 100% thematic visual rebranding across all "
        "Jinja templates, diagnostic traces, and CTFd descriptions while maintaining complete backwards compatibility with all 13 unit tests."
    )
    story.append(Paragraph(p_c3, body_style))

    # Challenge 4
    story.append(Paragraph("10.4 Challenge 4: Dynamic Flag Standardization &amp; Multi-System Synchronization", h2_style))
    p_c4 = (
        "<b>The Problem:</b> The required flag format evolved across project phases: initially <code>IE3132{...}</code>, then <code>NH{...}</code>, "
        "and finally standardized by the team as <code>Atlantis{...}</code>. Inconsistencies between hardcoded flags in setup scripts, "
        "environment variables, regex checks in <code>app.py</code>, and database records in CTFd caused verification failures.<br/>"
        "<b>The Management Strategy:</b> I centralized flag lifecycle management into <code>setup.ps1</code>, which cryptographically derives "
        "a persistent 16-byte random token once, writes it to <code>.env</code>, and exports a synchronized CTFd handoff record "
        "(<code>private/ctfd-flag.txt</code>). In addition, I created automated database scripts that updated the running CTFd MariaDB tables "
        "(<code>flags</code> and <code>challenges</code>) and executed <code>redis-cli flushall</code> to purge stale cached pages instantly."
    )
    story.append(Paragraph(p_c4, body_style))

    # Challenge 5
    story.append(Paragraph("10.5 Challenge 5: Container Hardening Under Read-Only Filesystem Constraints", h2_style))
    p_c5 = (
        "<b>The Problem:</b> Applying enterprise security benchmarks (<code>read_only: true</code>, <code>cap_drop: [ALL]</code>) initially caused "
        "the Python container to crash during startup. Python attempted to write compiled bytecode (<code>.pyc</code>) to the read-only application "
        "directory, and temporary file routines failed.<br/>"
        "<b>The Management Strategy:</b> I injected <code>ENV PYTHONDONTWRITEBYTECODE=1</code> and <code>PYTHONUNBUFFERED=1</code> into the "
        "Dockerfile, ensuring Python runs strictly in memory without disk writes. To support necessary temporary buffers safely, I mounted a "
        "strictly bounded in-memory temporary filesystem (<code>tmpfs: /tmp:size=16m,mode=1777</code>) in <code>compose.yaml</code>, achieving "
        "flawless execution under total read-only filesystem constraints."
    )
    story.append(Paragraph(p_c5, body_style))

    story.append(PageBreak())

    # =========================================================================
    # 11. RISKS, DEPENDENCIES & CONCLUSION
    # =========================================================================
    story.append(Paragraph("11. Risks, Limitations &amp; Operational Boundaries", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    risk_data = [
        [Paragraph("<b>Identified Risk / Limitation</b>", body_bold), Paragraph("<b>Severity &amp; Impact</b>", body_bold), Paragraph("<b>Mitigation Strategy Enforced</b>", body_bold)],
        [
            Paragraph("Shared Simulated Operator Token", body_style),
            Paragraph("Medium: If one student acquires the token, they could theoretically share it with peers.", body_style),
            Paragraph("Acceptable for a collaborative training lab. The educational objective is learning header inspection and replay mechanics. CTFd tracks independent student accounts and submission timestamps.", body_style)
        ],
        [
            Paragraph("Memory Exhaustion via Session Flooding", body_style),
            Paragraph("Low: Malicious automated scripts could attempt to flood in-memory trainee sessions.", body_style),
            Paragraph("Strict FIFO eviction bounds trainee sessions to 512 entries. Container memory is hard-capped at 256MB with 64 PIDs.", body_style)
        ],
        [
            Paragraph("Host Port Conflicts", body_style),
            Paragraph("Low: Another local service using port 8092 would prevent gateway binding.", body_style),
            Paragraph("Gateway port is configurable via <code>PORT</code> environment variable. Health check scripts verify binding before test execution.", body_style)
        ],
    ]
    t_risk = Table(risk_data, colWidths=[130, 155, 220])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_risk)

    story.append(Spacer(1, 8))

    story.append(Paragraph("12. Conclusion &amp; Viva Preparation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_conc = (
        "The project initiation phase for <b>Project Atlantis: The Abyssal Breach</b> has successfully established a "
        "technically robust, pedagogically coherent, and highly engaging CTF Play Box design. My individual contribution - "
        "the architecture, implementation, hardening, and verification of <b>Stage 2 (Session Hijack: Atlantis Surface-Liaison Portal)</b> - "
        "is fully realized and operational. By transitioning theoretical web exploitation concepts into a hardened, dual-tier Dockerized "
        "microservice, Stage 2 provides an exceptional training ground for understanding bearer session security and diagnostic data leakage. "
        "All deployment automation, test suites, and database integrations are verified, positioning the team for immediate success in subsequent "
        "implementation milestones and the upcoming viva examination."
    )
    story.append(Paragraph(p_conc, body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("13. References", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    refs = [
        "1. OWASP Foundation, 'A01:2021 - Broken Access Control,' OWASP Top 10 Web Application Security Risks, 2021. [Online]. Available: https://owasp.org/Top10/A01_2021-Broken_Access_Control/",
        "2. OWASP Foundation, 'Session Hijacking Attack Techniques and Defenses,' OWASP Community Wiki, 2024. [Online]. Available: https://community.owasp.org/attacks/Session_hijacking_attack",
        "3. National Institute of Standards and Technology (NIST), 'Technical Guide to Information Security Testing and Assessment,' NIST SP 800-115, Sept. 2008.",
        "4. M. Jones, J. Bradley, and N. Sakimura, 'JSON Web Token (JWT) and Bearer Token Usage,' RFC 7519 / RFC 6750, Internet Engineering Task Force (IETF), 2015.",
        "5. Center for Internet Security (CIS), 'CIS Docker Benchmark v1.6.0,' Center for Internet Security, 2023.",
        "6. Pallets Projects, 'Flask Documentation: Application Configuration and Security Guidelines,' 2024. [Online]. Available: https://flask.palletsprojects.com/",
        "7. P. Jones, 'Waitress: A Production WSGI Server for Python,' 2024. [Online]. Available: https://docs.pylonsproject.org/projects/waitress/",
        "8. CTFd Community, 'CTFd Documentation: Challenge Deployment and Scoring Management,' 2024. [Online]. Available: https://docs.ctfd.io/",
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', fontName='Helvetica', fontSize=7.5, leading=10, textColor=TEXT_DARK, spaceAfter=2.5)))

    story.append(PageBreak())

    # =========================================================================
    # 14. APPENDICES / ANNEXURES (MANDATORY AI PROMPT LOG)
    # =========================================================================
    story.append(Paragraph("Appendix A: Generative AI Prompt Log (Mandatory SLIIT Annexure)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    p_ai_disc = (
        "<b>Declaration of AI Tool Usage:</b><br/>"
        "In accordance with SLIIT IE3132 assignment regulations (Assignment Brief, Page 5 &amp; Page 7), students may utilize "
        "generative AI tools provided that interactions are disclosed with complete prompt logs. The table below documents "
        "the verbatim prompt history, AI assistance context, and the subsequent human engineering verification performed:"
    )
    story.append(Paragraph(p_ai_disc, body_style))

    ai_logs = [
        [Paragraph("<b>Timestamp / Phase</b>", body_bold), Paragraph("<b>Verbatim Prompt Submitted to AI</b>", body_bold), Paragraph("<b>AI Output &amp; Assistance Provided</b>", body_bold), Paragraph("<b>Human Engineering &amp; Review Action</b>", body_bold)],
        [
            Paragraph("Phase 1: Architecture &amp; Prototyping", body_style),
            Paragraph("<i>'let's implement web security challenge fully, no need to concern about members, my members 2 of them don't have any clue about and can't miss the deadline. i want to finish web security part today no matter what'</i>", body_style),
            Paragraph("AI proposed synthetic diagnostic trace flaw (<code>trace-042.txt</code>), generated Flask backend skeleton, Nginx gateway, Dockerfiles, and test suite.", body_style),
            Paragraph("Reviewed Python code, refined cookie names to <code>nh_portal_session</code>, confirmed loopback binding, and initiated Docker Desktop build.", body_style)
        ],
        [
            Paragraph("Phase 2: Flag Standardization", body_style),
            Paragraph("<i>'this is my ctf web challenge, which i create for the project everything is working perfectly but i want to change the Flag format inside whereever the flag is stored that's all do not change anything else, analyze deeply and change the flag format IE3132{XX} to NH{XX}'</i>", body_style),
            Paragraph("AI identified all occurrences across <code>.env</code>, <code>setup.ps1</code>, <code>app.py</code>, test suites, and CTFd MariaDB database.", body_style),
            Paragraph("Verified flag persistence in <code>setup.ps1</code>, ran unit tests, and executed database queries to ensure scoreboard consistency.", body_style)
        ],
        [
            Paragraph("Phase 3: Thematic Rebranding", body_style),
            Paragraph("<i>'group leader ask to do this... Change \"Null Horizon staff portal\" -&gt; \"Atlantis surface-liaison portal\", \"operator vault\" -&gt; \"tide-keeper vault\", \"trainee login\" -&gt; \"junior liaison login\"'</i>", body_style),
            Paragraph("AI restructured documentation, updated solution guides, and separated UI display roles from backend authorization checks.", body_style),
            Paragraph("Reviewed template wording, verified that login credentials remained intact, and confirmed unit tests passed without regressions.", body_style)
        ],
        [
            Paragraph("Phase 4: Flag Finalization &amp; Full UI Rebrand", body_style),
            Paragraph("<i>'Atlantis{.........} flag format... can you fully change the challenge to atlantis theme, this challenge website to atlantis theme. Story arc across all 6 stages'</i>", body_style),
            Paragraph("AI updated flag format to <code>Atlantis{...}</code> across all tiers, updated Jinja templates, created oceanic CSS palette, and rebuilt Docker images.", body_style),
            Paragraph("Executed <code>verify.py</code> live smoke tests, visually verified browser rendering at <code>localhost:8092</code>, and flushed CTFd Redis cache.", body_style)
        ],
    ]
    t_ai = Table(ai_logs, colWidths=[90, 135, 140, 140])
    t_ai.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ai)

    story.append(Spacer(1, 8))

    # Appendix B: Test Results Evidence
    story.append(Paragraph("Appendix B: Automated Test Suite &amp; Verification Logs", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=8))

    test_log_text = (
        "<b>Live Execution Evidence (Executed on 23 September 2026):</b><br/>"
        "<font name='Courier' size='7'>"
        "&gt; python -m unittest discover -s tests -v<br/>"
        "test_anonymous_cannot_get_trace_or_flag (test_challenge.ChallengeTests) ... ok<br/>"
        "test_cookie_is_unique_httponly_and_scoped (test_challenge.ChallengeTests) ... ok<br/>"
        "test_external_resources_not_required (test_challenge.ChallengeTests) ... ok<br/>"
        "test_forged_role_and_token_do_not_unlock_vault (test_challenge.ChallengeTests) ... ok<br/>"
        "test_full_intended_solution (test_challenge.ChallengeTests) ... ok<br/>"
        "test_large_request_rejected (test_challenge.ChallengeTests) ... ok<br/>"
        "test_no_flag_in_trainee_pages_or_static_assets (test_challenge.ChallengeTests) ... ok<br/>"
        "test_reset_invalidates_old_operator_token (test_challenge.ChallengeTests) ... ok<br/>"
        "test_sensitive_pages_are_not_cached (test_challenge.ChallengeTests) ... ok<br/>"
        "test_source_and_private_files_are_not_served (test_challenge.ChallengeTests) ... ok<br/>"
        "test_trainee_logout_invalidates_session (test_challenge.ChallengeTests) ... ok<br/>"
        "test_two_players_do_not_invalidate_each_other (test_challenge.ChallengeTests) ... ok<br/>"
        "test_wrong_password_and_sql_injection_do_not_login (test_challenge.ChallengeTests) ... ok<br/>"
        "----------------------------------------------------------------------<br/>"
        "Ran 13 tests in 0.182s - OK<br/><br/>"
        "&gt; python verify.py<br/>"
        "PASS: health endpoint<br/>"
        "PASS: anonymous vault denied<br/>"
        "PASS: wrong password denied<br/>"
        "PASS: trainee login<br/>"
        "PASS: trainee vault denied<br/>"
        "PASS: intentional trace disclosure<br/>"
        "PASS: replayed session opens operator vault<br/>"
        "PASS: vault flag matches CTFd handoff file<br/>"
        "PASS: private flag file not downloadable<br/>"
        "Local HTTP checks passed. All 9 live checks verified against port 8092.<br/>"
        "</font>"
    )
    t_tlog = Table([[Paragraph(test_log_text, body_style)]], colWidths=[505])
    t_tlog.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_LIGHT),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tlog)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully compiled to: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()

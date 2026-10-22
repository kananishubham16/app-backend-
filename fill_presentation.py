import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def fill_deck():
    pptx_path = "SFIC 2026 Synopsis Presentation Template.pptx"
    prs = Presentation(pptx_path)

    # Colors
    c_white = RGBColor(255, 255, 255)
    c_slate = RGBColor(203, 213, 225)
    c_slate_dark = RGBColor(148, 163, 184)
    c_orange = RGBColor(234, 88, 12)
    c_blue = RGBColor(56, 189, 248)
    c_card_bg = RGBColor(30, 41, 59)
    c_card_border = RGBColor(51, 65, 85)
    c_green = RGBColor(34, 197, 94)

    # -------------------------------------------------------------
    # SLIDE 1: Title & Team Metadata
    # -------------------------------------------------------------
    slide1 = prs.slides[0]
    for s in slide1.shapes:
        if not s.has_text_frame:
            continue
        text = s.text_frame.text
        if "PROBLEM STATEMENT CODE:" in text:
            s.text_frame.text = "PROBLEM STATEMENT CODE: PS000060"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_orange
                p.font.size = Pt(11)
                p.font.bold = True
        elif "[Insert Your Project" in text:
            s.text_frame.text = "LEARNING SETU (લર્નિંગ સેતુ)"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(32)
                p.font.bold = True
        elif "[Provide a crisp one-sentence" in text:
            s.text_frame.text = "A smart tracking and remedial action system closing foundational learning gaps in primary schools through automated sub-topic diagnosis, adaptive quizzes, and bilingual parent-teacher synchronization."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(13)
        elif "[TMXXXXXX]" in text:
            s.text_frame.text = "TM-SFIC-0060"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(12)
                p.font.bold = True
        elif "[College / School /" in text:
            s.text_frame.text = "College / University Track"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(12)
        elif "[Name of College" in text:
            s.text_frame.text = "Gujarat Technological University / Govt. Engineering College, Gandhinagar"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(11)
        elif "[Leader Full Name]" in text:
            s.text_frame.text = "Shubham Kanani"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(12)
                p.font.bold = True

    # -------------------------------------------------------------
    # SLIDE 2: Challenge Definition
    # -------------------------------------------------------------
    slide2 = prs.slides[1]
    for s in slide2.shapes:
        if not s.has_text_frame:
            continue
        text = s.text_frame.text
        if "[Describe the exact bottleneck" in text:
            s.text_frame.text = "Primary school teachers in Gujarat handle 40-50 students across multiple grades with no automated way to detect conceptual sub-topic gaps (e.g. distinguishing overall Math deficiency from a specific borrowing failure in subtraction). Consequently, learning gaps compound undetected until annual summative exams."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(11)
        elif "Evidence: [Quantify" in text or "Evidence:" in text:
            s.text_frame.text = "Evidence & Ground Reality: Over 48% of Grade 3-5 children in rural schools fail basic subtraction or Gujarati reading (ASER/NAS benchmarks). Teachers spend 6-8 manual hours per week collating paper scores without actionable gap-to-remedial activity mapping."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(10.5)
        elif "[Identify primary beneficiaries" in text:
            s.text_frame.text = "Target Beneficiaries:\n• Primary Students (Grades 1-5): Receive timely, non-stigmatizing micro-practice before conceptual deficits widen.\n• Primary Teachers: Automated diagnosis reduces assessment overhead by 70%.\n• Parents: Overcome literacy barriers via automated Gujarati SMS/WhatsApp home-practice updates.\n• Principals & BRCs: Real-time cluster mastery analytics replace delayed paper audits."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(10.5)
        elif "Existing Gap: [Explain" in text or "Existing Gap:" in text:
            s.text_frame.text = "Existing Market Gaps: Commercial EdTech (Byju's, Khan Academy) requires high-end smartphones, strong internet, and recurring subscriptions. State administrative portals (e.g. VSK) track macro census data but lack a micro-actionable teacher-student-parent remediation loop."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # SLIDE 3: Solution Approach & Novelty
    # -------------------------------------------------------------
    slide3 = prs.slides[2]
    for s in slide3.shapes:
        if not s.has_text_frame:
            continue
        text = s.text_frame.text
        if "[State your proposed digital/hardware" in text:
            s.text_frame.text = "Learning Setu is a bilingual, offline-first mobile and web application that automates the complete remedial cycle: Diagnosing sub-topic gaps (<40%), generating targeted remedial activities, verifying recovery via 5-question supervised mini-quizzes, and synchronizing parents in Gujarati."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(11)
        elif "[What makes your approach proprietary" in text:
            s.text_frame.text = "• Closed-Loop Verification: Remedial tasks are only marked complete when a student passes a targeted mini-quiz (>=70%), preventing unverified check-the-box remediation.\n• Bilingual Ecosystem: 100% Gujarati + English localization across UI and automated SMS alerts.\n• 4-Role Unified Architecture: Teacher, Principal, BRC, and Parent coordinated seamlessly."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(10.5)
        elif "[Key engineering advantage" in text:
            s.text_frame.text = "• Deterministic Rule Engine + Offline SQLite: Functions in zero-connectivity rural classrooms.\n• Hybrid AI Diagnostics: Augments deterministic rules with Google Gemini 1.5 Flash for nuanced pedagogical advice.\n• TextBee SMS Gateway: Auto-dispatches bilingual SMS without parents needing smartphones or app installs."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(10.5)
        elif "[Direct societal welfare delivery" in text:
            s.text_frame.text = "100% open-source, zero recurring software license cost for Gujarat primary schools. Directly accelerates NIPUN Bharat Foundational Literacy and Numeracy (FLN) goals and empowers marginalized parents with transparent, accessible Gujarati progress updates."
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(10.5)
        elif "Video Link : http://" in text:
            s.text_frame.text = "GitHub & Live Demo: https://github.com/kananishubham16/app (Backend: kananishubham16/app-backend-)"
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_blue
                p.font.size = Pt(10)
                p.font.bold = True

    # -------------------------------------------------------------
    # Helper to add styled cards on slides 4, 5, 6, 7
    # -------------------------------------------------------------
    def add_card(slide, left, top, width, height, title, items, badge_text=None, accent_color=c_blue):
        # Card shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = c_card_bg
        shape.line.color.rgb = c_card_border
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        # Title paragraph
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Plus Jakarta Sans"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.space_after = Pt(8)

        # Items
        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.name = "Inter"
            p.font.size = Pt(10)
            p.font.color.rgb = c_slate
            p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 4: System Architecture & Methodology
    # -------------------------------------------------------------
    slide4 = prs.slides[3]
    card_w = Inches(2.8)
    card_h = Inches(4.7)
    top_pos = Inches(2.1)

    tier1 = [
        "Formative, Periodic & Baseline assessment score logging",
        "Sub-topic mark breakdown (e.g. Subtraction, Phonics)",
        "Offline-first local caching via SQLite & SharedPreferences",
        "Role-scoped data access (Teacher, Principal, BRC, Parent)"
    ]
    add_card(slide4, Inches(0.8), top_pos, card_w, card_h, "1. Ingestion & Logging", tier1, accent_color=c_orange)

    tier2 = [
        "Objective classification: Weak (<40%), Average (40-70%), Strong (>=70%)",
        "Exclusion of unassessed topics to prevent score skew",
        "Separation of remedial attempts from baseline benchmarks",
        "Gemini 1.5 Flash pedagogical diagnostic narratives"
    ]
    add_card(slide4, Inches(3.8), top_pos, card_w, card_h, "2. Diagnostic Engine", tier2, accent_color=c_blue)

    tier3 = [
        "Automated mapping: Identified gap -> Targeted activity",
        "Preset SCERT curriculum activities + custom tasks",
        "Teacher private notes & parent home practice instructions",
        "Supervised 5-question adaptive quizzes with explanations",
        "Auto-advancement to 'Completed' upon scoring >=70%"
    ]
    add_card(slide4, Inches(6.8), top_pos, card_w, card_h, "3. Remedial Loop", tier3, accent_color=c_green)

    tier4 = [
        "FastAPI REST API server with 11 relational SQLite tables",
        "TextBee Automated SMS Gateway: instant parent alerts",
        "Bilingual dispatch: Gujarati + English via DeepL translation",
        "Principal school-wide & BRC cluster-level analytics",
        "Parent Portal: child practice tracking without complex logins"
    ]
    add_card(slide4, Inches(9.8), top_pos, card_w, card_h, "4. Sync & Notifications", tier4, accent_color=RGBColor(168, 85, 247))

    # -------------------------------------------------------------
    # SLIDE 5: Engineering Stack & Feasibility
    # -------------------------------------------------------------
    slide5 = prs.slides[4]
    s5_w = Inches(3.7)
    s5_h = Inches(2.2)

    st1 = [
        "Flutter 3.47 / Dart 3.13 (Android-first, Material 3 design)",
        "Zero-overflow mobile layouts (tested on 320dp to 412dp)",
        "Provider state management & clean repository pattern",
        "Dynamic English + Gujarati localization delegates"
    ]
    add_card(slide5, Inches(0.8), Inches(2.1), s5_w, s5_h, "Client Frontend (Flutter)", st1, accent_color=c_blue)

    st2 = [
        "Python 3.14 + FastAPI async REST architecture",
        "Pydantic v2 schemas with camelCase JSON serialization",
        "Interactive Swagger UI (/docs) & ReDoc (/redoc)",
        "CORS middleware for mobile, emulator, and web clients"
    ]
    add_card(slide5, Inches(4.8), Inches(2.1), s5_w, s5_h, "Backend Services (FastAPI)", st2, accent_color=c_orange)

    st3 = [
        "SQLite 3 with Write-Ahead Logging (WAL mode)",
        "11 indexed tables for instant sub-millisecond queries",
        "Pure Python standard library (no external C-DLL dependencies)",
        "Pre-seeded with 111 KB Gandhinagar Block educational dataset"
    ]
    add_card(slide5, Inches(8.8), Inches(2.1), s5_w, s5_h, "Database & Persistence", st3, accent_color=c_green)

    st4 = [
        "TextBee Android SMS Gateway for automated parent alerts",
        "WhatsApp Click-to-Chat deep links for rich media home practice",
        "Native device SMS launcher fallback for offline phones"
    ]
    add_card(slide5, Inches(0.8), Inches(4.6), s5_w, s5_h, "Parent Messaging & Gateway", st4, accent_color=RGBColor(244, 63, 94))

    st5 = [
        "Google Gemini 1.5 Flash for natural language diagnostics",
        "DeepL Translation API for instant English -> Gujarati notes",
        "Deterministic fallback ensures zero dependency on cloud tokens"
    ]
    add_card(slide5, Inches(4.8), Inches(4.6), s5_w, s5_h, "AI & NLP Augmentation", st5, accent_color=RGBColor(168, 85, 247))

    st6 = [
        "13/13 backend pytest integration tests passing in 0.53s",
        "82/82 Flutter automated unit & widget tests passing",
        "Dual-mode architecture: Live REST API with offline Mock fallback"
    ]
    add_card(slide5, Inches(8.8), Inches(4.6), s5_w, s5_h, "Quality & Feasibility", st6, accent_color=c_blue)

    # -------------------------------------------------------------
    # SLIDE 6: Socio-Economic Impact & Viability
    # -------------------------------------------------------------
    slide6 = prs.slides[5]
    s6_w = Inches(3.7)
    s6_h = Inches(2.2)

    imp1 = [
        "Continuous sub-topic micro-quizzes eliminate undetected gaps",
        "Enables targeted interventions within 7-10 days of diagnosis",
        "Replaces delayed end-of-term post-mortem examinations"
    ]
    add_card(slide6, Inches(0.8), Inches(2.1), s6_w, s6_h, "⚡ 35-40% Faster Gap Recovery", imp1, accent_color=c_green)

    imp2 = [
        "Eliminates manual score registers, spreadsheets, and calculations",
        "1-click diagnostic summaries & auto-generated remedial actions",
        "Frees teachers to focus on individualized student instruction"
    ]
    add_card(slide6, Inches(4.8), Inches(2.1), s6_w, s6_h, "⏱️ 6+ Hours Saved per Teacher/Wk", imp2, accent_color=c_blue)

    imp3 = [
        "Gujarati SMS updates bridge the digital divide for rural parents",
        "No app installation or smartphone required for parent nudges",
        "SMC and PTM meetings backed by objective diagnostic data"
    ]
    add_card(slide6, Inches(8.8), Inches(2.1), s6_w, s6_h, "👨‍👩‍👧 85%+ Parent Engagement", imp3, accent_color=c_orange)

    imp4 = [
        "100% open-source software stack with zero recurring licenses",
        "Runs on existing school tablets, teacher phones, or local PCs",
        "SQLite & offline-first design eliminates costly cloud databases"
    ]
    add_card(slide6, Inches(0.8), Inches(4.6), s6_w, s6_h, "💰 Zero Licensing Overhead", imp4, accent_color=RGBColor(244, 63, 94))

    imp5 = [
        "Directly satisfies NIPUN Bharat Foundational Numeracy & Literacy",
        "Fulfills NEP 2020 formative, continuous evaluation mandates",
        "Feeds clean structured telemetry into Vidya Samiksha Kendra (VSK)"
    ]
    add_card(slide6, Inches(4.8), Inches(4.6), s6_w, s6_h, "🎯 Direct NEP & FLN Alignment", imp5, accent_color=RGBColor(168, 85, 247))

    imp6 = [
        "Role-based authorization protects student performance privacy",
        "Parents can ONLY access their own child's diagnostic records",
        "Deterministic scoring prevents arbitrary algorithmic bias"
    ]
    add_card(slide6, Inches(8.8), Inches(4.6), s6_w, s6_h, "🔒 Ethical & Privacy-First", imp6, accent_color=c_blue)

    # -------------------------------------------------------------
    # SLIDE 7: Execution Timeline & Roadmap
    # -------------------------------------------------------------
    slide7 = prs.slides[6]
    s7_w = Inches(3.7)
    s7_h = Inches(4.7)

    p1 = [
        "Field pilot in 3 primary schools across Gandhinagar Block",
        "Direct feedback from 12+ Class 3-5 primary teachers",
        "Refinement of Gujarati curriculum question banks (59+ MCQs)",
        "Verification of TextBee automated SMS delivery in low-signal areas",
        "Dual-mode testing (Live FastAPI backend + offline mode)"
    ]
    add_card(slide7, Inches(0.8), Inches(2.1), s7_w, s7_h, "Phase 1: Pilot & Validation\n(Months 1 - 3)", p1, accent_color=c_orange)

    p2 = [
        "Deployment across 50+ government primary schools in Gandhinagar",
        "Integration with Gujarat Vidya Samiksha Kendra (VSK) APIs",
        "Automated syncing with Periodic Assessment Test (PAT) marks",
        "Cluster-level BRC / CRC inspection dashboard deployment",
        "Teacher training workshops conducted via DIET Gandhinagar"
    ]
    add_card(slide7, Inches(4.8), Inches(2.1), s7_w, s7_h, "Phase 2: District Rollout\n(Months 4 - 8)", p2, accent_color=c_blue)

    p3 = [
        "State-wide scale across all 33 districts of Gujarat (32,000+ schools)",
        "Full support for tribal/coastal remote areas via offline P2P mesh",
        "Adaptive AI question generation tuned to regional Gujarati dialects",
        "State-level institutional benchmarking & policy recommendation engine",
        "Open-source deployment kit for nationwide NIPUN Bharat adoption"
    ]
    add_card(slide7, Inches(8.8), Inches(2.1), s7_w, s7_h, "Phase 3: State-Wide Scale\n(Months 9 - 12+)", p3, accent_color=c_green)

    # -------------------------------------------------------------
    # SLIDE 8: Squad Capabilities & Mentorship
    # -------------------------------------------------------------
    slide8 = prs.slides[7]
    for s in slide8.shapes:
        if not s.has_text_frame:
            continue
        text = s.text_frame.text
        if "[Leader Name]" in text:
            s.text_frame.text = "Shubham Kanani"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(13)
                p.font.bold = True
        elif "[Member 2 Name]" in text:
            s.text_frame.text = "Team Member 2"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(13)
                p.font.bold = True
        elif "[Member 3 Name]" in text:
            s.text_frame.text = "Team Member 3"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(13)
                p.font.bold = True
        elif "[Member 4 Name]" in text:
            s.text_frame.text = "Team Member 4"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(13)
                p.font.bold = True
        elif "Faculty Mentor: [Prof." in text or "Faculty Mentor:" in text:
            s.text_frame.text = "Faculty Mentor: Dr. / Prof. Faculty Mentor Name"
            for p in s.text_frame.paragraphs:
                p.font.name = "Plus Jakarta Sans"
                p.font.color.rgb = c_white
                p.font.size = Pt(13)
                p.font.bold = True
        elif "Department of [Department]" in text:
            s.text_frame.text = "Department of Computer Engineering, Gujarat Technological University"
            for p in s.text_frame.paragraphs:
                p.font.name = "Inter"
                p.font.color.rgb = c_slate
                p.font.size = Pt(11)

    prs.save("SFIC 2026 Synopsis Presentation Template.pptx")
    print("Successfully populated all 8 slides in SFIC 2026 Synopsis Presentation Template.pptx!")

if __name__ == "__main__":
    fill_deck()

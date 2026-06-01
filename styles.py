# ═══════════════════════════════════════════════════════
#  FaceMark  –  Dual-theme stylesheet  (v3.0)
#  Usage:
#    from styles import get_style
#    app.setStyleSheet(get_style("dark"))   # or "light"
# ═══════════════════════════════════════════════════════

_SHARED = """
QMainWindow, QDialog { font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif; font-size: 13px; }
QWidget            { font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif; font-size: 13px; background: transparent; }
"""

# ───────────────────────────────────────────────────────
#  DARK  THEME   (deep navy-black + cyan accent)
# ───────────────────────────────────────────────────────
DARK_STYLE = _SHARED + """

QMainWindow, QDialog { background: #0a0c12; color: #dde3f0; }

/* ── SIDEBAR ── */
#sidebar {
    background-color: #0e1018;
    border-right: 1px solid #1c2133;
    min-width: 228px; max-width: 228px;
}
#logo_label {
    font-size: 17px; font-weight: 800; color: #38bdf8;
    padding: 28px 22px 6px 22px; letter-spacing: 2.5px;
}
#sub_logo {
    font-size: 9px; color: #2e3a52;
    padding: 0 22px 22px 22px; letter-spacing: 4px;
}

/* ── NAV BUTTONS ── */
#nav_btn {
    background: transparent; color: #5a6a85;
    border: none; border-radius: 10px;
    padding: 11px 16px; text-align: left;
    font-size: 13px; font-weight: 500; margin: 2px 10px;
}
#nav_btn:hover { background: #151c2e; color: #c8d4e8; padding-left: 20px; }
#nav_btn:pressed { background: #111828; color: #8fa3c4; padding-left: 18px; }

#nav_btn_active {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0e2a40, stop:1 #0e1a30);
    color: #38bdf8; border: none; border-left: 3px solid #38bdf8;
    border-radius: 10px; padding: 11px 16px 11px 13px;
    text-align: left; font-size: 13px; font-weight: 700; margin: 2px 10px;
}
#nav_btn_active:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #113350, stop:1 #0e2038); color: #67d8ff; }
#nav_btn_active:pressed { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0a1e2e, stop:1 #0a1525); }

/* ── THEME TOGGLE BUTTON (sidebar) ── */
#theme_btn {
    background: #151c2e; color: #5a6a85;
    border: 1px solid #1c2840; border-radius: 20px;
    padding: 7px 18px; font-size: 11px; font-weight: 700;
    margin: 0 14px 4px 14px; letter-spacing: 0.5px;
}
#theme_btn:hover { background: #1a2438; color: #c8d4e8; border-color: #253348; }
#theme_btn:pressed { background: #0e1428; border-color: #38bdf8; color: #38bdf8; }

/* ── CONTENT AREA ── */
#content_area { background: #0a0c12; }

/* ── STAT CARDS ── */
#stat_card {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #12161f, stop:1 #0e1420);
    border: 1px solid #1c2133; border-top-color: #232c42; border-radius: 16px;
}
#stat_card:hover { border-color: #2a3a58; }
#card_title { font-size: 11px; color: #3a4a65; font-weight: 700; letter-spacing: 1.5px; }
#card_value       { font-size: 38px; font-weight: 800; color: #dde3f0; letter-spacing: -1px; }
#card_value_blue  { font-size: 38px; font-weight: 800; color: #38bdf8; letter-spacing: -1px; }
#card_value_green { font-size: 38px; font-weight: 800; color: #34d399; letter-spacing: -1px; }
#card_value_red   { font-size: 38px; font-weight: 800; color: #f87171; letter-spacing: -1px; }

/* ── TYPOGRAPHY ── */
#page_title    { font-size: 22px; font-weight: 700; color: #eaf0fb; letter-spacing: 0.2px; }
#page_subtitle { font-size: 12px; color: #364155; }
#form_label    { font-size: 11px; color: #4a5c7a; font-weight: 700; letter-spacing: 0.8px; }
#section_card  { background: #0e1220; border: 1px solid #1c2133; border-radius: 16px; }

/* ── INPUTS ── */
QLineEdit {
    background: #080b14; border: 1px solid #1a2236; border-top-color: #141c30;
    border-radius: 9px; padding: 10px 14px; color: #dde3f0; font-size: 13px;
    selection-background-color: #1d4a70; selection-color: #e2ecff;
}
QLineEdit:hover  { border-color: #253348; background: #0a0e1a; }
QLineEdit:focus  { border: 1px solid #38bdf8; background: #080d18; color: #eaf4ff; }
QLineEdit:disabled { background: #0a0d18; color: #2a3348; border-color: #131c2e; }

QComboBox {
    background: #080b14; border: 1px solid #1a2236; border-radius: 9px;
    padding: 10px 14px; color: #dde3f0; font-size: 13px;
}
QComboBox:hover  { border-color: #253348; background: #0a0e1a; }
QComboBox:focus  { border: 1px solid #38bdf8; background: #080d18; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox::down-arrow { image: none; }
QComboBox QAbstractItemView {
    background: #0e1220; border: 1px solid #1c2440; border-radius: 10px; padding: 4px;
    selection-background-color: #0e2a40; selection-color: #38bdf8; color: #c8d4e8; outline: none;
}
QComboBox QAbstractItemView::item { min-height: 32px; padding: 6px 12px; border-radius: 6px; }
QComboBox QAbstractItemView::item:hover { background: #151e30; color: #e2f0ff; }

/* ── BUTTONS ── */
#primary_btn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #3ecfff, stop:1 #0ea5e9);
    color: #03080f; border: none; border-bottom: 2px solid #0886be;
    border-radius: 10px; padding: 11px 24px; font-size: 13px; font-weight: 700;
}
#primary_btn:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #57daff, stop:1 #22b8f5); border-bottom-color: #0993d2; }
#primary_btn:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #0993c8, stop:1 #0a7db5); border-bottom-width: 1px; padding-top: 12px; padding-bottom: 10px; }
#primary_btn:disabled { background: #151c2e; color: #2e3d54; border: none; }

#success_btn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #4ade80, stop:1 #16a34a);
    color: #021408; border: none; border-bottom: 2px solid #0f7a38;
    border-radius: 10px; padding: 11px 24px; font-size: 13px; font-weight: 700;
}
#success_btn:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #6aee98, stop:1 #22c55e); border-bottom-color: #15863e; }
#success_btn:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #15813a, stop:1 #0d6030); border-bottom-width: 1px; padding-top: 12px; padding-bottom: 10px; }
#success_btn:disabled { background: #0a1a10; color: #1a3025; border: none; }

#danger_btn {
    background: transparent; color: #f87171;
    border: 1px solid #7f1d1d; border-bottom: 2px solid #991b1b;
    border-radius: 10px; padding: 10px 20px; font-size: 12px; font-weight: 600;
}
#danger_btn:hover   { background: #1f0808; color: #fca5a5; border-color: #b91c1c; border-bottom-color: #dc2626; }
#danger_btn:pressed { background: #140404; border-bottom-width: 1px; padding-top: 11px; padding-bottom: 9px; }

#capture_btn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #a78bfa, stop:1 #7c3aed);
    color: #f5f0ff; border: none; border-bottom: 2px solid #5b21b6;
    border-radius: 10px; padding: 11px 24px; font-size: 13px; font-weight: 700;
}
#capture_btn:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #c4b5fd, stop:1 #8b5cf6); border-bottom-color: #6d28d9; }
#capture_btn:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #5b21b6, stop:1 #4c1d95); border-bottom-width: 1px; padding-top: 12px; padding-bottom: 10px; }
#capture_btn:disabled { background: #1a1228; color: #2e2048; border: none; }

/* ── CAMERA ── */
#camera_label { background: #06080f; border-radius: 12px; color: #2e3a52; font-size: 13px; }

/* ── TABLE ── */
QTableWidget {
    background: #0e1220; border: 1px solid #1c2133; border-radius: 14px;
    gridline-color: transparent; color: #c8d4e8; font-size: 13px;
    selection-background-color: #0f2240; outline: none;
}
QTableWidget::item { padding: 0 12px; border-bottom: 1px solid #141c2e; }
QTableWidget::item:hover    { background: #111928; }
QTableWidget::item:selected { background: #0e2a40; color: #c8e8ff; }
QHeaderView::section {
    background: #0a0e1a; color: #3a4a65; font-size: 10px; font-weight: 700;
    letter-spacing: 1.5px; padding: 12px 14px;
    border: none; border-bottom: 1px solid #1c2133; border-right: 1px solid #131c2e;
}
QHeaderView::section:first  { border-top-left-radius: 14px; }
QHeaderView::section:last   { border-top-right-radius: 14px; border-right: none; }
QHeaderView::section:hover  { background: #0e1424; color: #5a6a85; }

/* ── SCROLLBAR ── */
QScrollBar:vertical { background: #080b14; width: 7px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #1c2840; border-radius: 4px; min-height: 28px; }
QScrollBar::handle:vertical:hover   { background: #253550; }
QScrollBar::handle:vertical:pressed { background: #38bdf8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #080b14; height: 7px; border-radius: 4px; }
QScrollBar::handle:horizontal { background: #1c2840; border-radius: 4px; min-width: 28px; }
QScrollBar::handle:horizontal:hover { background: #253550; }

/* ── FACE STATUS ── */
#face_status_ok      { background: #031a0e; color: #34d399; border: 1px solid #064a28; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 12px; }
#face_status_error   { background: #1c0808; color: #f87171; border: 1px solid #4a1010; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 12px; }
#face_status_neutral { background: #0c1020; color: #3a4a65; border: 1px solid #1a2236; border-radius: 8px; padding: 8px 16px; font-weight: 600; font-size: 12px; }

/* ── BADGE ── */
#badge_present { background: #042312; color: #34d399; border: 1px solid #064a28; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 700; }
#badge_absent  { background: #1c0808; color: #f87171; border: 1px solid #4a1010; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 700; }

/* ── DIALOGS ── */
QMessageBox { background: #0e1220; color: #dde3f0; border: 1px solid #1c2133; border-radius: 12px; }
QMessageBox QLabel { color: #c8d4e8; background: transparent; }
QMessageBox QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #1c2e48, stop:1 #141e32);
    color: #c8d4e8; border: 1px solid #1e2e48; border-bottom: 2px solid #0f1a2e;
    border-radius: 8px; padding: 7px 22px; font-size: 12px; font-weight: 600; min-width: 80px;
}
QMessageBox QPushButton:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #243654, stop:1 #192438); color: #eaf0ff; }
QMessageBox QPushButton:pressed { background: #0e1828; border-bottom-width: 1px; padding-top: 8px; padding-bottom: 6px; }
QMessageBox QPushButton:default {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #3ecfff, stop:1 #0ea5e9);
    color: #02080f; border: none; border-bottom: 2px solid #0886be;
}
QMessageBox QPushButton:default:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #57daff, stop:1 #22b8f5); }
QMessageBox QPushButton:default:pressed { background: #0993c8; border-bottom-width: 1px; }

QToolTip { background: #0e1628; color: #c8d4e8; border: 1px solid #1e2e48; border-radius: 7px; padding: 6px 10px; font-size: 12px; }

QGroupBox { color: #3a4a65; font-size: 11px; font-weight: 700; letter-spacing: 1.2px; border: 1px solid #1c2133; border-radius: 13px; margin-top: 18px; padding-top: 14px; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 8px; color: #3a4a65; background: #0a0c12; }

#divider { background: #1c2133; max-height: 1px; min-height: 1px; }
"""


# ───────────────────────────────────────────────────────
#  LIGHT  THEME   (warm white + indigo accent)
# ───────────────────────────────────────────────────────
LIGHT_STYLE = _SHARED + """

QMainWindow, QDialog { background: #f4f6fb; color: #1e293b; }
QWidget { color: #1e293b; }

/* ── SIDEBAR ── */
#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
    min-width: 228px; max-width: 228px;
}
#logo_label {
    font-size: 17px; font-weight: 800; color: #4f46e5;
    padding: 28px 22px 6px 22px; letter-spacing: 2.5px;
}
#sub_logo {
    font-size: 9px; color: #94a3b8;
    padding: 0 22px 22px 22px; letter-spacing: 4px;
}

/* ── NAV BUTTONS ── */
#nav_btn {
    background: transparent; color: #94a3b8;
    border: none; border-radius: 10px;
    padding: 11px 16px; text-align: left;
    font-size: 13px; font-weight: 500; margin: 2px 10px;
}
#nav_btn:hover   { background: #f1f5f9; color: #334155; padding-left: 20px; }
#nav_btn:pressed { background: #e8eef6; color: #475569; padding-left: 18px; }

#nav_btn_active {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #ede9fe, stop:1 #f0f4ff);
    color: #4f46e5; border: none; border-left: 3px solid #4f46e5;
    border-radius: 10px; padding: 11px 16px 11px 13px;
    text-align: left; font-size: 13px; font-weight: 700; margin: 2px 10px;
}
#nav_btn_active:hover   { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #e0d9fd, stop:1 #e8eeff); color: #3730a3; }
#nav_btn_active:pressed { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #c7d2fe, stop:1 #dbeafe); }

/* ── THEME TOGGLE ── */
#theme_btn {
    background: #f1f5f9; color: #64748b;
    border: 1px solid #e2e8f0; border-radius: 20px;
    padding: 7px 18px; font-size: 11px; font-weight: 700;
    margin: 0 14px 4px 14px; letter-spacing: 0.5px;
}
#theme_btn:hover   { background: #e2e8f0; color: #334155; border-color: #cbd5e1; }
#theme_btn:pressed { background: #dbeafe; border-color: #4f46e5; color: #4f46e5; }

/* ── CONTENT AREA ── */
#content_area { background: #f4f6fb; }

/* ── STAT CARDS ── */
#stat_card {
    background: #ffffff;
    border: 1px solid #e2e8f0; border-top-color: #f8fafc; border-radius: 16px;
}
#stat_card:hover { border-color: #c7d2fe; }
#card_title { font-size: 11px; color: #94a3b8; font-weight: 700; letter-spacing: 1.5px; }
#card_value       { font-size: 38px; font-weight: 800; color: #1e293b; letter-spacing: -1px; }
#card_value_blue  { font-size: 38px; font-weight: 800; color: #4f46e5; letter-spacing: -1px; }
#card_value_green { font-size: 38px; font-weight: 800; color: #16a34a; letter-spacing: -1px; }
#card_value_red   { font-size: 38px; font-weight: 800; color: #dc2626; letter-spacing: -1px; }

/* ── TYPOGRAPHY ── */
#page_title    { font-size: 22px; font-weight: 700; color: #0f172a; letter-spacing: 0.2px; }
#page_subtitle { font-size: 12px; color: #94a3b8; }
#form_label    { font-size: 11px; color: #64748b; font-weight: 700; letter-spacing: 0.8px; }
#section_card  { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; }

/* ── INPUTS ── */
QLineEdit {
    background: #ffffff; border: 1px solid #e2e8f0; border-top-color: #cbd5e1;
    border-radius: 9px; padding: 10px 14px; color: #1e293b; font-size: 13px;
    selection-background-color: #c7d2fe; selection-color: #1e1b4b;
}
QLineEdit:hover  { border-color: #a5b4fc; background: #fafbff; }
QLineEdit:focus  { border: 1px solid #4f46e5; background: #ffffff; color: #0f172a; }
QLineEdit:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }
QLineEdit::placeholder { color: #cbd5e1; }

QComboBox {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 9px;
    padding: 10px 14px; color: #1e293b; font-size: 13px;
}
QComboBox:hover  { border-color: #a5b4fc; background: #fafbff; }
QComboBox:focus  { border: 1px solid #4f46e5; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox::down-arrow { image: none; }
QComboBox QAbstractItemView {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 4px;
    selection-background-color: #ede9fe; selection-color: #4f46e5; color: #334155; outline: none;
}
QComboBox QAbstractItemView::item { min-height: 32px; padding: 6px 12px; border-radius: 6px; }
QComboBox QAbstractItemView::item:hover { background: #f1f5f9; color: #1e293b; }

/* ── BUTTONS ── */
#primary_btn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #818cf8, stop:1 #4f46e5);
    color: #ffffff; border: none; border-bottom: 2px solid #3730a3;
    border-radius: 10px; padding: 11px 24px; font-size: 13px; font-weight: 700;
}
#primary_btn:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #a5b4fc, stop:1 #6366f1); border-bottom-color: #4338ca; }
#primary_btn:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #4338ca, stop:1 #3730a3); border-bottom-width: 1px; padding-top: 12px; padding-bottom: 10px; }
#primary_btn:disabled { background: #e2e8f0; color: #94a3b8; border: none; }

#success_btn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #4ade80, stop:1 #16a34a);
    color: #052e16; border: none; border-bottom: 2px solid #15803d;
    border-radius: 10px; padding: 11px 24px; font-size: 13px; font-weight: 700;
}
#success_btn:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #86efac, stop:1 #22c55e); border-bottom-color: #16a34a; }
#success_btn:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #15803d, stop:1 #166534); border-bottom-width: 1px; padding-top: 12px; padding-bottom: 10px; }
#success_btn:disabled { background: #dcfce7; color: #86efac; border: none; }

#danger_btn {
    background: transparent; color: #dc2626;
    border: 1px solid #fca5a5; border-bottom: 2px solid #f87171;
    border-radius: 10px; padding: 10px 20px; font-size: 12px; font-weight: 600;
}
#danger_btn:hover   { background: #fff1f2; color: #b91c1c; border-color: #f87171; border-bottom-color: #dc2626; }
#danger_btn:pressed { background: #ffe4e6; border-bottom-width: 1px; padding-top: 11px; padding-bottom: 9px; }

#capture_btn {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #c084fc, stop:1 #9333ea);
    color: #ffffff; border: none; border-bottom: 2px solid #7e22ce;
    border-radius: 10px; padding: 11px 24px; font-size: 13px; font-weight: 700;
}
#capture_btn:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #d8b4fe, stop:1 #a855f7); border-bottom-color: #9333ea; }
#capture_btn:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #7e22ce, stop:1 #6b21a8); border-bottom-width: 1px; padding-top: 12px; padding-bottom: 10px; }
#capture_btn:disabled { background: #f3e8ff; color: #d8b4fe; border: none; }

/* ── CAMERA ── */
#camera_label { background: #f8fafc; border-radius: 12px; color: #94a3b8; font-size: 13px; }

/* ── TABLE ── */
QTableWidget {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
    gridline-color: transparent; color: #334155; font-size: 13px;
    selection-background-color: #ede9fe; outline: none;
}
QTableWidget::item { padding: 0 12px; border-bottom: 1px solid #f1f5f9; }
QTableWidget::item:hover    { background: #f8f9ff; }
QTableWidget::item:selected { background: #ede9fe; color: #3730a3; }
QHeaderView::section {
    background: #f8fafc; color: #94a3b8; font-size: 10px; font-weight: 700;
    letter-spacing: 1.5px; padding: 12px 14px;
    border: none; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #f1f5f9;
}
QHeaderView::section:first  { border-top-left-radius: 14px; }
QHeaderView::section:last   { border-top-right-radius: 14px; border-right: none; }
QHeaderView::section:hover  { background: #f1f5f9; color: #64748b; }

/* ── SCROLLBAR ── */
QScrollBar:vertical { background: #f8fafc; width: 7px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 4px; min-height: 28px; }
QScrollBar::handle:vertical:hover   { background: #94a3b8; }
QScrollBar::handle:vertical:pressed { background: #4f46e5; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #f8fafc; height: 7px; border-radius: 4px; }
QScrollBar::handle:horizontal { background: #cbd5e1; border-radius: 4px; min-width: 28px; }
QScrollBar::handle:horizontal:hover { background: #94a3b8; }

/* ── FACE STATUS ── */
#face_status_ok      { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 12px; }
#face_status_error   { background: #fff1f2; color: #dc2626; border: 1px solid #fecaca; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 12px; }
#face_status_neutral { background: #f8fafc; color: #94a3b8; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 16px; font-weight: 600; font-size: 12px; }

/* ── BADGE ── */
#badge_present { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 700; }
#badge_absent  { background: #fff1f2; color: #dc2626; border: 1px solid #fecaca; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 700; }

/* ── DIALOGS ── */
QMessageBox { background: #ffffff; color: #1e293b; border: 1px solid #e2e8f0; border-radius: 12px; }
QMessageBox QLabel { color: #334155; background: transparent; }
QMessageBox QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #f8fafc, stop:1 #f1f5f9);
    color: #334155; border: 1px solid #e2e8f0; border-bottom: 2px solid #cbd5e1;
    border-radius: 8px; padding: 7px 22px; font-size: 12px; font-weight: 600; min-width: 80px;
}
QMessageBox QPushButton:hover   { background: #e2e8f0; color: #1e293b; border-color: #cbd5e1; }
QMessageBox QPushButton:pressed { background: #dbeafe; border-bottom-width: 1px; padding-top: 8px; }
QMessageBox QPushButton:default {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #818cf8, stop:1 #4f46e5);
    color: #ffffff; border: none; border-bottom: 2px solid #3730a3;
}
QMessageBox QPushButton:default:hover   { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #a5b4fc, stop:1 #6366f1); }
QMessageBox QPushButton:default:pressed { background: #4338ca; border-bottom-width: 1px; }

QToolTip { background: #ffffff; color: #334155; border: 1px solid #e2e8f0; border-radius: 7px; padding: 6px 10px; font-size: 12px; }

QGroupBox { color: #94a3b8; font-size: 11px; font-weight: 700; letter-spacing: 1.2px; border: 1px solid #e2e8f0; border-radius: 13px; margin-top: 18px; padding-top: 14px; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 8px; color: #94a3b8; background: #f4f6fb; }

#divider { background: #e2e8f0; max-height: 1px; min-height: 1px; }
"""


# ── Convenience getter ──────────────────────────────────
def get_style(theme: str = "dark") -> str:
    """Return stylesheet for the given theme ('dark' or 'light')."""
    return DARK_STYLE if theme == "dark" else LIGHT_STYLE


# Legacy compat – old code that does `from styles import MAIN_STYLE` still works
MAIN_STYLE = DARK_STYLE
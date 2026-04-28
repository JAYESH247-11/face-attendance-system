# Updated styles.py
MAIN_STYLE = """
/* Global Smoothness */
QMainWindow, QDialog, QWidget {
    background-color: #0b0d11;
    color: #f1f5f9;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* SIDEBAR: Sleeker and more integrated */
#sidebar {
    background-color: #11141d;
    border-right: 1px solid #1e293b;
    min-width: 240px;
    max-width: 240px;
}

#logo_label {
    font-size: 22px;
    font-weight: 800;
    color: #38bdf8;
    padding: 30px 24px 4px 24px;
    letter-spacing: -0.5px;
}

#sub_logo {
    font-size: 10px;
    color: #64748b;
    padding: 0px 24px 30px 24px;
    letter-spacing: 2px;
    font-weight: 600;
}

/* NAV BUTTONS: Modern pill shape and transitions */
#nav_btn {
    background: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 12px;
    padding: 14px 20px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
    margin: 4px 14px;
}

#nav_btn:hover {
    background-color: #1e293b;
    color: #f8fafc;
}

#nav_btn_active {
    background-color: #0ea5e9;
    color: #ffffff;
    border-radius: 12px;
    padding: 14px 20px;
    font-weight: 600;
    margin: 4px 14px;
}

/* CARDS: Added subtle borders and depth */
#section_card, #stat_card {
    background-color: #11141d;
    border: 1px solid #1e293b;
    border-radius: 20px;
}

#stat_card:hover {
    border-color: #38bdf8;
}

#card_title {
    font-size: 11px;
    color: #94a3b8;
    font-weight: 700;
    letter-spacing: 0.05em;
}

#card_value_blue { font-size: 32px; font-weight: 800; color: #38bdf8; }
#card_value_green { font-size: 32px; font-weight: 800; color: #10b981; }
#card_value_red { font-size: 32px; font-weight: 800; color: #ef4444; }

/* INPUTS: Softer focus effects */
QLineEdit, QComboBox {
    background-color: #1a1f2e;
    border: 2px solid #1e293b;
    border-radius: 12px;
    padding: 12px 16px;
    color: #f1f5f9;
}

QLineEdit:focus {
    border: 2px solid #38bdf8;
    background-color: #1e293b;
}

/* ACTION BUTTONS: High-contrast primary actions */
#primary_btn, #success_btn, #capture_btn {
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    font-size: 13px;
}

#primary_btn { background-color: #0ea5e9; color: white; }
#primary_btn:hover { background-color: #0284c7; }

#success_btn { background-color: #10b981; color: white; }
#success_btn:hover { background-color: #059669; }

#danger_btn {
    color: #f87171;
    border: 2px solid #f87171;
    border-radius: 12px;
    background: transparent;
}
#danger_btn:hover { background-color: #ef444415; }

/* TABLE: Clean and minimal */
QTableWidget {
    background-color: transparent;
    border: none;
    alternate-background-color: #11141d;
}

QHeaderView::section {
    background-color: #0b0d11;
    color: #64748b;
    font-weight: 700;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #1e293b;
}

QTableWidget::item {
    border-bottom: 1px solid #1e293b;
    padding: 12px;
}

/* --- QMessageBox: Simple & Professional --- */
QMessageBox {
    background-color: #11141d; /* કાર્ડ જેવો ડાર્ક કલર */
    border: 1px solid #1e293b;
    border-radius: 12px;
}

QMessageBox QLabel {
    color: #f1f5f9;
    font-size: 14px;
    padding: 10px;
}

QMessageBox QPushButton {
    background-color: #0ea5e9;
    color: white;
    border-radius: 8px;
    padding: 6px 20px;
    font-weight: 600;
    min-width: 70px;
}

QMessageBox QPushButton:hover {
    background-color: #0284c7;
}

QMessageBox QPushButton:pressed {
    background-color: #0369a1;
}
"""
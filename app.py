import random
import re
import os

import streamlit as st
import pandas as pd
from auth import Auth

from bank import Bank
from account import SavingAccount
from statement import build_statement_pdf


st.set_page_config(
    page_title="State Bank of India",
    page_icon="$",
    layout="wide",
    initial_sidebar_state="expanded",
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def add_login_styles():
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    linear-gradient(120deg, rgba(5, 40, 95, 0.92), rgba(11, 78, 162, 0.76)),
                    url("https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=1500&q=80");
                background-size: cover;
                background-position: center;
            }

            .main .block-container {
                max-width: 480px;
                padding-top: 8vh;
            }

            .login-shell {
                border-radius: 8px;
                padding: 1.4rem 1.45rem 1.2rem;
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.5);
                box-shadow: 0 24px 70px rgba(0, 0, 0, 0.26);
            }

            .login-badge {
                width: 48px;
                height: 48px;
                display: grid;
                place-items: center;
                border-radius: 50%;
                color: #ffffff;
                background: #0b4ea2;
                font-weight: 900;
                margin-bottom: 0.9rem;
            }

            .login-shell h1 {
                color: #142033;
                margin: 0;
                font-size: 1.65rem;
                line-height: 1.2;
            }

            .login-shell p {
                color: #667085;
                margin: 0.45rem 0 1.1rem;
            }

            [data-testid="stTextInput"] label {
                color: #142033;
                font-weight: 700;
            }

            div.stButton > button {
                width: 100%;
                min-height: 2.85rem;
                border-radius: 8px;
                border: 1px solid #0b4ea2;
                background: #0b4ea2;
                color: white;
                font-weight: 800;
                box-shadow: 0 12px 28px rgba(11, 78, 162, 0.28);
            }

            div.stButton > button:hover {
                border-color: #062f6f;
                background: #062f6f;
                color: #ffffff;
            }

            .login-note {
                margin-top: 1rem;
                padding: 0.85rem;
                border-radius: 8px;
                background: #eef5fb;
                color: #36516d;
                font-size: 0.9rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


if not st.session_state.logged_in:
    add_login_styles()
    st.markdown(
        """
        <div class="login-shell">
            <div class="login-badge">SBI</div>
            <h1>State Bank of India</h1>
            <p>Secure admin access for the banking dashboard.</p>
        """,
        unsafe_allow_html=True,
    )

    username = st.text_input("Enter username").strip()
    password = st.text_input("Enter password", type="password")


    if st.button("Login"):
        if Auth.login(username, password):
            st.session_state.logged_in = True
            st.success("Login Successful")

            st.rerun()

        else:
            st.error("Invalid username or password")

    st.markdown(
        '<div class="login-note">Use your admin credentials to manage accounts, KYC, loans, fixed deposits, and statements.</div></div>',
        unsafe_allow_html=True,
    )

    st.stop()

bank = Bank()


def money(value):
    return f"Rs. {value:,.0f}"


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_photo(uploaded_file, account_no):
    if not uploaded_file:
        return ""
    extension = os.path.splitext(uploaded_file.name)[1].lower() or ".jpg"
    file_path = os.path.join(UPLOAD_DIR, f"{account_no}{extension}")
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path


def add_styles():
    st.markdown(
        """
        <style>
            :root {
                --ink: #142033;
                --muted: #667085;
                --line: #d8e4ee;
                --panel: rgba(255, 255, 255, 0.94);
                --blue: #0b4ea2;
                --deep-blue: #062f6f;
                --teal: #0f9f9a;
                --green: #22a06b;
                --gold: #f2b84b;
                --red: #d94f62;
            }

            .stApp {
                background:
                    radial-gradient(circle at 14% 0%, rgba(11, 78, 162, 0.16), transparent 28rem),
                    radial-gradient(circle at 88% 8%, rgba(15, 159, 154, 0.12), transparent 24rem),
                    linear-gradient(135deg, #f8fbff 0%, #eef5fb 48%, #ffffff 100%);
                color: var(--ink);
            }

            .main .block-container {
                max-width: 1180px;
                padding-top: 2.1rem;
                padding-bottom: 3rem;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #05285f 0%, #0b4ea2 58%, #063979 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }

            [data-testid="stSidebar"] * {
                color: #f3f8ff;
            }

            h1, h2, h3, p {
                letter-spacing: 0;
            }

            .brand {
                padding: 0.35rem 0 1.25rem;
            }

            .brand-badge {
                width: 42px;
                height: 42px;
                border-radius: 50%;
                display: grid;
                place-items: center;
                margin-bottom: 0.75rem;
                color: #0b4ea2;
                background: #ffffff;
                font-weight: 900;
                box-shadow: 0 12px 26px rgba(0, 0, 0, 0.18);
            }

            .brand h2 {
                color: #ffffff;
                margin: 0;
                font-size: 1.2rem;
                line-height: 1.25;
            }

            .brand p {
                color: rgba(255, 255, 255, 0.72);
                margin: 0.25rem 0 0;
                font-size: 0.9rem;
            }

            .hero {
                position: relative;
                overflow: hidden;
                min-height: 340px;
                border-radius: 8px;
                border: 1px solid rgba(11, 78, 162, 0.16);
                padding: 2.2rem;
                background:
                    linear-gradient(115deg, rgba(5, 40, 95, 0.96), rgba(11, 78, 162, 0.84) 58%, rgba(15, 159, 154, 0.68)),
                    url("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1500&q=80");
                background-size: cover;
                background-position: center;
                box-shadow: 0 26px 58px rgba(6, 47, 111, 0.18);
            }

            .hero-kicker {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                margin-bottom: 0.85rem;
                padding: 0.4rem 0.65rem;
                border-radius: 999px;
                color: #ffffff;
                background: rgba(255, 255, 255, 0.14);
                border: 1px solid rgba(255, 255, 255, 0.24);
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
            }

            .hero h1 {
                color: #ffffff;
                font-size: clamp(2.4rem, 5vw, 4.7rem);
                line-height: 0.98;
                margin: 0 0 1rem;
                max-width: 760px;
            }

            .hero p {
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.05rem;
                line-height: 1.65;
                max-width: 610px;
                margin: 0;
            }

            .hero-strip {
                position: absolute;
                left: 2.2rem;
                right: 2.2rem;
                bottom: 1.4rem;
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
            }

            .strip-item {
                border-radius: 8px;
                padding: 0.85rem 1rem;
                background: rgba(255, 255, 255, 0.14);
                border: 1px solid rgba(255, 255, 255, 0.22);
                backdrop-filter: blur(10px);
            }

            .strip-item span {
                display: block;
                color: rgba(255, 255, 255, 0.72);
                font-size: 0.78rem;
                text-transform: uppercase;
            }

            .strip-item strong {
                color: #ffffff;
                font-size: 1rem;
            }

            .metric-card, .panel, .account-card {
                border-radius: 8px;
                border: 1px solid var(--line);
                background: var(--panel);
                box-shadow: 0 14px 38px rgba(21, 32, 51, 0.08);
            }

            .metric-card {
                min-height: 132px;
                padding: 1.2rem;
                position: relative;
                overflow: hidden;
            }

            .metric-card::after {
                content: "";
                position: absolute;
                right: -34px;
                top: -34px;
                width: 92px;
                height: 92px;
                border-radius: 50%;
                background: rgba(11, 78, 162, 0.08);
            }

            .metric-card span {
                display: block;
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 700;
                text-transform: uppercase;
            }

            .metric-card strong {
                display: block;
                color: var(--ink);
                font-size: 2rem;
                line-height: 1.15;
                margin-top: 0.42rem;
            }

            .metric-card small {
                display: block;
                color: var(--blue);
                margin-top: 0.55rem;
                font-weight: 700;
            }

            .action-grid {
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 0.85rem;
                margin-top: 1rem;
            }

            .action-tile {
                min-height: 96px;
                border-radius: 8px;
                padding: 1rem;
                background: #ffffff;
                border: 1px solid var(--line);
                box-shadow: 0 12px 30px rgba(21, 32, 51, 0.06);
            }

            .action-tile span {
                display: block;
                color: var(--blue);
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
            }

            .action-tile strong {
                display: block;
                margin-top: 0.45rem;
                color: var(--ink);
                font-size: 1.02rem;
            }

            .status-pill {
                display: inline-flex;
                align-items: center;
                border-radius: 999px;
                padding: 0.35rem 0.65rem;
                background: #eaf7ef;
                color: #146c43;
                font-weight: 800;
                font-size: 0.82rem;
            }

            .module-card {
                border-radius: 8px;
                padding: 1rem;
                border: 1px solid var(--line);
                background: #ffffff;
                box-shadow: 0 12px 30px rgba(21, 32, 51, 0.06);
                margin-bottom: 0.8rem;
            }

            .panel {
                padding: 1.25rem;
                margin-top: 1.1rem;
            }

            .panel-title {
                margin: 0;
                color: var(--ink);
                font-size: 1.25rem;
                font-weight: 800;
            }

            .panel-copy {
                margin: 0.25rem 0 0;
                color: var(--muted);
            }

            .account-card {
                padding: 1rem 1.1rem;
                margin-bottom: 0.85rem;
            }

            .account-card span {
                color: var(--muted);
                font-size: 0.86rem;
            }

            .account-card strong {
                display: block;
                color: var(--ink);
                margin: 0.25rem 0;
                font-size: 1.13rem;
            }

            div.stButton > button {
                width: 100%;
                min-height: 2.8rem;
                border-radius: 8px;
                border: 1px solid var(--blue);
                background: var(--blue);
                color: white;
                font-weight: 800;
                box-shadow: 0 10px 24px rgba(11, 78, 162, 0.22);
            }

            div.stButton > button:hover {
                border-color: var(--deep-blue);
                background: var(--deep-blue);
                color: #ffffff;
            }

            .cash-stage {
                position: relative;
                overflow: hidden;
                min-height: 285px;
                border-radius: 8px;
                border: 1px solid rgba(13, 148, 136, 0.28);
                background:
                    radial-gradient(circle at 50% 34%, rgba(217, 154, 43, 0.16), transparent 10rem),
                    linear-gradient(135deg, #effff9, #ffffff 58%, #fff7e6);
                box-shadow: 0 20px 45px rgba(21, 32, 51, 0.1);
                margin: 1.1rem 0 1.2rem;
            }

            .machine {
                position: absolute;
                left: 50%;
                top: 47%;
                width: 172px;
                height: 132px;
                transform: translate(-50%, -50%);
                border-radius: 8px;
                background: linear-gradient(160deg, #173a5e, #0d9488);
                box-shadow: 0 20px 38px rgba(21, 32, 51, 0.25);
                z-index: 4;
            }

            .machine::before {
                content: "";
                position: absolute;
                left: 28px;
                top: 25px;
                width: 116px;
                height: 20px;
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.25);
            }

            .machine::after {
                content: "";
                position: absolute;
                left: 35px;
                bottom: 31px;
                width: 102px;
                height: 12px;
                border-radius: 999px;
                background: #f8d46a;
                box-shadow: inset 0 0 0 2px rgba(21, 32, 51, 0.1);
            }

            .bill {
                position: absolute;
                left: 50%;
                top: 47%;
                width: 82px;
                height: 39px;
                border-radius: 6px;
                border: 1px solid rgba(21, 32, 51, 0.16);
                background:
                    radial-gradient(circle at 50% 50%, rgba(255,255,255,0.6) 0 15%, transparent 16%),
                    linear-gradient(135deg, #d8ffe8, #55c987);
                color: #0b6b49;
                display: grid;
                place-items: center;
                font-weight: 900;
                box-shadow: 0 9px 18px rgba(21, 32, 51, 0.13);
                opacity: 0;
                z-index: 3;
            }

            .bill::after {
                content: "Rs";
                font-size: 0.85rem;
            }

            .deposit .bill {
                animation: cashDeposit 1.35s ease-in-out forwards;
            }

            .withdraw .bill {
                animation: cashWithdraw 1.35s ease-in-out forwards;
            }

            .bill:nth-child(2) { animation-delay: 0.03s; }
            .bill:nth-child(3) { animation-delay: 0.16s; }
            .bill:nth-child(4) { animation-delay: 0.29s; }
            .bill:nth-child(5) { animation-delay: 0.42s; }
            .bill:nth-child(6) { animation-delay: 0.55s; }
            .bill:nth-child(7) { animation-delay: 0.68s; }

            .success-pop {
                position: absolute;
                left: 50%;
                bottom: 1.2rem;
                min-width: min(360px, calc(100% - 2rem));
                transform: translateX(-50%) scale(0.84);
                border-radius: 8px;
                padding: 0.9rem 1.1rem;
                text-align: center;
                background: rgba(255, 255, 255, 0.94);
                border: 1px solid rgba(13, 148, 136, 0.25);
                color: #083f36;
                box-shadow: 0 16px 35px rgba(21, 32, 51, 0.13);
                opacity: 0;
                z-index: 6;
                animation: popSuccess 0.55s cubic-bezier(.17,.67,.22,1.35) 0.95s forwards;
            }

            .success-pop strong {
                display: block;
                font-size: 1.05rem;
            }

            .success-pop span {
                display: block;
                color: var(--muted);
                margin-top: 0.2rem;
            }

            .withdraw .success-pop {
                border-color: rgba(217, 79, 98, 0.23);
                color: #742938;
            }

            .spark {
                position: absolute;
                left: 50%;
                top: 47%;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                transform: translate(-50%, -50%);
                opacity: 0;
                z-index: 2;
                box-shadow:
                    0 -92px 0 var(--gold),
                    68px -68px 0 var(--teal),
                    92px 0 0 var(--green),
                    68px 68px 0 var(--red),
                    0 92px 0 var(--gold),
                    -68px 68px 0 var(--teal),
                    -92px 0 0 var(--green),
                    -68px -68px 0 var(--red);
                animation: sparkPop 0.72s ease-out 0.82s forwards;
            }

            @keyframes cashDeposit {
                0% {
                    transform: translate(var(--from-x), var(--from-y)) rotate(var(--rot)) scale(1);
                    opacity: 0;
                }
                20% {
                    opacity: 1;
                }
                66% {
                    transform: translate(calc(var(--from-x) * 0.2), -20px) rotate(0deg) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translate(-41px, 22px) rotate(0deg) scale(0.34);
                    opacity: 0;
                }
            }

            @keyframes cashWithdraw {
                0% {
                    transform: translate(-41px, 20px) rotate(0deg) scale(0.32);
                    opacity: 0;
                }
                25% {
                    opacity: 1;
                }
                100% {
                    transform: translate(var(--to-x), var(--to-y)) rotate(var(--rot)) scale(1);
                    opacity: 1;
                }
            }

            @keyframes popSuccess {
                0% {
                    opacity: 0;
                    transform: translateX(-50%) scale(0.84);
                }
                100% {
                    opacity: 1;
                    transform: translateX(-50%) scale(1);
                }
            }

            @keyframes sparkPop {
                0% {
                    opacity: 0;
                    transform: translate(-50%, -50%) scale(0.25);
                }
                38% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                    transform: translate(-50%, -50%) scale(1.65);
                }
            }

            @media (max-width: 760px) {
                .hero {
                    min-height: 430px;
                    padding: 1.3rem;
                }

                .hero-strip {
                    left: 1.3rem;
                    right: 1.3rem;
                    grid-template-columns: 1fr;
                }

                .metric-card strong {
                    font-size: 1.45rem;
                }

                .action-grid {
                    grid-template-columns: 1fr;
                }

                .cash-stage {
                    min-height: 330px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def cash_animation(kind, amount, name):
    action = "Deposit successful" if kind == "deposit" else "Withdrawal successful"
    detail = (
        f"{money(amount)} added to {name}'s account."
        if kind == "deposit"
        else f"{money(amount)} paid out from {name}'s account."
    )
    positions = [
        ("-238px", "105px", "-238px", "-78px", "-18deg"),
        ("-148px", "132px", "-160px", "-112px", "14deg"),
        ("-48px", "150px", "-64px", "-138px", "-7deg"),
        ("58px", "138px", "64px", "-128px", "9deg"),
        ("154px", "112px", "158px", "-96px", "-14deg"),
        ("232px", "142px", "232px", "-58px", "19deg"),
    ]

    bills = "".join(
        (
            '<div class="bill" '
            f'style="--from-x:{from_x}; --from-y:{from_y}; '
            f'--to-x:{to_x}; --to-y:{to_y}; --rot:{rot};"></div>'
        )
        for from_x, from_y, to_x, to_y, rot in positions
    )

    st.markdown(
        f"""
        <div class="cash-stage {kind}">
            <div class="spark"></div>
            {bills}
            <div class="machine"></div>
            <div class="success-pop">
                <strong>{action}</strong>
                <span>{detail}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home():
    total_accounts = len(bank.accounts)
    total_balance = sum(account.get_balance() for account in bank.accounts)
    highest_balance = max([account.get_balance() for account in bank.accounts], default=0)

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Branch dashboard</div>
            <h1>State Bank of India</h1>
            <p>Manage customers, deposits, withdrawals, transfers, and balances from a modern daily banking dashboard.</p>
            <div class="hero-strip">
                <div class="strip-item"><span>Records</span><strong>Local account data</strong></div>
                <div class="strip-item"><span>Cash Desk</span><strong>Deposit and withdraw</strong></div>
                <div class="strip-item"><span>Service</span><strong>Fast customer lookup</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-card"><span>Total Accounts</span><strong>{total_accounts}</strong><small>Saved customers</small></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><span>Total Balance</span><strong>{money(total_balance)}</strong><small>Across all accounts</small></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-card"><span>Highest Balance</span><strong>{money(highest_balance)}</strong><small>Top account value</small></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="panel">
            <p class="panel-title">Quick actions</p>
            <p class="panel-copy">Common branch tasks are available from the sidebar.</p>
            <div class="action-grid">
                <div class="action-tile"><span>Open</span><strong>Create Account</strong></div>
                <div class="action-tile"><span>Cash In</span><strong>Deposit Money</strong></div>
                <div class="action-tile"><span>Cash Out</span><strong>Withdraw Money</strong></div>
                <div class="action-tile"><span>Lookup</span><strong>Search Account</strong></div>
                <div class="action-tile"><span>KYC</span><strong>Verify Customer</strong></div>
                <div class="action-tile"><span>PDF</span><strong>Bank Statement</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="panel"><p class="panel-title">Customer snapshot</p><p class="panel-copy">Recent accounts are shown for quick review.</p></div>',
        unsafe_allow_html=True,
    )

    if not bank.accounts:
        st.info("No accounts yet. Create an account to begin.")
        return

    for account in bank.accounts[:4]:
        st.markdown(
            f"""
            <div class="account-card">
                <span>Account {account.account_no}</span>
                <strong>{account.name}</strong>
                <span>Available balance: {money(account.get_balance())}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def accounts_dataframe():
    return pd.DataFrame(
        [
            {
                "Account No": account.account_no,
                "Name": account.name,
                "Balance": money(account.get_balance()),
                "KYC": account.kyc_status,
                "Phone": account.phone,
            }
            for account in bank.accounts
        ]
    )


add_styles()

st.sidebar.markdown(
    '<div class="brand"><div class="brand-badge">SBI</div><h2>State Bank of India</h2><p>Banking management system</p></div>',
    unsafe_allow_html=True,
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Create Account",
        "View Account",
        "KYC Verification",
        "Bank Statement PDF",
        "Deposit",
        "Withdraw",
        "Transaction History",
        "Transfer Money",
        "Loan Module",
        "Fixed Deposit Module",
        "Credit Card Module",
        "Delete Account",
        "Search Account",
        "Balance Inquiry",
        "Mini Statement",
        "Update Account",
        "AI Banking Assistant",
    ],
)

if menu == "Home":
    render_home()

elif menu == "Create Account":
    st.title("Create Account")
    st.caption("Open a new saving account with an automatic SBI account number.")

    account_no = st.text_input("Account Number", value=bank.generate_account_no(), disabled=True)
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")
    balance = st.number_input("Opening Balance", min_value=0, step=100)

    if st.button("Create Account"):
        account_no = bank.generate_account_no()
        name = name.strip()
        phone = phone.strip()
        address = address.strip()

        if not account_no or not name:
            st.error("Please enter account number and customer name.")
        elif bank.find_account(account_no):
            st.error("This account number already exists.")
        else:
            photo_path = ""
            account = SavingAccount(
                account_no,
                name,
                balance,
                phone=phone,
                address=address,
                photo_path=photo_path,
            )
            bank.create_account(account)
            st.success(f"Account created successfully. Account No: {account_no}")

elif menu == "View Account":
    st.title("View Accounts")
    st.caption("Review all customer balances.")

    if bank.accounts:
        st.dataframe(accounts_dataframe(), use_container_width=True, hide_index=True)
    else:
        st.info("No accounts available.")

elif menu == "KYC Verification":

    import random
    import re
    import os

    st.title("eKYC Verification System")

    account_no = st.text_input("Account Number")

    account = bank.find_account(account_no.strip()) if account_no else None

    if account:

        st.success(f"Customer Name : {account.name}")

        aadhaar = st.text_input(
            "Aadhaar Number",
            value=getattr(account, "aadhaar_number", "")
        )

        pan = st.text_input(
            "PAN Number",
            value=getattr(account, "pan_number", "")
        )

        phone = st.text_input(
            "Phone Number",
            value=account.phone
        )

        address = st.text_area(
            "Address",
            value=account.address
        )

        aadhaar_file = st.file_uploader(
            "Upload Aadhaar Card",
            type=["jpg","jpeg","png","pdf"]
        )

        pan_file = st.file_uploader(
            "Upload PAN Card",
            type=["jpg","jpeg","png","pdf"]
        )

        selfie = st.camera_input("Capture Live Face")

        st.divider()

        if "otp" not in st.session_state:
            st.session_state.otp = ""

        if st.button("Generate OTP"):

            st.session_state.otp = str(random.randint(100000,999999))

            st.info(f"Demo OTP : {st.session_state.otp}")

        otp = st.text_input("Enter OTP")

        otp_verified = False

        if st.button("Verify OTP"):

            if otp == st.session_state.otp:

                otp_verified = True

                st.success("OTP Verified Successfully")

            else:

                st.error("Invalid OTP")

                st.divider()

        if st.button("Complete eKYC"):

            if len(aadhaar) != 12 or not aadhaar.isdigit():
                st.error("Invalid Aadhaar Number")

            elif not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan.upper()):
                st.error("Invalid PAN Number")

            elif aadhaar_file is None:
                st.error("Upload Aadhaar Card")

            elif pan_file is None:
                st.error("Upload PAN Card")

            elif selfie is None:
                st.error("Capture Live Face")

            elif otp != st.session_state.otp:
                st.error("OTP Verification Failed")

            else:

                os.makedirs("uploads", exist_ok=True)

                aadhaar_path = os.path.join(
                    "uploads",
                    f"{account.account_no}_aadhaar_{aadhaar_file.name}"
                )

                with open(aadhaar_path, "wb") as f:
                    f.write(aadhaar_file.getbuffer())

                pan_path = os.path.join(
                    "uploads",
                    f"{account.account_no}_pan_{pan_file.name}"
                )

                with open(pan_path, "wb") as f:
                    f.write(pan_file.getbuffer())

                selfie_path = save_uploaded_photo(
                    selfie,
                    account.account_no
                )

                bank.update_kyc(
                    account.account_no,
                    phone,
                    address,
                    selfie_path,
                    "Verified",
                    aadhaar,
                    pan,
                    aadhaar_path,
                    pan_path,
                    True,
                    True
                )

                st.balloons()

                st.success("✅ eKYC Completed Successfully")

                st.write("### KYC Summary")

                st.write("Customer :", account.name)
                st.write("Aadhaar :", aadhaar)
                st.write("PAN :", pan.upper())
                st.write("Phone :", phone)
                st.write("Address :", address)
                st.write("OTP :", "Verified")
                st.write("Face :", "Verified")
                st.write("Status :", "Verified")

elif menu == "Bank Statement PDF":
    st.title("Bank Statement PDF")
    st.caption("Generate a printable PDF statement using ReportLab.")

    account_no = st.text_input("Account Number")
    if st.button("Generate Statement"):
        account = bank.find_account(account_no.strip())
        if account:
            pdf_bytes = build_statement_pdf(account)
            st.success("Statement generated successfully.")
            st.download_button(
                "Download PDF Statement",
                data=pdf_bytes,
                file_name=f"{account.account_no}_statement.pdf",
                mime="application/pdf",
            )
        else:
            st.error("Account not found.")

elif menu == "Deposit":
    st.title("Deposit")
    st.caption("Add money to an existing account.")

    account_no = st.text_input("Account Number")
    amount = st.number_input("Amount", min_value=1, step=100)

    if st.button("Deposit Money"):
        account = bank.find_account(account_no.strip())

        if not account:
            st.error("Account not found.")
        elif account.deposit(amount):
            bank.save_accounts()
            cash_animation("deposit", amount, account.name)
            st.success(f"{money(amount)} deposited successfully.")
        else:
            st.error("Please enter a valid deposit amount.")

elif menu == "Transaction History":
    st.header("Transaction History")

    account_no = st.text_input("Enter Account Number :")

    if st.button("View History"):
        account = bank.find_account(account_no.strip())


        if account:
            data = []

            for transaction in account.transactions:
                if isinstance(transaction, dict):
                    data.append({
                        "Type": transaction.get("type", "Unknown"),
                        "Amount": transaction.get("amount", 0),
                        "Date": transaction.get("date", "")

                    })
                else:
                    data.append({

                        "Type": transaction.transaction_type,
                        "Amount": transaction.amount,
                        "Date": transaction.date
                    })

            if data:
                st.dataframe(data, use_container_width=True, hide_index=True)

            else:
                st.warning("No transaction found.")

        else:
            st.error("Account not found.")


elif menu == "Withdraw":
    st.title("Withdraw")
    st.caption("Withdraw money from an existing account.")

    account_no = st.text_input("Account Number")
    amount = st.number_input("Amount", min_value=1, step=100)

    if st.button("Withdraw Money"):
        account = bank.find_account(account_no.strip())

        if not account:
            st.error("Account not found.")
        elif account.withdraw(amount):
            bank.save_accounts()
            cash_animation("withdraw", amount, account.name)
            st.success(f"{money(amount)} withdrawn successfully.")
        else:
            st.error("Insufficient balance.")


# --- YAHAN SE NAYA CODE JODNA SHURU KAREIN ---

elif menu == "Transfer Money":
    st.title("Transfer Money")
    sender_no = st.text_input("Sender Account Number")
    receiver_no = st.text_input("Receiver Account Number")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Transfer"):
        if bank.transfer_money(sender_no.strip(), receiver_no.strip(), amount):
            st.success("Transfer Successful!")
        else:
            st.error("Transfer failed! Check account numbers or balance.")

elif menu == "Loan Module":
    st.title("Loan Module")
    st.caption("Create and track customer loans.")

    account_no = st.text_input("Account Number")
    loan_type = st.selectbox("Loan Type", ["Personal Loan", "Home Loan", "Car Loan", "Education Loan", "Business Loan"])
    amount = st.number_input("Loan Amount", min_value=1, step=1000)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.1, step=0.1)
    tenure_months = st.number_input("Tenure (Months)", min_value=1, step=1)

    if st.button("Create Loan"):
        if bank.add_loan(account_no.strip(), loan_type, amount, interest_rate, tenure_months):
            st.success("Loan created successfully.")
        else:
            st.error("Loan failed. Check account number and values.")

    account = bank.find_account(account_no.strip()) if account_no else None
    if account and account.loans:
        st.subheader("Loan Records")
        st.dataframe(account.loans, use_container_width=True, hide_index=True)

elif menu == "Fixed Deposit Module":
    st.title("Fixed Deposit Module")
    st.caption("Create fixed deposit records with maturity value.")

    account_no = st.text_input("Account Number")
    amount = st.number_input("FD Amount", min_value=1, step=1000)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.1, step=0.1)
    tenure_months = st.number_input("Tenure (Months)", min_value=1, step=1)

    if st.button("Create Fixed Deposit"):
        if bank.add_fixed_deposit(account_no.strip(), amount, interest_rate, tenure_months):
            st.success("Fixed deposit created successfully.")
        else:
            st.error("FD failed. Check account number and values.")

    account = bank.find_account(account_no.strip()) if account_no else None
    if account and account.fixed_deposits:
        st.subheader("Fixed Deposit Records")
        st.dataframe(account.fixed_deposits, use_container_width=True, hide_index=True)

elif menu == "Credit Card Module":
    st.title("Credit Card Module")
    st.caption("Issue customer credit cards and store limits.")

    account_no = st.text_input("Account Number")
    card_type = st.selectbox("Card Type", ["Classic", "Silver", "Gold", "Platinum"])
    credit_limit = st.number_input("Credit Limit", min_value=1, step=1000)

    if st.button("Issue Credit Card"):
        if bank.add_credit_card(account_no.strip(), card_type, credit_limit):
            st.success("Credit card issued successfully.")
        else:
            st.error("Credit card failed. Check account number and limit.")

    account = bank.find_account(account_no.strip()) if account_no else None
    if account and account.credit_cards:
        st.subheader("Credit Card Records")
        st.dataframe(account.credit_cards, use_container_width=True, hide_index=True)

elif menu == "Delete Account":
    st.title("Delete Account")
    acc_no = st.text_input("Enter Account Number to Delete")
    if st.button("Delete Account"):
        if bank.delete_account(acc_no.strip()):
            st.success(f"Account {acc_no} deleted successfully.")
        else:
            st.error("Account not found.")

elif menu == "Search Account":
    st.title("Search Account")
    acc_no = st.text_input("Enter Account Number")
    if st.button("Search"):
        account = bank.find_account(acc_no.strip())
        if account:
            st.write(f"**Name:** {account.name}")
            st.write(f"**Balance:** {money(account.get_balance())}")
            st.write(f"**Phone:** {account.phone or '-'}")
            st.write(f"**KYC Status:** {account.kyc_status}")
            photo_path = getattr(account, "photo_path", "")
            if photo_path and os.path.exists(photo_path):
                st.image(photo_path, caption=account.name, width=180)
        else:
            st.error("Account not found.")

elif menu == "Balance Inquiry":
    st.title("Balance Inquiry")

    acc_no = st.text_input("Account Number")

    if st.button("Check Balance"):
        account = bank.find_account(acc_no)

        if account:
            st.success(f"Current Balance: ₹{account.balance}")
        else:
            st.error("Account not found")

elif menu == "Mini Statement":
    st.title("Mini Statement")

    acc_no = st.text_input("Account Number")

    if st.button("View Statement"):
        account = bank.find_account(acc_no)

        if account and hasattr(account, "transactions"):
            st.write(account.transactions[-5:])
        else:
            st.info("No transactions found")


elif menu == "Update Account":
    st.title("Update Account")

    acc_no = st.text_input("Account Number")

    if st.button("Find Account"):
        account = bank.find_account(acc_no)

        if account:
            st.session_state["update_account"] = account

    if "update_account" in st.session_state:

        account = st.session_state["update_account"]

        phone = st.text_input("Phone", value=account.phone)
        address = st.text_area("Address", value=account.address)

        if st.button("Update Account"):
            account.phone = phone
            account.address = address

            bank.save_data()

            st.success("Account Updated Successfully")


elif menu == "AI Banking Assistant":

    st.title("🤖 AI Banking Assistant")

    question = st.text_input("Ask a Banking Question")

    if question:

        q = question.lower()

        if "loan" in q:
            st.success("Loan is borrowed money which is repaid with interest.")

        elif "fd" in q:
            st.success("Fixed Deposit gives higher interest than savings account.")

        elif "credit card" in q:
            st.success("Credit Card allows spending on approved credit limit.")

        elif "balance" in q:
            st.success("Use Balance Inquiry to check account balance.")

        else:
            st.info("Please ask a banking related question.")

# --- YAHAN PAR KHATAM KAREIN ---

# Transfer Mony
#Account ko dalete
# sarch Account
# sql file


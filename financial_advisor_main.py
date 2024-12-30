import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import requests

# Function for Budget Planner
def budget_planner():
    st.title("Personalized Budget Planner")

    # User Inputs
    st.header("Enter Your Income and Expenses")
    income = st.number_input("Monthly Income (in your currency)", min_value=0.0, step=0.01)
    categories = ["Rent", "Groceries", "Utilities", "Transportation", "Entertainment", "Others"]
    expenses = {}
    for category in categories:
        expenses[category] = st.number_input(f"{category} Expenses", min_value=0.0, step=0.01)

    # Calculate Savings
    total_expenses = sum(expenses.values())
    savings = income - total_expenses

    # Display Results
    st.subheader("Budget Summary")
    st.write(f"**Total Income:** {income}")
    st.write(f"**Total Expenses:** {total_expenses}")
    st.write(f"**Remaining Savings:** {savings}")

    if savings < 0:
        st.warning("You are overspending! Consider reducing your expenses.")
    elif savings == 0:
        st.info("You are breaking even. Try to save more for unexpected expenses.")
    else:
        st.success("Great! You are saving money!")

    # Visualization
    st.subheader("Expense Distribution")
    expense_data = pd.DataFrame({
        "Category": categories,
        "Amount": [expenses[category] for category in categories]
    })
    fig, ax = plt.subplots()
    ax.pie(expense_data["Amount"], labels=expense_data["Category"], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)

# Function for Tax Calculator
def tax_calculator():
    st.title("Tax Calculator and Suggestions")

    # Input Section
    st.header("Enter Your Income Details")
    annual_income = st.number_input("Enter your Annual Income (₹)", min_value=0.0, format="%.2f")
    deductions = st.number_input("Enter Total Deductions (₹)", min_value=0.0, format="%.2f")

    # Tax Slabs (Example for India)
    tax_slabs = [
        (0, 250000, 0.0),  # No tax for income up to ₹2,50,000
        (250001, 500000, 0.05),  # 5% for ₹2,50,001 to ₹5,00,000
        (500001, 1000000, 0.2),  # 20% for ₹5,00,001 to ₹10,00,000
        (1000001, float('inf'), 0.3)  # 30% for income above ₹10,00,000
    ]

    # Tax Calculation
    if st.button("Calculate Tax"):
        taxable_income = annual_income - deductions
        if taxable_income < 0:
            taxable_income = 0

        total_tax = 0
        for lower, upper, rate in tax_slabs:
            if taxable_income > lower:
                income_in_slab = min(taxable_income, upper) - lower
                total_tax += income_in_slab * rate

        # Display Results
        st.subheader("Tax Calculation Results")
        st.write(f"Taxable Income: ₹{taxable_income}")
        st.write(f"Total Tax Payable: ₹{total_tax}")

        # Tax-Saving Suggestions
        st.subheader("Tax-Saving Suggestions")
        st.write("- **Invest in 80C**: You can claim deductions up to ₹1,50,000 by investing in ELSS, PPF, or other tax-saving instruments.")
        st.write("- **Medical Insurance (80D)**: Claim deductions for health insurance premiums paid for yourself or family.")
        st.write("- **Home Loan Interest (Section 24)**: Deduct interest paid on your home loan (up to ₹2,00,000).")
        st.write("- **Other Deductions**: Explore sections 80G (donations), 80E (education loans), and more.")

# Function for Retirement Planning Tool
def retirement_plan(current_age, retirement_age, current_savings, annual_expenses, inflation_rate):
    years_to_retirement = retirement_age - current_age
    future_expenses = annual_expenses * ((1 + inflation_rate) ** years_to_retirement)
    savings_needed = future_expenses * 25  # Rule of thumb: 25x annual expenses needed for retirement
    
    monthly_savings = (savings_needed - current_savings) / (years_to_retirement * 12)
    return monthly_savings, savings_needed

def retirement_planner():
    st.title("Retirement Planning Tool")

    # User Inputs
    current_age = st.number_input("Enter your current age", min_value=18, max_value=100, step=1)
    retirement_age = st.number_input("Enter your desired retirement age", min_value=current_age+1, max_value=100, step=1)
    current_savings = st.number_input("Enter your current savings", min_value=0.0, step=0.01)
    annual_expenses = st.number_input("Enter your annual expenses", min_value=0.0, step=0.01)
    inflation_rate = st.number_input("Enter the expected annual inflation rate (in decimal)", min_value=0.0, max_value=1.0, step=0.01)

    if st.button("Calculate Retirement Savings"):
        monthly_savings, savings_needed = retirement_plan(current_age, retirement_age, current_savings, annual_expenses, inflation_rate)
        st.write(f"Monthly Savings Required: ₹{monthly_savings:.2f}")
        st.write(f"Total Savings Needed for Retirement: ₹{savings_needed:.2f}")

# Function for Loan Eligibility and EMI Calculator
def emi_calculator(principal, interest_rate, tenure_years):
    monthly_interest_rate = interest_rate / (12 * 100)
    number_of_months = tenure_years * 12
    emi = principal * monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_months / ((1 + monthly_interest_rate) ** number_of_months - 1)
    return emi

def loan_eligibility(income, current_debts, proposed_loan_amount):
    debt_to_income_ratio = current_debts / income
    eligibility = "Eligible" if debt_to_income_ratio < 0.4 else "Not Eligible"
    return eligibility

def loan_calculator():
    st.title("Loan Eligibility and EMI Calculator")

    # User Inputs
    principal = st.number_input("Enter loan amount", min_value=0.0, step=0.01)
    interest_rate = st.number_input("Enter interest rate (annual %)", min_value=0.0, step=0.01)
    tenure_years = st.number_input("Enter loan tenure (in years)", min_value=1, max_value=30, step=1)

    if st.button("Calculate EMI"):
        emi = emi_calculator(principal, interest_rate, tenure_years)
        st.write(f"EMI: ₹{emi:.2f}")

    # Loan Eligibility Inputs
    income = st.number_input("Enter your annual income", min_value=0.0, step=0.01)
    current_debts = st.number_input("Enter your current debts", min_value=0.0, step=0.01)

    if st.button("Check Loan Eligibility"):
        eligibility = loan_eligibility(income, current_debts, principal)
        st.write(f"Loan Eligibility: {eligibility}")

# Function for Real-Time Stock Market Insights
def stock_insights(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="5d")  # Get the last 5 days of stock data
    price = data['Close'][-1]
    trend = "Up" if data['Close'][-1] > data['Close'][0] else "Down"
    return price, trend

def stock_market_insights():
    st.title("Real-Time Stock Market Insights")

    # User Inputs
    ticker = st.text_input("Enter stock symbol (e.g., AAPL, TSLA)", max_chars=5)

    if st.button("Get Stock Insights"):
        price, trend = stock_insights(ticker)
        st.write(f"Stock Price for {ticker}: ₹{price:.2f}")
        st.write(f"Trend: {trend}")

# Function for Cryptocurrency Portfolio Tracker
def get_crypto_price(crypto):
    url = f'https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD'
    response = requests.get(url)
    data = response.json()
    return data['USD']

def portfolio_value(portfolio):
    total_value = 0
    for crypto, amount in portfolio.items():
        price = get_crypto_price(crypto)
        total_value += price * amount
    return total_value

def crypto_tracker():
    st.title("Cryptocurrency Portfolio Tracker")

    # Example portfolio
    portfolio = {"BTC": 1.5, "ETH": 10}  # Example portfolio
    total_value = portfolio_value(portfolio)

    st.write(f"Total Portfolio Value: ${total_value:.2f}")

# Function for Sustainability Score for Investments
def sustainability_score(stock_symbol):
    esg_scores = {
        "AAPL": 85,  # Example ESG score (higher is better)
        "TSLA": 60,
        "AMZN": 70
    }
    return esg_scores.get(stock_symbol, "No data available")

def sustainability_score_tool():
    st.title("Sustainability Score for Investments")

    stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL)")

    if st.button("Get ESG Score"):
        score = sustainability_score(stock_symbol)
        st.write(f"ESG Score for {stock_symbol}: {score}")

# Function for Financial Literacy Section
def financial_literacy_quiz():
    st.title("Financial Literacy Quiz")
    answer = st.text_input("What is the best way to save money for retirement? (Investing/Saving/Spending)")
    if answer.lower() == "investing":
        st.write("Correct! Investing is a key strategy for retirement.")
    else:
        st.write("Incorrect. Try again!")

def financial_literacy_section():
    st.title("Financial Literacy Section")
    financial_literacy_quiz()

# Main Function
def main():
    st.sidebar.title("Navigation")
    options = ["Home", "Budget Planner", "Tax Calculator", "Retirement Planner", "Loan Calculator", "Stock Market Insights", "Crypto Tracker", "Sustainability Score", "Financial Literacy", "Exit"]
    choice = st.sidebar.selectbox("Select a Feature", options)

    if choice == "Home":
        st.title("Welcome to the AI-Powered Financial Advisor")
        st.write("Select a feature from the sidebar to explore various tools.")
    elif choice == "Budget Planner":
        budget_planner()
    elif choice == "Tax Calculator":
        tax_calculator()
    elif choice == "Retirement Planner":
        retirement_planner()
    elif choice == "Loan Calculator":
        loan_calculator()
    elif choice == "Stock Market Insights":
        stock_market_insights()
    elif choice == "Crypto Tracker":
        crypto_tracker()
    elif choice == "Sustainability Score":
        sustainability_score_tool()
    elif choice == "Financial Literacy":
        financial_literacy_section()
    elif choice == "Exit":
        st.write("Goodbye!")

if __name__ == "__main__":
    main()

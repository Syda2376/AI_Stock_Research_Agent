import re
import requests
from bs4 import BeautifulSoup
from database import get_connection


NSE_URL = (
    "https://nsearchives.nseindia.com/corporate/ixbrl/"
    "INTEGRATED_FILING_INDAS_152826_24042026225714_iXBRL_WEB.html"
)

COMPANY_SYMBOL = "RELIANCE"
REPORT_DATE = "2026-03-31"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_numbers(text):
    pattern = r"\(?[\d,]+\.\d+\)?"
    matches = re.findall(pattern, text)

    numbers = []

    for value in matches:
        value = value.replace(",", "")

        if value.startswith("(") and value.endswith(")"):
            value = "-" + value[1:-1]

        numbers.append(float(value))

    return numbers


# Download filing
response = requests.get(
    NSE_URL,
    headers=headers,
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


# Extract fundamentals
financial_data = {}

for row in soup.find_all("tr"):

    text = row.get_text(" ", strip=True)

    if "Revenue from operations" in text and "revenue" not in financial_data:
        numbers = get_numbers(text)

        if len(numbers) >= 2:
            financial_data["revenue"] = numbers[-1]

    elif "Total profit (loss) for period" in text and "net_profit" not in financial_data:
        numbers = get_numbers(text)

        if len(numbers) >= 2:
            financial_data["net_profit"] = numbers[-1]

    elif "Basic earnings (loss) per share from continuing operations" in text:
        numbers = get_numbers(text)

        if len(numbers) >= 2:
            financial_data["eps"] = numbers[-1]

    elif "Debt equity ratio" in text:
        numbers = get_numbers(text)

        if len(numbers) >= 2:
            financial_data["debt_to_equity"] = numbers[-1]

    elif "Total equity" in text and "total_equity" not in financial_data:
        numbers = get_numbers(text)

        if len(numbers) >= 2:
            financial_data["total_equity"] = numbers[-1]


print("\nExtracted fundamental data:")

for key, value in financial_data.items():
    print(f"{key}: {value}")


# Get company ID 
connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id
    FROM companies
    WHERE symbol = %s
""", (COMPANY_SYMBOL,))

company = cursor.fetchone()

if not company:
    print("Company not found in database.")
    cursor.close()
    connection.close()
    exit()

company_id = company[0]


# Insert fundamentals into database
cursor.execute("""
    INSERT INTO fundamentals
    (
        company_id,
        report_date,
        revenue,
        net_profit,
        eps,
        pe_ratio,
        debt_to_equity,
        roe
    )
    VALUES (%s, %s, %s, %s, %s, NULL, %s, NULL)
    ON CONFLICT (company_id, report_date)
    DO UPDATE SET
        revenue = EXCLUDED.revenue,
        net_profit = EXCLUDED.net_profit,
        eps = EXCLUDED.eps,
        debt_to_equity = EXCLUDED.debt_to_equity
""", (
    company_id,
    REPORT_DATE,
    financial_data.get("revenue"),
    financial_data.get("net_profit"),
    financial_data.get("eps"),
    financial_data.get("debt_to_equity")
))


connection.commit()

cursor.close()
connection.close()

print("\nFundamentals saved to PostgreSQL successfully!")
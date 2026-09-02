from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = "financial_data.xlsx"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_data():

    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)

    return pd.DataFrame()


df = load_data()


# ---------------------------------------------------------
# HTML DASHBOARD
# ---------------------------------------------------------

HTML = """

<!DOCTYPE html>

<html>

<head>

    <title>AI Financial Analyst</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>

        body {

            font-family: Arial, sans-serif;

            background: #f4f6f8;

            margin: 0;

            padding: 30px;

        }


        .container {

            max-width: 1200px;

            margin: auto;

        }


        h1 {

            color: #222;

            margin-bottom: 5px;

        }


        .subtitle {

            color: #666;

            margin-bottom: 30px;

        }


        .box {

            background: white;

            padding: 25px;

            border-radius: 12px;

            margin-bottom: 25px;

            box-shadow: 0 2px 8px rgba(0,0,0,0.08);

        }


        .cards {

            display: grid;

            grid-template-columns: repeat(3, 1fr);

            gap: 20px;

            margin-bottom: 25px;

        }


        .card {

            background: white;

            padding: 25px;

            border-radius: 12px;

            box-shadow: 0 2px 8px rgba(0,0,0,0.08);

        }


        .card h3 {

            color: #555;

        }


        .value {

            font-size: 30px;

            font-weight: bold;

            color: #222;

        }


        select {

            padding: 12px;

            font-size: 16px;

            border-radius: 6px;

            border: 1px solid #ccc;

            min-width: 220px;

        }


        input[type="file"] {

            margin: 10px 0;

        }


        input[type="text"] {

            width: 70%;

            padding: 12px;

            border: 1px solid #ccc;

            border-radius: 6px;

            font-size: 15px;

        }


        button {

            background: #222;

            color: white;

            border: none;

            padding: 11px 18px;

            border-radius: 6px;

            cursor: pointer;

        }


        button:hover {

            background: #444;

        }


        .success {

            color: green;

            font-weight: bold;

            margin-bottom: 20px;

        }


        .error {

            color: red;

            font-weight: bold;

            margin-bottom: 20px;

        }


        #answer {

            margin-top: 20px;

            font-size: 17px;

            font-weight: bold;

        }


        @media(max-width: 800px) {

            .cards {

                grid-template-columns: 1fr;

            }


            input[type="text"] {

                width: 90%;

                margin-bottom: 10px;

            }

        }

    </style>

</head>


<body>


<div class="container">


    <!-- TITLE -->

    <h1>

        🤖 AI Financial Analyst

    </h1>


    <p class="subtitle">

        Financial Analytics Dashboard using Python, Pandas, Flask & Chart.js

    </p>


    <!-- MESSAGES -->

    {% if message %}

        <div class="success">

            {{ message }}

        </div>

    {% endif %}


    {% if error %}

        <div class="error">

            {{ error }}

        </div>

    {% endif %}


    <!-- COMPANY SELECTOR -->

    <div class="box">

        <h2>

            🏢 Select Company

        </h2>


        <form method="GET" action="/">

            <select

                name="company"

                onchange="this.form.submit()"

            >

                {% for company in companies %}

                    <option

                        value="{{ company }}"

                        {% if company == selected_company %}

                        selected

                        {% endif %}

                    >

                        {{ company }}

                    </option>

                {% endfor %}

            </select>

        </form>


        <p>

            Select a company to view its financial performance.

        </p>

    </div>


    <!-- FILE UPLOAD -->

    <div class="box">

        <h2>

            📁 Upload Financial Data

        </h2>


        <p>

            Upload an Excel (.xlsx) or CSV (.csv) financial dataset.

        </p>


        <form

            action="/upload"

            method="POST"

            enctype="multipart/form-data"

        >

            <input

                type="file"

                name="file"

                accept=".xlsx,.xls,.csv"

                required

            >


            <br>


            <button type="submit">

                Upload Data

            </button>

        </form>

    </div>


    {% if data_available %}


    <!-- KPI CARDS -->

    <div class="cards">


        <!-- REVENUE -->

        <div class="card">

            <h3>

                💰 {{ selected_company }} Revenue

            </h3>


            <div class="value">

                ${{ revenue }}B

            </div>


            <p>

                Latest Year: {{ latest_year }}

            </p>

        </div>


        <!-- NET INCOME -->

        <div class="card">

            <h3>

                📊 {{ selected_company }} Net Income

            </h3>


            <div class="value">

                ${{ profit }}B

            </div>


            <p>

                Latest Year: {{ latest_year }}

            </p>

        </div>


        <!-- GROWTH -->

        <div class="card">

            <h3>

                📈 Average Revenue Growth

            </h3>


            <div class="value">

                {{ avg_growth }}%

            </div>


            <p>

                Year-over-Year

            </p>

        </div>


        <!-- ASSETS -->

        <div class="card">

            <h3>

                🏦 Total Assets

            </h3>


            <div class="value">

                ${{ assets }}B

            </div>


            <p>

                Latest Year: {{ latest_year }}

            </p>

        </div>


        <!-- LIABILITIES -->

        <div class="card">

            <h3>

                📋 Total Liabilities

            </h3>


            <div class="value">

                ${{ liabilities }}B

            </div>


            <p>

                Latest Year: {{ latest_year }}

            </p>

        </div>


        <!-- CASH FLOW -->

        <div class="card">

            <h3>

                💵 Operating Cash Flow

            </h3>


            <div class="value">

                ${{ cash_flow }}B

            </div>


            <p>

                Latest Year: {{ latest_year }}

            </p>

        </div>


    </div>


    <!-- REVENUE CHART -->

    <div class="box">

        <h2>

            📈 {{ selected_company }} Revenue Trend

        </h2>


        <canvas id="revenueChart"></canvas>

    </div>


    <!-- NET INCOME CHART -->

    <div class="box">

        <h2>

            💰 {{ selected_company }} Net Income Trend

        </h2>


        <canvas id="profitChart"></canvas>

    </div>


    <!-- AI QUESTION ANSWER -->

    <div class="box">

        <h2>

            🤖 Ask Your Financial Data

        </h2>


        <p>

            Try questions like:

        </p>


        <ul>

            <li>

                What is the revenue?

            </li>


            <li>

                What is the net income?

            </li>


            <li>

                What is the growth?

            </li>


            <li>

                What are the total assets?

            </li>


            <li>

                What are the liabilities?

            </li>


            <li>

                What is the operating cash flow?

            </li>

        </ul>


        <input

            type="text"

            id="question"

            placeholder="Ask a financial question..."

        >


        <button onclick="askQuestion()">

            Ask

        </button>


        <div id="answer"></div>

    </div>


    <!-- JAVASCRIPT -->

    <script>


        const years = {{ years | safe }};


        const revenues = {{ revenues | safe }};


        const profits = {{ profits | safe }};


        // Revenue Chart

        new Chart(

            document.getElementById("revenueChart"),

            {

                type: "line",

                data: {

                    labels: years,

                    datasets: [{

                        label: "Revenue ($B)",

                        data: revenues,

                        borderWidth: 3,

                        tension: 0.3

                    }]

                },

                options: {

                    responsive: true

                }

            }

        );


        // Net Income Chart

        new Chart(

            document.getElementById("profitChart"),

            {

                type: "line",

                data: {

                    labels: years,

                    datasets: [{

                        label: "Net Income ($B)",

                        data: profits,

                        borderWidth: 3,

                        tension: 0.3

                    }]

                },

                options: {

                    responsive: true

                }

            }

        );


        // AI QUESTION

        async function askQuestion() {


            const question =

                document.getElementById("question").value;


            if (!question) {

                document.getElementById("answer").innerText =

                    "Please enter a question.";

                return;

            }


            const response = await fetch(

                "/chat",

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify({

                        question: question,

                        company: "{{ selected_company }}"

                    })

                }

            );


            const data = await response.json();


            document.getElementById("answer").innerText =

                data.answer;

        }


    </script>


    {% endif %}


</div>


</body>

</html>

"""


# ---------------------------------------------------------
# DASHBOARD DATA
# ---------------------------------------------------------

def get_dashboard_data(company):


    company_data = df[

        df["Company"].astype(str).str.lower()

        == company.lower()

    ].copy()


    if company_data.empty:

        return None


    company_data = company_data.sort_values("Year")


    latest_year = company_data["Year"].max()


    latest = company_data[

        company_data["Year"] == latest_year

    ].iloc[0]


    revenue = round(

        float(latest["Revenue"]),

        1

    )


    profit = round(

        float(latest["Net_Income"]),

        1

    )


    # Revenue by year

    yearly_revenue = (

        company_data

        .groupby("Year")["Revenue"]

        .sum()

        .sort_index()

    )


    # Growth

    growth = (

        yearly_revenue

        .pct_change()

        * 100

    )


    if len(growth.dropna()) > 0:

        avg_growth = round(

            growth.dropna().mean(),

            1

        )

    else:

        avg_growth = 0


    # Assets

    assets = round(

        float(latest["Total_Assets"]),

        1

    )


    # Liabilities

    liabilities = round(

        float(latest["Total_Liabilities"]),

        1

    )


    # Operating cash flow

    cash_flow = round(

        float(latest["Operating_Cash_Flow"]),

        1

    )


    # Profit by year

    yearly_profit = (

        company_data

        .groupby("Year")["Net_Income"]

        .sum()

        .sort_index()

    )


    return {


        "latest_year": latest_year,


        "revenue": revenue,


        "profit": profit,


        "avg_growth": avg_growth,


        "assets": assets,


        "liabilities": liabilities,


        "cash_flow": cash_flow,


        "years":

            yearly_revenue.index.tolist(),


        "revenues":

            yearly_revenue

            .round(1)

            .tolist(),


        "profits":

            yearly_profit

            .round(1)

            .tolist()

    }


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.route("/")

def home():


    global df


    if df.empty:

        return render_template_string(

            HTML,

            data_available=False,

            companies=[],

            selected_company="",

            message=None,

            error="No financial data found."

        )


    companies = sorted(

        df["Company"]

        .dropna()

        .astype(str)

        .unique()

        .tolist()

    )


    selected_company = request.args.get(

        "company",

        companies[0]

    )


    if selected_company not in companies:

        selected_company = companies[0]


    data = get_dashboard_data(

        selected_company

    )


    return render_template_string(

        HTML,

        data_available=True,

        companies=companies,

        selected_company=selected_company,

        message=request.args.get("message"),

        error=None,

        **data

    )


# ---------------------------------------------------------
# UPLOAD EXCEL / CSV
# ---------------------------------------------------------

@app.route(

    "/upload",

    methods=["POST"]

)

def upload():


    global df


    file = request.files.get("file")


    if not file:

        return "Please select a file."


    try:


        filename = file.filename.lower()


        if filename.endswith(".xlsx"):

            df = pd.read_excel(file)


        elif filename.endswith(".xls"):

            df = pd.read_excel(file)


        elif filename.endswith(".csv"):

            df = pd.read_csv(file)


        else:

            return (

                "Please upload an Excel "

                "or CSV file."

            )


        required_columns = [

            "Company",

            "Year",

            "Revenue",

            "Net_Income",

            "Total_Assets",

            "Total_Liabilities",

            "Operating_Cash_Flow"

        ]


        missing = [

            col

            for col in required_columns

            if col not in df.columns

        ]


        if missing:

            return (

                "Missing columns: "

                + ", ".join(missing)

            )


        companies = sorted(

            df["Company"]

            .dropna()

            .astype(str)

            .unique()

            .tolist()

        )


        first_company = companies[0]


        data = get_dashboard_data(

            first_company

        )


        return render_template_string(

            HTML,

            data_available=True,

            companies=companies,

            selected_company=first_company,

            message=

                "✅ Financial data uploaded successfully!",

            error=None,

            **data

        )


    except Exception as e:


        return (

            "Error reading file: "

            + str(e)

        )


# ---------------------------------------------------------
# FINANCIAL QUESTION ANSWERING
# ---------------------------------------------------------

@app.route(

    "/chat",

    methods=["POST"]

)

def chat():


    global df


    data = request.json


    question = data.get(

        "question",

        ""

    ).lower()


    company = data.get(

        "company",

        ""

    )


    company_data = df[

        df["Company"].astype(str).str.lower()

        == company.lower()

    ]


    if company_data.empty:

        return {

            "answer":

                "Company data not found."

        }


    latest_year = company_data["Year"].max()


    latest = company_data[

        company_data["Year"] == latest_year

    ].iloc[0]


    # Revenue

    if "revenue" in question:


        return {

            "answer":

                f"{company} revenue in "

                f"{latest_year} was "

                f"${latest['Revenue']:.1f}B."

        }


    # Net Income

    if (

        "profit" in question

        or "net income" in question

    ):


        return {

            "answer":

                f"{company} net income in "

                f"{latest_year} was "

                f"${latest['Net_Income']:.1f}B."

        }


    # Growth

    if "growth" in question:


        yearly = (

            company_data

            .groupby("Year")["Revenue"]

            .sum()

            .sort_index()

        )


        growth = (

            yearly.pct_change()

            * 100

        )


        if len(growth.dropna()) > 0:

            avg = growth.dropna().mean()

        else:

            avg = 0


        return {

            "answer":

                f"{company} average revenue "

                f"growth was {avg:.1f}%."

        }


    # Assets

    if "asset" in question:


        return {

            "answer":

                f"{company} total assets in "

                f"{latest_year} were "

                f"${latest['Total_Assets']:.1f}B."

        }


    # Liabilities

    if "liabilit" in question:


        return {

            "answer":

                f"{company} total liabilities in "

                f"{latest_year} were "

                f"${latest['Total_Liabilities']:.1f}B."

        }


    # Cash Flow

    if (

        "cash flow" in question

        or "cashflow" in question

    ):


        return {

            "answer":

                f"{company} operating cash flow in "

                f"{latest_year} was "

                f"${latest['Operating_Cash_Flow']:.1f}B."

        }


    return {

        "answer":

            "I can answer questions about "

            "revenue, net income, growth, "

            "assets, liabilities and "

            "operating cash flow."

    }


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc


# ============================================================
# DATA
# ============================================================

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "Dataset"
    / "File_3_Cleaned.csv"
)

df = pd.read_csv(DATA_FILE)


# ============================================================
# APP
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="Passenger Survival Dashboard"
)


# ============================================================
# FILTER
# ============================================================

def filter_data(data, sex, pclass, embarked):

    filtered = data.copy()

    if sex:
        filtered = filtered[
            filtered["Sex"].isin(sex)
        ]

    if pclass:
        filtered = filtered[
            filtered["Pclass"].isin(pclass)
        ]

    if embarked:
        filtered = filtered[
            filtered["Embarked"].isin(embarked)
        ]

    return filtered


# ============================================================
# EMPTY CHART
# ============================================================

def empty_figure(message="No data available"):

    fig = go.Figure()

    fig.update_layout(
        template="plotly_dark",
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": message,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 16},
            }
        ],
        margin=dict(l=20, r=20, t=55, b=20),
    )

    return fig


# ============================================================
# BAR CHART
# ============================================================

def bar_chart(data, column, title, label):

    if data.empty:
        return empty_figure()

    grouped = (
        data.groupby(column)
        .agg(
            Passengers=("PassengerId", "count"),
            Survivors=("Survived", "sum"),
        )
        .reset_index()
    )

    grouped["Category"] = grouped[column].astype(str)

    plot_data = grouped.melt(
        id_vars="Category",
        value_vars=[
            "Passengers",
            "Survivors"
        ],
        var_name="Measure",
        value_name="Count",
    )

    fig = px.bar(
        plot_data,
        x="Category",
        y="Count",
        color="Measure",
        barmode="group",
        title=title,
        labels={
            "Category": label,
            "Count": "Passengers",
        },
        template="plotly_dark",
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
        legend_title_text="",
        hovermode="x unified",
    )

    return fig


# ============================================================
# AGE CHART
# ============================================================

def age_histogram(data):

    if data.empty:
        return empty_figure()

    fig = px.histogram(
        data,
        x="Age",
        color="Survived",
        nbins=20,
        barmode="overlay",
        opacity=0.75,
        title="Age Distribution",
        labels={
            "Age": "Age",
            "Survived": "Survived",
        },
        category_orders={
            "Survived": [0, 1]
        },
        template="plotly_dark",
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
        hovermode="x unified",
    )

    return fig


# ============================================================
# TICKET CHART
# ============================================================

def top_tickets(data):

    if data.empty:
        return empty_figure()

    top = (
        data.groupby("Ticket")
        .agg(
            Passengers=("PassengerId", "count"),
            Survivors=("Survived", "sum"),
        )
        .sort_values(
            [
                "Passengers",
                "Survivors"
            ],
            ascending=[
                False,
                False
            ],
        )
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top.sort_values("Passengers"),
        x="Passengers",
        y="Ticket",
        orientation="h",
        text="Survivors",
        title="Top 10 Ticket Groups",
        labels={
            "Passengers": "Passengers",
            "Ticket": "Ticket",
        },
        template="plotly_dark",
    )

    fig.update_traces(
        texttemplate="Survivors: %{text}",
        textposition="outside",
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=70,
            t=60,
            b=20,
        ),
    )

    return fig


# ============================================================
# SCATTER CHART
# ============================================================

def fare_age_scatter(data):

    if data.empty:
        return empty_figure()

    fig = px.scatter(
        data,
        x="Age",
        y="Fare",
        color="Survived",
        hover_data=[
            "PassengerId",
            "Pclass",
            "Sex",
            "Embarked",
        ],
        title="Age vs Fare",
        labels={
            "Age": "Age",
            "Fare": "Fare",
            "Survived": "Survived",
        },
        category_orders={
            "Survived": [0, 1]
        },
        template="plotly_dark",
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    return fig


# ============================================================
# KPI CARD
# ============================================================

def kpi_card(title, component_id, icon):

    return dbc.Card(
        dbc.CardBody(
            [

                html.Div(
                    [
                        html.Span(
                            icon,
                            className="fs-3 me-2",
                        ),

                        html.Span(
                            title,
                            className="text-secondary fw-semibold",
                        ),
                    ],

                    className=(
                        "d-flex align-items-center "
                        "justify-content-center mb-2"
                    ),
                ),

                html.H2(
                    id=component_id,
                    className=(
                        "text-center fw-bold "
                        "mb-0 text-info"
                    ),
                ),

            ]
        ),

        className="h-100 shadow border-0",
    )


# ============================================================
# SECTION TITLE
# ============================================================

def section_title(number, title):

    return html.Div(
        [

            html.Span(
                number,
                className="badge bg-info me-2 fs-6",
            ),

            html.Span(
                title,
                className="fw-bold fs-5",
            ),

        ],

        className="d-flex align-items-center mb-3 mt-2",
    )


# ============================================================
# LAYOUT
# ============================================================

app.layout = dbc.Container(
    [

        # ====================================================
        # HEADER
        # ====================================================

        dbc.Card(
            dbc.CardBody(
                [

                    html.H1(
                        "Passenger Survival Dashboard",
                        className=(
                            "text-center fw-bold mb-2"
                        ),
                    ),

                    html.P(
                        "Interactive analysis of passenger "
                        "characteristics and survival outcomes",
                        className=(
                            "text-center text-secondary mb-0"
                        ),
                    ),

                ]
            ),

            className=(
                "shadow border-0 mt-3 mb-4"
            ),
        ),


        # ====================================================
        # FILTERS
        # ====================================================

        dbc.Card(
            dbc.CardBody(
                [

                    html.Div(
                        [

                            html.Span(
                                "FILTERS",
                                className="badge bg-info me-2",
                            ),

                            html.Span(
                                "Select one or more values "
                                "to update the dashboard",
                                className="text-secondary",
                            ),

                        ],

                        className="mb-3",
                    ),


                    dbc.Row(
                        [

                            # ==================================
                            # SEX
                            # ==================================

                            dbc.Col(
                                [

                                    html.Label(
                                        "Sex",
                                        className=(
                                            "fw-semibold mb-1"
                                        ),
                                    ),

                                    dcc.Dropdown(
                                        id="sex-filter",

                                        options=[
                                            {
                                                "label": "Female",
                                                "value": "female",
                                            },

                                            {
                                                "label": "Male",
                                                "value": "male",
                                            },
                                        ],

                                        placeholder="All",

                                        clearable=True,

                                        multi=True,

                                        className="text-dark",

                                    ),

                                ],

                                md=3,

                            ),


                            # ==================================
                            # PASSENGER CLASS
                            # ==================================

                            dbc.Col(
                                [

                                    html.Label(
                                        "Passenger Class",
                                        className=(
                                            "fw-semibold mb-1"
                                        ),
                                    ),

                                    dcc.Dropdown(
                                        id="class-filter",

                                        options=[
                                            {
                                                "label": "Class 1",
                                                "value": 1,
                                            },

                                            {
                                                "label": "Class 2",
                                                "value": 2,
                                            },

                                            {
                                                "label": "Class 3",
                                                "value": 3,
                                            },
                                        ],

                                        placeholder="All",

                                        clearable=True,

                                        multi=True,

                                        className="text-dark",

                                    ),

                                ],

                                md=3,

                            ),


                            # ==================================
                            # EMBARKED
                            # ==================================

                            dbc.Col(
                                [

                                    html.Label(
                                        "Embarked",
                                        className=(
                                            "fw-semibold mb-1"
                                        ),
                                    ),

                                    dcc.Dropdown(
                                        id="embarked-filter",

                                        options=[
                                            {
                                                "label": "Cherbourg (C)",
                                                "value": "C",
                                            },

                                            {
                                                "label": "Queenstown (Q)",
                                                "value": "Q",
                                            },

                                            {
                                                "label": "Southampton (S)",
                                                "value": "S",
                                            },
                                        ],

                                        placeholder="All",

                                        clearable=True,

                                        multi=True,

                                        className="text-dark",

                                    ),

                                ],

                                md=3,

                            ),


                            # ==================================
                            # RESET
                            # ==================================

                            dbc.Col(
                                [

                                    html.Label(
                                        "Actions",
                                        className=(
                                            "fw-semibold mb-1"
                                        ),
                                    ),

                                    dbc.Button(
                                        "↻  Reset Filters",
                                        id="reset-button",
                                        color="info",
                                        className=(
                                            "w-100 fw-bold"
                                        ),
                                    ),

                                ],

                                md=3,

                            ),

                        ],

                        className="g-3",

                    ),

                ]
            ),

            className="shadow border-0 mb-4",

        ),


        # ====================================================
        # KPIs
        # ====================================================

        section_title(
            "1",
            "Key Performance Indicators",
        ),

        dbc.Row(
            [

                dbc.Col(
                    kpi_card(
                        "Total Passengers",
                        "kpi-passengers",
                        "👥",
                    ),
                    md=3,
                ),

                dbc.Col(
                    kpi_card(
                        "Total Survivors",
                        "kpi-survivors",
                        "✓",
                    ),
                    md=3,
                ),

                dbc.Col(
                    kpi_card(
                        "Survival Rate",
                        "kpi-rate",
                        "%",
                    ),
                    md=3,
                ),

                dbc.Col(
                    kpi_card(
                        "Average Fare",
                        "kpi-fare",
                        "$",
                    ),
                    md=3,
                ),

            ],

            className="g-3 mb-4",

        ),


        # ====================================================
        # TRENDS
        # ====================================================

        section_title(
            "2",
            "Trends and Comparisons",
        ),

        dbc.Row(
            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="age-chart",
                                config={
                                    "displayModeBar": False
                                },
                            )
                        ),
                        className="shadow border-0",
                    ),

                    md=6,
                ),


                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="class-chart",
                                config={
                                    "displayModeBar": False
                                },
                            )
                        ),
                        className="shadow border-0",
                    ),

                    md=6,
                ),

            ],

            className="g-3 mb-4",

        ),


        # ====================================================
        # DETAILED ANALYSIS
        # ====================================================

        section_title(
            "3",
            "Detailed Analysis",
        ),

        dbc.Row(
            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="embarked-chart",
                                config={
                                    "displayModeBar": False
                                },
                            )
                        ),
                        className="shadow border-0",
                    ),

                    md=4,
                ),


                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="scatter-chart",
                                config={
                                    "displayModeBar": False
                                },
                            )
                        ),
                        className="shadow border-0",
                    ),

                    md=4,
                ),


                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id="ticket-chart",
                                config={
                                    "displayModeBar": False
                                },
                            )
                        ),
                        className="shadow border-0",
                    ),

                    md=4,
                ),

            ],

            className="g-3 mb-4",

        ),


        # ====================================================
        # FOOTER
        # ====================================================

        html.Hr(),

        html.P(
            "Dashboard built with Python, Pandas, "
            "Plotly and Dash.",
            className=(
                "text-center text-secondary mb-4"
            ),
        ),

    ],

    fluid=True,

    className="px-4 py-2",
)


# ============================================================
# CALLBACK
# ============================================================

@app.callback(

    # FILTER VALUES
    Output(
        "sex-filter",
        "value",
    ),

    Output(
        "class-filter",
        "value",
    ),

    Output(
        "embarked-filter",
        "value",
    ),

    # KPIs
    Output(
        "kpi-passengers",
        "children",
    ),

    Output(
        "kpi-survivors",
        "children",
    ),

    Output(
        "kpi-rate",
        "children",
    ),

    Output(
        "kpi-fare",
        "children",
    ),

    # CHARTS
    Output(
        "class-chart",
        "figure",
    ),

    Output(
        "age-chart",
        "figure",
    ),

    Output(
        "embarked-chart",
        "figure",
    ),

    Output(
        "scatter-chart",
        "figure",
    ),

    Output(
        "ticket-chart",
        "figure",
    ),

    # INPUTS
    Input(
        "sex-filter",
        "value",
    ),

    Input(
        "class-filter",
        "value",
    ),

    Input(
        "embarked-filter",
        "value",
    ),

    Input(
        "reset-button",
        "n_clicks",
    ),

)
def update_dashboard(
    sex,
    pclass,
    embarked,
    n_clicks,
):

    # ========================================================
    # RESET
    # ========================================================

    if ctx.triggered_id == "reset-button":

        sex = None
        pclass = None
        embarked = None


    # ========================================================
    # FILTER DATA
    # ========================================================

    filtered = filter_data(
        df,
        sex,
        pclass,
        embarked,
    )


    # ========================================================
    # KPIs
    # ========================================================

    total = len(filtered)

    survivors = (
        int(
            filtered["Survived"].sum()
        )
        if total
        else 0
    )

    rate = (
        survivors / total * 100
        if total
        else 0
    )

    avg_fare = (
        filtered["Fare"].mean()
        if total
        else 0
    )


    # ========================================================
    # RETURN
    # ========================================================

    return (

        sex,
        pclass,
        embarked,

        f"{total:,}",

        f"{survivors:,}",

        f"{rate:.1f}%",

        f"${avg_fare:,.2f}",

        bar_chart(
            filtered,
            "Pclass",
            "Passengers & Survivors by Class",
            "Class",
        ),

        age_histogram(
            filtered
        ),

        bar_chart(
            filtered,
            "Embarked",
            "Survival by Embarkation",
            "Embarked",
        ),

        fare_age_scatter(
            filtered
        ),

        top_tickets(
            filtered
        ),

    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
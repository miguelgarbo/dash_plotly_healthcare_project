from dash import dcc, Input, Output, Dash, clientside_callback, State, html
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd
from dash_iconify import DashIconify

def load_file():

    df = pd.read_csv("assets/healthcare.csv")

    billAmountCol = df["Billing Amount"]
    dateAdCol = df["Date of Admission"]

    billAmountCol = pd.to_numeric(billAmountCol, errors='coerce')
    dateAdCol = pd.to_datetime(dateAdCol)
    # creating a new column, will help to do the analysis with this field
    # dt = data type, as our dataAdCol is now a datetime we can take the month by it
    df["YearMonth"] = dateAdCol.dt.to_period("M")

    return df


data = load_file()

number_records = len(data)
average_billing = data["Billing Amount"].mean()


# test data for radio group
data_fake = [["react", "React"], ["ng", "Angular"],
             ["svelte", "Svelte"], ["vue", "Vue"]]

# Creating a web app with dash
app = Dash()

theme_toggle =  dmc.ActionIcon(
                    [
                        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
                        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
                    ],
                    variant="transparent",
                    color="yellow",
                    id="color-scheme-toggle",
                    size="lg",
                )


def pageMain() -> dmc.Flex: return dmc.Flex([
            dmc.Flex([dmc.Title
                      ("HealthCare DashBoard", order=2, fw=700,
                       style={"border-bottom": "1px solid var(--mantine-color-red-6)"}),

                      DashIconify(icon="mdi:medical-bag", width=28,
                                  height=28, style={"marginLeft": "10px"}),
                      
                     theme_toggle, 

                      ], 
                                        
                     justify="space-between",
                     align="center",
                     direction="row",
                     ),

            dmc.Flex([
                dmc.Title
                    (f"Total Patient Records: {number_records}", order=3, fw=700, ta="center", mt=30),
                 dmc.Title
                    (f"Average Billing Amount: {average_billing}", order=3, fw=700, ta="center")

                 ], direction="column", gap=20, ta="center"),


            dmc.Flex([dmc.Select(

                            placeholder="Select a Gender",
                            id="gender-filter",
                            value=None,
                            data=[
                                {"label": gender, "value": gender} for gender in data['Gender'].unique()],
                            w=200,
                        ),

                # Hospital Statistics

                # Male or female demographics
                dmc.Flex([
                    dmc.Flex([

                        dmc.Title
                        ("Patient Demographics", order=4),
                        dcc.Graph(id="age-distribution")
                    ],
                        direction="column", gap="1vw", className="border"

                    ),
                    dmc.Flex([

                        dmc.Title
                        ("Medical Condition Distribution", order=4),
                        dcc.Graph(id="condition-distribution")

                    ],
                        direction="column", className="border"
                    )

                ], direction="row", mt=40, gap="2vw", wrap="wrap"),

                dmc.Flex([
                    # Insurance provider data

                    dmc.Flex([
                        dmc.Title
                        ("Insurance Provider Comparison", order=4),
                        dcc.Graph(id="insurance-comparision"),
                    ], direction="column", className="border"),

                    # Billing Distribution
                    dmc.Flex([
                        dmc.Title
                        ("Billing Distribution", order=4),

                        dcc.Slider(
                            id="billing-slider",
                            min=data["Billing Amount"].min(),
                            max=data["Billing Amount"].max(),
                            value=data["Billing Amount"].median(),
                            marks={int(value): f'${int(value):,}' for value in data['Billing Amount'].quantile(
                                [0, 0.25, 0.5, 0.75, 1]).values},
                            step=100
                        ),

                        dcc.Graph(id="billing-distribution"),
                    ], direction="column", gap="1vw", className="border")

                ], direction="row", gap='2vw', wrap="wrap"),

                dmc.Flex([
                    dmc.Flex([
                        dmc.Title
                        ("Trends In Admission", order=4),

                        dmc.RadioGroup(
                            children=dmc.Group([dmc.Radio("Line Chart", value="line"),
                                                dmc.Radio(
                                                    "Bar Chart", value="bar")
                                                ]),
                            id="chart-type",
                            value="line",
                            size="sm",
                            mb=10,
                        ),

                        dmc.Select(
                            placeholder="Select a Medical Conditional",
                            id="condition-filter",
                            value="pd",
                            data=[
                                {"value": condition, "label": condition}
                                for condition in data["Medical Condition"].unique()
                            ],
                            w=200,
                            mb=10,
                        ),
                        dcc.Graph(id="admission-trends")

                    ], direction="column", className="border"),

                    
                ], gap="2vw")

            ], gap=30, direction="column", id="main_card", wrap="wrap"),


        ],justify="center", align="center", mt="35px", direction="column", ta="center", pl="5vw", pr="5vw", wrap="wrap",
        )


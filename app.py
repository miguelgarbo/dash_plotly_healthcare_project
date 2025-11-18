from dash import dcc, Input, Output, Dash, clientside_callback, State
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd
from dash_iconify import DashIconify
import pageMain


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


app.layout = dmc.MantineProvider(
    theme="light",
    children=[
        
        dmc.Flex(dmc.Button(
                        # props as configured above:
                        "Abrir Pagina",
                        id='button-page',
                        variant="filled",
                        color="blue",
                        size="lg",
                        radius="md",
                        loading=False,
                        disabled=False,
                        # other props...
)), 
    dmc.AppShell([
        
        dmc.AppShellMain(children=[
            
            ], id='page')
    ])
        
        
    ]
)

#Create our Events / CallBacks
#testando callback com botao

#callbacks da pagina main

@app.callback(
    Output("age-distribution","figure"),
    Input("gender-filter","value")
)
def update_distribution(selected_gender):
    
    gender  = data["Gender"]
    
    if selected_gender:
        filtered_data = data[gender == selected_gender]
    else:
        filtered_data = data
    
    if filtered_data.empty:
        return {}
    
    fig = px.histogram(
        filtered_data,
        x="Age",
        nbins=10,
        color="Gender",
        title="Age Distribution By Gender",
        color_discrete_sequence=["blue","red"]     
    )
    
    return fig
    

@app.callback(
    Output("condition-distribution","figure"),
    Input("gender-filter","value")
)
def update_medical_conditional(selected_gender):
    
    gender =  data["Gender"]
    
    filtered_data = data[gender == selected_gender] if selected_gender else data
    
    fig = px.pie(filtered_data,
                 names="Medical Condition",
                 title="Medical Condition Distribution")
    
    
    return fig


#Insurance Provider Comparison
@app.callback(
    Output("insurance-comparision","figure"),
    Input("gender-filter","value")
)
def update_insurances_provider(selected_gender):
    
    filtered_data = data[data["Gender"]==selected_gender] if selected_gender else data
    
    fig = px.bar(
        filtered_data, x="Insurance Provider", y="Billing Amount", color="Medical Condition",
        barmode="group",
        title="Insurance Provider Price Comparison",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
       
    return fig

#Billing Distribution
@app.callback(
    Output("billing-distribution","figure"),
    [Input("billing-slider", "value"),
     Input("gender-filter","value")]
)
def update_billing_distribution(slider_value, selected_gender):
    
    gender = data["Gender"]
    
    filtered_data = data[gender== selected_gender] if selected_gender else data
    
    filtered_data = filtered_data[filtered_data["Billing Amount"] <= slider_value]    
    
    fig = px.histogram(filtered_data, x="Billing Amount", 
                       nbins=10, title="Billing Amount Distribution")
    
    return fig


def change_type_chart(type, final_chart):
    title_value = "Admission Trends Over Time"
    
    if(type =="line"):
        fig = px.line(final_chart, x="YearMonth",y="Count",title=title_value)
    else:
        fig = px.bar(final_chart, x="YearMonth", y="Count", title=title_value)
        
    return fig


#Trends In Admission
@app.callback(
    Output("admission-trends","figure"),
    [Input("chart-type", "value"),
     Input("condition-filter", "value")]
)
def update_trends_admission(chart_type, med_conditional_value):
    
    med_condition = data["Medical Condition"]
    
    filtered_data = data[med_condition == med_conditional_value] if med_conditional_value else data
    
    trend_df = filtered_data.groupby("YearMonth").size().reset_index(name="Count")
    trend_df['YearMonth'] = trend_df['YearMonth'].astype(str)
    
        
    return change_type_chart(chart_type, trend_df)
    

clientside_callback(
    """
    (n) => {
        document.documentElement.setAttribute(
            'data-mantine-color-scheme',
            (n % 2) ? 'dark' : 'light'
        );
        
        theme = document.documentElement.getAttribute('data-mantine-color-scheme');
        const mainCard = document.querySelector(".default");
        
        pink_hover = document.querySelectorAll("div.pink-hover");
        blue_hover = document.querySelectorAll("div.blue-hover");
    
        const borders = document.querySelectorAll(".border");
        
        if(theme == 'dark'){
              borders.forEach(border =>{
            
            console.log("...");
           border.classList.toggle("border-night"); 
            mainCard.classList.toggle("default-night");

        });   
        
        
        }else{
             borders.forEach(border =>{
            
            console.log("...");
            border.classList.remove("border-night");

        });     
        
            mainCard.classList.remove("default-night");
        
        }

        return window.dash_clientside.no_update      
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "n_clicks"),
)

@app.callback(
    Output("main_card", "className"),
    Input("gender-filter", "value"),
)
def expose_filter_gender(selected_gender):
    
    if selected_gender:
        if selected_gender == "Female":
            print("aqui woman")
            return "default pink-hover"
        else:
            print("aqui man")

            return "default blue-hover"
    else:
            return 'default'

##fim callbacks pagina main

@app.callback(
    Output("page", "children"),
    Input("button-page", "n_clicks")
)
def render_page(n_clicks):
    print(n_clicks)
    
    if(n_clicks ==None):
        n_clicks =0
   
    if(n_clicks >= 1):

            return pageMain.pageMain()
    
    

    

        
    
app.run(host="0.0.0.0", port=8050)

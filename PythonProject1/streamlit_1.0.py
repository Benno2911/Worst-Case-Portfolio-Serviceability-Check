import streamlit as st
import numpy as np
import pandas as pd

def calc_liquid_share(decline,init_donation,donation_factor,guaranteed_share,simulation_years):
    #decline=np.array(decline) #not necessary since numPy does this automatically
    num_scenarios = len(decline)
    total_portfolio_value=np.full(num_scenarios,1) #calculate everything in % of total portfolio value at start
    values=np.full((num_scenarios,4),0.25) #order: stocks, bonds, flat berlin, flat potsdam
    #loan_bank=0.5*0.3 #30% of flat price from bank loan
    yearly_repayment_bank=0.5*0.3/simulation_years #repayment of 10% of flat price per year, adds up to whole loan
    last_donation=np.full(num_scenarios,init_donation) #% of total portfolio value at the start as donation

    values=values*(1-decline)
    value_liquid=values[:,1]+values[:,0] #assets used for donations and repayments
    value_flats=values[:,2]+values[:,3] #assets untouched by donations and repayments

    for i in range(1,simulation_years+1): # years of simulation
        next_donation=last_donation*donation_factor+total_portfolio_value*guaranteed_share #calculate donation
        value_liquid = value_liquid - next_donation - yearly_repayment_bank #new asset values for donations and repayments
        last_donation=next_donation #update donation
        # no check for liquid_value>0 needed since it can't increase at any point
        total_portfolio_value = value_liquid + value_flats # update portfolio value
    return value_liquid,total_portfolio_value

@st.cache_data
def generate_scenarios(num_scen, min_dec, max_dec):
    return (np.random.randint(low=min_dec*100, high=(max_dec*100)+1, size=(num_scen, 4))) / 100.0

### Streamlit setup

st.set_page_config(page_title="Worst-Case Portfolio Serviceability Check", layout="wide")
st.title("Worst-Case Portfolio Serviceability Check")

with st.sidebar:
    st.header("parameter:")

    num_scenarios = st.slider(
        "number of scenarios",
        min_value=1000,
        max_value=50000,
        value=1000,
        step=500
    )
    decline_range = st.slider(
        "range of decline",
        min_value=0.00,
        max_value=0.99,
        value=(0.10,0.50),
        step=0.01,
        format="%.2f"
    )
    min_decline = decline_range[0]
    max_decline=decline_range[1]
    st.markdown("Declines are generated randomly between "+ str(min_decline * 100) +"% and "+ str(max_decline * 100) +"%.")

    with st.expander("additional parameter:"):
        don_factor = st.slider(
            "% of donation from previous year as new donation",
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        don_init = st.slider(
            "% of portfolio assumed for initial donation",
            min_value=0,
            max_value=100,
            value=5,
            step=1
        )
        guar_share = st.slider(
            "% of start-of-the-year portfolio value as guaranteed donation",
            min_value=0.0,
            max_value=20.0,
            value=2.5,
            step=0.5
        )
        sim_len = st.slider(
            "number of years to simulate",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )

scenarios_data = generate_scenarios(num_scenarios, min_decline, max_decline)
residual_liquid,portfolio_total = calc_liquid_share(scenarios_data,don_init/100.0,don_factor/100.0,guar_share/100.0,sim_len)
solvable_relative = (np.sum(residual_liquid>0)/num_scenarios)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Number of scenarios",
        value=f"{num_scenarios:,}".replace(",", ".")
    )
with col2:
    st.metric(
        label="Number of serviceable scenarios",
        value=f"{np.sum(residual_liquid>0):,}".replace(",", ".")
    )

st.progress(solvable_relative, text=f"{solvable_relative*100:.2f}% of scenarios are serviceable.")

#add visualizations
bins = np.arange(-0.20, 0.20, 0.01)
hist_values, bin_edges = np.histogram(residual_liquid,bins=bins)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
x_ticks = []
for center in bin_centers:
    x_ticks.append(f"{round(center * 100)}%")
df_hist = pd.DataFrame({
    'Scenario_share': hist_values/num_scenarios
}, index=x_ticks)

st.header("Distribution of liquid assets in % of starting value")
st.bar_chart(
    height=600,
    data=df_hist,
    sort=False,
    x_label='% of starting portfolio value',
    y_label='share of scenarios'
)

import numpy as np
import pandas as pd

def count_serviceable_scenarios(decline)->int:
    #decline=np.array(decline) #not necessary since numPy does this automatically
    num_scenarios = len(decline)
    total_portfolio_value=np.full(num_scenarios,1) #calculate everything in % of total portfolio value at start
    values=np.full((num_scenarios,4),0.25) #order: stocks, bonds, flat berlin, flat potsdam
    #loan_bank=0.5*0.3 #30% of flat price from bank loan
    yearly_repayment_bank=0.5*0.1 #repayment of 10% of flat price per year, adds up to whole loan
    last_donation=np.full(num_scenarios,0.05) #5% of total portfolio value at the start as assumption

    values=values*(1-decline) #update values
    value_liquid=values[:,1]+values[:,0] #assets used for donations and repayments
    value_flats=values[:,2]+values[:,3] #assets untouched by donations and repayments

    for i in range(1,4): # 3 years of simulation
        next_donation=last_donation*0.5+total_portfolio_value*0.025 #calculate donation
        value_liquid = value_liquid - next_donation - yearly_repayment_bank #new asset values for donations and repayments
        last_donation=next_donation #update donation
        # no check for liquid_value>0 needed since it can't increase at any point
        total_portfolio_value = value_liquid + value_flats # update portfolio value
    return np.sum(value_liquid>0)

dec=(np.random.randint(low=10, high=71, size=(100, 4))) / 100.0
#dec=(np.random.randint(size=(100,4),low=10, high=71))/100.0 #randomly initialize decline df with values 10% - 70%
print(str(count_serviceable_scenarios(dec)/len(dec))+"% of scenarios are serviceable")

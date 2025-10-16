decline=(1/3,0.2,0.1,0.1) #example from the task
total_portfolio_value=1 #calculate everything in % of total portfolio value at start
value_stocks=0.25 #stocks make up 25%
value_bonds=0.25 #bonds make up 25%
value_flat_berlin=0.25 #flat in berlin makes up 25%
value_flat_potsdam=0.25 #flat in potsdam makes up 25%

loan_bank=0.5*0.3 #30% of flat price from bank loan
yearly_repayment_bank=0.5*0.1 #repayment of 10% of flat price per year, adds up to whole loan
last_donation=0.05 #5% of total portfolio value at the start as assumption

value_stocks=value_stocks*(1-decline[0]) #update values
value_bonds=value_bonds*(1-decline[1])
value_flat_berlin=value_flat_berlin*(1-decline[2])
value_flat_potsdam=value_flat_potsdam*(1-decline[3])
value_liquid=value_bonds+value_stocks #assets used for donations and repayments
value_flats=value_flat_berlin+value_flat_potsdam #assets untouched by donations and repayments
print(value_stocks)

for i in range(1,4): # 3 years of simulation
    next_donation=last_donation*0.5+total_portfolio_value*0.025 #calculate donation
    value_liquid = value_liquid - next_donation - yearly_repayment_bank #new asset values for donations and repayments
    last_donation=next_donation
    if value_liquid>=0: #if donations and repayments are possible
        total_portfolio_value = value_liquid + value_flats
    else:
        total_portfolio_value = -1
    print(str(round(total_portfolio_value*100,2))+ "% left total after year "+str(i))
    print(str(round(value_liquid*100,2))+ "% left liquid after year "+str(i))

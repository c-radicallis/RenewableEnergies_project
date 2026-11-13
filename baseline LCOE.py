# ---- Inputs (justified, see sources) ----
efficency_thermal = 0.36          # Statement Table 1
LHV = 11.25e3                     # Wh/kg  (Statement Table 1)
rho = 0.95                        # kg/L   (Statement Table 1)
EFHFO = 3.15                      # kgCO2/kgHFO (Statement Table 1)
P_base = 4e6 # Base Load = 4 MW
P_peak = 11.5e6 # Peak Load = 11.5 MW
AEP = 67976.55e6 #Wh/yr

t = 20                            # years (Statement §4.1)
r = 0.065                          # Spanish regulated returns 5.58-7.09% (BOE-A-2019-16862) + island risk
fuel_euro_per_L = 0.60            # Las Palmas HSFO 664 $/t (11/11/2026), 1.106 $/€, rho 0.95, +5% shipping
fuel_euro_per_kgHFO = fuel_euro_per_L / rho
carbon_euro_per_kgCO2 = 86.65/1e3    # EU ETS Dec-26 EUA 86.69 €/t (Platts, 6/11/2026)

OPEX_fixed_percentage = 0.04      # Statement Table 2
d = 0.003                         # Statement Table 2 (applied to efficiency)
CAPEX_euro_per_kW = 1200   # basis for fixed OPEX only; baseline CAPEX = 0 (sunk, §4.2)


# Calculating baeline Thermal LCOE
fuel_eWh_per_kgHFO = LHV * efficency_thermal #eletric energy per kg of HFO
fuel_euro_per_Wh = fuel_euro_per_kgHFO/fuel_eWh_per_kgHFO
print("Fuel cost (€/MWh) = %.1f" %(fuel_euro_per_Wh*1e6))

fuel_eWh_per_kgCO2 = fuel_eWh_per_kgHFO / EFHFO
carbon_euro_per_Wh = carbon_euro_per_kgCO2 / fuel_eWh_per_kgCO2 # €/Wh
print("Carbon tax (€/MWh) = %.1f" %(carbon_euro_per_Wh*1e6)) 

OPEX_variable = AEP*(fuel_euro_per_Wh + carbon_euro_per_Wh) # €/year
print("OPEX variable (M€/year) = %.1f" %(OPEX_variable*1e-6))

CAPEX = P_peak*CAPEX_euro_per_kW/1000 # W * €/W
print("CAPEX (M€) = %.1f" %(CAPEX*1e-6))

OPEX_fixed = CAPEX*OPEX_fixed_percentage  # €/year
print("OPEX fixed (M€/year) = %.1f" %(OPEX_fixed*1e-6))

# ---- Baseline LCOE ----
E = AEP / 1e6                                                                        # MWh/yr
years = range(t)
discounted_costs = []
discounted_energy = []

for year in years:

    cost_n = (OPEX_fixed+OPEX_variable) / ((1+r)**year)

    AEP_n = AEP * (1-d)**year
    energy_n = AEP_n / ((1+r)**year)

    # Discounting
    discounted_costs.append(cost_n)
    discounted_energy.append(energy_n)

LCOE = sum(discounted_costs) / sum(discounted_energy)
print(f"\n Baseline Thermal LCOE: {LCOE*1e6:.2f} €/MWh")


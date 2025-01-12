import CoolProp.CoolProp as CP

refrigerant = 'R410A'
T_evap_C = 15 # Evaporator temperature in °C
T_cond_C = 68 # Condenser temperature in °C

# Define efficiencies and pressure drops
compressor_efficiency = 0.6 # Isentropic efficiency of the compressor
evaporator_pressure_drop = 0.4*100000 #in Pascal
condenser_pressure_drop = 0.4*100000 #in Pascal

T_evap = T_evap_C + 273.15
T_cond = T_cond_C + 273.15

superheat = 5
supercool = superheat

P4 = CP.PropsSI('P', 'T', T_evap , 'Q', 0, refrigerant)

P1 = P4 - evaporator_pressure_drop
T1 = T_evap + superheat
H1 = CP.PropsSI('H', 'P', P1, 'Q', 1, refrigerant)
S1 = CP.PropsSI('S', 'T', T1, 'Q', 1, refrigerant)

P3 = CP.PropsSI('P', 'T', T_cond , 'Q', 0, refrigerant)

P2 = P3 + condenser_pressure_drop
H2iso = CP.PropsSI('H', 'P', P2, 'S', S1, refrigerant)
H2 = H1 + (H2iso - H1)/compressor_efficiency
T2 = CP.PropsSI('T', 'P', P2, 'H', H2, refrigerant)
S2 = CP.PropsSI('S', 'T', T2, 'P', P2, refrigerant)

T3 = T_cond - supercool
H3 = CP.PropsSI('H', 'P', P3, 'Q', 0, refrigerant)
S3 = CP.PropsSI('S', 'H', H3, 'P', P3, refrigerant)

T4 = T_evap
H4 = H3
H4_l = CP.PropsSI('H', 'T', T4, 'Q', 0, refrigerant)
H4_v = CP.PropsSI('H', 'T', T4, 'Q', 1, refrigerant)
X4 = (H4-H4_l)/(H4_v-H4_l) #vapor quality at 4
S4 = CP.PropsSI('S', 'T', T4, 'Q', 1, refrigerant)

COP = (H2- H3) / (H2 - H1)

print(f"State 1 - T= {T1:.2f} K, P={P1/1000:.2f} kPa, H={H1/1000:.2f} kJ/kg, S={S1:.2f} J/K")
print(f"State 2 - T= {T2:.2f} K, P={P2/1000:.2f} kPa, H={H2/1000:.2f} kJ/kg, S={S2:.2f} J/K")
print(f"State 3 - T= {T3:.2f} K, P={P3/1000:.2f} kPa, H={H3/1000:.2f} kJ/kg, S={S3:.2f} J/K")
print(f"State 4 - T= {T4:.2f} K, P={P4/1000:.2f} kPa, H={H4/1000:.2f} kJ/kg, S={S4:.2f} J/K Q={X4:.2f}")
print(f"COP = {COP:.2f}")
# Aircraft Performance Calculator with User Input

def calculate_range(fuel_capacity, fuel_consumption_rate, true_air_speed):
    range_in_hours = fuel_capacity / fuel_consumption_rate
    range_in_miles = range_in_hours * true_air_speed
    return range_in_miles

def calculate_endurance(fuel_capacity, fuel_consumption_rate):
    return fuel_capacity / fuel_consumption_rate

def calculate_total_weight(payload_weight, fuel_weight, empty_weight, crew_weight):
    return payload_weight + fuel_weight + empty_weight + crew_weight

def calculate_cg_position(moment_list, total_weight):
    total_moment = sum(moment_list)
    return total_moment / total_weight

def calculate_lift(cl, rho, v, s):
    return 0.5 * cl * rho * v**2 * s

def calculate_drag(cd, rho, v, s):
    return 0.5 * cd * rho * v**2 * s

def calculate_weight(mass, g=9.81):
    return mass * g

def calculate_acceleration(thrust, drag, weight, mass):
    return (thrust - drag - weight) / mass

def calculate_velocity(velocity, acceleration, time):
    return velocity + acceleration * time

def calculate_displacement(velocity, time):
    return velocity * time

# ================= USER INPUTS =================
fuel_capacity = float(input("Enter fuel capacity (gallons): "))
fuel_consumption_rate = float(input("Enter fuel consumption rate (gallons/hour): "))
true_air_speed = float(input("Enter true air speed (knots): "))
payload_weight = float(input("Enter payload weight (pounds): "))
fuel_weight = float(input("Enter fuel weight (pounds): "))
empty_weight = float(input("Enter empty weight (pounds): "))
crew_weight = float(input("Enter crew weight (pounds): "))

moment_list = [float(x) for x in input("Enter moments (comma-separated): ").split(",")]

cl = float(input("Enter lift coefficient (Cl): "))
rho = float(input("Enter air density (kg/m^3): "))
v = float(input("Enter velocity (m/s): "))
s = float(input("Enter wing area (m^2): "))
cd = float(input("Enter drag coefficient (Cd): "))
mass = float(input("Enter aircraft mass (kg): "))
thrust = float(input("Enter thrust (N): "))
drag = float(input("Enter drag (N): "))
velocity = float(input("Enter initial velocity (m/s): "))
acceleration = float(input("Enter acceleration (m/s^2): "))
time = float(input("Enter time (s): "))

# ================= CALCULATIONS =================
range_val = calculate_range(fuel_capacity, fuel_consumption_rate, true_air_speed)
endurance = calculate_endurance(fuel_capacity, fuel_consumption_rate) 
total_weight = calculate_total_weight(payload_weight, fuel_weight, empty_weight, crew_weight)
cg_position = calculate_cg_position(moment_list, total_weight)
lift = calculate_lift(cl, rho, v, s)
drag_force = calculate_drag(cd, rho, v, s)
weight = calculate_weight(mass)
acceleration_val = calculate_acceleration(thrust, drag, weight, mass)
velocity_val = calculate_velocity(velocity, acceleration_val, time)
displacement = calculate_displacement(velocity_val, time)

# ================= OUTPUT =================
print("\n--- Aircraft Performance Results ---")
print(f"Range: {range_val:.2f} miles")
print(f"Endurance: {endurance:.2f} hours")
print(f"Total Weight: {total_weight:.2f} pounds")
print(f"CG Position: {cg_position:.2f} feet")
print(f"Lift: {lift:.2f} N")
print(f"Drag: {drag_force:.2f} N")
print(f"Weight: {weight:.2f} N")
print(f"Acceleration: {acceleration_val:.2f} m/s^2")
print(f"Velocity: {velocity_val:.2f} m/s")
print(f"Displacement: {displacement:.2f} m")

import random

# Q-table initialization
actions = ["adjust_sodium_limit", "adjust_fluid_intake", "modify_physical_activity", "update_diet", "restrict_alcohol"]
q_table = {action: 0.0 for action in actions}

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.2
q_threshold = 0.5  # Minimum Q-value to select an action

def calculate_difference(old_state, new_state):
    """Calculate differences between old and new states."""
    return {
        "serum_creatinine_change": new_state["serum_creatinine"] - old_state["serum_creatinine"],
        "gfr_change": new_state["gfr"] - old_state["gfr"],
        "hematuria_change": new_state["hematuria"] - old_state["hematuria"],
        "bun_change": new_state["bun"] - old_state["bun"],
        "serum_calcium_change": new_state["serum_calcium"] - old_state["serum_calcium"],
        "oxalate_levels_change": new_state["oxalate_levels"] - old_state["oxalate_levels"],
        "blood_pressure_change": new_state["blood_pressure"] - old_state["blood_pressure"],
        "urine_ph_change": new_state["urine_ph"] - old_state["urine_ph"],
    }

def select_actions(difference, epsilon):
    """Select multiple actions based on epsilon-greedy and Q-values."""
    selected_actions = []
    for action in actions:
        if random.uniform(0, 1) < epsilon or q_table[action] > q_threshold:
            selected_actions.append(action)
    return selected_actions if selected_actions else [random.choice(actions)]

def update_q_table(selected_actions, reward):
    """Update Q-values for all selected actions."""
    reward_per_action = reward / len(selected_actions)
    for action in selected_actions:
        q_table[action] += learning_rate * (reward_per_action + discount_factor * max(q_table.values()) - q_table[action])

def dynamic_adjustment(old_state, difference):
    """Determine dynamic adjustment values based on patient metrics."""
    adjustments = {
        "sodium_limit_adjustment": max(0.1, min(0.5, 0.1 * abs(difference["gfr_change"]))),
        "fluid_intake_adjustment": max(0.2, min(0.6, 0.2 * abs(difference["serum_creatinine_change"]))),
        "physical_activity_change": "Strength exercises adjusted to twice a week" if old_state["blood_pressure"] > 140 else "Aerobic exercises thrice a week",
        "diet_change": "Low-protein diet with fruits and vegetables" if old_state["bun"] > 20 else "Balanced diet",
        "alcohol_limit_change": "Strictly no alcohol" if old_state["ana"] == 1 else "Limit alcohol to occasional"
    }
    return adjustments

# Workflow
while True:
    # Input old state
    old_state = {
        "serum_creatinine": float(input("Enter old serum_creatinine: ")),
        "gfr": float(input("Enter old gfr: ")),
        "hematuria": int(input("Enter old hematuria (0 or 1): ")),
        "serum_calcium": float(input("Enter old serum_calcium: ")),
        "ana": int(input("Enter old ana: ")),
        "oxalate_levels": float(input("Enter old oxalate_levels: ")),
        "blood_pressure": float(input("Enter old blood_pressure: ")),
        "urine_ph": float(input("Enter old urine_ph: ")),
        "bun": float(input("Enter old bun: ")),
    }
    
    # Input treatment plan
    treatment_plan = {
        "sodium_limit": float(input("Enter sodium limit (grams): ")),
        "fluid_intake": float(input("Enter fluid intake (liters): ")),
        "physical_activity": input("Enter physical activity: "),
        "diet": input("Enter diet: "),
        "alcohol_limit": input("Enter alcohol limit: ")
    }
    
    # Input new state
    new_state = {
        "serum_creatinine": float(input("Enter new serum_creatinine: ")),
        "gfr": float(input("Enter new gfr: ")),
        "hematuria": int(input("Enter new hematuria (0 or 1): ")),
        "serum_calcium": float(input("Enter new serum_calcium: ")),
        "ana": int(input("Enter new ana: ")),
        "oxalate_levels": float(input("Enter new oxalate_levels: ")),
        "blood_pressure": float(input("Enter new blood_pressure: ")),
        "urine_ph": float(input("Enter new urine_ph: ")),
        "bun": float(input("Enter new bun: "))
    }
    
    # Calculate difference
    difference = calculate_difference(old_state, new_state)
    print(f"Difference: {difference}")
    
    # Select actions
    selected_actions = select_actions(difference, epsilon)
    print(f"Actions chosen: {selected_actions}")
    
    # Determine dynamic adjustments
    adjustments = dynamic_adjustment(old_state, difference)
    
    # Apply actions to treatment plan dynamically
    for action in selected_actions:
        if action == "adjust_sodium_limit":
            treatment_plan["sodium_limit"] -= adjustments["sodium_limit_adjustment"]
        elif action == "adjust_fluid_intake":
            treatment_plan["fluid_intake"] -= adjustments["fluid_intake_adjustment"]
        elif action == "modify_physical_activity":
            treatment_plan["physical_activity"] = adjustments["physical_activity_change"]
        elif action == "update_diet":
            treatment_plan["diet"] = adjustments["diet_change"]
        elif action == "restrict_alcohol":
            treatment_plan["alcohol_limit"] = adjustments["alcohol_limit_change"]
    
    print(f"Updated Treatment Plan: {treatment_plan}")
    
    # Calculate reward
    reward = (new_state["gfr"] - old_state["gfr"]) - 5 * new_state["hematuria"]
    print(f"Reward: {reward}")
    
    # Update Q-table
    update_q_table(selected_actions, reward)
    print(f"Updated Q-table: {q_table}")
    
    # Continue or exit
    cont = input("Continue? (yes/no): ")
    if cont.lower() != "yes":
        break

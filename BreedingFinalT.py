import pandas as pd
import tkinter as tk
from tkinter import messagebox
from itertools import combinations
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Read the DataFrame from CSV
df = pd.read_csv("PalsPowerFrame.csv")

# T: Sort to optimize searching (because why fucking not?)
df['Power'] = df['Power'].astype(int)  # PD is stupid sometimes
df = df.sort_values(by='Power', ascending=False)
# print(df)


# T: Function fto get list all of my pals
available_pals = list(range(1, 12))+list(range(13, 23))+list(range(25, 29))+list(range(30, 34))+list(range(35, 40)) + \
    list(range(42, 44))+list(range(42, 44)) + \
    [47, 59, 65, 64, 67, 68, 71, 86, 97, 103]+list(range(52, 56))
pall_names = []
pall_powers = []
for i in available_pals:
    pal = df.loc[df['PDN'] == i].iloc[0]['Name']
    pal_power = df.loc[df['PDN'] == i].iloc[0]['Power']
    pall_names.append(pal)
    pall_powers.append(pal_power)
print(pall_names)
print(f"Available range: {min(pall_powers)}-{max(pall_powers)}")


# T: Loading palmap
maps = pd.read_csv("Map.csv")
maps = maps.sort_values(by='palres')


# Function to handle breeding button click
def breed_pals(pokemon_a_name, pokemon_b_name):

    # Find powers of Pokemon A and Pokemon B
    pokemon_a_power = df.loc[df['Name'] == pokemon_a_name, 'Power'].iloc[0]
    pokemon_b_power = df.loc[df['Name'] == pokemon_b_name, 'Power'].iloc[0]

    # Calculate the average power (PowerD)
    result_power = ((pokemon_a_power + pokemon_b_power) / 2)

    # Find the pokemon with the closest power to PowerD
    closest_pokemon = None
    closest_pokemon_pdn = None
    closest_distance = float('inf')  # Initialize with a large value

    # T: Just get a needed pal, no need for hard things :)
    closest_index = (df['Power'] - result_power).abs().idxmin()
    result_df = df.loc[[closest_index]].iloc[0]

    print(result_power)
    print(result_df)
    # print(result_df)
    # Show result in a message box
    return result_df


def seq_butt():
    target_pokemon = entry_target.get()
    pal = df.loc[df['Name'] == target_pokemon].iloc[0]

    if pal["Power"] in range(min(pall_powers), max(pall_powers)):
        print("All_Set", pal["Power"])
    else:
        print("Loh", pal["Power"])




# T: Button function
def breed_pals_butt():
    pokemon_a_name = entry_a.get()
    pokemon_b_name = entry_b.get()
    row = breed_pals(pokemon_a_name, pokemon_b_name)
    messagebox.showinfo(
        "Result", f"The Pokémon with the closest power to the average is: {row.Name}\nIts PDN is: {row.PDN}")

# Function to handle checking button click


def check_pal():
    target_pokemon = entry_target.get()
    closest_pairs = maps.loc[maps['palres'] == target_pokemon]
    print(closest_pairs)

    result = ""
    if not closest_pairs.empty:
        result = "Breeding pairs for creating " + target_pokemon + " are:\n"
        for index, row in closest_pairs.iterrows():
            result += f"{row.pal1}+{row.pal2} \n"
    else:
        result = "No breeding pairs found for creating " + target_pokemon
    messagebox.showinfo("Result", result)


# T: Script to check EVERY pal combo
def compute():
    pal1_arr = []
    pal2_arr = []
    res_pal = []
    for index, pal1 in df.iterrows():
        for index, pal2 in df.iterrows():
            pal1_arr.append(pal1['Name'])
            pal2_arr.append(pal2['Name'])
            res_pal.append(breed_pals(pal1['Name'], pal2['Name']).Name)
    d = {'pal1': pal1_arr, 'pal2': pal2_arr, 'palres': res_pal}
    df2 = pd.DataFrame(data=d, index=range(0, len(res_pal)))
    df2.to_csv('out.csv', index=False)


def D_Window():
    pass


    # Create a Tkinter window
window = tk.Tk()
window.title("Palworld Breeding Helper")

# Create labels and entry widgets
label_a = tk.Label(window, text="Pal A:")
label_a.grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(window)
entry_a.grid(row=0, column=1, padx=5, pady=5)

label_b = tk.Label(window, text="Pal B:")
label_b.grid(row=1, column=0, padx=5, pady=5)
entry_b = tk.Entry(window)
entry_b.grid(row=1, column=1, padx=5, pady=5)

label_target = tk.Label(window, text="Target Pal:")
label_target.grid(row=2, column=0, padx=5, pady=5)
entry_target = tk.Entry(window)
entry_target.grid(row=2, column=1, padx=5, pady=5)

# Create buttons
button_breed = tk.Button(window, text="Breed", command=breed_pals_butt)
button_breed.grid(row=3, column=0, padx=5, pady=5)

button_breed = tk.Button(window, text="Compute", command=compute)
button_breed.grid(row=3, column=1, padx=5, pady=5)

button_breed = tk.Button(window, text="Check_pal", command=check_pal)
button_breed.grid(row=3, column=2, padx=5, pady=5)

# Run the Tkinter event loop
window.mainloop()


def T_Window():
    # Create a Tkinter window
    pass
    window = tk.Tk()
    window.title("Palworld Breeding Helper")

    label_target = tk.Label(window, text="Target Pal:")
    label_target.grid(row=2, column=0, padx=5, pady=5)
    entry_target = tk.Entry(window)
    entry_target.grid(row=2, column=1, padx=5, pady=5)

    # Create buttons
    button_breed = tk.Button(window, text="Breed", command=seq_butt)
    button_breed.grid(row=3, column=0, padx=5, pady=5)

    button_breed = tk.Button(window, text="Compute", command=compute)
    button_breed.grid(row=3, column=1, padx=5, pady=5)

    # Run the Tkinter event loop
    window.mainloop()
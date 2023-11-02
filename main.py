import tkinter as tk
from tkinter import ttk


def calculate_power(hp, mana, stamina, defense, phys_atk, mag_atk, speed, intelligence):
    unified1 = (5 * mag_atk * (mana / 30) + phys_atk) * (1.5 ** ((speed / 100) - 1))
    unified2 = unified1 * (stamina / 100) + (hp + 3 * defense) * (1.1 ** (stamina / 100))
    power = (unified2 * (2 ** ((intelligence - 100) / 20)) - 1) / 10
    return power


class Mage:
    def __init__(self, name, age, power_level, specialization, experience):
        self.name = name
        self.age = age
        self.power_level = power_level
        self.specialization = specialization
        self.experience = experience

    def __repr__(self):
        return f"{self.name}, {self.age} years old, Power Level: {self.power_level}, Specialization: {self.specialization}, Experience: {self.experience} years"

    def __lt__(self, other):
        if self.power_level == other.power_level:
            return self.experience < other.experience
        return self.power_level < other.power_level

    def __eq__(self, other):
        return self.power_level == other.power_level and self.experience == other.experience


class StatsVisualizerProto:
    def __init__(self, root, update_callback=None):
        self.root = root
        self.root.title("Stats Visualizer")
        self.update_callback = update_callback

        # Define the stats variables
        self.hp_var = tk.DoubleVar(value=100)
        self.mana_var = tk.DoubleVar(value=100)
        self.stamina_var = tk.DoubleVar(value=100)
        self.defense_var = tk.DoubleVar(value=10)
        self.phys_atk_var = tk.DoubleVar(value=4)
        self.mag_atk_var = tk.DoubleVar(value=0)
        self.speed_var = tk.DoubleVar(value=100)
        self.intelligence_var = tk.DoubleVar(value=100)

        # Update the power value and trigger the callback if provided
        def update_power(*args):
            power = calculate_power(
                self.hp_var.get(),
                self.mana_var.get(),
                self.stamina_var.get(),
                self.defense_var.get(),
                self.phys_atk_var.get(),
                self.mag_atk_var.get(),
                self.speed_var.get(),
                self.intelligence_var.get()
            )
            self.power_label.config(text=f"Total Power: {power:.2f}")
            if self.update_callback:
                self.update_callback(power)

        def override_value(var, entry, scale):
            try:
                value = int(entry.get())
                if value > scale.cget("to") or value < scale.cget("from"):
                    new_max = 2 * value
                    scale.config(from_=0, to=new_max)
                var.set(value)
                update_power()
            except ValueError:
                pass

        stats = [
            ("Health", self.hp_var),
            ("Mana", self.mana_var),
            ("Stamina", self.stamina_var),
            ("Defense", self.defense_var),
            ("Phys Atk", self.phys_atk_var),
            ("Mag Atk", self.mag_atk_var),
            ("Speed", self.speed_var),
            ("Intelligence", self.intelligence_var)
        ]
        for i, (label, var) in enumerate(stats):
            ttk.Label(root, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)
            scale = tk.Scale(root, from_=0, to_=200, orient="horizontal", variable=var, resolution=1)
            scale.grid(row=i, column=2, sticky="ew", padx=10, pady=5)
            scale.bind("<Motion>", update_power)
            entry = ttk.Entry(root, width=5)
            entry.grid(row=i, column=3, padx=10, pady=5)
            button = ttk.Button(root, text="Override",
                                command=lambda var=var, entry=entry, scale=scale: override_value(var, entry, scale))
            button.grid(row=i, column=4, padx=10, pady=5)

        self.power_label = ttk.Label(root, text="Total Power: 0")
        self.power_label.grid(row=len(stats), column=0, columnspan=5, pady=20)

        update_power()  # Initialize with the default power value


class MageCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mage Creator")

        # Mage attributes
        self.name_var = tk.StringVar()
        self.age_var = tk.IntVar()
        self.description_var = tk.StringVar()
        self.years_practicing_var = tk.IntVar()
        self.personality_var = tk.StringVar()
        self.power_var = tk.DoubleVar()

        # Layout for Mage attributes
        attributes = [
            ("Name", self.name_var),
            ("Age", self.age_var),
            ("Description", self.description_var),
            ("Years Practicing", self.years_practicing_var),
            ("Personality", self.personality_var),
            ("Power", self.power_var)
        ]

        for i, (label_text, var) in enumerate(attributes):
            ttk.Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label_text == "Power":
                ttk.Label(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)
                ttk.Button(root, text="Adjust Stats", command=self.open_stats_visualizer).grid(row=i, column=2, padx=10,
                                                                                               pady=5)
            else:
                ttk.Entry(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5, sticky="ew", columnspan=2)

    def open_stats_visualizer(self):
        # Launch StatsVisualizer in a new window
        new_window = tk.Toplevel(self.root)
        StatsVisualizerProto(new_window, self.update_power)

    def update_power(self, power):
        self.power_var.set(round(power, 2))


# Uncommenting the following code will open the Mage Creator GUI
root = tk.Tk()
app = MageCreator(root)
root.mainloop()


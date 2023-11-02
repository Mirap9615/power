import tkinter as tk
from tkinter import ttk
import uuid

import json
import os

CMD_FILENAME = "cmd.json"  # The central mage database


def load_mages_from_cmd():
    if not os.path.exists(CMD_FILENAME):
        return []

    with open(CMD_FILENAME, 'r') as file:
        content = file.read()
        if not content:
            return []
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []


def save_mage_to_cmd(mage_data):
    mages = load_mages_from_cmd()
    mages.append(mage_data)

    with open(CMD_FILENAME, 'w') as file:
        json.dump(mages, file, indent=4)


def calculate_power(hp, mana, stamina, defense, phys_atk, mag_atk, speed, intelligence):
    unified1 = (5 * mag_atk * (mana / 30) + phys_atk) * (1.5 ** ((speed / 100) - 1))
    unified2 = unified1 * (stamina / 100) + (hp + 3 * defense) * (1.1 ** (stamina / 100))
    power = (unified2 * (2 ** ((intelligence - 100) / 20)) - 1) / 10
    return power


class Mage:
    def __init__(self, name="", age=0, description="", years_practicing=0, personality="",
                 health=100, mana=100, stamina=100, defense=10, phys_atk=4, mag_atk=0, speed=100, intelligence=100):
        # Basic attributes
        self._name = name
        self._age = age
        self._description = description
        self._years_practicing = years_practicing
        self._personality = personality
        self.id = str(uuid.uuid4())

        # Stats
        self._health = health
        self._mana = mana
        self._stamina = stamina
        self._defense = defense
        self._phys_atk = phys_atk
        self._mag_atk = mag_atk
        self._speed = speed
        self._intelligence = intelligence

    @property
    def power(self):
        return calculate_power(self._health, self._mana, self._stamina, self._defense, self._phys_atk, self._mag_atk,
                               self._speed, self._intelligence)

    # Getters and setters for attributes
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_age(self):
        return self._age

    def set_age(self, age):
        self._age = age

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    def get_years_practicing(self):
        return self._years_practicing

    def set_years_practicing(self, years):
        self._years_practicing = years

    def get_personality(self):
        return self._personality

    def set_personality(self, personality):
        self._personality = personality

    # Getters and setters for stats
    def get_stat(self, stat_name):
        return getattr(self, f"_{stat_name}")

    def set_stat(self, stat_name, value):
        setattr(self, f"_{stat_name}", value)

    def set_stats(self, health, mana, stamina, defense, phys_atk, mag_atk, speed, intelligence):
        self._health = health
        self._mana = mana
        self._stamina = stamina
        self._defense = defense
        self._phys_atk = phys_atk
        self._mag_atk = mag_atk
        self._speed = speed
        self._intelligence = intelligence

    def get_id(self):
        return self.id


class StatsVisualizer:
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

        update_power()


# Updated MageCreator class with the new functionality for the "Save Mage" button

class MageCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mage Creator")

        self.current_mage = Mage()

        self.name_var = tk.StringVar(value=self.current_mage.get_name())
        self.age_var = tk.IntVar(value=self.current_mage.get_age())
        self.description_var = tk.StringVar(value=self.current_mage.get_description())
        self.years_practicing_var = tk.IntVar(value=self.current_mage.get_years_practicing())
        self.personality_var = tk.StringVar(value=self.current_mage.get_personality())
        self.power_var = tk.DoubleVar(value=self.current_mage.power)

        # Layout for Mage attributes
        attributes = [
            ("Name", self.name_var, self.current_mage.set_name),
            ("Age", self.age_var, self.current_mage.set_age),
            ("Description", self.description_var, self.current_mage.set_description),
            ("Years Practicing", self.years_practicing_var, self.current_mage.set_years_practicing),
            ("Personality", self.personality_var, self.current_mage.set_personality),
            ("Power", self.power_var, None)
        ]

        for i, (label_text, var, setter) in enumerate(attributes):
            ttk.Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if label_text in ["Age", "Years Practicing"]:
                # Add the label to display the current value for age and years practicing
                ttk.Label(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5, sticky="e")

                scale = tk.Scale(root, from_=0, to_=200, orient="horizontal", variable=var, resolution=1)
                scale.grid(row=i, column=2, sticky="w", padx=10, pady=5)

                entry = ttk.Entry(root, width=5)
                entry.grid(row=i, column=3, padx=10, pady=5)

                button = ttk.Button(root, text="Override",
                                    command=lambda var=var, entry=entry, scale=scale: self.override_value(var, entry,
                                                                                                          scale))
                button.grid(row=i, column=4, padx=10, pady=5)
            elif label_text == "Power":
                ttk.Label(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)
                ttk.Button(root, text="Adjust Stats", command=self.open_stats_visualizer).grid(row=i, column=2, padx=10,
                                                                                               pady=5)
            else:
                entry = ttk.Entry(root, textvariable=var)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew", columnspan=2)
                if setter:
                    entry.bind("<FocusOut>", lambda event, setter=setter, var=var: setter(var.get()))

        self.name_entry = root.nametowidget(self.name_var.get())

        # Add the Save Mage button
        self.save_button = ttk.Button(root, text="Save Mage", command=self.save_current_mage, state=tk.NORMAL)
        self.save_button.grid(row=len(attributes), column=0, columnspan=3, pady=20, padx=10, sticky="ew")


    def open_stats_visualizer(self):
        # Launch StatsVisualizer in a new window
        new_window = tk.Toplevel(self.root)
        StatsVisualizer(new_window, self.update_power)

    def update_power(self, power):
        rounded_power = round(power, 2)
        self.power_var.set(rounded_power)
        # Can also update the Mage's stats if needed

    def extract_mage_data(self):
        """Extract mage data from the GUI to a dictionary format."""
        mage_data = {
            "name": self.name_var.get(),
            "age": self.age_var.get(),
            "description": self.description_var.get(),
            "years_practicing": self.years_practicing_var.get(),
            "personality": self.personality_var.get(),
            "power": self.power_var.get(),
            "health": self.current_mage.get_stat("health"),
            "mana": self.current_mage.get_stat("mana"),
            "stamina": self.current_mage.get_stat("stamina"),
            "defense": self.current_mage.get_stat("defense"),
            "phys_atk": self.current_mage.get_stat("phys_atk"),
            "mag_atk": self.current_mage.get_stat("mag_atk"),
            "speed": self.current_mage.get_stat("speed"),
            "intelligence": self.current_mage.get_stat("intelligence"),
            "id": self.current_mage.get_id(),
        }
        return mage_data

    def save_current_mage(self):
        """Save the current mage to the CMD."""
        mage_data = self.extract_mage_data()
        save_mage_to_cmd(mage_data)
        self.root.destroy()

    def override_value(self, var, entry, scale):
        try:
            value = int(entry.get())
            if value > scale.cget("to") or value < scale.cget("from"):
                new_max = 2 * value
                scale.config(from_=0, to=new_max)
            var.set(value)
        except ValueError:
            pass


class MageEdit(MageCreator):
    def __init__(self, parent, mage_data):
        super().__init__(parent)

        # Overwrite the current_mage data with the passed mage_data
        self.current_mage.load_from_dict(mage_data)

        # Update the GUI elements with the mage's data
        self.name_var.set(self.current_mage.get_name())
        self.age_var.set(self.current_mage.get_age())


class MageDisplay:
    def __init__(self, root):
        self.root = root

    @classmethod
    def see_mages(cls):
        # Create a new window to display mages
        new_window = tk.Toplevel()
        new_window.title("Mages Overview")
        new_window.geometry("1000x600")  # Adjust size as needed

        mages = load_mages_from_cmd()

        if not mages:
            ttk.Label(new_window, text="No mages found.").pack(pady=20)
            return

        # Header
        header_labels = ["Name", "Age", "Description", "Years Practicing", "Personality", "Power"]
        for col, attribute in enumerate(header_labels):
            ttk.Label(new_window, text=attribute, font=('Arial', 10, 'bold')).grid(row=0, column=col, padx=30, pady=10)

        # Populate the mages
        for row, mage in enumerate(mages, start=1):
            ttk.Label(new_window, text=mage["name"]).grid(row=row, column=0, padx=30, pady=0)
            ttk.Label(new_window, text=mage["age"]).grid(row=row, column=1, padx=5, pady=5)
            ttk.Label(new_window, text=mage["description"]).grid(row=row, column=2, padx=5, pady=5)
            ttk.Label(new_window, text=mage["years_practicing"]).grid(row=row, column=3, padx=5, pady=5)
            ttk.Label(new_window, text=mage["personality"]).grid(row=row, column=4, padx=5, pady=5)
            ttk.Label(new_window, text=mage["power"]).grid(row=row, column=5, padx=5, pady=5)

            edit_button = ttk.Button(new_window, text="Edit", command=lambda mage=mage: MageEdit(new_window, mage))
            edit_button.grid(row=row, column=6, padx=5, pady=5)

        # Add a scrollbar if needed
        scrollbar = tk.Scrollbar(new_window)
        scrollbar.grid(row=1, column=8, sticky='ns')
        new_window.grid_rowconfigure(1, weight=0)

class MageInteractive:
    def __init__(self, root):
        self.root = root
        self.root.title("Mage Interactive")
        self.root.geometry("800x400")

        # Button to open MageCreator
        self.create_mage_button = ttk.Button(root, text="Create Mage", command=self.open_mage_creator)
        self.create_mage_button.pack(pady=20)

        self.create_mage_button = ttk.Button(root, text="Load Mage")
        self.create_mage_button.pack(pady=20)

        self.create_mage_button = ttk.Button(root, text="See Mages", command=MageDisplay.see_mages)
        self.create_mage_button.pack(pady=20)

    def open_mage_creator(self):
        # Launch MageCreator in a new window
        new_window = tk.Toplevel(self.root)
        MageCreator(new_window)


if __name__ == '__main__':
    root = tk.Tk()
    app = MageInteractive(root)
    root.mainloop()

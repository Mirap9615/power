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

    # Check if mage with the same ID already exists
    for i, mage in enumerate(mages):
        if mage["id"] == mage_data["id"]:
            # Update the existing mage
            mages[i] = mage_data
            break
    else:
        # If the loop completes without breaking (i.e., no existing mage found), append the new mage
        mages.append(mage_data)

    with open(CMD_FILENAME, 'w') as file:
        json.dump(mages, file)


def update_mage_in_cmd(updated_mage_data):
    mages = load_mages_from_cmd()

    # Print out the updated mage data
    print("Updated Mage Data:", updated_mage_data)

    # Find the mage to update and replace it
    for i, mage in enumerate(mages):
        print(f"Checking mage with ID: {mage['id']}")
        if mage["id"] == updated_mage_data["id"]:
            # Print the mage before updating
            print("Mage Before Update:", mage)

            mages[i] = updated_mage_data

            # Print the mage after updating
            print("Mage After Update:", mages[i])
            break

    # Print entire mages list before saving
    print("Mages List Before Saving:", mages)

    # Save the updated list of mages
    with open(CMD_FILENAME, 'w') as file:
        json.dump(mages, file)

    # Optional: Load and print the saved mages list to verify
    saved_mages = load_mages_from_cmd()
    print("Saved Mages List:", saved_mages)


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
        self.set_stat("health", health)
        self.set_stat("mana", mana)
        self.set_stat("stamina", stamina)
        self.set_stat("defense", defense)
        self.set_stat("phys_atk", phys_atk)
        self.set_stat("mag_atk", mag_atk)
        self.set_stat("speed", speed)
        self.set_stat("intelligence", intelligence)

    def get_id(self):
        return self.id

    def load_completely(self, mage_data):
        self.id = mage_data["id"]
        self._name = mage_data["name"]
        self._age = mage_data["age"]
        self._description = mage_data["description"]
        self._years_practicing = mage_data["years_practicing"]
        self._personality = mage_data["personality"]

        self._health = mage_data["health"]
        self._mana = mage_data["mana"]
        self._stamina = mage_data["stamina"]
        self._defense = mage_data["defense"]
        self._phys_atk = mage_data["phys_atk"]
        self._mag_atk = mage_data["mag_atk"]
        self._speed = mage_data["speed"]
        self._intelligence = mage_data["intelligence"]

    def to_dict(self):
        """Extract mage data from the GUI to a dictionary format."""
        mage_data = {
            "id": self.get_id(),
            "name": self.get_name(),
            "age": self.get_age(),
            "description": self.get_description(),
            "years_practicing": self.get_years_practicing(),
            "personality": self.get_personality(),
            "health": self.get_stat("health"),
            "mana": self.get_stat("mana"),
            "stamina": self.get_stat("stamina"),
            "defense": self.get_stat("defense"),
            "phys_atk": self.get_stat("phys_atk"),
            "mag_atk": self.get_stat("mag_atk"),
            "speed": self.get_stat("speed"),
            "intelligence": self.get_stat("intelligence"),
        }
        return mage_data


class StatsVisualizer:
    def __init__(self, root, update_callback=None, initial_stats=None):
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

        if initial_stats:
            self.hp_var.set(initial_stats["health"])
            self.mana_var.set(initial_stats["mana"])
            self.stamina_var.set(initial_stats["stamina"])
            self.defense_var.set(initial_stats["defense"])
            self.phys_atk_var.set(initial_stats["phys_atk"])
            self.mag_atk_var.set(initial_stats["mag_atk"])
            self.speed_var.set(initial_stats["speed"])
            self.intelligence_var.set(initial_stats["intelligence"])

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
                self.adjust_stats_button = ttk.Button(self.root, text="Adjust Stats",
                                                      command=self.open_stats_visualizer)
                self.adjust_stats_button.grid(row=i, column=2, padx=10, pady=5)

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
    def __init__(self, parent, mage_data, on_close_callback=None):

        self.edit_window = tk.Toplevel(parent)
        # First, initialize Mage object with the provided mage_data
        self.current_mage = Mage()

        print(f"ID before super init: {self.current_mage.id}")
        super().__init__(self.edit_window)
        self.current_mage.load_completely(mage_data)
        self.current_mage.id = mage_data['id']

        # Define all the variables for stats in MageEdit
        self.power_var = tk.DoubleVar(value=self.current_mage.power)
        self.health_var = tk.DoubleVar(value=self.current_mage.get_stat("health"))
        self.mana_var = tk.DoubleVar(value=self.current_mage.get_stat("mana"))
        self.stamina_var = tk.DoubleVar(value=self.current_mage.get_stat("stamina"))
        self.defense_var = tk.DoubleVar(value=self.current_mage.get_stat("defense"))
        self.phys_atk_var = tk.DoubleVar(value=self.current_mage.get_stat("phys_atk"))
        self.mag_atk_var = tk.DoubleVar(value=self.current_mage.get_stat("mag_atk"))
        self.speed_var = tk.DoubleVar(value=self.current_mage.get_stat("speed"))
        self.intelligence_var = tk.DoubleVar(value=self.current_mage.get_stat("intelligence"))

        print(f"ID after super init: {self.current_mage.id}")

        self.edit_window.title("Mage Editor")
        self.update_gui_from_mage(mage_data)

        self.adjust_stats_button.destroy()
        self.adjust_stats_button = ttk.Button(self.edit_window, text="Adjust Stats",
                                              command=self.open_stats_visualizer_from_edit)
        self.adjust_stats_button.grid(row=5, column=2, padx=10, pady=5)

        self.save_button.config(command=self.save_edited_mage)

        self.on_close_callback = on_close_callback

        self.edit_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_gui_from_mage(self, mage_data):
        # This function sets the GUI variables based on the mage data provided

        self.name_var.set(mage_data['name'])
        self.age_var.set(mage_data['age'])
        self.description_var.set(mage_data['description'])
        self.years_practicing_var.set(mage_data['years_practicing'])
        self.personality_var.set(mage_data['personality'])
        self.power_var.set(calculate_power(
            mage_data['health'],
            mage_data['mana'],
            mage_data['stamina'],
            mage_data['defense'],
            mage_data['phys_atk'],
            mage_data['mag_atk'],
            mage_data['speed'],
            mage_data['intelligence']
        ))
        self.health_var.set(mage_data['health'])
        self.mana_var.set(mage_data['mana'])
        self.stamina_var.set(mage_data['stamina'])
        self.defense_var.set(mage_data['defense'])
        self.phys_atk_var.set(mage_data['phys_atk'])
        self.mag_atk_var.set(mage_data['mag_atk'])
        self.speed_var.set(mage_data['speed'])
        self.intelligence_var.set(mage_data['intelligence'])

    def update_mage_from_gui(self):
        self.current_mage.set_name(self.name_var.get())
        self.current_mage.set_age(self.age_var.get())
        self.current_mage.set_description(self.description_var.get())
        self.current_mage.set_years_practicing(self.years_practicing_var.get())
        self.current_mage.set_personality(self.personality_var.get())
        self.current_mage.set_stat("health", self.health_var.get())
        self.current_mage.set_stat("mana", self.mana_var.get())
        self.current_mage.set_stat("stamina", self.stamina_var.get())
        self.current_mage.set_stat("defense", self.defense_var.get())
        self.current_mage.set_stat("phys_atk", self.phys_atk_var.get())
        self.current_mage.set_stat("mag_atk", self.mag_atk_var.get())
        self.current_mage.set_stat("speed", self.speed_var.get())
        self.current_mage.set_stat("intelligence", self.intelligence_var.get())

    def save_edited_mage(self):
        self.update_mage_from_gui()
        mage_data = self.current_mage.to_dict()
        update_mage_in_cmd(mage_data)

        self.on_close()

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.edit_window.destroy()

    def save_current_mage(self):
        pass

    def open_stats_visualizer_from_edit(self):
        mage_stats = {
            "health": self.current_mage.get_stat("health"),
            "mana": self.current_mage.get_stat("mana"),
            "stamina": self.current_mage.get_stat("stamina"),
            "defense": self.current_mage.get_stat("defense"),
            "phys_atk": self.current_mage.get_stat("phys_atk"),
            "mag_atk": self.current_mage.get_stat("mag_atk"),
            "speed": self.current_mage.get_stat("speed"),
            "intelligence": self.current_mage.get_stat("intelligence")
        }

        def update_callback(power):
            # This function will be called when the stats are adjusted in StatsVisualizer
            # Update the MageEdit's mage stats here
            self.current_mage.set_stat("health", self.health_var.get())
            self.current_mage.set_stat("mana", self.mana_var.get())
            self.current_mage.set_stat("stamina", self.stamina_var.get())
            self.current_mage.set_stat("defense", self.defense_var.get())
            self.current_mage.set_stat("phys_atk", self.phys_atk_var.get())
            self.current_mage.set_stat("mag_atk", self.mag_atk_var.get())
            self.current_mage.set_stat("speed", self.speed_var.get())
            self.current_mage.set_stat("intelligence", self.intelligence_var.get())

        stats_visualizer = StatsVisualizer(self.edit_window, update_callback, mage_stats)


class MageDisplay:
    def __init__(self, root):
        self.root = root
        self.mage_widgets = []
        self.mage_edit_windows = {}
        self.new_window = None

    def clear_mage_widgets(self):
        for widget in self.mage_widgets:
            widget.destroy()
        self.mage_widgets.clear()

    def refresh_mages(self):
        # Clear only the mage entries, not the headers
        for widget in self.mage_widgets[6:]:  # Assuming 6 headers
            widget.destroy()
        self.mage_widgets = self.mage_widgets[:6]  # Keep the headers
        self.populate_mages()

    def see_mages(self):
        # If the window doesn't exist or has been closed, recreate it
        if self.new_window is None or not self.new_window.winfo_exists():
            self.new_window = tk.Toplevel(self.root)
            self.new_window.title("Mages Overview")
            self.new_window.geometry("1000x600")

            # Create headers only once
            header_labels = ["Name", "Age", "Description", "Years Practicing", "Personality", "Power"]
            for col, attribute in enumerate(header_labels):
                header = ttk.Label(self.new_window, text=attribute, font=('Arial', 10, 'bold'))
                header.grid(row=0, column=col, padx=30, pady=10)
                self.mage_widgets.append(header)

        self.refresh_mages()

    def populate_mages(self):
        mages = load_mages_from_cmd()

        if not mages:
            label = ttk.Label(self.new_window, text="No mages found.")
            label.pack(pady=20)
            self.mage_widgets.append(label)
            return

        # Populate the mages
        for row, mage in enumerate(mages, start=1):
            # Create labels for each attribute
            name_label = ttk.Label(self.new_window, text=mage["name"])
            age_label = ttk.Label(self.new_window, text=mage["age"])
            description_label = ttk.Label(self.new_window, text=mage["description"])
            years_practicing_label = ttk.Label(self.new_window, text=mage["years_practicing"])
            personality_label = ttk.Label(self.new_window, text=mage["personality"])
            power_label = ttk.Label(self.new_window, text=round(
                calculate_power(
                    mage["health"], mage["mana"], mage["stamina"],
                    mage["defense"], mage["phys_atk"], mage["mag_atk"],
                    mage["speed"], mage["intelligence"]
                ), 2)
                                    )

            # Add labels to the grid
            name_label.grid(row=row, column=0, padx=30, pady=0)
            age_label.grid(row=row, column=1, padx=5, pady=5)
            description_label.grid(row=row, column=2, padx=5, pady=5)
            years_practicing_label.grid(row=row, column=3, padx=5, pady=5)
            personality_label.grid(row=row, column=4, padx=5, pady=5)
            power_label.grid(row=row, column=5, padx=5, pady=5)

            # Add edit button
            edit_button = ttk.Button(
                self.new_window, text="Edit",
                command=lambda m=mage: self.open_mage_edit(m)
            )
            edit_button.grid(row=row, column=6, padx=5, pady=5)

            # Save the widgets to the list
            self.mage_widgets.extend([
                name_label, age_label, description_label, years_practicing_label,
                personality_label, power_label, edit_button
            ])

    def open_mage_edit(self, mage):
        # Check if the MageEdit window for this mage is already open
        if mage["id"] in self.mage_edit_windows and self.mage_edit_windows[mage["id"]].edit_window.winfo_exists():
            # Bring the MageEdit window to the front if it's already open
            self.mage_edit_windows[mage["id"]].edit_window.lift()
        else:
            # Open a new MageEdit window
            edit_window = MageEdit(self.new_window, mage, self.refresh_mages)
            self.mage_edit_windows[mage["id"]] = edit_window


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

        self.create_mage_button = ttk.Button(root, text="See Mages", command=self.open_mage_display)
        self.create_mage_button.pack(pady=20)

    def open_mage_creator(self):
        # Launch MageCreator in a new window
        new_window = tk.Toplevel(self.root)
        MageCreator(new_window)

    def open_mage_display(self):
        # Create an instance of MageDisplay and call see_mages on it
        mage_display = MageDisplay(self.root)
        mage_display.see_mages()


if __name__ == '__main__':
    root = tk.Tk()
    app = MageInteractive(root)
    root.mainloop()

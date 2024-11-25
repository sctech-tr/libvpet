import json
from datetime import datetime, timedelta

class VirtualPet:
    def __init__(self, file_path, name=None):
        self.file_path = file_path
        self.name = name
        self.cooldowns = {
            'feed': timedelta(hours=2),
            'play': timedelta(hours=1),
            'sleep': timedelta(hours=8),
        }
        self.data = self._load_pet() or {}
        if not self.data and self.name:
            self.create()  # Create a pet if no data is loaded and name is provided

    def _load_pet(self):
        """Loads pet data from a JSON file, or initializes it if not found."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Creating a new pet file at '{self.file_path}'.")
            return None

    def _save_pet(self):
        """Saves the current pet data to a JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"{self.data['name']}'s data has been saved.")

    def create(self):
        """Creates a new pet with default stats if none exist."""
        if self.data:
            print("Pet already exists. Load or use a different file to create a new pet.")
            return

        self.data = {
            "name": self.name,
            "hunger": 0,
            "happiness": 10,
            "health": 10,
            "age": 0,
            "last_fed": datetime.now().isoformat(),
            "last_played": datetime.now().isoformat(),
            "last_slept": datetime.now().isoformat(),
        }
        self._save_pet()
        print(f"{self.name} has been created!")

    def status(self):
        """Displays the current status of the pet, including mood and health."""
        if not self.data:
            print("No pet data found.")
            return

        mood = self._determine_mood()
        print(f"\n--- {self.data['name']}'s Status ---")
        print(f"Age: {self.data['age']} days")
        print(f"Hunger Level: {self.data['hunger']}")
        print(f"Happiness Level: {self.data['happiness']}")
        print(f"Health: {self.data['health']}")
        print(f"Mood: {mood}")

    def _determine_mood(self):
        """Determines the pet's mood based on its happiness and hunger levels."""
        if self.data["hunger"] > 7:
            return "Hungry"
        elif self.data["happiness"] > 7:
            return "Happy"
        elif self.data["health"] < 5:
            return "Sick"
        return "Neutral"

    def _time_since_last(self, action):
        """Calculates time since last action."""
        last_action_time = datetime.fromisoformat(self.data[f"last_{action}"])
        return datetime.now() - last_action_time

    def feed(self):
        """Feeds the pet, decreasing hunger and boosting health if needed."""
        if not self.data:
            print("Pet not found. Use `create` to make a new pet.")
            return

        if self._time_since_last('fed') >= self.cooldowns['feed']:
            self.data["hunger"] = max(0, self.data["hunger"] - 1)
            self.data["health"] = min(10, self.data["health"] + 1)  # Health boost
            self.data["last_fed"] = datetime.now().isoformat()
            print(f"{self.data['name']} has been fed!")
        else:
            print("It's too soon to feed again. Try later.")

        self._save_pet()

    def play(self):
        """Plays with the pet, increasing happiness and potentially health."""
        if not self.data:
            print("Pet not found. Use `create` to make a new pet.")
            return

        if self._time_since_last('played') >= self.cooldowns['play']:
            self.data["happiness"] = min(10, self.data["happiness"] + 1)
            self.data["health"] = min(10, self.data["health"] + 0.5)  # Small health increase
            self.data["last_played"] = datetime.now().isoformat()
            print(f"{self.data['name']} enjoyed playing!")
        else:
            print("Your pet needs some rest. Try playing later.")

        self._save_pet()

    def sleep(self):
        """Puts the pet to sleep, which restores health and reduces hunger slightly."""
        if not self.data:
            print("Pet not found. Use `create` to make a new pet.")
            return

        if self._time_since_last('slept') >= self.cooldowns['sleep']:
            self.data["hunger"] = min(10, self.data["hunger"] + 1)  # Slight increase in hunger
            self.data["health"] = min(10, self.data["health"] + 2)  # Boost health
            self.data["last_slept"] = datetime.now().isoformat()
            print(f"{self.data['name']} had a restful sleep!")
        else:
            print("Your pet isn't tired yet.")

        self._save_pet()

    def age_pet(self):
        """Ages the pet by 1 day, affecting hunger and health."""
        if not self.data:
            print("Pet not found. Use `create` to make a new pet.")
            return

        self.data["age"] += 1
        self.data["hunger"] = min(10, self.data["hunger"] + 1)  # Increase hunger daily
        self.data["health"] = max(0, self.data["health"] - 0.5)  # Gradual health decay
        print(f"{self.data['name']} has aged by 1 day!")

        self._save_pet()

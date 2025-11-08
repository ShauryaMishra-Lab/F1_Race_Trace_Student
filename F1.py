"""
f1_race_trace_student.py

This code uses the fastf1 library to load race lap data for the 2021 Grand Prix
Formula 1 race. This Processes the lap times to compute 
race time and gap to the leader for each lap, and then saves the processed
data and a race-trace plot to the local `Max Verstappen` folder.

"""

import fastf1
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


 """
 Create a local cache directory for fastf1 data to speed up repeated runs.
 If the directory already exists this is a no-op.
"""
cache = Path.home() / ".fastf1"
cache.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(cache)


"""
Define the target year and race name. The script will load the race session
(R = race) for the given year and race name via fastf1.get_session.
"""
year = 2021
race = "Bahrain Grand Prix"

print(f"Loading data for {race} {year}...")
session = fastf1.get_session(year, race, "R")
session.load()


laps = session.laps
laps = laps[~laps["LapTime"].isna()].copy()


laps["total_time"] = laps.groupby("Driver")["LapTime"].cumsum()


leader_time = laps.groupby("LapNumber")["total_time"].min().rename("leader_time")
laps = laps.merge(leader_time, on="LapNumber")
laps["gap"] = (laps["total_time"] - laps["leader_time"]).dt.total_seconds()


"""
This creates an output directory to save the processed laps as CSV,
and export a plot showing each driver's gap to the leader over the race.
"""
out = Path("Max Verstappen")
out.mkdir(exist_ok=True)

csv_name = str(year) + "_" + race.replace(" ", "_") + ".csv"
csv_file = out / csv_name
laps.to_csv(csv_file, index=False)
print("Saved lap data to " + str(csv_file))


plt.figure(figsize=(10,6))
for driver, grp in laps.groupby("Driver"):
    plt.plot(grp["LapNumber"], grp["gap"], label=driver)
plt.xlabel("Lap Number")
plt.ylabel("Gap to Leader (s)")
plt.title(f"{race} {year} - Race Trace")
plt.legend(fontsize=7, ncol=3)
plt.tight_layout()

png_file = out / f"{year}_{race.replace(' ', '_')}.png"
plt.savefig(png_file, dpi=150)
plt.close()
print(f"Saved chart to {png_file}")

print("Done! check the 'Max Verstappen' folder.")

from circleutils import OSUFile, Spinner
import numpy as np


## From .osu file
file = OSUFile.read("../ressources/49374.osu")

# For DTHR and NoMod
spinner_data = file.get_spinner_data([["DT", "HR"], []])
print(spinner_data)
print(spinner_data[0].leeway, spinner_data[1].leeway)

# For EZ only
spinner_data = file.get_spinner_data(["EZ"])
print(spinner_data[0].leeway)

## From raw data
SAMPLE_START_TIME = np.array([22745,  46370, 124370])
SAMPLE_END_TIME = np.array([24245, 48245, 126245])
SAMPLE_OVERALL_DIFFICULTY = 4

spinner_data = Spinner.calc_spinner_data(
    SAMPLE_START_TIME,
    SAMPLE_END_TIME,
    SAMPLE_OVERALL_DIFFICULTY,
    [["DT", "HR"], [], ["EZ"]]
)
print(spinner_data[0].leeway, spinner_data[1].leeway, spinner_data[2].leeway)

from circleutils import OSUFile


# Read a .osu file
osu_file = OSUFile.read("../ressources/1428960.osu")

# Print some of the content
print(osu_file.version)
print(osu_file.general)

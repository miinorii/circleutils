from circleutils import Collection

# Build from scratch
col = Collection(
    date=20230701,
    content={"cool scores": ["ffd15440497451079d4244d73460e09d", "1c65239ed051d9161855500b665f4b6e"]}
)

# Read from file
col = Collection.read("../ressources/collection_sample.db")

print(col.date)
print(col.content)

# Add a new group
col.content["new group"] = ["1c65239ed051d9161855500b665f4b6e", "690c6f208909cdaeb73676f49f9c4f58"]

# Save to file
col.save("mycol.db")

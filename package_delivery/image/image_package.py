import matplotlib.pyplot as plt

# Load the image
image_path = 'C:/Users/brand/IdeaProjects/Package_Delivery_Program_New/package_delivery/image/Picture1.jpg'
image = plt.imread(image_path)

# Create a figure with the original image dimensions
fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))

# Display the image with SciView
ax.imshow(image)

# Route coordinates (x, y) on the image Picture1.jpg dimensions 672x756
route_coordinate = [
    (398, 458),  # 4001 South 700 East, Salt Lake City, UT,84106
    (309, 316),  # 195 W Oakland Ave, Salt Lake City, UT,84115
    (372, 320),  # 2530 S 500 E, Salt Lake City, UT,84106
    (344, 57),   # 233 Canyon Rd, Salt Lake City, UT,84103
    (290, 351),  # 380 W 2880 S, Salt Lake City, UT,84115
    (336, 122),  # 410 S State St, Salt Lake City, UT,84111
    (171, 369),  # 3060 Lester St, West Valley City, UT,84119
    (469, 287),  # 1330 2100 S, Salt Lake City, UT,84106
    (335, 111),  # 300 State St, Salt Lake City, UT,84103
    (413, 139),  # 600 E 900 South, Salt Lake City, UT,84105
    (110, 593),  # 2600 Taylorsville Blvd Salt Lake City, UT,84118
    (67, 478),   # 3575 W Valley Central Station bus Loop, West Valley City, UT,84119
    (131, 129),  # 2010 W 500 S, Salt Lake City, UT,84104
    (550, 517),  # 4580 S 2300 E, Holladay, UT,84117
    (216, 376),  # 3148 S 1100 W, Salt Lake City, UT,84104
    (184, 547),  # 1488 4800 S Salt Lake City, UT,84123
    (310, 424),  # 177 W Price Ave, Salt Lake City, UT,84115
    (330, 420),  # 3595 Main St, Salt Lake City, UT,84115
    (422, 678),  # 6351 South 900 East, Murray, UT,84121
    (102, 572),  # 5100 South 2700 West, Salt Lake City, UT,84118
    (339, 557),  # 5025 State St, Murray, UT,84107
    (413, 594),  # 5383 South 900 East #104, Salt Lake City, UT,84117
    (213, 186),  # 1060 Dalton Ave S, Salt Lake City, UT,84104
    (327, 345),  # 2835 Main St, Salt Lake City, UT,84115
    (469, 288),  # 1330 2100 S, Salt Lake City, UT,84106
    (239, 397),  # 3365 S 900 W, Salt Lake City, UT,84119
    (130, 325),  # 2300 Parkway Blvd, West Valley City, UT,84119
    (447, 490),  # 4300 S 1300 E,Millcreek,UT,84117
]

# Overlay markers on the image
for (x, y) in route_coordinate:
    ax.scatter(x, y, marker='o', color='red', s=50)  # Adjust marker properties

# Set axis limits and turn off axes
ax.set_xlim(0, image.shape[1])
ax.set_ylim(image.shape[0], 0)
ax.axis('off')  # Turn off axes

# Display the image with markers using SciView
plt.show()

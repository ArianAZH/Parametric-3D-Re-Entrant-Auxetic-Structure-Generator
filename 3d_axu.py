import cadquery as cq
import pyvista as pv
import numpy as np

# Define geometric parameters
high = 8 # z (mm)
length = 8  # x y (mm)
thickness = 1 # thikness of ligament (mm)
theta = np.degrees(54.74)
mid_l = (high/2)/np.tan(theta)

spacing_xy = (length + 2*mid_l)
spacing_z = high
num_repeat_x = 5
num_repeat_y = 5
num_repeat_z = 8

# Define vertex coordinates
points = [
    (-length/2, -length/2, -high/2),
    (-length/2,  length/2, -high/2),
    ( length/2,  length/2, -high/2),
    ( length/2, -length/2, -high/2),
    (-mid_l, -mid_l, 0),
    (-mid_l,  mid_l, 0),
    ( mid_l,  mid_l, 0),
    ( mid_l, -mid_l, 0),
    (-length/2, -length/2, high/2),
    (-length/2,  length/2, high/2),
    ( length/2,  length/2, high/2),
    ( length/2, -length/2, high/2),
    (-(mid_l+length/2), -mid_l           , 0),
    (-(mid_l)         , -(mid_l+length/2), 0),
    (-(mid_l+length/2),  mid_l           , 0),
    (-mid_l           ,  (mid_l+length/2), 0),
    ( (mid_l+length/2),  mid_l           , 0),
    ( mid_l           ,  (mid_l+length/2), 0),
    ( (mid_l+length/2), -mid_l           , 0),
    ( mid_l           , -(mid_l+length/2), 0),
]

# Define edge connections between points
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (0, 4), (1, 5), (2, 6), (3, 7),
    (4, 8), (5, 9), (6, 10), (7, 11),
    (8, 9), (9,10), (10, 11), (11, 8),
    (4, 12), (4, 13), (5, 14), (5, 15),
    (6, 16), (6, 17), (7, 18), (7, 19),
]

# Build 3D model using cylinders and spheres
model = cq.Workplane("XY")


# Create cylinders along each edge
for start_idx, end_idx in edges:
    start = points[start_idx]
    end = points[end_idx]
    length = np.linalg.norm(np.array(end) - np.array(start))
    direction = tuple(np.array(end) - np.array(start))
    cyl = cq.Solid.makeCylinder(thickness, length, start, direction)
    model = model.union(cyl)

# Add spheres at each vertex
for p in points:
    sphere = cq.Workplane("XY").sphere(thickness).translate(tuple(p))
    model = model.union(sphere)

cells = []
ask_run = input("cubic(1) or pyramid(2) geometry? : ")

if ask_run =="1":
    for i in range(num_repeat_y):
        for j in range(num_repeat_x):
            for k in range(num_repeat_z):
                cells.append(
                    model.translate((i*spacing_xy, j*spacing_xy, k*spacing_z))
                )
elif ask_run =="2":
    for k in range(num_repeat_y):
        cells_in_layer_x = num_repeat_x - k
        cells_in_layer_y = num_repeat_y - k
        offset_x = k * spacing_xy / 2
        offset_y = k * spacing_xy / 2
        for i in range(cells_in_layer_x):
            for j in range(cells_in_layer_y):
                x = i * spacing_xy + offset_x
                y = j * spacing_xy + offset_y
                z = k * spacing_z
                cells.append(model.translate((x, y, z)))
else:
    print("Exiting without creating geometry.")
    exit()
compound = cq.Compound.makeCompound([s.val() for s in cells])


print("Exporting files...")
cq.exporters.export(compound, "3drentreant.step", tolerance=0.1)
cq.exporters.export(compound, "3drentreant.stl", tolerance=0.1)

print("Visualizing...")
# Visualize STL only
mesh = pv.read("3drentreant.stl")
plotter = pv.Plotter()
plotter.add_mesh(mesh, color="red", show_edges=False)
plotter.add_axes()
plotter.show_grid()
plotter.show()
print("Done! Geometry exported as single combined solid.")
import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from matplotlib.patches import Polygon as MplPolygon
import numpy as np
import matplotlib.cm as cm

# Function to generate random quadrangles
def generate_random_quadrangle(xlim, ylim):
    return Polygon([(random.uniform(0, xlim), random.uniform(0, ylim)) for _ in range(4)])

# Parameters
num_quadrangles = 5  # Number of quadrangles
xlim, ylim = 10, 10  # Limits for the random generation

# Generate random quadrangles
quadrangles = []
for _ in range(num_quadrangles):
    quad = generate_random_quadrangle(xlim, ylim)
    # Ensure the geometry is valid
    if not quad.is_valid:
        quad = make_valid(quad)
    quadrangles.append(quad)

# Step 1: Combine all quadrangles into a single geometry
combined = unary_union(quadrangles)  # Combine all polygons into one geometry

# Ensure combined is a MultiPolygon (or list of polygons) for easy processing
if isinstance(combined, Polygon):
    combined = [combined]
elif isinstance(combined, MultiPolygon):
    combined = list(combined.geoms)

# Step 2: Create a dictionary to store overlap counts for each distinct region
overlap_counts = {}

# Count how many polygons each region in the combined geometry overlaps
for region in combined:
    count = sum(1 for quad in quadrangles if region.intersects(quad))
    overlap_counts[tuple(region.exterior.coords)] = count

# Step 3: Plotting
fig, ax = plt.subplots()
ax.set_xlim(0, xlim)
ax.set_ylim(0, ylim)

# Plot original quadrangles (optional)
for q in quadrangles:
    if isinstance(q, Polygon):
        x, y = q.exterior.xy
        ax.plot(x, y, color='black', alpha=0.5)
    elif isinstance(q, MultiPolygon):
        for poly in q.geoms:
            x, y = poly.exterior.xy
            ax.plot(x, y, color='black', alpha=0.5)

# Adjust color scaling
max_intersections = max(overlap_counts.values(), default=1)
manual_vmin = 1  # Start the color scale at 1 (blue)
manual_vmax = max_intersections  # Set vmax to the maximum overlap count

norm = plt.Normalize(vmin=manual_vmin, vmax=manual_vmax)

# Use the reversed RdBu colormap (blue to red)
cmap = cm.RdBu.reversed()

# Step 4: Add regions with colors based on the number of overlaps
for region_coords, count in overlap_counts.items():
    region_polygon = Polygon(region_coords)
    color = cmap(norm(count))
    ax.add_patch(MplPolygon(np.array(region_polygon.exterior.xy).T, closed=True, color=color, alpha=0.7))

plt.gca().set_aspect('equal', adjustable='box')
plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', label='Number of Intersections')
plt.show()

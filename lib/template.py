"""
Template for python code generation
"""

from objects.cube import Cube
import matplotlib.pyplot as plt

cubes = []

fig = plt.figure()
ax = fig.gca(projection='3d')

"PLACEHOLDER"

for cube in cubes:
	cube.draw(fig, ax)

plt.subplots_adjust(top=1, right=1, bottom=0, left=0)

ax.auto_scale_xyz([0, 10], [0, 10], [0, 10])
plt.show()
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial.transform import Rotation as R

class Cube:
	def __init__(self, width, height=-1, length=-1):
		self.width = width
		
		# handle single argument input for cubes
		if height == -1 and length == -1:
			self.height = self.length = self.width
		elif height == -1 or length == -1:
			raise TypeError('Cube expects 1 or 3 arguments')
		else:
			self.height = height
			self.length = length

		# cube vertices with shift (-0.5) to move origin to cube's center
		self.points = np.array([
			[0, 0, 0, 1],
			[1, 0, 0, 1],
			[1, 1, 0, 1],
			[0, 1, 0, 1],
			[0, 0, 1, 1],
			[1, 0, 1, 1],
			[1, 1, 1, 1],
			[0, 1, 1, 1]
		])

		# initial scale matrix
		self.scale_matrix = np.array([
			[self.width, 0, 0, 0], 
			[0, self.height, 0, 0], 
			[0, 0, self.length, 0],
			[0, 0, 0, 1]
		])

		# initialize transformation matrix
		self.matrix = np.identity(4)

	def rotate(self, x=0, y=0, z=0):
		"""Apply rotation to transformation matrix"""
		quaternion = R.from_euler('xyz', [x, y, z], degrees=True)
		rotation_matrix = np.array(quaternion.as_matrix())
		rotation_matrix = np.pad(rotation_matrix, [(0, 1), (0, 1)], mode='constant')
		rotation_matrix[3,3] = 1

		self.matrix = np.matmul(self.matrix, rotation_matrix)

	def translate(self, x=0, y=0, z=0):
		"""Apply translation to transformation matrix"""
		translation = np.identity(4)
		translation[0, 3] += x
		translation[1, 3] += y
		translation[2, 3] += z
		
		self.matrix = np.matmul(self.matrix, translation)

	def log_transformation_matrix(self):
		"""Output tranformation matrix to the terminal"""
		print(f'cube({self.width}, {self.height}, {self.length}):')

		rows = self.matrix.tolist()

		for row in rows:
			print(list(map(self.trunc, row)))

	@staticmethod
	def trunc(value):
		"""Custom round method to keep ints"""
		return round(value, 3) if math.modf(value)[0] != 0 else round(value)

	def apply_transformations(self, log=True):
		if log:
			# log t matrix before applying scale 
			# and centering cube (as in examples)
			self.log_transformation_matrix()

		# move origin point to cube's center 
		self.translate(-self.width/2, -self.height/2, -self.length/2)

		# scale cube
		self.matrix = np.matmul(self.matrix, np.transpose(self.scale_matrix))

		# apply transformation matrix and get cube points matrix
		result = np.matmul(self.matrix, np.transpose(self.points))
		result = np.delete(np.transpose(result), 3, 1)

		return result
                
	def draw(self, fig, ax):
		"""Plot cube on a common figure. 
		fig and ax are passed from the template"""

		points = self.apply_transformations()                
		ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])

		# cube polygons collection
		verts = [
			[points[0], points[1], points[2], points[3]],
			[points[4], points[5], points[6], points[7]], 
			[points[0], points[1], points[5], points[4]], 
			[points[2], points[3], points[7], points[6]], 
			[points[1], points[2], points[6], points[5]],
			[points[4], points[7], points[3], points[0]]
		]
		
		# render polygons
		ax.add_collection3d(Poly3DCollection(verts, 
		facecolors='blue', linewidths=1, edgecolors='b', alpha=0.3))


			
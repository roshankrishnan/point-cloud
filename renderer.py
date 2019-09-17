from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from OpenGL.arrays import vbo
import numpy as np
import sys

global coords, colors, vertex_vbo, color_vbo, X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW

def display():
	global X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW, vertex_vbo, color_vbo, coords
	glGetError()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Performing translation and rotation
	glTranslatef(X_AXIS, Y_AXIS, Z_AXIS)
	glRotatef(PITCH, 1.0, 0.0, 0.0)
	glRotatef(ROLL, 0.0, 1.0, 0.0)
	glRotatef(YAW, 0.0, 0.0, 1.0)

	glBindBuffer(GL_ARRAY_BUFFER, vertex_vbo)
	glVertexPointer(3, GL_FLOAT, 0, None)
	glEnableClientState(GL_VERTEX_ARRAY)  
	glBindBuffer(GL_ARRAY_BUFFER, color_vbo) 
	glColorPointer(3, GL_FLOAT, 0, None) 
	glEnableClientState(GL_COLOR_ARRAY)
	glBindBuffer(GL_ARRAY_BUFFER, 0) 

	glDrawArrays(GL_QUADS, 0, 6*4*len(coords))
	glDisableClientState(GL_VERTEX_ARRAY)
	glDisableClientState(GL_COLOR_ARRAY)
	glFlush()
	glutSwapBuffers()
def generate_cube_vertices(point_vals):
	global X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW, coords, colors
	coords_arr = []
	colors_arr = []
	# Add 8 vertices in cube, colors for each vertex
	for x, y, z, r, g, b in point_vals:
		vertex_1 = [x, y, z]
		vertex_2 = [x+0.25, y, z]
		vertex_3 = [x+0.25, y+0.25, z]
		vertex_4 = [x, y+0.25, z]
		vertex_5 = [x, y, z+0.25]
		vertex_6 = [x+0.25, y, z+0.25]
		vertex_7 = [x+0.25, y+0.25, z+0.25]
		vertex_8 = [x, y+0.25, z+0.25]

		coords_arr.extend([vertex_1, vertex_2, vertex_3, vertex_4])
		coords_arr.extend([vertex_5, vertex_6, vertex_7, vertex_8])
		coords_arr.extend([vertex_1, vertex_4, vertex_8, vertex_5])
		coords_arr.extend([vertex_1, vertex_3, vertex_7, vertex_6])
		coords_arr.extend([vertex_1, vertex_2, vertex_6, vertex_5])
		coords_arr.extend([vertex_4, vertex_3, vertex_7, vertex_8])
		for x in range(24):
			colors_arr.append([r, g, b])
	coords = np.array(coords_arr, dtype=np.float32)
	colors = np.array(colors_arr, dtype=np.float32)
	#Calculate centroid for all vertices across cubes in each axis
	X_AXIS, Y_AXIS, Z_AXIS = coords.sum(axis=0) / len(coords)
	Z_AXIS -= 0.2
	PITCH, ROLL, YAW = 0.0, 0.0, 0.0
def onKeyDown(*args):
	global X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW
	# Retrieving key events and storing translation/rotation values
	key = args[0].decode("utf-8")
	if key == 'q':
		sys.exit()
	elif key == 'w':
		Y_AXIS += 0.1
	elif key == 's':
		Y_AXIS -= 0.1
	elif key == 'a':
		X_AXIS -= 0.1
	elif key == 'd':
		X_AXIS += 0.1
	elif key == 'z':
		Z_AXIS += 0.1
	elif key == 'x':
		Z_AXIS -= 0.1
	elif key == 'i':
		YAW += 1.0
	elif key == 'k':
		YAW -= 1.0
	elif key == 'j':
		PITCH -= 1.0
	elif key == 'l':
		PITCH += 1.0
	elif key == 'n':
		ROLL -= 1.0
	elif key == 'm':
		ROLL += 1.0
	# Clamping rotation
	np.clip(ROLL, -360.0, 360.0)
	np.clip(PITCH, -360.0, 360.0)
	np.clip(YAW, -360.0, 360.0)
	display()

def main():
	global coords, colors, vertex_vbo, color_vbo
	# IO using numpy
	file = sys.argv[1]
	if file:
		# Skipping header row in csv
		point_vals = np.loadtxt(file, delimiter = ',', skiprows=1)
		generate_cube_vertices(point_vals)
		# OpenGL Boilerplate setup
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
		glutInitWindowSize(500, 500)
		glutInitWindowPosition(200, 200)
		window = glutCreateWindow("Point Cloud Viewer")
		glutDisplayFunc(display)
		glutKeyboardFunc(onKeyDown)
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClearDepth(1.0) 
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)   
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(70., 640.0 / 360.0, 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)
		# Setup buffers for parallelization
		vertex_vbo, color_vbo = glGenBuffers(2)
		glBindBuffer(GL_ARRAY_BUFFER, vertex_vbo)
		glBufferData(GL_ARRAY_BUFFER, coords, GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
		glBufferData(GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		# Render Loop
		glutMainLoop()
 
if __name__ == "__main__":
	main()
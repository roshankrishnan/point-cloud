from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import numpy as np
import sys

global coords, colors, X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW

def display():
	global X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW, coords, colors
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Performing translation and rotation
	glTranslatef(X_AXIS, Y_AXIS, Z_AXIS)
	glRotatef(PITCH, 1.0, 0.0, 0.0)
	glRotatef(ROLL, 0.0, 1.0, 0.0)
	glRotatef(YAW, 0.0, 0.0, 1.0)
	i = 0
	glBegin(GL_QUADS)
	for p1, p2, p3, p4, p5, p6, p7, p8 in coords:
		glColor3f(colors[i][0], colors[i][1], colors[i][2])

		glVertex3f(p1[0], p1[1], p1[2])
		glVertex3f(p2[0], p2[1], p2[2])
		glVertex3f(p3[0], p3[1], p3[2])
		glVertex3f(p4[0], p4[1], p4[2])

		glVertex3f(p5[0], p5[1], p5[2])
		glVertex3f(p6[0], p6[1], p6[2])
		glVertex3f(p7[0], p7[1], p7[2])
		glVertex3f(p8[0], p8[1], p8[2])

		glVertex3f(p1[0], p1[1], p1[2])
		glVertex3f(p4[0], p4[1], p4[2])
		glVertex3f(p8[0], p8[1], p8[2])
		glVertex3f(p5[0], p5[1], p5[2])

		glVertex3f(p1[0], p1[1], p1[2])
		glVertex3f(p3[0], p3[1], p3[2])
		glVertex3f(p7[0], p7[1], p7[2])
		glVertex3f(p6[0], p6[1], p6[2])

		glVertex3f(p1[0], p1[1], p1[2])
		glVertex3f(p2[0], p2[1], p2[2])
		glVertex3f(p6[0], p6[1], p6[2])
		glVertex3f(p5[0], p5[1], p5[2])

		glVertex3f(p4[0], p4[1], p4[2])
		glVertex3f(p3[0], p3[1], p3[2])
		glVertex3f(p7[0], p7[1], p7[2])
		glVertex3f(p8[0], p8[1], p8[2])

		i +=1
	glEnd()
	glutSwapBuffers()
def generate_cube_vertices(point_vals):
	global X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW, coords, colors
	X_AXIS, Y_AXIS, Z_AXIS = 0.0, 0.0, 0.0
	coords_arr = []
	colors_arr = []
	# Add 8 vertices in cube, colors for each vertex
	for x, y, z, r, g, b in point_vals:
		X_AXIS += x
		Y_AXIS += y
		Z_AXIS += z
		cube = []
		cube.append([x, y, z])
		cube.append([x+0.25, y, z])
		cube.append([x+0.25, y+0.25, z])
		cube.append([x, y+0.25, z])
		cube.append([x, y, z+0.25])
		cube.append([x+0.25, y, z+0.25])
		cube.append([x+0.25, y+0.25, z+0.25])
		cube.append([x, y+0.25, z+0.25])
		coords_arr.append(cube)
		colors_arr.append([r, g, b])
	coords = np.array(coords_arr, dtype=np.float32)
	colors = np.array(colors_arr, dtype=np.float32)
	#Calculate centroid for all vertices across cubes in each axis
	X_AXIS /= len(coords)
	Y_AXIS /= len(coords)
	Z_AXIS /= len(coords)
	Z_AXIS -= 20.0
	PITCH, ROLL, YAW = 0.0, 0.0, 0.0
def onKeyDown(*args):
	global X_AXIS, Y_AXIS, Z_AXIS, PITCH, ROLL, YAW
	# Retrieving key events and storing translation/rotation values
	key = args[0].decode("utf-8")
	if key == 'q':
		sys.exit()
	elif key == 'w':
		Y_AXIS -= 0.1
	elif key == 's':
		Y_AXIS += 0.1
	elif key == 'a':
		X_AXIS += 0.1
	elif key == 'd':
		X_AXIS -= 0.1
	elif key == 'z':
		Z_AXIS -= 0.1
	elif key == 'x':
		Z_AXIS += 0.1
	elif key == 'i':
		YAW -= 1.0
	elif key == 'k':
		YAW += 1.0
	elif key == 'j':
		PITCH += 1.0
	elif key == 'l':
		PITCH -= 1.0
	elif key == 'n':
		ROLL += 1.0
	elif key == 'm':
		ROLL -= 1.0
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
		
		# Render Loop
		glutMainLoop()
 
if __name__ == "__main__":
	main()
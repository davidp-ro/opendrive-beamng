"""
  This file is ran on the "main" machine where you want to see the visualization
or manipulate the data
"""

import socket
import pickle
from datetime import datetime

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from beamngpy.sensors import Lidar
from beamngpy.visualiser import LidarVisualiser

SERVER = '192.168.0.152'  # VM Address
PORT = 6555

WINDOW_SIZE = 512

def lidar_resize(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)

def open_window(width, height):
    title = ""
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(width, height)
    title_list = ["LIDAR Visualizer @ ", SERVER, ":", str(PORT)]
    title = title.join(title_list).encode('ascii')
    glutCreateWindow(title)
    lidar_resize(width, height)

def main():
    open_window(WINDOW_SIZE, WINDOW_SIZE)
    lidar_visualizer = LidarVisualiser(Lidar.max_points)
    lidar_visualizer.open(WINDOW_SIZE, WINDOW_SIZE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        packet = b""

        def update():
            nonlocal packet
            packet += s.recv(1024)
                
            try:
                data = pickle.loads(packet)
                print("Data recieved @ ", datetime.now())
                lidar_visualizer.update_points(data[0], data[1])
                glutPostRedisplay()
                packet = b""
            except:
                pass

        glutReshapeFunc(lidar_resize)
        glutIdleFunc(update)
        glutMainLoop()

if __name__ == '__main__':
    main()

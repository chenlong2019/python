import sys
from qgis.core import QgsApplication
from qgis.gui import QgsMapCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog

def init():
  a = QgsApplication([], True)
  QgsApplication.setPrefixPath('qgis', True)
  QgsApplication.initQgis()
  return a

def show_canvas(app):
  canvas = QgsMapCanvas()
  canvas.show()
  app.exec_()
app = init()
show_canvas(app)
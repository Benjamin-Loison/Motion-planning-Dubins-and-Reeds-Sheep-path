#!/usr/bin/python3

# initial Qt graphics source: https://zetcode.com/pyqt/qpropertyanimation/ anim_along_curve.py

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPainterPath, QTransform
from PyQt5.QtCore import QPointF, QPropertyAnimation, pyqtProperty, Qt
import os, matplotlib.pyplot as plt
from math import cos, sin, atan, radians, pi

path = 'C:\\Users\\Benjamin\\Desktop\\BensFolder\\School\\ENS\\Saclay\\M1\\Robotics\\Motion-planning-Dubins-and-Reeds-Sheep-paths\\'

os.chdir(path)

##

windowWidth, windowHeight = 1920, 1080
windowWidthDiv2, windowHeightDiv2 = windowWidth // 2, windowHeight // 2
unitSize = 100

class Vehicle(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.pix = QPixmap("smallCar.png")
        self.h = self.pix.height()
        self.w = self.pix.width()

        self.setPixmap(self.pix)

    def setPos(self, pos):
        self.move(pos.x() - self.w / 2, pos.y() - self.h / 2)

    def setAngle(self, angle):
        pass

    pos = pyqtProperty(QPointF, fset=setPos)
    angle = pyqtProperty(float, fset=setAngle)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initView()
        self.initAnimation()

    def initView(self):
        self.path = QPainterPath()

        self.path.moveTo(graphicStart[0], graphicStart[1])

        self.path.arcTo(graphicStart[0], graphicStart[1] - graphicR // 2, graphicR, graphicR, 180, -90)
        self.path.lineTo(graphicEnd[0] - graphicR, graphicEnd[1] - graphicR // 2)
        self.path.arcTo(graphicEnd[0] - graphicR, graphicEnd[1] - graphicR // 2, graphicR, graphicR, 90, -90)

        self.path.lineTo(graphicEnd[0], graphicEnd[1])

        self.vehicle = Vehicle(self)

        self.setWindowTitle("Dubin's car")
        self.setGeometry(0, 0, windowWidth, windowHeight)
        self.showMaximized()
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.drawPath(self.path)
        qp.end()

    def initAnimation(self):
        self.anim = QPropertyAnimation(self.vehicle, b'pos')
        self.anim.setDuration(7000)

        self.anim.setStartValue(QPointF(graphicStart[0], graphicStart[1]))

        vals = [p/100 for p in range(0, 101)]

        for i in vals:
            self.anim.setKeyValueAt(i, self.path.pointAtPercent(i))

        self.anim.setEndValue(QPointF(graphicEnd[0], graphicEnd[1]))
        self.anim.start()

minTurnRadius = 2
r = minTurnRadius
start = [-5, 0]
startAngle = radians(90)
end = [5, 0]
endAngle = -radians(90)

graphicStart = [start[0] * unitSize + windowWidthDiv2,
                start[1] * unitSize + windowHeightDiv2]
graphicEnd = [end[0] * unitSize + windowWidthDiv2,
              end[1] * unitSize + windowHeightDiv2]
graphicR = r * unitSize

# RSR case

centerC1 = [start[0] + r * cos(startAngle - pi / 2),
            start[1] + r * sin(startAngle - pi / 2)]

centerC2 = [end[0] + r * cos(endAngle - pi / 2),
            end[1] + r * sin(endAngle - pi / 2)]

V1 = [centerC2[0] - centerC1[0],
      centerC2[1] - centerC1[1]]

circle1 = plt.Circle((centerC1[0], centerC1[1]), r)
circle2 = plt.Circle((centerC2[0], centerC2[1]), r)

fig, ax = plt.subplots()

ax.add_patch(circle1)
ax.add_patch(circle2)

alpha = atan(V1[1] / V1[0])
P3 = [centerC1[0] + r * sin(alpha),
      centerC1[1] + r * cos(alpha)]
P4 = [centerC2[0] + r * sin(alpha),
      centerC2[1] + r * cos(alpha)]
P5 = [centerC1[0] - r * sin(alpha),
      centerC1[1] - r * cos(alpha)]
P6 = [centerC2[0] - r * sin(alpha),
      centerC2[1] - r * cos(alpha)]

plt.scatter(start[0], start[1], color = 'green')
plt.scatter(end[0], end[1], color = 'green')

plt.scatter(P3[0], P3[1], color = 'red')
plt.scatter(P4[0], P4[1], color = 'red')
plt.scatter(P5[0], P5[1], color = 'blue')
plt.scatter(P6[0], P6[1], color = 'blue')
#plt.show()

app = QApplication()
ex = Window()
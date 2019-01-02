from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
def Hand():
	app = MyApp()
	app.run()


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
 
        self.disableMouse()
        tex = loader.loadTexture('HandTexture.png')

        self.Hand = Actor("Hand.egg")
        self.Hand.setScale(1.5, 1.5, 1.5)
        self.Hand.setTexture(tex, 1)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.moveFinger, "MoveFingerTask")
        
        self.Hand.reparentTo(self.render)

    def moveFinger(self, task):
        #self.Hand.listJoints()
        angleDegrees = task.time * 100.0
        myNodePath = self.Hand.controlJoint(None,"modelRoot","index1")
        myNodePath.setHpr(0,30*sin(angleDegrees*pi/180),0)
        return task.cont
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = 60
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 4)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.done
 

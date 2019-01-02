from math import pi, sin, cos
import multiprocessing


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
def Hand(fingerInput):
	app = MyHand(fingerInput)
	app.run()


class MyHand(ShowBase):
    def __init__(self,fingerInput):
        ShowBase.__init__(self)
        self.fingerPositions = fingerInput;
 
        self.disableMouse()
        tex = loader.loadTexture('HandTexture.png')

        self.Hand = Actor("Hand.egg")
        self.Hand.setScale(1.5, 1.5, 1.5)
        self.Hand.setTexture(tex, 1)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.moveFingers, "MoveFingerTask")
        #self.taskMgr.add(self.updateFingers(fingerInput), "UpdateFingerTask")
        
        self.Hand.reparentTo(self.render)

    def moveFingers(self, task):
        #self.Hand.listJoints()
        angleDegrees = 90*self.fingerPositions.get() #task.time * 100.0
        #print(angleDegrees)
        fingerList = ["pinky","ring","middle","index","thumb"]
        jointNumber = 3
        for finger in fingerList:
            if finger == "thumb":
                NodePath = self.Hand.controlJoint(None,"modelRoot", finger+ str(1))
                Init_Rot = NodePath.getHpr()
                NodePath.setHpr(-15*(sin(angleDegrees*pi/180)+1) + Init_Rot.getX(),
                                -5*(sin(angleDegrees*pi/180)-2) + Init_Rot.getY(),
                                                                 Init_Rot.getZ())
                NodePath = self.Hand.controlJoint(None,"modelRoot", finger+ str(2))
                Init_Rot = NodePath.getHpr()
                NodePath.setHpr(Init_Rot.getX() + 15*(sin(angleDegrees*pi/180)-1),
                                Init_Rot.getY() - 15*(sin(angleDegrees*pi/180)-1),
                                       Init_Rot.getZ())
                NodePath = self.Hand.controlJoint(None,"modelRoot", finger+ str(3))
                Init_Rot = NodePath.getHpr()
                NodePath.setHpr(Init_Rot.getX() + 15*(sin(angleDegrees*pi/180)-1),
                                Init_Rot.getY() - 5*(sin(angleDegrees*pi/180)-1),
                                       Init_Rot.getZ())
            else:
                for i in range(1,jointNumber+1):
                    NodePath = self.Hand.controlJoint(None,"modelRoot", finger+str(i))
                    NodePath.setHpr(45*(sin(angleDegrees*pi/180)-1),0,0)
        return task.cont
    #def updateFingers(self,task):
    #    self.fingerPositions = input.get()
    #    return task.cont
    def spinCameraTask(self, task):
        angleDegrees = 60
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 4)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.done
 

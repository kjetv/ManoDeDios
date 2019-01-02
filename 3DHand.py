from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
 
        # Disable the camera trackball controls.
        self.disableMouse()
 
        # Load the environment model.
        #self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        #self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        #self.scene.setScale(0.25, 0.25, 0.25)
        #self.scene.setPos(-8, 42, 0)
 
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
 
        # Load and transform the panda actor.
        self.pandaActor = self.loader.loadModel("Hand.egg")
        self.pandaActor.setScale(1.5, 1.5, 1.5)

        self.pandaActor.reparentTo(self.render)
        tex = loader.loadTexture('HandTexture.png')
        self.pandaActor.setTexture(tex, 1)

        #self.taskMgr.add(self.moveLeg, "MoveLegTask")
        


        self.pandaActor.reparentTo(self.render)
    def moveLeg(self, task):
        angleDegrees = task.time * 100.0
        myNodePath = self.pandaActor.controlJoint(None,"modelRoot","Bone_lr_leg_hip")
        myNodePath.setHpr(0,30*sin(angleDegrees*pi/180)-180,0)
        return task.cont
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
 
app = MyApp()
app.run()
#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

def cos(angle):
    return math.cos(math.radians(angle))

def sin(angle):
    return math.sin(math.radians(angle))

def atan(angle):
    return math.atan(math.radians(angle))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
         # Get active design
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
 
        # Get root component in this design
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)  

        
        
        # R = 28
        # # R = 26
        # E = 1
        # r = 4/2
        # N = 14

        
        # N = 20
        N = 62 # 기어비 : N/2
        r = 0.4
        R = r*N

        # X = lambda seta : (R*cos(seta)) - (r * cos(seta+atan(sin((1-N)*seta) / (R/(E*N)) - cos((1-N)*seta)))) - (E*cos(N*seta))
        # Y = lambda seta : (R*sin(seta)) - (r * sin(seta+atan(sin((1-N)*seta) / (R/(E*N)) - sin((1-N)*seta)))) - (E*sin(N*seta))
        
        XE = lambda seta : (R+r)*cos(seta) - (r)*cos(((R+r)/r) * seta)
        YE = lambda seta : (R+r)*sin(seta) - (r)*sin(((R+r)/r) * seta)

        XH = lambda seta : (R-r)*cos(seta) + (r)*cos(((R-r)/r) * seta)
        YH = lambda seta : (R-r)*sin(seta) - (r)*sin(((R-r)/r) * seta)

        X_ = lambda seta : (R)*cos(seta)
        Y_ = lambda seta : (R)*sin(seta)
        
        radio = 360 / N
        off = 0
        th = True

        last_point=None
        line=None

        lines=[]

        points = adsk.core.ObjectCollection.create()
        for angle in drange(0,360, 1.5):
            
            if angle >= off + radio:
                off += radio
                th = not th

            X =  XE if th else XH
            Y =  YE if th else YH


            point_x = X(angle)*0.1
            point_y = Y(angle)*0.1


            # if angle==0:
                # the first point
                # last_point = adsk.core.Point3D.create(point_x,point_y, 0)
            # else:
                # sketch.sketchCurves.sketchFittedSplines.add()
                # line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                #     last_point, 
                #     adsk.core.Point3D.create(point_x,point_y, 0)
                #     )
                # # last_point=line.endSketchPoint
                # lines.append(line)
                # pass

            points.add(adsk.core.Point3D.create(point_x,point_y, 0))
            app.activeViewport.refresh()

        # Add the geometry to a collection. This uses a utility function that
        # automatically finds the connected curves and returns a collection.
        # curves = sketch.findConnectedCurves(lines[0])
        sketch.sketchCurves.sketchFittedSplines.add(points)
        # Create the offset.
        dirPoint = adsk.core.Point3D.create(0, 0, 0)
        # offsetCurves = sketch.offset(curves, dirPoint, pin_radius)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

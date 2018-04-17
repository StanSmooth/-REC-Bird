
import time
import numpy as np
import cv2

imgproc.start_tag_detector()
imgproc.set_tag_family("Tag36h11")
periIdeal=180
basicctl.takeoff()
time.sleep(0.1)

xmax=630
ymax=340

x1t=3*xmax/12
x2t=9*xmax/12
y1t=xmax/3
y2t=2*xmax/3

cond = 0
vitesse=0.5
vitesseRot=0.1
sleep=0.1
condhover=0

while cond !=1:

    detections = imgproc.tag_detections()
    img = imgproc.latest_frame()
    i = 0
    for (id, good, points) in detections:
        cv2.putText(img, 'id = ' + str(id), (10, 30 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        for (x, y) in points:
            cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
        i+=1
        #print(i)
        if detections[0][0]==1:
            print("executez l'ordre 66")
            cond=1
            
        if detections[0][0]==0:
            topLeftx=detections[0][2][3][0]
            topLefty=detections[0][2][3][1]
            topRightx=detections[0][2][2][0]
            topRighty=detections[0][2][2][1]
            downRightx=detections[0][2][1][0]
            downRighty=detections[0][2][1][1]
            downLeftx=detections[0][2][0][0]
            downLefty=detections[0][2][0][1]
	
            long=downRightx-downLeftx
            larg=downLefty-topLefty
            peri=2*(long+larg)
            

        
            if peri < periIdeal*80/100:
                basicctl.move_rel(-vitesse, 0, 0, 0)
                print("avance")
                time.sleep(sleep)
                condhover=0

            if peri > periIdeal*120/100:
                basicctl.move_rel(vitesse, 0, 0, 0)
                time.sleep(sleep)
                print("recule")
                condhover=0

            if ((peri > periIdeal*80/100) and (peri < periIdeal*120/100) and (condhover==0))  :
                basicctl.move_rel(0, 0, 0, 0)
                condhover=1
                
                
            #if (((downLeftx-topLeftx)*150/100) > (downRightx-topRightx)):
                #print("translation droite")

            #if (((downRightx-topRightx)*150/100) > (downLeftx-topLeftx)):
                #print("translation gauche")


            if((downLeftx>x1t and downLeftx<x2t) and (topLeftx>x1t and topLeftx<x2t) and (downRightx>x1t and downRightx<x2t) and (topRightx>x1t and topRightx<x2t)):
                print("oklm")
            

            if ((downLeftx > x2t) and (downRightx > x2t) and (topRightx > x2t) and (topLeftx > x2t)):
                print("translation droite")
                basicctl.move_rel(0, 0, 0, vitesseRot)
                #time.sleep(sleep)

            if ((downLeftx < x1t) and (downRightx < x1t) and (topRightx < x1t) and (topLeftx < x1t)):
                print("translation gauche")
                basicctl.move_rel(0, 0, 0, -vitesseRot)
                #time.sleep(sleep)

        
        imgproc.show_frame(img)
    
    
        time.sleep(sleep)
basicctl.land()
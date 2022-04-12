import cv2
from cvzone.HandTrackingModule import HandDetector

# Dimension of Frame
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

# Detector
detector = HandDetector(detectionCon=0.8)
startDistance = None
scale = 0
cx,cy = 500,500

# Getting the Frames from Web Cam
while True:
    success,img = cap.read()
    hands,img = detector.findHands(img)
    overLayImg = cv2.imread("./1.png")
    if len(hands) == 2:
        # print(detector.fingersUp(hands[0]),detector.fingersUp(hands[1]))
        if detector.fingersUp(hands[0]) == [1,1,0,0,0] and detector.fingersUp(hands[1]) == [1,1,0,0,0]:
            # print("Zoom")
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            # tip of the index finger -> point 8
            # lmList1[8],lmList2[8]
            if startDistance is None:
                # length,info,img = detector.findDistance(lmList1[8][0:2],lmList2[8][0:2],img)
                length,info,img = detector.findDistance(hands[0]["center"],hands[1]["center"],img)
                # print(length)
                startDistance = length
            # length,info,img = detector.findDistance(lmList1[8][0:2],lmList2[8][0:2],img)
            length,info,img = detector.findDistance(hands[0]["center"],hands[1]["center"],img)
            scale = int((length - startDistance)//2)
            cx,cy = info[4],info[5]
            # print(scale)
    else:
        startDistance = None

    try:
        h1,w1,_ = overLayImg.shape
        newH,newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2
        overLayImg = cv2.resize(overLayImg,(newH,newW))
        # 225 // 2 = 112.5 = 112 -> 112 * 2 = 224 -> lost one pixel from width and height -> we need to make them equal
        img[cy-newH//2:cy+newH//2,cx-newW//2:cx+newW//2] = overLayImg
        cv2.imshow("Front View",img)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    except:
        pass
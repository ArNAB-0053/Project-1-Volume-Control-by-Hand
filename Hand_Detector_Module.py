import mediapipe as mp
import cv2
import time



# while(True):
class HandDetector():
    def __init__(self, 
            mode = False, 
            maxHands = 2, 
            model_complexity=1, 
            detectionConfidence = 0.5, 
            trackConfidence = 0.5,
        ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(thickness = 2, circle_radius = 2, color = (0, 250, 0))

    def FindHands(self, frame, draw = True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(frameRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handlms, self.mpHands.HAND_CONNECTIONS, self.drawSpec, self.drawSpec)
        return frame
    
    def FindPosition(self, frame, draw = True, handNo=0):
        lmList = []
    
        if self.results.multi_hand_landmarks:
            exHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(exHand.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x*w) , int(lm.y*h)
                    # print(id, cx, cy)
                    lmList.append([id, cx, cy])

                    if draw:
                    # if id == 4: # We can use (0 -20) and each of index has specific hand part
                        cv2.circle(frame, (cx, cy), 3, (255, 50, 0), cv2.FILLED)

        return lmList
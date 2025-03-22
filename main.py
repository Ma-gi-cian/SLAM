import sdl2
import cv2
import sdl2.ext
import numpy as np

W = 1920//2
H = 1080 // 2

class Features(object):
    def __init__(self):
        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher()
        self.last = None

    def extract(self, img):
        ## detect features 
        feats = cv2.goodFeaturesToTrack(np.mean(img, axis = 2).astype(np.uint8), 3000, qualityLevel=0.01, minDistance = 3)

        kps = [ cv2.KeyPoint(x=f[0][0], y=f[0][1], size=20) for f in feats]
        kps, des = self.orb.compute(img, kps)
        ## matching 
        matches = None
        if self.last is not None:
            matches = self.bf.match(des, self.last['des'])
            print(matches)
        self.last = { 'kps': kps, 'des': des } 
        return kps, des, matches

def process_frame(img):
    img = cv2.resize(img, (W, H))
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_Quit:
            exit(0)
    surf = sdl2.ext.pixels3d(window.get_surface())
    keypoints, descriptors, matches = fe.extract(img)
    for kps in keypoints:
        u,v = int(round(kps.pt[0])), int(round(kps.pt[1]))
        cv2.circle(img, (u,v), color=(0,234,0), radius = 3)
    surf[:, :, 0:3] = img.swapaxes(0,1)
    window.refresh()

file_path = "test_countryroad.mp4"

fe =  Features() 

if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
    print(sdl2.SDL_GetError())
    exit(1)

# Example SDL2 code (replace with your actual code)
window = sdl2.ext.Window("SDL2 Example", size=(W, H), position = (100,100))
window.show()

cap = cv2.VideoCapture(file_path)

while cap.isOpened():
    ret , frame = cap.read()
    if ret == True:
        process_frame(frame)
    else :
        break

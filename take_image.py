import cv2
import  os

# path direction
image_dir = "IMG"
current_dir = os.getcwd()
image_savepath = os.path.join(current_dir, image_dir)

try:
    os.mkdir(image_savepath)   
except:
    pass

cap = cv2.VideoCapture(0)
num = 0
if not (cap.isOpened()):
    print("Could not open video device")

while cap.isOpened():
    # Capture frame-by-frame    
    ret, frame = cap.read()
    k = cv2.waitKey(5)
    # Waits for a user input to quit the application
    if k == 27:
        break
    elif k == ord("s"):
        cv2.imwrite( image_savepath + '/' +  f"image{str(num)}.png",frame)
        print("Image " + str(num) + " saved!")
        num += 1
    cv2.imshow("img",frame)
cap.release()
cv2.destroyAllWindows()


#The thinh thinh#

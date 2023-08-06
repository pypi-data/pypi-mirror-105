import cv2
import time as t

pT = 0


# ****************************************************************************

def showFrameRate(frame):
    """
    To use just call the function and pass the main frame/image
    :param frame:
    :return Put's the FPS text on frame/image given as param:
    """
    global pT

    cT = t.time()
    fps = 1 / (cT - pT)
    pT = cT

    cv2.putText(frame, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)


def dummy():
    """
    call this to test
    if you want to use the main one call showFrameRate
    :return:
    """
    cam = cv2.VideoCapture(0)

    while True:
        s, img = cam.read()

        showFrameRate(img)
        cv2.imshow("img", img)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    """
    Call this dummy func to test the package
    """
    dummy()

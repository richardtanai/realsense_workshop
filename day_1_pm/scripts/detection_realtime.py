from camera import D435
from model import MaskRCNN_MODEL

import cv2



def main():
    my_d435 = D435()
    my_model = MaskRCNN_MODEL()

    while True:
        cap = my_d435.capture()
        img_bgr = cap["color"]

        img = my_model.process_image(img_bgr)


        cv2.imshow("Live Capture", img)

        # process image here


        # press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    my_d435.stop()





if __name__ == "__main__":
    main()

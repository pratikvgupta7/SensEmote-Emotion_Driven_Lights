import numpy as np
import cv2
preimg = cv2.imread('/piemote/image.jpg',1)
cv2.imshow('image',preimg)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2 as cv
import numpy as np

img = np.random.randint(0, 255, (119, 162), dtype=np.uint8)
cv.imshow("test", img)
cv.waitKey(0)
cv.destroyAllWindows()
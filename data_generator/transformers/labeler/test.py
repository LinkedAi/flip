import cv2

# load image PNG format
img = cv2.imread('test2.png', cv2.IMREAD_COLOR)

# canny edge detection - edge gradient
edged = cv2.Canny(img, 10, 250)

# Morphological Transformations
# applying closing function 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

# resources
# Morphological Transformations
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

#finding_contours 
(cnts, _) = cv2.findContours(
    closed.copy(),
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)

idx=0

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    # print(x,y)
    if w>50 and h>50:
        idx+=1
        new_img=img[y:y+h,x:x+w]
        cv2.imwrite(str(idx) + '.png', new_img)

        # Window name in which image is displayed
        window_name = 'Object'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        # Using cv2.imshow() method
        # Displaying the image  
        
        # cv2.circle(img, (x,y), 2, 
        #     (0,255,0), thickness=6, lineType=8, shift=0)
        copyimg=img.copy()
        ww=new_img.shape[0]
        hh=new_img.shape[1]

        # # print(hh)
        # cv2.rectangle(copyimg,start_point=(x,y),end_point=(x+ww,y+hh),color=(0,255,0),thickness=6)

        cv2.imshow(window_name, img)
        k = cv2.waitKey(0) & 0xFF

        # wait for ESC key to exit 
        if k == 27:
            cv2.destroyAllWindows() 


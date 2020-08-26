import cv2
import numpy as np
import matplotlib.pyplot as plt


def inv_channels(image):
    image[..., :3] = image[..., (2, 1, 0)]
    return image


def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    scale = 1.0

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, scale)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # distance matrix
    # dst_mat = np.zeros((h, w, 4), np.uint8)

    # perform the actual rotation and return the image
    return cv2.warpAffine(
        image,
        M,
        (nW, nH),
        # dst_mat,
        # flags=cv2.INTER_LINEAR,
        # borderMode=cv2.BORDER_TRANSPARENT,
    )


def overlay_transparent(
    background: np.ndarray,
    overlay: np.ndarray,
    mask: np.ndarray,
    x: int,
    y: int,
    hist_match=False,
    min_object_brightness=0,
):

    background_width = background.shape[1]
    background_height = background.shape[0]

    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    x = x or 0
    y = y or 0

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]
        mask = mask[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]
        mask = mask[:h]

    mask = mask / 255.0

    if mask.ndim < background.ndim:
        mask = np.expand_dims(mask, axis=-1)

    if overlay.ndim < background.ndim:
        overlay = np.expand_dims(overlay, axis=-1)

    if background.ndim > 2 and background.shape[2] > 3:
        background = background[..., :3]

    if hist_match:
        overlay = histogram_matching_h(
            overlay, background[y : y + h, x : x + w], min_v=min_object_brightness
        )
    background[y : y + h, x : x + w] = (1.0 - mask) * background[
        y : y + h, x : x + w
    ] + mask * overlay
    return background


def crop_from_contour(image):
    _, _, _, a = cv2.split(image)
    ret, thresh = cv2.threshold(a, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    index = 0
    for i in range(len(contours)):
        if len(contours[i]) > len(contours[index]):
            index = i
    rect = cv2.boundingRect(contours[index])
    cropped_img = image[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]

    # plt.imshow(cropped_img)
    # plt.show()

    return cropped_img

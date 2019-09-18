#!/usr/local/bin/python3
#https://stackoverflow.com/questions/29313667/how-do-i-remove-the-background-from-this-kind-of-image
import cv2
import numpy as np
import sys

def removeBackgroundFromImage(src):
    #== Parameters =======================================================================
    BLUR = 21
    CANNY_THRESH_1 = 5
    CANNY_THRESH_2 = 250
    MASK_DILATE_ITER = 50
    MASK_ERODE_ITER = 5
    MASK_COLOR = (0.6118, 0.9098, 0.8667) # In BGR format


    #== Processing =======================================================================

    #-- Read image -----------------------------------------------------------------------
    img = cv2.imread(src)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2, 2)
    edges = cv2.dilate(edges, None, iterations=MASK_DILATE_ITER)
    edges = cv2.erode(edges, None, iterations=MASK_ERODE_ITER)

    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)


    # Previously, for a previous version of cv2, this line was: 
    #  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Thanks to notes from commenters, I've updated the code but left this note
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]


    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)


    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask
    cv2.imwrite('mask.jpg', mask)

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    # cv2.imwrite(sys.argv[1], masked)
    return masked
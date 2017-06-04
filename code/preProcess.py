# -*- coding:utf-8 -*-
# import cv2
# import numpy as np
# from matplotlib import pyplot
#
# # 加载图片
# img = cv2.imread('../data/result_11_3.png')
#
# # 转换为灰度图像
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # 移除noisy
# img1 = cv2.GaussianBlur(gray, (3, 3), 0)
#
# # 边缘检测
# laplacian = cv2.Laplacian(img1, cv2.CV_64F)
# sobelx = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize=5)  # x
# sobely = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize=5)  # y
#
# pyplot.subplot(2, 2, 1), pyplot.imshow(img1, cmap='gray')
# pyplot.title('Origin'), pyplot.xticks([]), pyplot.yticks([])
# pyplot.subplot(2, 2, 2), pyplot.imshow(laplacian, cmap='gray')
# pyplot.title('Laplacian'), pyplot.xticks([]), pyplot.yticks([])
# pyplot.subplot(2, 2, 3), pyplot.imshow(sobelx, cmap='gray')
# pyplot.title('Sobel X'), pyplot.xticks([]), pyplot.yticks([])
# pyplot.subplot(2, 2, 4), pyplot.imshow(sobely, cmap='gray')
# pyplot.title('Sobel Y'), pyplot.xticks([]), pyplot.yticks([])
#
# pyplot.show()


# import cv2
# from matplotlib import pyplot as plt
#
# img = cv2.imread('../data/final_image16.png', 0)
# edges = cv2.Canny(img, 100, 200)
#
# plt.subplot(121), plt.imshow(img, cmap='gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(edges, cmap='gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()


from PIL import Image

pil_im = Image.open('../data/89.png')
pil_im = pil_im.convert('L')
pil_im.save('../data/newGG3.png')





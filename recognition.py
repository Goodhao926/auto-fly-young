import tensorflow as tf
import numpy as np
import cv2 as cv
from datasetGen.utils.VerifyCode import VeifyCode
label = ['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
         'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

model = tf.keras.models.load_model('model.h5')  # 加载模型


def predict(filename):
    imgs = pre_process(filename)
    result = []
    for idx, img in enumerate(imgs):
        src = tf.reshape(img, [1, 22, 22, 1])
        src = tf.cast(src, dtype=tf.float32) / 255.
        res = np.argmax(model.predict(src))
        result.append(label[res])
    return "".join(result)


def pre_process(filename):
    img = cv.imread(filename)
    lowerb = 0
    upperb = 120
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.medianBlur(img_gray, ksize=3)
    back_mask = cv.inRange(img_blur, lowerb, upperb)
    contours, hierarchy = cv.findContours(back_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    img = cv.cvtColor(back_mask, cv.COLOR_GRAY2BGR)
    code_imgs = []
    contours = VeifyCode.contours_sort(contours)
    for cidx, cnt in enumerate(contours):
        (x, y, w, h) = cv.boundingRect(cnt)
        digit = img[y:y + h, x:x + w]
        digit = VeifyCode.getStandardDigit(digit)
        digit = cv.cvtColor(digit,cv.COLOR_BGR2GRAY)
        code_imgs.append(digit)
    return code_imgs


if __name__ == '__main__':
    while True:
        filename = VeifyCode.getVerifyCode()
        img = cv.imread(filename)
        res = predict(filename)
        print(res)
        cv.imshow("main", img)
        cv.waitKey()


import cv2 as cv
import numpy as np
import requests
import time, shutil, os
import glob
class VeifyCode:
    url = ""
    code_len = 4
    dir = "test"
    @staticmethod
    def getVerifyCode():
        url = "http://125.88.59.131:10001/common/image_code.jsp?time=" + str(time.time_ns())
        img = requests.get(url)

        with open('datasetGen/tmp/img.jpg',"wb") as f:
            f.write(img.content)

        return 'datasetGen/tmp/img.jpg'


    @staticmethod
    def getStandardDigit(img):
        STD_WIDTH = 22
        STD_HEIGHT = 22
        res = cv.resize(img, (STD_WIDTH, STD_HEIGHT))
        return res

    @staticmethod
    def divide(filename):
        try:
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
                code_imgs.append(digit)
            filenames = []
            if len(code_imgs) == VeifyCode.code_len:
                for idx, item in enumerate(code_imgs):
                    fn = "tmp/{}.jpg".format(idx)
                    cv.imwrite(fn, item)
                    filenames.append(fn)
                return filenames
            return None
        except:
            import traceback
            traceback.print_exc()

    @staticmethod
    def contours_sort(contours, method=0):
        if method == 0:
            contours = sorted(contours, key=lambda x: cv.boundingRect(x)[0])
        else:
            contours = sorted(contours, key=lambda x: cv.boundingRect(x)[0], reverse=True)

        return contours

    @staticmethod
    def save(chars):
        if len(chars) != VeifyCode.code_len:
            return False
        for i in range(VeifyCode.code_len):
            from_ = "tmp/{}.jpg".format(i)
            to_dir = "../dataset/"+ VeifyCode.dir +"/" + chars[i]
            if not os.path.exists(to_dir):
                os.mkdir(to_dir)
            idx = len(os.listdir(to_dir))
            shutil.move(from_, "{}/{}.jpg".format(to_dir, idx))

    @staticmethod
    def getDatasetSize():
        return len(glob.glob("../dataset/"+VeifyCode.dir +"/*/*"))


if __name__ == "__main__":
    print(VeifyCode.getDatasetSize())
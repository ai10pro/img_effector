import cv2
import numpy as np



# -------画像サイズ取得処理----------
def get_img_size(file_name):
    if file_name:
        img = cv2.imread(file_name,cv2.IMREAD_COLOR)
        height, width, channels = img.shape[:3]
        print("width: " + str(width))
        print("height: " + str(height))
        return height,width
    else :
        return None,None
#----------------------------------

#-----ドット絵処理------------
# 減色処理
def sub_color(src, K):
    Z = src.reshape((-1,3))     # 次元数を1落とす
    Z = np.float32(Z)           # float32型に変換
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)    # 基準の定義
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)    # K-means法で減色
    center = np.uint8(center)    # UINT8に変換
    res = center[label.flatten()]
    return res.reshape((src.shape))    # 配列の次元数と入力画像と同じに戻す

# モザイク処理
def mosaic(img, alpha):
    h, w, ch = img.shape
    img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
    img = cv2.resize(img,(w,h), interpolation=cv2.INTER_NEAREST)
    return img

def pixel_art(img, alpha=2 ,K=4):
    img = mosaic(img,alpha)
    return sub_color(img, K)
#-----ドット絵処理ここまで-----
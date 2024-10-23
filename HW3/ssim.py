import sys
import cv2

def calculate_ssim(image1_path, image2_path):
    # 讀取圖像
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # 将图像转换为灰度图像
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算SSIM
    ssim_score = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0][0]
    return ssim_score

if __name__=="__main__":
    #print(len(sys.argv))
    if len(sys.argv)<3:
          print(0)
          exit(0)
    fna, fnb = sys.argv[1], sys.argv[2]
    res = calculate_ssim(fna, fnb)
    print(res)

if False:
    # 使用範例
    image1_path = "01output1.jpg"
    image2_path = "01output2.jpg"
    #image2_path = "out01_img_blue.jpg"
    ssim_value = calculate_ssim(image1_path, image2_path)
    #print(f"SSIM 值為: {ssim_value:.2f} ")
    print("%.2f"%(ssim_value))
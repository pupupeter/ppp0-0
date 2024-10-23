import sys
import cv2
import numpy as np

def calculate_psnr(image1_path, image2_path):
    # 讀取圖像
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # 確保兩張圖像大小相同
    if img1.shape != img2.shape:
        #raise ValueError("圖像大小不一致")
        return 0

    # 計算 MSE（均方誤差）
    mse = np.mean((img1 - img2) ** 2)
    #print('mse:',mse)
    if mse==0:
        return 99

    # 計算 PSNR
    max_pixel_value = 255  # 圖像像素值範圍（0-255）
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))

    return psnr

if __name__=="__main__":
    #print(len(sys.argv))
    if len(sys.argv)<3:
          print(0)
          exit(0)
    fna, fnb = sys.argv[1], sys.argv[2]
    res = calculate_psnr(fna, fnb)
    print(res)
     
if False:
    # 使用範例
    image1_path = "01output1.jpg"
    image2_path = "01output2.jpg"
    #image2_path = "out01_img_blue.jpg"
    psnr_value = calculate_psnr(image1_path, image2_path)
    #print(f"PSNR 值為: {psnr_value:.2f} dB")
    #print(f"SSIM 值為: {ssim_value:.2f} ")

    print("%.2f"%(psnr_value))
import cv2
import sys
import os
import csv

args = sys.argv

img_name = args[1]

load_img = cv2.imread(img_name)
load_img_width = load_img.shape[1]
input_size = 900
input_img = cv2.resize(load_img, dsize=None, fx=(input_size/load_img_width), fy=(input_size/load_img_width),interpolation=cv2.INTER_LANCZOS4)


csv_file = open("special_memoria_status.csv", "r", encoding="utf-8", errors="", newline="" )
f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
csv_data = [row for row in f]


status_count = [0 for i in range(20)]
image_num = len(os.listdir("special_memoria"))
target_count = 0

before_ratio_param = 1.0
output_frame = input_img.copy()
window_width = input_img.shape[1]

first_find_flag = False

for int_memoria_no in range(1,image_num+1):
    print(str(int_memoria_no)+"/"+str(image_num))

    memoria_no = str(int_memoria_no)
    input_memoria_img = cv2.imread("special_memoria/"+memoria_no+".png")
    memoria_width = input_memoria_img.shape[1]
    find_flag = False
    check_num = 21
    if first_find_flag:
        check_num = 9
    for ratio_param in range(check_num):
        #リサイズ
        dif =24.6

        ratio = (window_width / dif) / memoria_width
        ratio_change_param = 0
        if ratio_param % 2 == 0:
            ratio_change_param -= int(ratio_param/2)
        else:
            ratio_change_param += int(ratio_param/2)

        ratio = (ratio * before_ratio_param) * (20+ratio_change_param)/20
        #method = cv2.TM_CCOEFF
        method = cv2.INTER_LANCZOS4
        #method = cv2.TM_CCOEFF_NORMED
        #method = cv2.TM_CCORR
        #method = cv2.TM_CCORR_NORMED
        #method = cv2.TM_SQDIFF
        #method = cv2.TM_SQDIFF_NORMED

        resize_memoria_img = cv2.resize(input_memoria_img, dsize=None, fx=ratio, fy=ratio,interpolation=method)


        res = cv2.matchTemplate(input_img, resize_memoria_img, cv2.TM_CCOEFF_NORMED)
        width = resize_memoria_img.shape[1]
        height = resize_memoria_img.shape[0]
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        #if maxVal < 0.30:
        #    break
        #loc = np.where(res >= 0.70) # 閾値で絞る
        if maxVal > 0.70:
            pt = (maxLoc[0], maxLoc[1])
            cv2.rectangle(output_frame, pt, (pt[0]+width,pt[1]+height), (255,0,0), 2)

            for data in csv_data[1:]:
                if data[0] == memoria_no:
                    for i in range(len(status_count)):
                        status_count[i] += float(data[2+i])
                    print(data[1])
                    target_count += 1
                    find_flag = True
                    first_find_flag = True
                    before_ratio_param *= (50+ratio_change_param)/50
                    break
        if find_flag:
            break

cv2.imwrite(img_name[:-4]+"_output.png", output_frame)
print("\n------------集計枚数："+str(target_count)+"枚 --------------")
for i in range(len(status_count)):
    if i == 0:
        print("[レギオンマッチスキル]")
    elif i == 8:
        print("\n[レギオンマッチ補助スキル]")
        
    print(csv_data[0][2+i] +":" + str(round(status_count[i],2)))

with open('output/status_count.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_data[0][2:])
    writer.writerow(status_count)
    
print("------------------finish------------------")
#%%
import cv2
import requests

#ローカル画像を分析してFaceAPIで解析する
#https://docs.microsoft.com/ja-jp/azure/cognitive-services/computer-vision/quickstarts/python-disk
#バイナリファイルを送ればよいみたい

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '8962a5a2af4343e4a0ce106e6e48fba0',
}

write_file_name = './tmp.jpg'
api_url = 'https://japanwest.api.cognitive.microsoft.com/face/v1.0/detect'

# VideoCaptureのインスタンスを作成する。
# 引数でカメラを選べれる。
cap = cv2.VideoCapture(0)

params = {
    # Request parameters
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
}


try:
    while True:
        ret, frame = cap.read()
        cv2.imwrite(write_file_name, frame)
        with open(write_file_name, 'rb') as f:
            img = f.read()
        response = requests.post(api_url,params=params,headers=headers,data=img)
        
        cv2.imshow('Raw Frame', frame)

        data = response.json()

        for id in range(len(data)):
            rect = data[id]['faceRectangle']
            emotion = data[id]['faceAttributes']['emotion']
            
            top = int(rect['top'])
            left = int(rect['left'])
            btm = top + int(rect['height'])
            right = left + int(rect['width'])
            #draw.rectangle((left, top, right, btm), outline=(255, 255, 255))
            cv2.rectangle(frame, (left,top),(right,btm),(255,255,255),3)
            #cv2.putText(frame,emotion,(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
            emotion_result = ''
            dy = top + 0
            for e in emotion:
                emotion_result = e + ':' + str(emotion[e])
                dy = dy + 15
                cv2.putText(frame,emotion_result,(right + 10,dy), 0, 0.5,(255,255,255),1,cv2.LINE_AA)

        cv2.imshow('Raw Frame', frame)
        print("")

        k = cv2.waitKey(1)
        if k == 27:
            print()
            break
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

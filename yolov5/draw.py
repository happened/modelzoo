import json

import cv2

tmpimg = cv2.imread("./airplane.jpeg")
resp = '{\"box\":{\"x1\":0.0,\"x2\":50.256717681884766,\"y1\":83.32058715820313,\"y2\":121.6050796508789},\"class\":\"airplane\",\"label\":4,\"score\":0.588212788105011}'
res=json.loads(resp)
box_label_text = res["class"]
box_score = res["score"]
box_x1 = res["box"]["x1"]
box_x2 = res["box"]["x2"]
box_y1 = res["box"]["y1"]
box_y2 = res["box"]["y2"]

temp={'label': 'airplane', 'score': 0.90849966, 'box': [128.60185503959656, 90.94960391521454, 634.7544014453888, 257.90028870105743]}
box_x1=temp["box"][0]
box_y1=temp["box"][1]
box_x2=temp["box"][2]
box_y2=temp["box"][3]

print(box_x1,box_x2,box_y1,box_y2)
cv2.rectangle(tmpimg, (int(box_x1), int(box_y1)), (int(box_x2), int(box_y2)), (255, 255, 255), thickness=2)
cv2.putText(tmpimg, box_label_text + ": " + str(box_score),
            (int((box_x1 + box_x2) / 2), int((box_y1 + box_y2) / 2)), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            (0, 255, 0), thickness=2)
#cv2.imwrite(r"./test/dog_rlt.jpg", tmpimg)
cv2.imshow("img",tmpimg)
cv2.waitKey(0)

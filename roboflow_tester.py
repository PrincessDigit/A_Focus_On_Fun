# import the inference-sdk
from inference_sdk import InferenceHTTPClient
import cv2, os
from text_extractor import extractor
from nlp import languager
import copy
# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=""
)

# infer on a local image
year = 1813
i = os.listdir(f"{str(year)}/")[0]
base_path = "processed/"
if os.path.exists(base_path)== False:
    os.mkdir(base_path)
for i in os.listdir(f"{str(year)}/"):
    path = os.path.join(base_path, i)
    if os.path.exists(path) == False:
        os.mkdir(path)
    result = CLIENT.infer(os.path.join(f"{str(year)}/", i), model_id="newspaper-article-classification/2")
    img = cv2.imread(os.path.join(f"{str(year)}/", i))
    prediction = result['predictions']
    final = copy.copy(img)
    for v, p in enumerate(prediction):
        ## The API takes from the CENTER of the image!
        x = round(p['x'])
        y = round(p['y'])
        w = round(abs(p['width']*1.05))
        h = round(abs(p['height']*1.05))
        x -= round(w/2)
        if x < 0:
            x = 0
        y -= round(h/2)
        if y < 0:
            y = 0
        c = p['class']
        t = extractor()
        l = languager()
        if v == 0:
            continue
        # d = img[x:x+w, y:y+h]
        d = img[y:y+h, x:x+w]
        if c == 'articles' or c == 'articles -con-t-' or c == 'ads':
            rr = t.extract_text(d)
            scores = "ERROR"
            if rr is not None:
                scores, content = l.process_text(rr)
            with open(f"{os.path.join(path,str(v))}.txt", 'w') as file:
                file.write(f"Scores: {scores}\nText:{rr}\n\n{content}")
        if c == 'broken data':
            final = cv2.rectangle(final, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=8, lineType=cv2.LINE_AA)
        elif c == 'articles':
            final = cv2.putText(final, str(v), (x+30, y-30), cv2.FONT_HERSHEY_COMPLEX, fontScale=11, color=(255, 0, 0), thickness=5, lineType=cv2.LINE_AA)
            final = cv2.rectangle(final, (x, y), (x+w, y+h), (255, 0, 0), thickness=8, lineType=cv2.LINE_AA)
        elif c == 'articles -con-t-':
            final = cv2.putText(final, str(v), (x+30, y-30), cv2.FONT_HERSHEY_COMPLEX, fontScale=11, color=(0, 220, 250), thickness=5, lineType=cv2.LINE_AA)
            final = cv2.rectangle(final, (x, y), (x+w, y+h), (0, 220, 250), thickness=8, lineType=cv2.LINE_AA)
        elif c == 'date':
            final = cv2.rectangle(final, (x, y), (x+w, y+h), (0, 255, 0), thickness=8, lineType=cv2.LINE_AA)
        elif c == 'ads':
            final = cv2.putText(final, str(v), (x+30, y-30), cv2.FONT_HERSHEY_COMPLEX, fontScale=11, color=(200, 255, 0), thickness=5, lineType=cv2.LINE_AA)
            final = cv2.rectangle(final, (x, y), (x+w, y+h), (200, 255, 0), thickness=8, lineType=cv2.LINE_AA)
        elif c == 'Headline':
            final = cv2.rectangle(final, (x, y), (x+w, y+h), (125, 100, 200), thickness=8, lineType=cv2.LINE_AA)
        cv2.imwrite(f"{os.path.join(path, str(v))}.jpg", d)
    final_path = os.path.join(path,"predictions.jpg")
    print(final_path)
    cv2.imwrite(final_path, final)
    cv2.imshow("Final", final)
    cv2.waitKey()
    
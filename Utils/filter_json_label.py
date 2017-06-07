# coding=utf-8
import os,sys
import glob
import json
import csv

reload(sys) 
sys.setdefaultencoding("utf8")
print sys.getdefaultencoding()

label_dir = "/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/JPEGImages/label/*.json"
image_dir = "/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/JPEGImages/TestImages/"

output_file = "/Users/lairf/Documents/LinkfaceTrainingData/VechileLicense2017/JPEGImages/labels.csv"

with open(output_file, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for label_file in glob.glob(label_dir):
        with open(label_file) as file:
            text = file.read().decode("utf-8").strip()
            data = json.loads(text)
            imageFileName = data['image']['rawFilename']
            image_path = image_dir + imageFileName
            if os.path.exists(image_path):
                lines = data['objects']['ocr']
                outboxes = []
                outlabels = []
                outValues = []
                label = 0

                if lines and len(lines) == 10:
                    for line in lines:
                        left = (int(line['position']['left']) - 310)/620.0
                        top = (int(line['position']['top']) - 210)/420.0
                        right = (int(line['position']['right']) - 310)/620.0
                        bottom = (int(line['position']['bottom']) - 210)/420.0
                        outboxes.append([left, top, right - left, bottom - top])
                        outlabels.append(label)
                        # print(line)
                        if line.has_key('attributes') and line['attributes']['content']['value']:
                            outValues.append(line['attributes']['content']['value'])
                        label += 1
                    
                    # check card version
                    if outboxes[4][2] > outboxes[5][2]: # old version
                        outlabels[4] = 5
                        outlabels[5] = 4
                        outlabels[6] = 7
                        outlabels[7]= 6
                
    

                if len(outValues) == 10:
                    out = [outValues[i] for i in outlabels]
                    out.append(imageFileName)
                    spamwriter.writerow(out)
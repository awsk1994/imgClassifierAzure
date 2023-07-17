import os
import glob
import time
from classifier import classifyImg
import json

logDir = "log_1" # TODO: use timestamp
imgDir = "img"
outJsonFileName = "out.json" # use timestamp
count_quota_per_minute = 20

def jsonDump(filename, j):
    with open(filename, "w") as outfile:
        json.dump(j, outfile)

def get_imgs(directory):
    # use glob to find all JPG files in the directory
    jpg_files = glob.glob(os.path.join(directory, "*.jpg"))
    # print the list of JPG files
    return jpg_files

def main():
    if not os.path.exists(logDir):
        os.makedirs(logDir)

    imgs = get_imgs(imgDir)

    rets = []
    for img in imgs:
        print("Classifying {}".format(img))
        ret = classifyImg(img, logDir)
        rets.append(ret.to_json())
        print("Finished classifying img({})".format(img))
        print("Sleeping 3 seconds...")
        time.sleep(3)   # 20 calls per minute, meaning every call interval is 60/20 = 3

    jsonDump(outJsonFileName, rets)

main()
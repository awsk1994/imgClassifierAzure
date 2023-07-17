import os
import glob

from classifier import classifyImg
import json

logDir = "log_1" # TODO: use timestamp
logPath = "./out.log" # use timestamp
imgDir = "img"
outJsonFileName = "out.json" # use timestamp

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
        ret = classifyImg(img, logDir)
        rets.append(ret.to_json())
        print("Finished processing img({})".format(img))
    jsonDump(outJsonFileName, rets)

main()
import azure.ai.vision as sdk
import os
from classifierResult import ClassifierResult, STATUS_FAILED, STATUS_SUCCESS

def getImgName(imgPath):
    imgName = imgPath.split("\\")[-1]
    filename_without_extension = imgName.rstrip(".jpg")
    return filename_without_extension

def getLogFile(imgPath, logDir):
    imgName = getImgName(imgPath)
    logPath = "{}\\{}.log".format(logDir, imgName)
    print("Writing to {}".format(logPath))
    log_file = open(logPath, "a")
    # log_file.write("OK")
    log(log_file, "")
    return log_file

def log(logFile, content):
    logFile.write("{}\n".format(content))

def classifyImg(imgPath, logDir):
    logFile = getLogFile(imgPath, logDir)
    ret = ClassifierResult(imgPath)

    # Authenticate against the service
    service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
                                            os.environ["VISION_KEY"])

    # Select the image to analyze
    vision_source = sdk.VisionSource(
        filename=imgPath
        # url="https://learn.microsoft.com/azure/cognitive-services/computer-vision/media/quickstarts/presentation.png"
    )

    # Select analysis options
    analysis_options = sdk.ImageAnalysisOptions()

    analysis_options.features = (
        sdk.ImageAnalysisFeature.CROP_SUGGESTIONS |
        sdk.ImageAnalysisFeature.CAPTION |
        sdk.ImageAnalysisFeature.DENSE_CAPTIONS |
        sdk.ImageAnalysisFeature.OBJECTS |
        sdk.ImageAnalysisFeature.PEOPLE |
        sdk.ImageAnalysisFeature.TEXT |
        sdk.ImageAnalysisFeature.TAGS
    )

    analysis_options.language = "en"
    # chinese = "zh"

    analysis_options.gender_neutral_caption = True

    # Get results from the service
    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    result = image_analyzer.analyze()

    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
        log(logFile, " Image height: {}".format(result.image_height))
        log(logFile, " Image width: {}".format(result.image_width))
        log(logFile, " Model version: {}".format(result.model_version))

        if result.caption is not None:
            log(logFile, " Caption:")
            log(logFile, "   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

        if result.dense_captions is not None:
            log(logFile, " Dense Captions:")
            for caption in result.dense_captions:
                log(logFile, "   '{}', {}, Confidence: {:.4f}".format(caption.content, caption.bounding_box, caption.confidence))
                ret.add_caption(caption.content, caption.confidence)
        
        if result.objects is not None:
            log(logFile, " Objects:")
            for object in result.objects:
                log(logFile, "   '{}', {}, Confidence: {:.4f}".format(object.name, object.bounding_box, object.confidence))

        if result.tags is not None:
            log(logFile, " Tags:")
            for tag in result.tags:
                log(logFile, "   '{}', Confidence {:.4f}".format(tag.name, tag.confidence))
                ret.add_tag(tag.name, tag.confidence)

        if result.people is not None:
            log(logFile, " People:")
            for person in result.people:
                log(logFile, "   {}, Confidence {:.4f}".format(person.bounding_box, person.confidence))

        if result.crop_suggestions is not None:
            log(logFile, " Crop Suggestions:")
            for crop_suggestion in result.crop_suggestions:
                log(logFile, "   Aspect ratio {}: Crop suggestion {}"
                    .format(crop_suggestion.aspect_ratio, crop_suggestion.bounding_box))

        if result.text is not None:
            log(logFile, " Text:")
            for line in result.text.lines:
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                log(logFile, "   Line: '{}', Bounding polygon {}".format(line.content, points_string))
                ret.add_text(line.content)
                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                    log(logFile, "     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                        .format(word.content, points_string, word.confidence))

        result_details = sdk.ImageAnalysisResultDetails.from_result(result)
        log(logFile, " Result details:")
        log(logFile, "   Image ID: {}".format(result_details.image_id))
        log(logFile, "   Result ID: {}".format(result_details.result_id))
        log(logFile, "   Connection URL: {}".format(result_details.connection_url))
        log(logFile, "   JSON result: {}".format(result_details.json_result))
        ret.status = STATUS_SUCCESS
    else:
        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        log(logFile, " Analysis failed.")
        log(logFile, "   Error reason: {}".format(error_details.reason))
        log(logFile, "   Error code: {}".format(error_details.error_code))
        log(logFile, "   Error message: {}".format(error_details.message))
        ret.status = STATUS_FAILED

    return ret

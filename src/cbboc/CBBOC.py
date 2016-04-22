import time
import json
from datetime import datetime
from os import path
from .ProblemClass import ProblemClass
from . import ObjectiveFn
from . import TrainingCategory

BASE_TIME_IN_MILLIS = 60 * 1000

def trainClient(client, fns):
    startTime = time.time() * 1000  # Coverts to milliseconds
    maxTime = BASE_TIME_IN_MILLIS * len(fns) * client.getTrainingCategory()
    ObjectiveFn.trainingEndTime = startTime + maxTime
    
    try:
        client.train(fns, maxTime)
    except ObjectiveFn.EvaluationsExceededException:
        # TODO Consider logger
        pass
    except ObjectiveFn.TimeExceededException:
        # TODO Consider logger
        pass
    endTime = time.time() * 1000
    return endTime - startTime

def testClient(client, fns):
    startTime = time.time() * 1000  # Converts to milliseconds
    
    for fn in fns:
        try:
            ObjectiveFn.testingEndTime = time.time() * 1000 + BASE_TIME_IN_MILLIS
            client.test(fn, BASE_TIME_IN_MILLIS)
        except ObjectiveFn.EvaluationsExceededException:
            # TODO Consider logger
            pass
        except ObjectiveFn.TimeExceededException:
            # TODO Consider logger
            pass

    endTime = time.time() * 1000
    return endTime - startTime

def run(client):
    configFile = path.join(path.pardir, "resources", "classFolder.txt")
    with open(configFile, "r") as f:
        classFolder = f.read().strip()
    base_path = path.join(path.pardir, "resources", classFolder)
    problemClass = ProblemClass(base_path, client.getTrainingCategory())
    if client.getTrainingCategory() == TrainingCategory.NONE:
        actualTrainingTime = 0
        actualTestTime = testClient(client, problemClass.getTestingInstances())
        # TODO Logger
    elif client.getTrainingCategory() in [TrainingCategory.SHORT, TrainingCategory.LONG]:
        actualTrainingTime = trainClient(client, problemClass.getTrainingInstances())
        # TODO Logger
        actualTestTime = testClient(client, problemClass.getTestingInstances())
        # TODO logger
    else:
        raise ValueError("Unknown Training Category")
    dateFormatted = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = path.join(base_path, "results",
                         "CBBOCresults-" + client.__class__.__name__ + '-' + classFolder + '-' + dateFormatted + ".json")
    results = {"competitorName": client.__class__.__name__,
               "competitorLanguage": "Python",
               "problemClassName": classFolder,
               "trainingCategory": client.getTrainingCategory(),
               "datetime": dateFormatted,
               "trainingResults": [],
               "testingResults": [],
               "trainingWallClockUsage": actualTrainingTime,
               "testingWallClockUsage": actualTestTime}
    # Extract information from both the training and the testing instances
    for key, instances in [("trainingResults", problemClass.getTrainingInstances()),
                           ("testingResults", problemClass.getTestingInstances())]:
        for instance in instances:
            result = {}
            bestInfo = instance.getRemainingEvaluationsAtBestValue()
            result["remainingEvaluationsWhenBestReached"] = bestInfo[0]
            result["bestValue"] = bestInfo[1]
            result["remainingEvaluations"] = instance.getRemainingEvaluations()
            results[key].append(result)
    as_string = json.dumps(results, f, indent=4, sort_keys=True)
    with open(filename, "w") as f:
        f.write(as_string)
    print(as_string)

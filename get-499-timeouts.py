import pandas as pd
import re

# Constants
HOUR_COLUMN = 0
HTTP_METHOD_COLUMN = 8
HTTP_PATH_COLUNM = 12

def __MAIN__():
    paths = [
        "./../../../Downloads/f6f10e2f-473b-4f10-8f1f-327689a8595d.csv",
        "./../../../Downloads/514ca1bd-ad13-4d78-bbfb-b71b5ddc6d5b.csv",
        "./../../../Downloads/116c9cb1-9f4b-41f0-853a-9053cc907384.csv",
    ]

    combinedData = {}
    for path in paths:
        
        data = pd.read_csv(
            filepath_or_buffer = path, 
            usecols = [HOUR_COLUMN, HTTP_METHOD_COLUMN, HTTP_PATH_COLUNM]
        ).to_numpy()

        combinedData.update({path: data})

    sortedResponse = getSortedDictionaryResponse(combinedData)

    totalCases = 0
    for row in sortedResponse:
        totalCases += sortedResponse[row]

    for row in sortedResponse:
        print(str(sortedResponse[row]) + "/" + str(totalCases) + " times -> " + row)

    
def getSortedDictionaryResponse(combinedData):
    response = {}

    for key in combinedData:
        for row in combinedData[key]:
            url = str(row[2])

            cleanedUrl = cleanExternalSites(
                cleanSession(
                    cleanMeli(
                        cleanQueryParams(
                            cleanEmptyPages(url)
                        )
                    )
                )
            )

            rowToCount = row[1] + " - " + cleanedUrl

            previouslyData = response.get(rowToCount)
            if previouslyData:
                response.update({rowToCount: previouslyData + 1})
            else:
                response.update({rowToCount: 1})

    return dict(sorted(response.items(), key = lambda x:x[1], reverse=True))


def cleanMeli(input):
    return re.sub(r'https:\/\/www\.mercadoli(v|b)re(\.com)\...', "", input)

def cleanSession(input):
    return re.sub(r'([0-9a-z]){32}\/', "SESSION/", input)

def cleanQueryParams(input):
    return input.split("?")[0]

def cleanEmptyPages(input):
    if input == "nan":
        return "EMPTY-PAGE"
    else:
        return input

def cleanExternalSites(input):
    return re.sub(r'http(s):\/\/.*', "EXTERNAL-PAGE", input)

__MAIN__()
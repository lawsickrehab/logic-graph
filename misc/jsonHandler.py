from os import listdir, mkdir, path
import json
class jsonHandler:
    data = {}
    filenamePrefix = ""
    def load(filePath):
        srcFilename = filePath.split("/")[-1]
        jsonHandler.filenamePrefix = srcFilename[:srcFilename.rfind(".")]
        print(f"Set filename Prefix to {jsonHandler.filenamePrefix}")
        try:
            with open(filePath, encoding="UTF-8") as ifs:
                jsonHandler.data = json.loads(ifs.read())
        except FileNotFoundError:
            print("Error: File Not Found")
            return
        except Exception:
            print("Error")
            return
        print("successful")
    def getData():
        print(f"Data: \n{json.dumps(jsonHandler.data, indent=4, ensure_ascii=False)}")
    def getDataLen():
        print(f"Length: {len(jsonHandler.data)}")
    def separate(unitSize, outputDir):
        dataLst = []
        for item in jsonHandler.data.items():
            dataLst.append(item)
        outputDataLst = []
        for i in range(0, len(dataLst), unitSize):
            outputDataLstItem = {}
            for j in range(i, i + unitSize):
                if(j >= len(dataLst)):
                    break
                outputDataLstItem[dataLst[j][0]] = dataLst[j][1]
            outputDataLst.append(outputDataLstItem)
        if path.isdir(outputDir) == False:
            mkdir(outputDir)
        for i in range(len(outputDataLst)):
            outputDataLstItem = outputDataLst[i]
            with open(f"{outputDir}/{jsonHandler.filenamePrefix}-{i + 1}.json", "w+", encoding="UTF-8") as ofs:
                ofs.write(json.dumps(outputDataLstItem, ensure_ascii=False))
                print(f"Separate: Generating file {outputDir}/{i}.json ({i + 1}/{len(outputDataLst)})...")
        print(f"Successfully written to {outputDir}")
    def readCmd():
        while True:
            cmdLst = input("Enter the command: ").split()
            if (len(cmdLst) == 0):
                print("Please Enter a command. Try again.")
            elif (len(cmdLst) == 1):
                if (cmdLst[0] == "exit"):
                    return cmdLst
                elif (cmdLst[0] == "getData"):
                    return cmdLst
                elif (cmdLst[0] == "getDataLen"):
                    return cmdLst
                else:
                    print("Please Enter a command. Try again.")
            elif (len(cmdLst) == 2):
                if (cmdLst[0] == "load"):
                    return cmdLst
                else:
                    print("Please Enter a command. Try again.")
            elif (len(cmdLst) == 3):
                if (cmdLst[0] == "separate"):
                    if(cmdLst[1].isdigit() == False):
                        print("Please enter a valid unit size")
                    elif(int(cmdLst[1]) < 0):
                        print("Please enter a valid unit size")
                    else:
                        return cmdLst
                else:
                    print("Please Enter a command. Try again.")
            else:
                print("Please Enter a command. Try again.")
    def driver():
        while True:
            cmdLst = jsonHandler.readCmd()
            if(cmdLst[0] == "exit"):
                print("Program ended")
                return
            elif (cmdLst[0] == "load"):
                jsonHandler.load(cmdLst[1])
            elif (cmdLst[0] == "getData"):
                jsonHandler.getData()
            elif (cmdLst[0] == "getDataLen"):
                jsonHandler.getDataLen()
            elif (cmdLst[0] == "separate"):
                jsonHandler.separate(int(cmdLst[1]), cmdLst[2])
jsonHandler.driver()

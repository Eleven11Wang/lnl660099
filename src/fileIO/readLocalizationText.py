import time
class dataPoints(object):
    def __init__(self, name):
        self.planeDict = {}
        self.width = 0
        self.height = 0
        self.planes = 0
        self.point = 0
        self.name = name
        self.import_file()


    def import_file(self, stopPlane=30000):

        start = time.time()
        fp = open(self.name, "r")
        _ = fp.readline()
        line = fp.readline()
        width, height, planes, point = map(int, line.rstrip().split("\t"))
        self.width = width
        self.height = height
        self.planes = planes
        self.point = point
        _ = fp.readline()
        line = fp.readline()
        # rawArray=utils.MakeThreeDArray(width,height,planes)

        cnt = 0
        print("planes :{}, point: {}".format(planes,point))
        while line:
            cnt += 1
            dataLine = line.rstrip().split("\t")
            intensity = float(dataLine[4])
            widx, hity = float(dataLine[10]) * 93, float(dataLine[11]) * 93  # real world localization
            plane = int(dataLine[0])
            pos = (widx, hity)
            # rawArray[plane-1,hity,widx]=1
            if plane > stopPlane:
                break
            if plane not in self.planeDict:
                self.planeDict[plane] = []
            self.planeDict[plane].append([pos, intensity])
            line = fp.readline()
        end = time.time()
        print("import file time: ", str(end - start))
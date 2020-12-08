import numpy as np
import matplotlib.pyplot as plt


class Data():
    def __init__(self, fileName):
        self.x = []
        self.y = []
        self.error = []
        self.ErrorCheck = True
        self.fileName = fileName[:len(fileName)-1]

        if self.fileName[len(fileName) - 4:] == "txt":
            self.readData()
        elif self.fileName[len(fileName) - 4:] == "CSV":
            self.loadCSVFile()


        self.x_div = np.abs(self.x[0] - self.x[1])
        print("The x division is: " + str(self.x_div))
        self.signals = []

    def linearPlotData(self, title, xAxisTitle, yAxisTitle, x, y, error_y, label):
        figure = plt.figure()
        axes_1 = figure.add_subplot(121)
        axes_1.plot(x, y, "b+", label=label)
        axes_1.errorbar(x, y, error_y, fmt="b+")
        plt.xlabel(xAxisTitle)  #
        plt.ylabel(yAxisTitle)  # edit from axes
        plt.title(title)
        y_weights = (1 / error_y) * np.ones(np.size(y))
        y_errors = error_y * np.ones(np.size(y))
        fit_parameters, fit_errors = np.polyfit(x, y, 1, cov=True, w=y_weights)

        y_fitted = np.polyval(fit_parameters, x)
        axes_1.plot(x, y_fitted)
        axes_2 = figure.add_subplot(122)
        axes_2.set_xlabel(xAxisTitle)
        axes_2.set_ylabel(yAxisTitle)
        axes_2.errorbar(x, y - y_fitted, yerr=y_errors, fmt='b+')

        plt.savefig(title + ".png")

    def plotCustom(self):
        # get data
        plt.plot(self.x, self.y, "b+")

    def plotCustom2(self, x, y, axesTitle, label):
        figure = plt.figure()
        axes_1 = figure.add_subplot(111)
        axes_1.set_title(axesTitle)
        axes_1.plot(x, y, "b+", label=label)

    def readData(self):
        array = [[], [], []]
        temp2 = 0
        file = open(self.fileName)
        content = file.readlines()
        for counter in range(0, len(content)):
            temp = content[counter]
            if temp == "end\n":
                temp2 += 1
            else:
                array[temp2].append(float(temp))
            # end if
        # end for
        self.x = array[0]
        self.y = array[1]
        self.error = array[2]
        if len(self.error) == 0:
            self.ErrorCheck = False

        file.close()

    # organize data
    # show the plot
    def saveSignals(self):
        print(self.signals)
        print(np.array(self.signals))
        for i in range(0, 3, 1):
            file = open("x Values " + self.fileName + " Signal " + str(i) + ".txt", "a")
            for values in self.signals[i]:
                for item in values:
                    file.write(str(item))
                    file.write("\n")
                file.close()  # closes the x values file and opens a new one
                file = open("y Values " + self.fileName + " Signal " + str(i) + ".txt", "a")

            file.close()  # closes the second file

    def cutData(self, divisor):
        # use the divisor to split the data
        # check the divider is valid
        check = False
        i = 0
        if self.isDividerValid(divisor[i][0]) and self.isDividerValid(divisor[i][1]):
            i += 1
            if self.isDividerValid(divisor[i][0]) and self.isDividerValid(divisor[i][1]):
                i += 1
                if self.isDividerValid(divisor[i][0]) and self.isDividerValid(divisor[i][1]):
                    check = True
        if check == False:
            print("the divider is not correct")
            return 0
        divider = [[0, 0], [0, 0], [0, 0]]
        for counter in range(0, 3, 1):
            # gets the divisor in the terms of indices
            divider[counter][0] = self.x.index(divisor[counter][0])
            divider[counter][1] = self.x.index(divisor[counter][1])

        # use the divisor to split the data
        signals = [[], [], []]
        for counter in range(0, 3, 1):
            signals[counter] = [self.x[divider[counter][0]:divider[counter][1]],
                                self.y[divider[counter][0]:divider[counter][1]]]

        print(signals)
        # this stores the 3 points of interest using the data
        # signal[1] stores the first signal as [x values, y values]
        # plot the individual plots
        for i in range(0, 3, 1):
            self.plotCustom2(signals[i][0], signals[i][1], "Signal " + str(i), "Signal " + str(i))
        # print individual data to txt files by parsing

        self.signals = signals
        self.saveSignals()

    def isDividerValid(self, value):
        if value in self.x:
            print("Value is present")
            return True
        else:
            print("Value not found")
            # gives a better divisor
            temp = value // self.x_div
            temp = temp * self.x_div
            print("the number: " + str(value) + " Should be " + str(temp))
            return False

    def loadCSVFile(self):
        x_array = []
        y_array = []
        file = open(self.fileName)
        content = file.readlines()
        for counter in range(0, len(content), 1):
            entry = content[counter]
            temp = entry.split(",")

            # heading entry
            x = float(temp[3])
            y = float(temp[4])
            self.x.append(x)
            self.y.append(y)

def getfile():
    file = open("file_names.txt","r")
    content = file.readlines()
    return content



def main():
    path = "D:\\Documents\\Coding Reps\\Approximations\\SpinEcho"  # Put the file path here

    file = getfile()
    print(file)
    #choice = int(input("Enter number: "))
    choice = 201


    d = Data(path + "\\Data\\" + file[choice])
    # C:\Users\opopn\Desktop\Labs code\Data
    d.plotCustom()
    print(file[choice])



main()
plt.show()

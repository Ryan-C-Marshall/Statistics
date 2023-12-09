import math
import pygame


class VisualStatObject:
    """Basic inheritance class for all objects in this stat library."""

    def __init__(self):
        self.shape = pygame.Rect((50, 50), (50, 50))

    def draw(self, window):
        pass


class Graph(VisualStatObject):
    """Basic visual object for graphs in this stat library."""

    def __init__(self,
                 maxY, categoricalXAxis: bool = False, maxX: float = 0, minY: float = 0, minX: float = 0,
                 xCategoricalLabels: list[str] = None,
                 x=0, y=0, width: int | None = None, height: int | None = None, graphSize=0.75, borderWidth=0,
                 bgColour: tuple = (255, 255, 255), primaryColour: tuple = None, borderColour: tuple = None,
                 title: str = "", showXAxisLabel: bool = True, showYAxisLabel: bool = True,
                 xAxisLabel: str = "", yAxisLabel: str = "",
                 fontName: str = "freesanbold", axisMarkerDensity: float = 0.008
                 ):
        """
        :param maxY: The maximum y value to display on the graph. This determines the y axis scale.
        :param categoricalXAxis: A boolean representing whether the x axis is numerical or categorical.
        :param maxX: Necessary if the graph has a numerical x axis. This is the maximum x value, determines the x scale.
        :param minY: The minimum y value to display on the graph (useful if data is clustered around a nonzero value)
        :param minX: The minimum x value to display on the graph. Helps determine the x scale; same with min y.
        :param xCategoricalLabels: If the graph has a categorical x axis (e.g. bar chart), these are the x labels.
        :param x: The x position on the pygame window to display the graph object.
        :param y: The y position on the pygame window to display the graph object.
        :param width: The width of the graph object on the pygame window.
        :param height: The height of the graph object on the pygame window.
        :param graphSize: The proportional size of the working section of the graph; the rest is for labels, titles, etc
        :param borderWidth: The width of the object's border
        :param bgColour: The object's background colour. The complement of this is the default of 'primaryColour'.
        :param primaryColour: The primary colour of the graph: used for axes, labels, title, etc.
        :param borderColour: The border's colour. Defaults to primaryColour.
        :param title: The graph's title.
        :param showXAxisLabel: A boolean representing whether to show the x axis label.
        :param showYAxisLabel: A boolean representing whether to show the y axis label.
        :param xAxisLabel: The label for the x axis.
        :param yAxisLabel: The label for the y axis.
        :param fontName: The font to use for the graph
        :param axisMarkerDensity: The approximate number of axis marks per pixel. This value is used to calculate the
        actual distance between axis marks.
        """
        super().__init__()
        self.maxY = maxY
        self.categoricalXAxis = categoricalXAxis

        self.maxX = maxX
        if not self.categoricalXAxis and maxX == 0:
            raise ValueError("If the graph has a numerical X axis, a maximum x value must be provided.")

        self.minY = minY
        self.minX = minX
        self.xCategoricalLabels = xCategoricalLabels
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.graphSize = graphSize
        self.borderWidth = borderWidth
        self.showXAxisLabel = showXAxisLabel
        self.showYAxisLabel = showYAxisLabel
        self.bgColour = bgColour
        self.primaryColour = primaryColour if primaryColour is not None else complementary(bgColour)
        self.borderColour = borderColour if borderColour is not None else complementary(bgColour)
        self.title = title
        self.xAxisLabel = xAxisLabel
        self.yAxisLabel = yAxisLabel
        self.fontName = fontName
        self.axisMarkerDensity = axisMarkerDensity

        self.effectiveX: int | None = None
        self.effectiveY: int | None = None
        self.effectiveWidth: int | None = None
        self.effectiveHeight: int | None = None
        self.graphX: int | None = None
        self.graphY: int | None = None
        self.graphWidth: int | None = None
        self.graphHeight: int | None = None
        self.originX: int | None = None
        self.originY: int | None = None
        self.xScale: float | None = None
        self.yScale: float | None = None

        self.dimensionsSet = False

        if self.width is not None and self.height is not None:
            self.set_dimensions(pygame.Surface((0, 0)))

    def drawBorderAndBackground(self, window):
        """
        Draws the background and border for the graph object
        :param window: The pygame window to draw on
        :param backgroundX: The x value where the background starts (self.x + self.borderWidth)
        :param backgroundY: The y value where the background starts (self.y + self.borderWidth)
        :param backgroundWidth: The width of the background (self.width - 2 * self.borderWidth)
        :param backgroundHeight: The height of the background (self.height - 2 * self.borderWidth)
        :return: None
        """
        # border
        pygame.draw.rect(window, self.borderColour, (self.x, self.y, self.width, self.height))
        # background rect
        pygame.draw.rect(window, self.bgColour, (self.effectiveX, self.effectiveY,
                                                 self.effectiveWidth, self.effectiveHeight))

    def set_dimensions(self, window: pygame.Surface):
        self.width = self.width if self.width is not None else window.get_width()
        self.height = self.height if self.height is not None else window.get_height()

        self.effectiveX = self.x + self.borderWidth
        self.effectiveY = self.y + self.borderWidth

        self.effectiveWidth = self.width - 2 * self.borderWidth
        self.effectiveHeight = self.height - 2 * self.borderWidth

        self.graphWidth = self.graphSize * self.effectiveWidth
        self.graphHeight = self.graphSize * self.effectiveHeight

        self.graphX = self.effectiveX + (self.effectiveWidth - self.graphWidth) / 2
        self.graphY = self.effectiveY + (self.effectiveHeight - self.graphHeight) / 2

        if not self.categoricalXAxis:
            self.xScale = self.graphWidth / (self.maxX - self.minX)
            self.originX = self.graphX - self.xScale * self.minX

        self.yScale = self.graphHeight / (self.maxY - self.minY)
        self.originY = self.graphY + self.graphHeight + self.yScale * self.minY

        self.dimensionsSet = True

    def get_dimensions(self):
        if self.categoricalXAxis:
            return (
                self.width, self.height, self.effectiveX, self.effectiveY, self.effectiveWidth, self.effectiveHeight,
                self.graphX, self.graphY, self.graphWidth, self.graphHeight, self.yScale, self.originY)
        else:
            return (
                self.width, self.height, self.effectiveX, self.effectiveY, self.effectiveWidth, self.effectiveHeight,
                self.graphX, self.graphY, self.graphWidth, self.graphHeight,
                self.xScale, self.yScale, self.originX, self.originY)

    def get_origin(self) -> tuple[float, float]:
        if not self.dimensionsSet:
            raise EnvironmentError("Dimensions have not yet been set.")

        return self.originX, self.originY

    def getGraphDimensions(self) -> tuple[float, float]:
        if not self.dimensionsSet:
            raise EnvironmentError("Dimensions have not yet been set.")
        return self.graphWidth, self.graphHeight

    def draw(self, window: pygame.Surface):
        """
        Draws the outline of a graph, with no content. Content in graphs are drawn by child classes of this class.
        :param window: The pygame window to draw the graph outline on
        :return: None
        """
        # -- calculate dimensions and values -- #
        if not self.dimensionsSet:
            self.set_dimensions(window)

        axisLabelFont = pygame.font.SysFont(self.fontName, int(0.5 * (self.effectiveHeight - self.graphHeight) / 2))
        axisMarkerFont = pygame.font.SysFont(self.fontName, int(0.35 * (self.effectiveHeight - self.graphHeight) / 2))
        titleFont = pygame.font.SysFont(self.fontName, int(0.8 * (self.effectiveHeight - self.graphHeight) / 2))

        # draw background
        self.drawBorderAndBackground(window)

        # -- axes -- #
        # x axis
        pygame.draw.line(window, self.primaryColour, (self.graphX, self.graphY + self.graphHeight),
                         (self.graphX + self.graphWidth, self.graphY + self.graphHeight))
        # y axis
        pygame.draw.line(window, self.primaryColour, (self.graphX, self.graphY + self.graphHeight),
                         (self.graphX, self.graphY))

        # -- title --
        draw_text(window, self.title, (self.effectiveX + self.effectiveWidth / 2,
                                       self.effectiveY + (self.effectiveHeight - self.graphHeight) / 4),
                  self.primaryColour, titleFont)

        # -- labels --
        if self.showXAxisLabel:
            # x axis label
            draw_text(window, self.xAxisLabel,
                      (self.graphX + self.graphWidth / 2,
                       self.graphY + self.graphHeight + 0.35 * (self.effectiveHeight - self.graphHeight)),
                      self.primaryColour, axisLabelFont)

        if self.showYAxisLabel:
            # y axis label
            draw_text(window, self.yAxisLabel, (self.graphX - 0.35 * (self.effectiveWidth - self.graphWidth),
                                                self.graphY + self.graphHeight / 2),
                      self.primaryColour, axisLabelFont, 90)

        # -- axis marks --
        axisMarkLength = 0.005 * (self.graphHeight + self.graphWidth)

        # x marks and numbers
        if self.categoricalXAxis and self.xCategoricalLabels is not None:

            deltaLabel = self.graphWidth / len(self.xCategoricalLabels)
            for i, label in enumerate(self.xCategoricalLabels):
                draw_text(window, label,
                          (self.graphX + (i + 0.5) * deltaLabel,
                           self.graphY + self.graphHeight + (self.effectiveHeight - self.graphHeight) / 6),
                          self.primaryColour, axisMarkerFont)
        else:
            approxNumXAxisLabels: int = math.floor(self.axisMarkerDensity * self.graphWidth)

            # x units / label
            deltaXAxisLabel = next_lowest_decimultiple((self.maxX - self.minX) / approxNumXAxisLabels, [1, 2, 5])

            xAxisLabelSpacing = self.xScale * deltaXAxisLabel  # pixels/mark

            labelNum = 0
            while labelNum * xAxisLabelSpacing <= self.graphWidth:
                # main mark and label
                markPosition = self.graphX + labelNum * xAxisLabelSpacing
                pygame.draw.line(window, self.primaryColour,
                                 (markPosition, self.graphY + self.graphHeight - axisMarkLength),
                                 (markPosition, self.graphY + self.graphHeight + axisMarkLength))

                draw_text(window, str(sig_figs(labelNum * deltaXAxisLabel + self.minX, 2)),
                          (markPosition,
                           self.graphY + self.graphHeight + (self.effectiveHeight - self.graphHeight) / 6),
                          self.primaryColour, axisMarkerFont)

                # half mark
                if (labelNum + 0.5) * xAxisLabelSpacing <= self.graphWidth:
                    pygame.draw.line(window, self.primaryColour,
                                     (markPosition + 0.5 * xAxisLabelSpacing,
                                      self.graphY + self.graphHeight - axisMarkLength / 2),
                                     (markPosition + 0.5 * xAxisLabelSpacing,
                                      self.graphY + self.graphHeight + axisMarkLength / 2))

                # update position
                labelNum += 1

        # y marks and numbers
        approxNumYAxisLabels: int = math.floor(self.axisMarkerDensity * self.graphHeight)
        deltaYAxisLabel = next_lowest_decimultiple((self.maxY - self.minY) / approxNumYAxisLabels,
                                                   [1, 2, 5])  # y units / label
        yAxisLabelSpacing = self.yScale * deltaYAxisLabel  # pixels/mark

        labelNum = 0
        while labelNum * yAxisLabelSpacing <= self.graphHeight:
            # main mark and label
            markPosition = self.graphY + self.graphHeight - labelNum * yAxisLabelSpacing
            pygame.draw.line(window, self.primaryColour,
                             (self.graphX - axisMarkLength, markPosition),
                             (self.graphX + axisMarkLength, markPosition))

            draw_text(window, str(sig_figs(labelNum * deltaYAxisLabel + self.minY, 2)),
                      (self.graphX - (self.effectiveWidth - self.graphWidth) / 6, markPosition),
                      self.primaryColour, axisMarkerFont)

            # half mark
            if (labelNum + 0.5) * yAxisLabelSpacing <= self.graphHeight:
                pygame.draw.line(window, self.primaryColour,
                                 (self.graphX - axisMarkLength / 2, markPosition - 0.5 * yAxisLabelSpacing),
                                 (self.graphX + axisMarkLength / 2, markPosition - 0.5 * yAxisLabelSpacing))

            # shift position
            labelNum += 1


class StatVisualizer:

    def __init__(self, width: int, height: int, title: str, *initialObjects, fps=1):
        self.WIDTH = width
        self.HEIGHT = height
        self.TITLE = title
        self.objects = []

        self.FPS = fps

        for obj in initialObjects:
            self.objects.append(obj)

    def start(self):
        self.run()
        # threading.Thread(target=self.run()).start()

    def add_objects(self, *objects: VisualStatObject, objList=None):
        for obj in objects:
            self.objects.append(obj)

        if objList is not None:
            for obj in objList:
                self.objects.append(obj)

    def run(self):
        pygame.init()

        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        clock = pygame.time.Clock()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for obj in self.objects:
                obj.draw(window)

            pygame.display.update()

            clock.tick(self.FPS)

        pygame.quit()


class DiscreteData:

    def __init__(self, data: list, label: str = "", units: str = ""):
        self.data: list[float] = data
        self.label: str = label
        self.units: str = units
        self.size: int = len(data)

        self.median = median(self.data)

    def quarterOne(self):
        tempData = self.data.copy()
        tempData.sort()
        n = len(tempData)
        if ((n - 1) / 4) % 1 == 0:
            return tempData[int((n - 1) / 4 + 0.5)]  # + 0.5 for possible floating point error
        else:
            return (tempData[int((n - 1) / 4)] + tempData[int((n - 1) / 4) + 1]) / 2

    def quarterThree(self):
        tempData = self.data.copy()
        tempData.sort()
        n = len(tempData)
        if ((n - 1) / 4) % 1 == 0:
            return tempData[3 * int((n - 1) / 4 + 0.5)]  # + 0.5 for possible floating point error
        else:
            return (tempData[3 * int((n - 1) / 4)] + tempData[3 * int((n - 1) / 4) + 1]) / 2

    def max(self):
        return max(self.data)

    def min(self):
        return min(self.data)

    def getValue(self, index: int):
        """
        :param index: The index at which to get a value
        :return: The value at that index
        """
        return self.data[index]

    def getData(self) -> list[float]:
        return self.data

    def __str__(self):
        return self.label + ":\n" + str(self.data)


class MultivariableDiscreteData:

    def __init__(self, *data: DiscreteData, title=""):
        """
        :param data: The data; one list for each dimension. All lists must be the same length as the values match to
        make points. e.g. [1, 2, 2, 3], [25, 41, 49, 53]
        :param axisLabels: The labels for each axis (e.g. ["Petal length", "Petal width"] )
        :param units: The units for each dimension (e.g. [centimeters, millimeters])
        """
        # check the correct number of dimensions for the data
        if len(data) == 0:
            raise ValueError("No data was entered.")

        # check there are enough dimensions
        if len(data) < 2:
            raise ValueError("Multivariable Data must have at least two dimensions. " + str(len(data)) +
                             " is < 2. DiscreteData is a class to store single-dimensional data.")

        # check that all the data matches up to form points in n-dimensional space
        for i, discreteData in enumerate(data):
            if discreteData.size != data[0].size:
                raise ValueError("Data length mismatch. Dataset 1 has " + str(data[0].size) +
                                 " elements, but dataset " + str(i) + " has " + str(discreteData.size) + " elements.")

        self.title = title

        self.numDimensions: int = len(data)
        self.data: tuple[DiscreteData] = data
        self.numPoints: int = data[0].size

    def get_points_list(self) -> list[tuple]:
        return [tuple([self.data[i].getValue(j) for i in range(self.numDimensions)]) for j in range(self.numPoints)]

    def set_labels(self, *labels: str):
        if len(labels) != self.numDimensions:
            raise ValueError("Entered " + str(len(labels)) + " labels for " + str(self.numDimensions) +
                             " datasets. To retain the original label for a dataset, enter an empty string.")
        for i, label in enumerate(labels):
            if label != "":
                self.data[i].label = label

    def max(self, datasetNum: int) -> float:
        return self.data[datasetNum].max()

    def min(self, datasetNum: int) -> float:
        return self.data[datasetNum].min()

    def getData(self, datasetNum) -> list[float]:
        return self.data[datasetNum].getData()

    def __str__(self):
        dataString = ""
        for i, dataset in enumerate(self.data):
            dataString += "\nDataset " + str(i) + ":\n" + str(dataset)
        return "Dimensions: " + str(self.numDimensions) + dataString


class BoxplotGraph(Graph):
    def __init__(self,
                 *data: DiscreteData,
                 maxY: int | None = None, minY: int | None = None, xCategroicalLabels: list[str] = None,
                 x=0, y=0, width: int | None = None, height: int | None = None, borderWidth=0, graphSize=0.75,
                 title="", showXAxisLabel: bool = True, showYAxisLabel: bool = True,
                 xAxisLabel="", yAxisLabel="",
                 bgColour: tuple = (255, 255, 255), primaryColour: tuple = None, colours: list[tuple] = None,
                 borderColour: tuple = None,
                 fontName: str = "freesanbold", axisMarkerDensity: float = 0.008):
        """
        :param data: The (1D) datasets that will be displayed on the boxplot
        :param maxY: The maximum y value to display on the graph. This determines the y axis scale.
        :param categoricalXAxis: A boolean representing whether the x axis is numerical or categorical.
        :param minY: The minimum y value to display on the graph (useful if data is clustered around a nonzero value)
        :param xCategoricalLabels: If the graph has a categorical x axis (e.g. bar chart), these are the x labels.
        :param x: The x position on the pygame window to display the graph object.
        :param y: The y position on the pygame window to display the graph object.
        :param width: The width of the graph object on the pygame window.
        :param height: The height of the graph object on the pygame window.
        :param graphSize: The proportional size of the working section of the graph; the rest is for labels, titles, etc
        :param borderWidth: The width of the object's border
        :param bgColour: The object's background colour. The complement of this is the default of 'primaryColour'.
        :param primaryColour: The primary colour of the graph: used for axes, labels, title, etc.
        :param borderColour: The border's colour. Defaults to primaryColour.
        :param title: The graph's title.
        :param showXAxisLabel: A boolean representing whether to show the x axis label.
        :param showYAxisLabel: A boolean representing whether to show the y axis label.
        :param xAxisLabel: The label for the x axis.
        :param yAxisLabel: The label for the y axis.
        :param fontName: The font to use for the graph
        :param axisMarkerDensity: The approximate number of axis marks per pixel. This value is used to calculate the
        actual distance between axis marks.
        """

        self.data: tuple[DiscreteData] = data
        self.numDatasets = len(data)

        self.maxY = maxY if maxY is not None else max([dataset.max() for dataset in data])
        self.minY = minY if minY is not None else min([dataset.min() for dataset in data])

        self.xCategoricalLabels = xCategroicalLabels if xCategroicalLabels is not None else \
            [dataset.label for dataset in data]

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.graphSize = graphSize

        self.title = title
        self.showXAxisLabel: bool = showXAxisLabel
        self.showYAxisLabel: bool = showYAxisLabel
        self.xAxisLabel = xAxisLabel
        self.yAxisLabel = yAxisLabel

        self.bgColour = bgColour
        self.primaryColour = primaryColour if primaryColour is not None else complementary(self.bgColour)
        if self.primaryColour == (0, 0, 0):
            self.primaryColour = (100, 100, 100)

        self.colours: list[tuple] = colours if colours is not None else \
            [self.primaryColour for _ in range(self.numDatasets)]
        self.borderColour: tuple = borderColour if borderColour is not None else primaryColour

        self.fontName = fontName
        self.axisMarkerDensity = axisMarkerDensity  # marks per pixel

        self.borderWidth = borderWidth

        super().__init__(self.maxY, True, 0, self.minY, 0,
                         self.xCategoricalLabels, self.x, self.y, self.width, self.height, self.graphSize,
                         self.borderWidth, self.bgColour, self.primaryColour, self.borderColour, self.title,
                         self.showXAxisLabel, self.showYAxisLabel, self.xAxisLabel, self.yAxisLabel,
                         self.fontName, self.axisMarkerDensity)

    def draw(self, window: pygame.Surface):
        # -- calculate values and draw graph outline -- #
        super().draw(window)

        boxWidth = self.graphWidth / self.numDatasets
        boxProportion = 0.9  # amount of its possible width that the box will take up

        # -- graph -- #

        for i, dataset in enumerate(self.data):
            boxX = self.graphX + (i + 0.5 * (1 - boxProportion)) * boxWidth
            colour = self.colours[i] if self.colours[i] is not None else (100, 100, 100)
            lineColour = ((0 + colour[0]) / 2, ((0 + colour[1]) / 2), (0 + colour[2]) / 2)

            self.drawBoxplot(window, dataset, boxX, self.originY, self.yScale,
                             boxWidth * boxProportion, colour, lineColour)

    def drawBoxplot(self, window, data: DiscreteData, x, originY, scale, width, colour, lineColour):
        # -- get values -- #
        medianValue = data.median
        quarterOne = data.quarterOne()
        quarterThree = data.quarterThree()
        iqr = quarterThree - quarterOne

        lowerBound = value_before_threshold(quarterOne - 1.5 * iqr, data.data, False)
        upperBound = value_before_threshold(quarterThree + 1.5 * iqr, data.data, True)

        outliers = []
        for dataPoint in data.data:
            if dataPoint < lowerBound or dataPoint > upperBound:
                outliers.append(dataPoint)

        # -- box -- #
        pygame.draw.rect(window, lineColour,
                         (x, originY - quarterThree * scale, width, (quarterThree - quarterOne) * scale))
        pygame.draw.rect(window, colour,
                         (
                             x + 2, originY - quarterThree * scale + 2, width - 4,
                             (quarterThree - quarterOne) * scale - 4))

        # -- median line -- #
        pygame.draw.line(window, lineColour,
                         (x, originY - medianValue * scale), (x + width - 2, originY - medianValue * scale), 3)

        # -- tail lines -- #
        pygame.draw.line(window, lineColour,
                         (x + width / 2, originY - quarterOne * scale),
                         (x + width / 2, originY - lowerBound * scale), 1)
        pygame.draw.line(window, lineColour,
                         (x + width / 2, originY - quarterThree * scale),
                         (x + width / 2, originY - upperBound * scale), 1)

        # -- tail caps -- #
        pygame.draw.line(window, lineColour,
                         (x + width / 3, originY - lowerBound * scale),
                         (x + 2 * width / 3, originY - lowerBound * scale), 1)
        pygame.draw.line(window, lineColour,
                         (x + width / 3, originY - upperBound * scale),
                         (x + 2 * width / 3, originY - upperBound * scale), 1)

        # -- outliers -- #
        for value in outliers:
            pygame.draw.circle(window, colour, (x + width / 2, originY - value * scale), width * 0.05)
            pygame.draw.circle(window, lineColour, (x + width / 2, originY - value * scale), width * 0.05, 1)

    def set_title(self, title: str):
        self.title = title

    def set_x_label(self, xLabel: str):
        self.xAxisLabel = xLabel

    def set_y_label(self, yLabel: str):
        self.yAxisLabel = yLabel

    def set_colours(self, *colours: tuple[int]):
        """
        Sets the point colours for each dataset.
        :param colours: Tuples with rgb values corresponding to the desired colour for each dataset
        :return: None
        """
        if len(colours) != self.numDatasets:
            raise ValueError("The wrong number of arguments has been provided. Expecting " + str(self.numDatasets) +
                             " arguments, received " + str(len(colours)) + " arguments.")
        for i, colour in enumerate(colours):
            if not valid_rgb_colour(colour):
                raise ValueError("Element " + str(i) + " is not a colour.")

        self.colours = colours


class Scatterplot(Graph):
    """
    Describes a scatterplot object.
    """

    def __init__(self, *data: MultivariableDiscreteData,
                 maxY: int | None = None, maxX: float | None = None,
                 minY: float | None = None, minX: float | None = None,
                 x=0, y=0, width: int | None = None, height: int | None = None, graphSize=0.75, borderWidth=0,
                 bgColour: tuple = (255, 255, 255), primaryColour: tuple = None, borderColour: tuple = None,
                 colours: list[tuple] = None,
                 title: str = "", showXAxisLabel: bool = True, showYAxisLabel: bool = True,
                 xAxisLabel: str = "", yAxisLabel: str = "",
                 fontName: str = "freesanbold", axisMarkerDensity: float = 0.008,
                 bestFitLines: list[bool] = None, mainBestFitLine: bool = False,
                 pointSizes: list[float] = None):
        """
        :param data: The (2D) datasets that will be displayed on the scatterplot
        :param maxY: The maximum y value to display on the graph. This determines the y axis scale.
        :param maxX: Necessary if the graph has a numerical x axis. This is the maximum x value, determines the x scale.
        :param minY: The minimum y value to display on the graph (useful if data is clustered around a nonzero value)
        :param minX: The minimum x value to display on the graph. Helps determine the x scale; same with min y.
        :param x: The x position on the pygame window to display the graph object.
        :param y: The y position on the pygame window to display the graph object.
        :param width: The width of the graph object on the pygame window (when 0, defaults to the frame's width).
        :param height: The height of the graph object on the pygame window (when 0, defaults to the frame's width).
        :param graphSize: The proportional size of the working section of the graph; the rest is for labels, titles, etc
        :param borderWidth: The width of the object's border
        :param bgColour: The object's background colour. The complement of this is the default of 'primaryColour'.
        :param primaryColour: The primary colour of the graph: used for axes, labels, title, etc.
        :param borderColour: The border's colour. Defaults to primaryColour.
        :param title: The graph's title.
        :param showXAxisLabel: A boolean representing whether to show the x axis label.
        :param showYAxisLabel: A boolean representing whether to show the y axis label.
        :param xAxisLabel: The label for the x axis (default's to the first dataset's x label).
        :param yAxisLabel: The label for the y axis (default's to the first dataset's y label).
        :param fontName: The font to use for the graph
        :param axisMarkerDensity: The approximate number of axis marks per pixel. This value is used to calculate the
        actual distance between axis marks.
        :param bestFitLines: A list of booleans encoding whether to display each dataset's best fit line (default False)
        :param mainBestFitLine: A boolean encoding whether to display the best fit line encompassing all datasets
        :param colours: The colours for each dataset's points (defaults to black)
        :param pointSizes: The point sizes for the graph's points (defaults to scale with the graph's size)
        """

        # check the correct number of dimensions for the data
        for i, dataset in enumerate(data):
            if dataset.numDimensions != 2:
                raise ValueError("Scatterplots take 2-dimensional data. Dataset " + str(i) + " has " +
                                 str(dataset.numDimensions) + " dimensions.")

        # necessary variables
        self.datasets: tuple = data
        self.numDatasets: int = len(data)

        # other variables (set to default)
        self.maxX = maxX if maxX is not None else max([dataset.max(0) for dataset in self.datasets])
        self.maxY = maxY if maxY is not None else max([dataset.max(1) for dataset in self.datasets])
        self.minX = minX if minX is not None else min([dataset.min(0) for dataset in self.datasets])
        self.minY = minY if minY is not None else min([dataset.min(1) for dataset in self.datasets])

        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.graphSize = graphSize  # proportional size of the graph relative to the effective area

        self.borderWidth = borderWidth
        self.bgColour = bgColour
        self.primaryColour = primaryColour if primaryColour is not None else complementary(bgColour)
        self.borderColour = borderColour if borderColour is not None else self.primaryColour
        self.colours: list[tuple] = colours if colours is not None else \
            [self.primaryColour for _ in range(self.numDatasets)]

        self.title = title
        self.showXAxisLabel = showXAxisLabel
        self.showYAxisLabel = showYAxisLabel

        self.xAxisLabel: str = xAxisLabel if xAxisLabel != "" else self.datasets[0].data[0].label
        self.yAxisLabel: str = yAxisLabel if yAxisLabel != "" else self.datasets[0].data[1].label

        self.fontName = fontName

        self.axisMarkerDensity = axisMarkerDensity  # marks per pixel

        self.bestFitLines = bestFitLines if bestFitLines is not None else [False for _ in range(self.numDatasets)]
        self.mainBestFitLine = mainBestFitLine

        self.pointSizes: list[float] = pointSizes if pointSizes is not None else [None for _ in range(self.numDatasets)]

        super().__init__(self.maxY, False, self.maxX, self.minY, self.minX, None, self.x, self.y, self.width,
                         self.height, self.graphSize, self.borderWidth, self.bgColour, self.primaryColour,
                         self.borderColour, self.title, self.showXAxisLabel, self.showYAxisLabel,
                         self.xAxisLabel, self.yAxisLabel,
                         self.fontName, self.axisMarkerDensity)

        self.printBestFitInfo = True

    def draw(self, window: pygame.Surface):
        # -- draw graph frame and calculate defaults -- #
        super().draw(window)

        # scale values (in pixels per [unit])
        defaultPointSize = 0.007 * (self.graphWidth + self.graphHeight)

        # -- points and best fit lines -- #
        for i, dataset in enumerate(self.datasets):
            # set colour (default to the complement of the background) and point size
            colour = self.colours[i]
            pointSize: float = self.pointSizes[i] if self.pointSizes[i] is not None else defaultPointSize

            # draw points
            for xPointVal, yPointVal in dataset.get_points_list():
                pygame.draw.circle(window, colour,
                                   (self.originX + xPointVal * self.xScale, self.originY - yPointVal * self.yScale),
                                   pointSize)

            # draw best fit lines
            if self.bestFitLines[i]:
                slope, intercept = linear_regression(dataset.getData(0), dataset.getData(1))

                if self.printBestFitInfo:
                    print("Best fit line for " + dataset.title)
                    print("Slope: " + str(slope) +
                          ", intercept: " + str(intercept))
                    print()

                draw_line(window, self.originX, self.originY, self.xScale, self.yScale, slope, intercept,
                          dataset.min(0), dataset.max(0), colour)

        # -- main best fit line -- #
        if self.mainBestFitLine:
            xData = []
            yData = []
            for dataset in self.datasets:
                xData += dataset.getData(0)
                yData += dataset.getData(1)

            slope, intercept = linear_regression(xData, yData)

            if self.printBestFitInfo:
                print("Best fit line for all datasets in " + self.datasets[0].title[:8])
                print("Slope: " + str(slope) +
                      ", intercept: " + str(intercept))
                print("\n------------------------------------------------------------\n")
                self.printBestFitInfo = False

            draw_line(window, self.originX, self.originY, self.xScale, self.yScale, slope, intercept,
                      min(xData), max(xData), self.primaryColour)

    def set_title(self, title: str):
        self.title = title

    def set_x_label(self, xLabel: str):
        self.xAxisLabel = xLabel

    def set_y_label(self, yLabel: str):
        self.yLabel = yLabel

    def set_point_sizes(self, *pointSizes: int):
        """
        Sets the point radii for each dataset to the inputted values.
        Point sizes defaults to scale with the size of the scatterplot
        :param pointSizes: The desired radius of the points. If set to 0, the points scale with the size of the plot.
        :return: None
        """
        if len(pointSizes) != self.numDatasets:
            raise ValueError("The number of arugments must match the number of datasets. You entered " +
                             str(len(pointSizes)) + " arguments, but this scatterplot has " +
                             str(self.numDatasets) + " datasets.")

        self.pointSizes = pointSizes

    def set_colours(self, *colours: tuple[int]):
        """
        Sets the point colours for each dataset.
        :param colours: Tuples with rgb values corresponding to the desired colour for each dataset
        :return: None
        """
        if len(colours) != self.numDatasets:
            raise ValueError("The wrong number of arguments has been provided. Expecting " + str(self.numDatasets) +
                             " arguments, received " + str(len(colours)) + " arguments.")
        for i, colour in enumerate(colours):
            if not valid_rgb_colour(colour):
                raise ValueError("Element " + str(i) + " is not a colour.")

        self.colours = colours


def next_lowest_decimultiple(upperBound: float, multiples: list):
    powerOfTen = math.floor(math.log10(upperBound))
    upperBound /= (10 ** powerOfTen)
    decimultiple = 1
    multiples.sort(reverse=True)
    for number in multiples:
        if upperBound >= number:
            decimultiple = number
            break

    decimultiple *= (10 ** powerOfTen)

    return decimultiple


def value_before_threshold(bound: float, values: list, belowThreshold: bool = True) -> float:
    """
    Finds the value from a list closest to a given threshold, either above or below.
    :param bound: The bound to search for the closest value above / below.
    :param values: The values (data) to be searched through
    :param belowThreshold: If true, will find the largest value below the threshold. If false, smallest value above.
    :return: The value found
    """

    valuesCopy = values.copy()
    valuesCopy.sort()

    for i, value in enumerate(valuesCopy):
        if value > bound:
            return valuesCopy[i - belowThreshold]

    if belowThreshold:
        return valuesCopy[-1]
    else:
        raise ValueError("No values above threshold.")


def median(data: list) -> float:
    data = data.copy()
    data.sort()
    length = len(data)
    if length % 2 == 0:
        return (data[int(length / 2 - 0.5)] + data[int(length / 2 + 0.5)]) / 2

    return data[int(length / 2)]


def linear_regression(xData: list, yData: list) -> (float, float):
    if len(xData) != len(yData):
        raise ValueError("The length of the x and y data don't match.")

    slope = (len(xData) * sumProducts(xData, yData) - sum(xData) * sum(yData)) / \
            (len(xData) * sumProducts(xData, xData) - sum(xData) ** 2)

    intercept = (sum(yData) * sumProducts(xData, xData) - sum(xData) * sumProducts(xData, yData)) / \
                (len(xData) * sumProducts(xData, xData) - sum(xData) ** 2)

    return slope, intercept


def sumProducts(dataOne, dataTwo) -> float:
    if len(dataOne) != len(dataTwo):
        raise ValueError("The length of the two datasets doesn't match.")

    pSum = 0
    for i in range(len(dataOne)):
        pSum += (dataOne[i] * dataTwo[i])

    return pSum


def sig_figs(x: float, precision: int):
    """
    Rounds a number to number of significant figures
    Parameters:
    - x - the number to be rounded
    - precision (integer) - the number of significant figures
    Returns:
    - float
    """
    if x == 0:
        return 0

    return round(x, -int(math.floor(math.log10(abs(x)))) + (precision - 1))


def valid_rgb_colour(colour: tuple) -> bool:
    if len(colour) != 3:
        return False
    for n in colour:
        if not (0 <= n <= 255):
            return False
    return True


def complementary(colour: tuple) -> tuple:
    return 255 - colour[0], 255 - colour[1], 255 - colour[2]


def draw_line(window, originX, originY, xScale, yScale, slope, intercept, startX, endX, colour=(0, 0, 0), width=1):
    pygame.draw.line(window, colour,
                     (originX + xScale * startX, originY - yScale * (intercept + slope * startX)),
                     (originX + xScale * endX, originY - yScale * (intercept + slope * endX)),
                     width)


def draw_text(window: pygame.Surface, text: str, centerPosition: tuple, colour: tuple, font: pygame.font.Font,
              rotateDegrees: int = 0):
    renderedText = pygame.transform.rotate(font.render(text, True, colour), rotateDegrees)
    textRect = renderedText.get_rect()
    textRect.center = centerPosition
    window.blit(renderedText, textRect)

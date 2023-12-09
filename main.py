from ucimlrepo import fetch_ucirepo
from dataManipulation import *

# fetch dataset
iris = fetch_ucirepo(id=53)

# data (as pandas dataframes)
X = iris.data.features

# variable information
sepalLen = list(X["sepal length"])
sepalLenDict = {"Iris-setosa": sepalLen[:50], "Iris-versicolor": sepalLen[50:100], "Iris-virginica": sepalLen[100:]}
sepalWid = list(X["sepal width"])
sepalWidDict = {"Iris-setosa": sepalWid[:50], "Iris-versicolor": sepalWid[50:100], "Iris-virginica": sepalWid[100:]}
petalLen = list(X["petal length"])
petalLenDict = {"Iris-setosa": petalLen[:50], "Iris-versicolor": petalLen[50:100], "Iris-virginica": petalLen[100:]}
petalWid = list(X["petal width"])
petalWidDict = {"Iris-setosa": petalWid[:50], "Iris-versicolor": petalWid[50:100], "Iris-virginica": petalWid[100:]}

dataDictionaries = {"Sepal Length": sepalLenDict, "Sepal Width": sepalWidDict,
                    "Petal Length": petalLenDict, "Petal Width": petalWidDict}

# visualizer objects
WIDTH_GRAPH_MATRIX = 1600
HEIGHT_GRAPH_MATRIX = 1000

WIDTH_BOXPLOTS = 1200
HEIGHT_BOXPLOTS = 320

graphMatrixVisualizer = StatVisualizer(WIDTH_GRAPH_MATRIX, HEIGHT_GRAPH_MATRIX, "Iris Data")
boxplotsVisualizer = StatVisualizer(WIDTH_BOXPLOTS, HEIGHT_BOXPLOTS, "Boxplots")


# examples of functionality

def make_graph_matrix(statVisualizer: StatVisualizer, width, height, bestFitLines=False):
    for row, yVariable in enumerate(["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]):
        for col, xVariable in enumerate(["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]):
            if xVariable == yVariable:
                graph = BoxplotGraph(
                    DiscreteData(dataDictionaries[xVariable]["Iris-setosa"], label="Iris-setosa"),
                    DiscreteData(dataDictionaries[xVariable]["Iris-versicolor"], label="Iris-versicolor"),
                    DiscreteData(dataDictionaries[xVariable]["Iris-virginica"], label="Iris-virginica"),
                    x=col * width / 4, y=row * height / 4, width=int(width / 4), height=int(height / 4),
                    xAxisLabel=xVariable, yAxisLabel=yVariable, colours=[(20, 20, 255), (20, 255, 20), (230, 130, 50)],
                    showXAxisLabel=row == 3, showYAxisLabel=col == 0, graphSize=0.67, axisMarkerDensity=0.015,
                    borderWidth=3, borderColour=[(220, 61, 42), (0, 179, 44)][(row + col) % 2]
                )
                statVisualizer.add_objects(graph)
            else:
                graph = Scatterplot(
                    MultivariableDiscreteData(
                        DiscreteData(dataDictionaries[xVariable]["Iris-setosa"]),
                        DiscreteData(dataDictionaries[yVariable]["Iris-setosa"]),
                        title="Graph " + str(4 * row + col + 1) +
                              ": Iris-setosa " + xVariable + " x " + yVariable + " (blue)"
                    ),
                    MultivariableDiscreteData(
                        DiscreteData(dataDictionaries[xVariable]["Iris-versicolor"]),
                        DiscreteData(dataDictionaries[yVariable]["Iris-versicolor"]),
                        title="Graph " + str(4 * row + col + 1) +
                              ": Iris-versicolor " + xVariable + " x " + yVariable + " (green)"
                    ),
                    MultivariableDiscreteData(
                        DiscreteData(dataDictionaries[xVariable]["Iris-virginica"]),
                        DiscreteData(dataDictionaries[yVariable]["Iris-virginica"]),
                        title="Graph " + str(4 * row + col + 1) +
                              ": Iris-virginica " + xVariable + " x " + yVariable + " (orange)"
                    ),
                    x=col * width / 4, y=row * height / 4, width=int(width / 4), height=int(height / 4),
                    colours=[(20, 20, 255), (20, 255, 20), (230, 130, 50)],
                    showXAxisLabel=row == 3, showYAxisLabel=col == 0, xAxisLabel=xVariable, yAxisLabel=yVariable,
                    graphSize=0.67, axisMarkerDensity=0.015,
                    borderWidth=3, borderColour=[(220, 61, 42), (0, 179, 44)][(row + col) % 2],
                    bestFitLines=[bestFitLines, bestFitLines, bestFitLines], mainBestFitLine=bestFitLines
                )
                statVisualizer.add_objects(graph)

    statVisualizer.start()


def make_boxplots(statVisualizer: StatVisualizer, width):
    for i, variable in enumerate(["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]):
        graph = BoxplotGraph(
            DiscreteData(dataDictionaries[variable]["Iris-setosa"], label="Iris-setosa"),
            DiscreteData(dataDictionaries[variable]["Iris-versicolor"], label="Iris-versicolor"),
            DiscreteData(dataDictionaries[variable]["Iris-virginica"], label="Iris-virginica"),
            x=i * width / 4, width=int(width / 4),
            xAxisLabel="Iris Species", yAxisLabel=variable,
            colours=[(20, 20, 255), (20, 255, 20), (230, 130, 50)], axisMarkerDensity=0.01
        )
        statVisualizer.add_objects(graph)

    statVisualizer.start()


def best_fit_lines(statVisualizer: StatVisualizer, width, height):
    make_graph_matrix(statVisualizer, width, height, bestFitLines=True)


def descrpitive_statistics():
    for variable in ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]:
        for key in dataDictionaries[variable].keys():
            dataset: DiscreteData = DiscreteData(dataDictionaries.get(variable).get(key))
            print(variable + " for " + key + ":")
            print("Min: " + str(dataset.min()))
            print("1st quarter: " + str(dataset.quarterOne()))
            print("Median: " + str(median(dataset.getData())))
            print("3rd quarter: " + str(dataset.quarterThree()))
            print("Max: " + str(dataset.max()))
            print("\n-----------------------------------------\n")


if __name__ == "main":
    print("Welcome to this data manipulation and statistics library!\n")
    # Example 1
    # make_graph_matrix(graphMatrixVisualizer, WIDTH_GRAPH_MATRIX, HEIGHT_GRAPH_MATRIX)

    # Example 2
    # make_boxplots(boxplotsVisualizer, WIDTH_BOXPLOTS)

    # Example 3
    # best_fit_lines(graphMatrixVisualizer, WIDTH_GRAPH_MATRIX, HEIGHT_GRAPH_MATRIX)

    # Example 4
    # descrpitive_statistics()

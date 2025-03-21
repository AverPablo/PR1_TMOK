# -*- coding: utf-8 -*-
"""02_TrainTestSplitScikitLearn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m0TfWqNVNGsms4kJSKrmSVYihG4qhO0e

<h1>Understanding Train Test Split using Scikit-Learn (Python)</h1>

![](images/TrainTestProcedure.png)

A goal of supervised learning is to build a model that performs well on new data. If you have new data, it’s a good idea to see how your model performs on it. The problem is that you may not have new data, but you can simulate this experience with a procedure like train test split. This tutorial includes:

* What is the Train Test Split Procedure
* Using Train Test Split to Tune Models using Python
* The Bias-variance Tradeoff

<h2>What is the Train Test Split Procedure</h2>

![](images/TrainTestProcedure.png)

train test split is a model validation procedure that allows you to simulate how a model would perform on new/unseen data. Here is how the procedure works.

0. Make sure your data is arranged into a format acceptable for train test split. In scikit-learn, this consists of separating your full dataset into Features and Target.
1. Split the dataset into two pieces: a training set and a testing set. This consists of randomly selecting about 75% (you can vary this) of the rows and putting them into your training set and putting the remaining 25% to your test set. Note that the colors in “Features” and “Target” indicate where their data will go (“X_train”, “X_test”, “y_train”, “y_test”) for a particular train test split.
2. Train the model on the training set. This is “X_train” and “y_train” in the image.
3. Test the model on the testing set (“X_test” and “y_test” in the image) and evaluate the performance.

<h2>Consequences of NOT using Train Test Split</h2>

You could try not using train test split and <b>train and test the model on the same data</b>. I don’t recommend this approach as it doesn’t simulate how a model would perform on new/unseen data and it tends to reward overly complex models that overfit on the dataset.

The steps below go over how this inadvisable process works.

![](images/NotUsingTrainTestSplit.png)

0. Make sure your data is arranged into a format acceptable for train test split. In scikit-learn, this consists of separating your full dataset into Features and Target.
1. Train the model on “Features” and “Target”.
2. Test the model on “Features” and “Target” and evaluate the performance.

It is important to again emphasize that training on an entire data set and then testing on that same dataset can lead to overfitting. You might find the image below useful in explaining what overfitting is.  The green squiggly line best follows the training data. The problem is that it is likely overfitting on the training data meaning it is likely to perform worse on unseen/new data. [Image contributed by Chabacano to Wikipedia (CC BY-SA 4.0)](https://en.wikipedia.org/wiki/Overfitting#/media/File:Overfitting.svg)(https://creativecommons.org/licenses/by-sa/4.0/).

![](images/Overfitting.png)

<h2>Using Train Test Split to Tune Models using Python
</h2>

![](images/TrainTestRepeat.png)

This section is about the practical application of train test split to predicting home prices. It goes all the way from importing a dataset to performing a train test split to hyperparameter tuning (change hyperparameters in the image above is also known as hyperparameter tuning) a decision tree regressor to predict home prices and more.

<h3>Import Libraries</h3>

![](images/PythonLibraries.jpg)

Python has a lot of libraries that can help you accomplish your data science goals (the image above is likely from [Reddit](https://www.reddit.com/r/ProgrammerHumor/comments/6a59fw/import_essay/)) including scikit-learn, pandas, and NumPy which the code below imports
"""

import pandas as pd  # Импорт библиотеки pandas для работы с данными в формате таблиц (DataFrame).
import numpy as np   # Импорт библиотеки numpy для работы с массивами и числовыми операциями.
import matplotlib.pyplot as plt  # Импорт библиотеки matplotlib для визуализации данных с помощью графиков.
from sklearn import tree  # Импорт модуля tree из библиотеки scikit-learn для работы с деревьями решений.
from sklearn.model_selection import train_test_split  # Импорт функции train_test_split для разделения данных на обучающую и тестовую выборки.
from sklearn.tree import DecisionTreeRegressor  # Импорт класса DecisionTreeRegressor для создания модели регрессии на основе дерева решений.

"""<h3>Load the Dataset
</h3>

Kaggle hosts a dataset which contains the price at which houses were sold for King County, which includes Seattle between May 2014 and May 2015. You can download the dataset from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction) or load it from my [GitHub](https://raw.githubusercontent.com/mGalarnyk/Tutorial_Data/master/King_County/kingCountyHouseData.csv). The code below loads the dataset.
"""

# URL для загрузки данных о домах в округе Кинг
url = 'https://raw.githubusercontent.com/mGalarnyk/Tutorial_Data/master/King_County/kingCountyHouseData.csv'

# Загрузка данных из CSV файла в DataFrame
df = pd.read_csv(url)

# Выбор только тех столбцов, которые меня интересуют
columns = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'price']
df = df.loc[:, columns]  # Фильтрация DataFrame по выбранным столбцам

# Просмотр первых 10 строк отфильтрованного DataFrame
df.head(10)

"""<h3>Arrange Data into Features and Target</h3>

Scikit-Learn’s train_test_split expects data in the form of features and target. In scikit-learn, a features matrix is a two-dimensional grid of data where rows represent samples and columns represent features. A target is what you want to predict from the data. This tutorial uses ‘price’ as a target.
"""

# Определение признаков (features) для модели
features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors']  # Список признаков, которые будут использоваться для предсказания цены
X = df.loc[:, features]  # Извлечение данных по выбранным признакам из DataFrame df и сохранение их в переменной X
y = df.loc[:, ['price']]  # Извлечение данных по цене из DataFrame df и сохранение их в переменной y

"""![](images/KingCountyArrangeData.png)

<h3>Split Data into Training and Testing Sets (train test split)
</h3>

![](images/KingCountyTrainTestSplit.png)

The colors in the image above indicate which variable (X_train, X_test, y_train, y_test) from the original dataframe df will go to for our particular train test split (random_state = 0).

In the code below, train_test_split splits the data and returns a list which contains four NumPy arrays. train_size = .75 puts 75% of the data into a training set and the remaining 25% into a testing set.
"""

# Импортируем функцию train_test_split из библиотеки sklearn.model_selection
from sklearn.model_selection import train_test_split

# Разделение данных на обучающую и тестовую выборки
# X - это набор признаков (фич), а y - целевая переменная (метка)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size=0.75)

# X_train: обучающая выборка признаков (75% от общего набора)
# X_test: тестовая выборка признаков (25% от общего набора)
# y_train: целевая переменная для обучающей выборки
# y_test: целевая переменная для тестовой выборки

"""The image below shows the number of rows and columns the variables contain using the shape attribute before and after the train test split. 75 percent of the rows went to the training set (16209/ 21613 = .75) and 25 percent went to the test set (5404 / 21613 = .25).

![](images/KingCountyShape.png)

<h3>Understanding random_state</h3>

![](images/KingCountyRandomState.png)

The random_state is a pseudo-random number parameter that allows you to reproduce the same exact train test split each time you run the code. The image above shows that if you select a different value for random state, different information would go to X_train, X_test, y_train, and y_test. There are a number of reasons why people use random_state including software testing, tutorials (like this one), and talks. However, it is recommended you remove it if you are trying to see how well a model generalizes to new data.

<h3>Creating and Training a Model with Scikit-learn</h3>

<b>Step 1:</b> Import the model you want to use.

In scikit-learn, all machine learning models are implemented as Python classes.
"""

# Импорт класса DecisionTreeRegressor из библиотеки scikit-learn
from sklearn.tree import DecisionTreeRegressor

# DecisionTreeRegressor - это класс, который реализует алгоритм регрессии на основе дерева решений.
# Он используется для предсказания непрерывных значений, основываясь на входных данных.
# Деревья решений работают, разбивая данные на подмножества на основе значений признаков,
# что позволяет модели учитывать наиболее значимые факторы при предсказании.

"""<b>Step 2:</b> Make an instance of the model

In the code below, I set the hyperparameter max_depth = 2 to preprune my tree to make sure it doesn’t have a depth greater than 2. I should note the next section of the tutorial will go over how to choose an optimal max_depth for your tree.

Also note that in my code below, I made random_state = 0 so that you can get the same results as me.
"""

# Создание экземпляра модели DecisionTreeRegressor с заданной максимальной глубиной и случайным состоянием
reg = DecisionTreeRegressor(max_depth=2, random_state=0)

# В этой строке мы создаем объект модели регрессии на основе дерева решений.
# Параметр max_depth=2 ограничивает максимальную глубину дерева до 2 уровней.
# Это помогает предотвратить переобучение модели, так как более глубокие деревья могут подстраиваться под шум в данных.
# Параметр random_state=0 устанавливает начальное состояние генератора случайных чисел,
# что обеспечивает воспроизводимость результатов. Это означает, что каждый раз, когда мы запускаем код,
# модель будет обучаться на тех же случайных подвыборках данных.

"""<b>Step 3:</b> Train the model on the data, storing the information learned from the data."""

# Обучение модели DecisionTreeRegressor на обучающих данных
reg.fit(X_train, y_train)

# В этой строке мы обучаем модель дерева решений (DecisionTreeRegressor) на обучающих данных.
# Метод fit принимает два аргумента: X_train и y_train.
# X_train — это матрица признаков, содержащая входные данные для обучения модели.
# y_train — это вектор целевых значений, который модель будет пытаться предсказать на основе входных данных.
# В процессе обучения модель анализирует данные и строит дерево решений, которое будет использоваться для предсказания значений на новых данных.
# После выполнения этой строки модель будет готова к использованию для предсказания значений на тестовых данных.

"""<b>Step 4:</b> Predict labels of unseen (test) data"""

# Предсказание цен для первых 10 наблюдений в тестовом наборе данных
predictions = reg.predict(X_test[0:10])

# В этой строке мы используем обученную модель reg для предсказания значений на тестовых данных.
# Метод predict принимает в качестве аргумента набор данных, для которого мы хотим получить предсказания.
# В данном случае мы передаем первые 10 наблюдений из тестового набора данных X_test.
# Срез [0:10] выбирает первые 10 строк из X_test.
# Результатом выполнения метода predict будет массив предсказанных значений, который мы сохраняем в переменной predictions.
# Эти предсказанные значения представляют собой оценки целевой переменной (например, цен), основанные на входных данных из первых 10 наблюдений.

"""For the multiple predictions above, notice how many times some of the predictions are repeated. If you are wondering why, I encourage you to check out the code below which will start by looking at a single observation/house and then proceed to look at how the model makes its prediction."""

X_test.head(1)

"""The code below shows how to make a prediction for that single observation."""

# Предсказание для одного наблюдения из тестового набора данных
prediction_single = reg.predict(X_test.iloc[0].values.reshape(1, -1))

# В этой строке мы используем метод predict для получения предсказания для одного конкретного наблюдения из тестового набора данных.
# X_test.iloc[0] выбирает первое наблюдение из тестового набора данных X_test.
# Метод iloc используется для доступа к строкам и столбцам по их индексам.
# .values возвращает значения этого наблюдения в виде массива NumPy.
# reshape(1, -1) изменяет форму массива, чтобы он стал двумерным с одной строкой и необходимым количеством столбцов.
# Это необходимо, потому что метод predict ожидает входные данные в виде двумерного массива, где каждая строка представляет собой отдельное наблюдение.
# Результат выполнения метода predict сохраняется в переменной prediction_single, которая будет содержать предсказанное значение для данного наблюдения.

"""The image below shows how the trained model makes a prediction for the one observation.

![](images/HousePredictions.png)

If you are curious how these sorts of diagrams are made, consider checking out my tutorial [Visualizing Decision Trees using Graphviz and Matplotlib](https://towardsdatascience.com/visualizing-decision-trees-with-python-scikit-learn-graphviz-matplotlib-1c50b4aa68dc).

<h3>Measuring Model Performance</h3>

![](images/CoefficientDetermination.png)

While there are other ways of measuring model performance (root-mean-square error, mean absolute error, mean absolute error, etc), we are going to keep this simple and use R² otherwise known as the coefficient of determination as our metric. The best possible score is 1.0. A constant model that would always predict the mean value of price would get a R² score of 0.0 (interestingly it is possible to get a negative R² on the test set). The code below uses the trained model’s score method to return the R² of the model that was evaluated on the test set.
"""

# Оценка модели на тестовом наборе данных
score = reg.score(X_test, y_test)

# В этой строке мы используем метод score для оценки производительности модели reg на тестовом наборе данных.
# Метод score возвращает коэффициент детерминации R², который измеряет, насколько хорошо предсказанные значения модели соответствуют фактическим значениям.
# X_test - это входные данные тестового набора, а y_test - это истинные значения, которые мы хотим предсказать.
# Результат оценки сохраняется в переменной score, которая будет содержать значение от 0 до 1, где 1 означает идеальное соответствие.
# Затем мы выводим значение score на экран.
print(score)

"""You might be wondering if our R² above is good for our model. In general the higher the R², the better the model fits the data. Determining whether a model is performing well can also depend on your field of study. Something harder to predict will in general have a lower R². My argument below is that for housing data, we should have a higher R² based solely on our data.

Here is why. Domain experts generally agree that one of the most important factors in housing prices is location. After all, if you are looking for a home, most likely you care where it is located. As you can see in the trained model below, the decision tree only incorporates sqft_living.

![](images/treeNoCustomarrows.png)
"""

# Visualize Decision Tree using Graphviz
"""
# Экспортируем дерево решений в формате DOT, который может быть использован для визуализации.
tree.export_graphviz(reg,
                     out_file="images/temp.dot",  # Указываем имя выходного файла, в который будет сохранен граф в формате DOT.
                     feature_names=features,  # Указываем имена признаков, которые будут отображены в графе.
                     filled=True)  # Указываем, что узлы дерева должны быть заполнены цветом в зависимости от класса.
"""

# Для выполнения этой команды необходимо установить Graphviz и добавить его в системный путь.
# Команда ниже преобразует файл DOT в изображение PNG с заданным разрешением.
#!dot -Tpng -Gdpi=300 images/temp.dot -o images/temp.png

# Код для генерации дерева решений на основе matplotlib.
"""
# Создаем фигуру и оси для графика с заданными параметрами.
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=300)
# nrows и ncols указывают количество строк и столбцов подграфиков,
# figsize задает размер фигуры, а dpi определяет разрешение графика.

# Визуализируем дерево решений, используя функцию plot_tree из библиотеки sklearn.
tree.plot_tree(reg,
              feature_names=features,  # Указываем имена признаков для отображения в узлах дерева.
              filled=True)  # Указываем, что узлы должны быть заполнены цветом в зависимости от класса.
"""

"""Even if the model was performing very well, it is unlikely that our model would get buy-in from stakeholders or coworkers as traditionally speaking, there is more to homes than sqft_living.

Note that the original dataset has location information like ‘lat’ and ‘long’. The image below visualizes the price percentile of all the houses in the dataset based on ‘lat’ and ‘long’ (‘lat’ ‘long’ wasn’t included in data which the model trained on). There is definitely a relationship between home price and location.

A way to improve the model would be to make it incorporate location information (‘lat’, ‘long’) as it is likely places like Zillow found a way to incorporate that into their models.

![](images/KingCountyHousingPrices.png)

<h3>Tuning the max_depth of a Tree</h3>

The R² for the model trained earlier in the tutorial was about .438. However, suppose we want to improve the performance so that we can better make predictions on unseen data. While we could definitely add more features like lat long to the model or increase the number of rows in the dataset (find more houses), another way to improve performance is through hyperparameter tuning which involves selecting the optimal values of tuning parameters for a machine learning problem. These tuning parameters are often called hyperparameters. Before doing hyperparameter tuning, we need to take a step back and briefly go over the difference between parameters and hyperparameters.

<b>Parameters vs hyperparameters</b>

A machine learning algorithm estimates model parameters for a given data set and updates these values as it continues to learn. You can think of a model parameter as a learned value from applying the fitting process. For example, in logistic regression you have model coefficients. In a neural network, you can think of neural network weights as a parameter. Hyperparameters or tuning parameters are meta parameters that influence the fitting process itself. For logistic regression, there are many hyperparameters like regularization strength C. For a neural network, there are many hyperparameters like the number of hidden layers. If all of this sounds confusing, [Jason Brownlee has a good rule of thumb](https://machinelearningmastery.com/difference-between-a-parameter-and-a-hyperparameter/) which is “If you have to specify a model parameter manually then it is probably a model hyperparameter.”

<b> Hyperparameter Tuning </b>

There are a lot of different ways to hyperparameter tune a decision tree for regression. One way is to tune the max_depth hyperparameter. max_depth (hyperparameter) is not the same thing as depth (parameter of a decision tree). max_depth is a way to preprune a decision tree. In other words, if a tree is already as pure as possible at a depth, it will not continue to split. If this isn’t clear, I highly encourage you to check out my Understanding Decision Trees for Classification (Python) tutorial to see the difference between max_depth and depth.

The code below outputs the accuracy for decision trees with different values for max_depth.
"""

# Определяем диапазон значений для максимальной глубины дерева решений.
max_depth_range = list(range(1, 25))

# Создаем список для хранения среднего значения R² для каждого значения max_depth.
r2_list = []

# Проходим по каждому значению глубины в заданном диапазоне.
for depth in max_depth_range:
    # Создаем экземпляр регрессора дерева решений с заданной максимальной глубиной и фиксированным состоянием генератора случайных чисел.
    reg = DecisionTreeRegressor(max_depth=depth, random_state=0)

    # Обучаем модель на тренировочном наборе данных.
    reg.fit(X_train, y_train)

    # Оцениваем модель на тестовом наборе данных и получаем коэффициент детерминации R².
    score = reg.score(X_test, y_test)

    # Добавляем полученное значение R² в список для дальнейшего анализа.
    r2_list.append(score)

"""The graph below shows that the best model R² is when the hyperparameter max_depth is equal to 5. This process of selecting the best model (max_depth = 5 in this case) among many other candidate models (with different max_depth values in this case) is called model selection."""

# Создаем фигуру и ось для графика с заданными размерами и белым фоном
fig, ax = plt.subplots(nrows = 1, ncols = 1,
                       figsize = (10,7),
                       facecolor = 'white');

# Строим график зависимости R^2 от значений max_depth
ax.plot(max_depth_range,
       r2_list,
       lw=2,  # Устанавливаем толщину линии
       color='r')  # Устанавливаем цвет линии красным

# Устанавливаем пределы по оси X от 1 до максимального значения в max_depth_range
ax.set_xlim([1, max(max_depth_range)])

# Добавляем сетку на график для удобства восприятия
ax.grid(True,
       axis = 'both',  # Включаем сетку по обеим осям
       zorder = 0,  # Устанавливаем порядок наложения сетки
       linestyle = ':',  # Устанавливаем стиль линии сетки в виде пунктирной
       color = 'k')  # Устанавливаем цвет сетки черным

# Устанавливаем размер шрифта для меток на осях
ax.tick_params(labelsize = 18)

# Устанавливаем подпись для оси X
ax.set_xlabel('max_depth', fontsize = 24)

# Устанавливаем подпись для оси Y
ax.set_ylabel('R^2', fontsize = 24)

# Устанавливаем заголовок графика
ax.set_title('Model Performance on Test Set', fontsize = 24)

# Оптимизируем размещение элементов на графике
fig.tight_layout()

# Сохраняем график в файл с заданным разрешением (закомментировано)
#fig.savefig('images/Model_Performance.png', dpi = 300)

"""Note that the model above could have still been overfitted on the test set since the code  changed max_depth repeatedly to achieve the best model. In other words, knowledge of the test set could have leaked into the model as the code iterated through 24 different values for max_depth (the length of max_depth_range is 24). This would lessen the power of our evaluation metric R² as it would no longer be as strong an indicator of generalization performance. This is why in real life, we often have training, test, and validation sets when hyperparameter tuning.

<h2>The Bias-variance Tradeoff</h2>

In order to understand why max_depth of 5 was the “best model” for our data, take a look at the graph below which shows the model performance when tested on the training and test set.
"""

# Создаем список значений для максимальной глубины дерева, которые будем тестировать
max_depth_range = list(range(1, 25))

# Список для хранения значений R^2 для тестового набора данных
r2_test_list = []

# Список для хранения значений R^2 для обучающего набора данных
r2_train_list = []

# Проходим по каждому значению глубины дерева из заданного диапазона
for depth in max_depth_range:

    # Создаем экземпляр регрессора дерева решений с заданной максимальной глубиной и фиксированным состоянием генератора случайных чисел
    reg = DecisionTreeRegressor(max_depth = depth,
                             random_state = 0)

    # Обучаем модель на обучающем наборе данных
    reg.fit(X_train, y_train)

    # Оцениваем модель на тестовом наборе данных и сохраняем значение R^2
    score = reg.score(X_test, y_test)
    r2_test_list.append(score)

    # Плохая практика: оценка модели на тех же данных, на которых она обучалась
    score = reg.score(X_train, y_train)
    r2_train_list.append(score)

# Создаем фигуру и ось для графика с заданными размерами и белым фоном
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (10,7), facecolor = 'white');

# Строим график R^2 для обучающего набора данных в зависимости от max_depth
ax.plot(max_depth_range,
        r2_train_list,
        lw=2,  # Устанавливаем толщину линии
        color='b',  # Устанавливаем цвет линии для обучающего набора
        label = 'Training')  # Добавляем метку для легенды

# Строим график R^2 для тестового набора данных в зависимости от max_depth
ax.plot(max_depth_range,
        r2_test_list,
        lw=2,  # Устанавливаем толщину линии
        color='r',  # Устанавливаем цвет линии для тестового набора
        label = 'Test')  # Добавляем метку для легенды

# Устанавливаем пределы по оси X
ax.set_xlim([1, max(max_depth_range)])

# Включаем сетку на графике
ax.grid(True,
        axis = 'both',  # Включаем сетку по обеим осям
        zorder = 0,  # Устанавливаем порядок наложения
        linestyle = ':',  # Устанавливаем стиль линии сетки
        color = 'k')  # Устанавливаем цвет сетки

# Устанавливаем размер шрифта для меток на осях
ax.tick_params(labelsize = 18)

# Устанавливаем метки для осей X и Y
ax.set_xlabel('max_depth', fontsize = 24)
ax.set_ylabel('R^2', fontsize = 24)

# Устанавливаем пределы по оси Y
ax.set_ylim(.2,1)

# Добавляем легенду на график
ax.legend(loc = 'center right', fontsize = 20, framealpha = 1)

# Добавляем аннотацию для обозначения "Лучшей модели" с указанием координат и стрелкой
ax.annotate("Best Model",
            xy=(5, 0.5558073822490773), xycoords='data',
            xytext=(5, 0.4), textcoords='data', size = 20,
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3",
                            color  = 'black',
                            lw =  2),
            ha = 'center',
            va = 'center',
            bbox={'facecolor':'white', 'edgecolor':'none', 'pad':5}
            )

# Устанавливаем заголовок графика
ax.set_title('Model Performance on Training vs Test Set', fontsize = 24)

# Добавляем аннотации для обозначения областей "Высокий смещение" и "Высокая дисперсия"
ax.annotate('High Bias',
            xy=(.1, .032), xycoords='figure fraction', size = 12)

ax.annotate('High Variance',
            xy=(.82, .032), xycoords='figure fraction', size = 12)

# Получаем текущие пределы по осям для дальнейшего использования
temp = ax.get_xlim()
temp1 = ax.get_ylim()

# Оптимизируем размещение элементов на графике
fig.tight_layout()

# Сохраняем график в файл (закомментировано)
#fig.savefig('images/max_depth_vs_R2_Best_Model.png', dpi = 300)

"""Naturally, the training R² is always better than the test R² for every point on this graph because models make predictions on data they have seen before.

To the left side of the “Best Model” on the graph (anything less than max_depth = 5), we have models that underfit the data and are considered high bias because they do not not have enough complexity to learn enough about the data.

To the right side of the “Best Model” on the graph (anything more than max_depth = 5), we have models that overfit the data and are considered high variance because they are overly complex models that perform well on the training data, but perform badly on testing data.

The “Best Model” is formed by minimizing bias error (bad assumptions in the model) and variance error (oversensitivity to small fluctuations/noise in the training set).

<h2> Conclusion </h2>

![](images/grid_search_cross_validation.png)

A goal of supervised learning is to build a model that performs well on new data which train test split helps you simulate. With any model validation procedure it is important to keep in mind some advantages and disadvantages which in the case of train test split are:

Some Advantages:
* Relatively simple and easier to understand than other methods like K-fold cross validation
* Helps avoid overly complex models that don’t generalize well to new data

Some Disadvantages:
* Eliminates data that could have been used for training a machine learning model (testing data isn’t used for training)
* Results can vary for a particular train test split (random_state)
* When hyperparameter tuning, knowledge of the test set can leak into the model (this can be partially solved by using a training, test, and validation set).

Future tutorials will cover other model validation procedures like K-fold cross validation ([pictured in the image above from the scikit-learn documentation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-evaluating-estimator-performance)) which help mitigate these issues. It is also important to note that [recent progress in machine learning has challenged the bias variance tradeoff](https://arxiv.org/abs/2109.02355) which is fundamental to the rationale for the train test split process.

![](images/DoubleDescentTestErrors.png)
"""

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql.functions import col, asc,desc
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pyspark.sql import SQLContext
from pyspark.mllib.stat import Statistics
import pandas as pd
from pyspark.sql.functions import udf
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler,StandardScaler
from pyspark.ml import Pipeline
from sklearn.metrics import confusion_matrix

spark=SparkSession.builder \
.master ("local[*]")\
.appName("Breast cancer classification")\
.getOrCreate()
sc=spark.sparkContext
sqlContext=SQLContext(sc)

df=spark.read \
 .option("header","True")\
 .option("inferSchema","True")\
 .option("sep",",")\
 .csv("/FileStore/tables/breast_data_1.csv")
print("There are",df.count(),"rows",len(df.columns),
      "columns" ,"in the data.")

df.show(4)
df.printSchema()
 
# Assuming df is defined as the PySpark DataFrame

# Summary statistics for numerical columns
df.describe().show()

# Summary statistics for all columns
df.describe().toPandas().transpose()

# Assuming df is defined as the PySpark DataFrame

# Summary statistics for numerical columns
df.describe().show()

# Summary statistics for all columns
df.describe().toPandas().transpose()

 
 



from matplotlib import pyplot as plt

# Assuming df is defined somewhere above this code snippet

fig = plt.figure(figsize=(25, 15))  # Plot Size
st = fig.suptitle("Distribution of Features", fontsize=50, verticalalignment='center')  # Plot Main Title

for col, num in zip(df.toPandas().describe().columns, range(1, 11)):
    ax = fig.add_subplot(3, 4, num)
    ax.hist(df.toPandas()[col])
    plt.grid(False)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=15)
    plt.title(col.upper(), fontsize=20)

    # Adding labels
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')

plt.tight_layout()
st.set_y(0.95)
fig.subplots_adjust(top=0.85, hspace=0.4)
plt.show()


 
 

from pyspark.sql.functions import isnan, when, count, col
df.select([count(when(isnan(c), c)).alias(c) for c in df.columns]).toPandas().head()

df.groupBy('diagnosis').count().show()
 
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer

# Assuming df is correctly defined as a DataFrame with a column named "class"
# If "class" column is not in string format, cast it to string
df = df.withColumn("diagnosis", df["diagnosis"].cast("string"))

# Initialize StringIndexer
class_indexer = StringIndexer(inputCol="diagnosis", outputCol="label")

# Fit and transform the DataFrame
df = class_indexer.fit(df).transform(df)

# Show the transformed DataFrame
df.show(5)

df.select(['diagnosis', 'label']).show(10)
 
def transformColumnsToNumeric(df, inputCol):

    #apply StringIndexer to inputCol
    inputCol_indexer = StringIndexer(inputCol = inputCol, outputCol = inputCol + "-index").fit(df)
    df = inputCol_indexer.transform(df)

    onehotencoder_vector = OneHotEncoder(inputCol = inputCol + "-index", outputCol = inputCol + "-vector")
    df = onehotencoder_vector.fit(df).transform(df)

    return df

    pass
from pyspark.ml.feature import VectorAssembler
df.columns

import matplotlib.pyplot as plt
import pandas as pd

# Assuming df is a Spark DataFrame with a column named 'diagnosis'

# Convert Spark DataFrame to Pandas DataFrame
df_pandas = df.toPandas()

# Print unique values in the 'diagnosis' column
unique_diagnosis = df_pandas['diagnosis'].unique()
print(unique_diagnosis)

# Define colors for each diagnosis
colors_dict = {'B': 'blue', 'M': 'green'}

# Plot using Pandas
ax = df_pandas['diagnosis'].value_counts().plot(kind='bar', color=[colors_dict[d] for d in unique_diagnosis])
ax.set_facecolor('white')  # Set background color to white
plt.xlabel('Diagnosis')
plt.ylabel('Count')
plt.title('Count of Diagnosis')

# Customize legend
legend_labels = ['Benign (B)', 'Malignant (M)']  # Update legend labels if needed
plt.legend(legend_labels, loc='best')

plt.show()

 
from pyspark.sql.functions import col

# Assuming df is your Spark DataFrame
columns_to_drop = ['id', 'Unnamed: 32']

# Dropping columns
df = df.select([col(column) for column in df.columns if column not in columns_to_drop])











from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
# Define the Random Forest model
rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=10)
rf

# Train the model
model = rf.fit(train_df)

# Make predictions on the test data
predictions = model.transform(test_df)

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

print(f"Test Accuracy: {accuracy:.2f}")
# Assuming 'model' is your trained model and 'train_data' is your training dataset

# Make predictions on training data
train_predictions = model.transform(train_df)

# Define MulticlassClassificationEvaluator for training data
train_evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")

# Calculate training accuracy
train_accuracy = train_evaluator.evaluate(train_predictions)

# Print training accuracy
print(f"Training Accuracy: {train_accuracy:.2f}")



from pyspark.ml.classification import GBTClassifier
#gbt = GBTClassifier(maxIter=10, maxDepth=2, labelCol="label", featuresCol="features",seed=42)
gbt = GBTClassifier(labelCol="label", featuresCol="features",seed=42)
gbt
gbt_model = gbt.fit(train_df)
# Make predictions on the test set
predictions = gbt_model.transform(test_df)

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Split the data into training and test sets
train_df, test_df = df_transformed.randomSplit([0.8, 0.2], seed=123)

# Create a Logistic Regression base classifier
lr = LogisticRegression(regParam=0.01)

# Create an One-vs-Rest (OvR) classifier with the Logistic Regression base classifier
ovr = OneVsRest(classifier=lr)

# Fit the OvR model to the training data
ovr_model = ovr.fit(train_df)

# Make predictions on the test data
predictions = ovr_model.transform(test_df)

# Evaluate the model using accuracy
evaluator = MulticlassClassificationEvaluator(labelCol='label', predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

print("Accuracy on test data = %g" % accuracy)







from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql.functions import col, asc,desc
import matplotlib.pyplot as plt
import numpy as np

# Train the model
model = rf.fit(train_df)

# Make predictions on the test data
predictions = model.transform(test_df)

# We create two lists, (one for the true values and one for the predictions) just for a better display on the terminal
selection=predictions.select(F.col("label").cast("int"),F.col("prediction").cast("int"))
trueVal_list=list(selection.select("label").toPandas()["label"])
predictVal_list=list(selection.select("prediction").toPandas()["prediction"])
print("TRUE VALUES : ")
print(trueVal_list)
print("-------------------------------------------------------------------------------------------------------------------------------------------")
print("PREVISIONS : ")
print(predictVal_list)
print("-------------------------------------------------------------------------------------------------------------------------------------------")
print("")

#The sklearn library is used to produce the CONFUSION MATRIX and other metrics:
from sklearn.metrics import classification_report,confusion_matrix,roc_curve,auc
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator=MulticlassClassificationEvaluator(labelCol="label",predictionCol="prediction")
y_true=predictions.select(["label"]).collect()
y_predicted=predictions.select(["prediction"]).collect()

#Creation of the ROC-AUC CURVE graph
#Calculation of the values fpr, tpr, thresholds and roc_auc useful for the construction of the curve:
fpr, tpr, thresholds = roc_curve(y_true, y_predicted)
roc_auc = auc(fpr, tpr)

# ROC curve plot:
plt.plot(fpr, tpr, label='AUC = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'r--')  # random predictions curve
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate (Specifity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

#Other calculated metrics (accuracy, precision, f1 score and recall):
print(classification_report(y_true,y_predicted))
accuracy=evaluator.evaluate(predictions,{evaluator.metricName:"accuracy"})
precision=evaluator.evaluate(predictions,{evaluator.metricName:"precisionByLabel"})
f1_score=evaluator.evaluate(predictions,{evaluator.metricName:"f1"})
recall=evaluator.evaluate(predictions,{evaluator.metricName:"recallByLabel"})
print("Accuracy = %g " % accuracy)
print("Test error = %g " % (1.0-accuracy))
print("Precision = %g " % precision )
print("F1 score = %g " % f1_score)
print("Recall = %g " % recall)
print("-------------------------------------------------------------------------------------------------------------------------------------------")
print("")
print("")

# Assuming prediction is your DataFrame containing 'label' and 'prediction' columns
y_true = np.array(predictions.select("label").collect())
y_predicted = np.array(predictions.select("prediction").collect())

# Calculate confusion matrix
cm = confusion_matrix(y_true, y_predicted)

# Plot confusion matrix with labeled axes
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xlabel("Predicted labels")
plt.ylabel("True labels")

# Specify the class labels for x-axis and y-axis
class_labels = ["0", "1"]  # Assuming "0" represents one class and "1" represents the other
plt.xticks(np.arange(len(class_labels)), class_labels)
plt.yticks(np.arange(len(class_labels)), class_labels)

# Loop through data dimensions and create text annotations
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > cm.max() / 2 else "black")

plt.show()


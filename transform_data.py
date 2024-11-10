from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, year, lower

# Initialize Spark session
spark = SparkSession.builder.appName("SpotifyDataTransformation").getOrCreate()

# Load the CSV data
file_path = r"C:\temp\spotify_data.csv"  # Test with a simpler file path for permissions
df = spark.read.option("header", True).csv(file_path)

# Transformation 1: Extract the year from the "Release Date" column
df = df.withColumn("Year", year(col("Release Date")))

# Transformation 2: Split the 'Artists' column into multiple artist columns
df = df.withColumn("Artist_1", split(col("Artists"), ", ").getItem(0)) \
       .withColumn("Artist_2", split(col("Artists"), ", ").getItem(1)) \
       .withColumn("Artist_3", split(col("Artists"), ", ").getItem(2))

# Transformation 3: Convert text fields to lowercase for consistency
df = df.withColumn("Type", lower(col("Type"))) \
       .withColumn("Name", lower(col("Name"))) \
       .withColumn("Album", lower(col("Album"))) \
       .withColumn("Artist_1", lower(col("Artist_1"))) \
       .withColumn("Artist_2", lower(col("Artist_2"))) \
       .withColumn("Artist_3", lower(col("Artist_3")))

# Save the transformed data to a new CSV file
output_path = r"C:\temp\spotify_data_transformed"  # Output path to a simpler directory
df.write.mode("overwrite").option("header", True).csv(output_path)

# Stop the Spark session
spark.stop()

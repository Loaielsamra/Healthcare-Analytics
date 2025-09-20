from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, sum, lower, trim, count, round
from pyspark.sql.functions import date_format, month, year, when, datediff

DATA_PATH = "data/raw/noshowappointments.csv"
SAVE_PATH = "data/clean/cleaned_appointments.parquet"
spark = SparkSession.builder.appName("NoShowAppointments").getOrCreate()

df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)

# Clean the 'No-show' column by converting 'Yes' and 'No' to 1 and 0
df = df.withColumn(
    "No-show",
    when(lower(col("No-show")) == "yes", 1)
    .when(lower(col("No-show")) == "no", 0)
    .otherwise(col("No-show").cast("double")),
)

df.printSchema()
df.show(5)

initial_row_count = df.count()
print(f"Initial row count: {initial_row_count}")

df = df.dropDuplicates()

df.select([sum(col(c).isNull().cast("int")).alias(c) for c in df.columns]).show()

df = df.dropna()

cleaned_row_count = df.count()
print(f"Cleaned row count: {cleaned_row_count}")

# Standardize string columns
string_cols = ["Neighbourhood"]

for c in string_cols:
    df = df.withColumn(c, lower(trim(col(c))))

# Convert date columns to proper date format
df = df.withColumn("Year", year(col("AppointmentDay")))
df = df.withColumn("Month", month(col("AppointmentDay")))
df = df.withColumn("DayOfWeek", date_format(col("AppointmentDay"), "EEEE"))

# Create new features
df = df.withColumn(
    "AgeGroup",
    when(col("Age") < 18, "Child")
    .when((col("Age") >= 18) & (col("Age") < 60), "Adult")
    .otherwise("Senior"),
)

df = df.withColumn(
    "LateScheduling",
    when(datediff(col("AppointmentDay"), col("ScheduledDay")) > 0, True).otherwise(
        False
    ),
)

# Save the cleaned data to parquet files partitioned by Year and Month
df.write.mode("overwrite").partitionBy("Year", "Month").parquet(SAVE_PATH)

# Get total number of no-shows and total appointments per age group
no_show_distribution = df.groupBy("AgeGroup").agg(
    sum(col("No-show")).alias("TotalNoShows"), count(lit(1)).alias("TotalAppointments")
)

# Calculate no-show rate and format output
no_show_distribution = no_show_distribution.withColumn(
    "NoShowRate", round(col("TotalNoShows") / col("TotalAppointments"), 4)
).orderBy("AgeGroup")

no_show_distribution.show()


# Generate QA Report Content
report_content = "# Data Quality Assurance Report\n\n"

# Row Count Comparison
report_content += "## Row Counts\n"
report_content += f"- Initial Rows: **{initial_row_count}**\n"
report_content += f"- Rows After Cleaning: **{cleaned_row_count}**\n"
report_content += f"- Rows Dropped: **{initial_row_count - cleaned_row_count}**\n\n"

# Null Counts per Column
report_content += "## Null Counts\n"
null_counts_df = df.select(
    [(sum(col(c).isNull().cast("int"))).alias(c) for c in df.columns]
)
null_counts_data = null_counts_df.collect()[0].asDict()

report_content += "```\n"
for column, count in null_counts_data.items():  # noqa: F402
    report_content += f"{column}: {count}\n"
report_content += "```\n\n"

# No-show Distribution by Age Group
report_content += "## No-show Distribution by Age Group\n"
no_show_data = no_show_distribution.orderBy("AgeGroup").collect()

report_content += "| Age Group | Total Appointments | Total No-Shows | No-Show Rate |\n"
report_content += "|---|---|---|---|\n"

for row in no_show_data:
    report_content += f"| {row['AgeGroup']} | {row['TotalAppointments']} | {row['TotalNoShows']} | {row['NoShowRate']} |\n"

# Save Report to Markdown File
file_path = "docs/qa_report.md"

with open(file_path, "w") as md_file:
    md_file.write(report_content)

print(f"QA report saved to {file_path}")

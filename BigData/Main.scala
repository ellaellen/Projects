package edu.gatech.cse6250.main

import java.text.SimpleDateFormat
import java.time.temporal.ChronoUnit

import edu.gatech.cse6250.helper.{ CSVHelper, SparkHelper }
import edu.gatech.cse6250.model.{ Diagnostic, Admissions, Mortality, Patients }
import org.apache.spark.mllib.feature.StandardScaler
import org.apache.spark.mllib.linalg.{ DenseMatrix, Matrices, Vector, Vectors }
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.sql._
import scala.io.Source

import java.io.File;

object Main {
  def main(args: Array[String]) {
    import org.apache.log4j.{ Level, Logger }

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val spark = SparkHelper.spark
    val sc = spark.sparkContext

    val data_train = "../data/mortality/train"
    val data_validation = "../data/mortality/validation"
    val data_test = "../data/mortality/test"

    println("Build feature id map")
    /** load training data to build code map */
    val (admission, mortality, diagnostic) = loadRddRawData(spark, data_train)

    /* convert diag code */
    val conv_diag = diagnostic.map { f =>
      if (f.code.startsWith("E"))
        (f.patientID, f.hadmID, f.code.substring(0, 4))
      else
        (f.patientID, f.hadmID, f.code.substring(0, 3))
    }
    val converted_diag = conv_diag.map(f => f._3)

    /* create feature map */
    val featureMap = converted_diag.distinct.collect.zipWithIndex.toMap
    /* save feature map for reference */
    val mapping = featureMap.toList.sortBy(_._2).map(pair => s"${pair._1}|${pair._2}").mkString("\n")
    scala.tools.nsc.io.File("mapping.txt").writeAll(mapping)

    val dir: File = new File("/scala")
    if (!dir.exists()) {
      dir.mkdir()
    }
    println("Construct train set")
    val (patient_ids_train, labels_train, seq_data_train) = createDatasets(data_train, featureMap)
    scala.tools.nsc.io.File("scala/mortality.ids.train").writeAll(patient_ids_train)
    scala.tools.nsc.io.File("scala/mortality.labels.train").writeAll(labels_train)
    scala.tools.nsc.io.File("scala/mortality.seqs.train").writeAll(seq_data_train.replace("List(", "[").replace(")", "]"))
    println("Construct test set")
    val (patient_ids_test, labels_test, seq_data_test) = createDatasets(data_test, featureMap)
    scala.tools.nsc.io.File("scala/mortality.ids.test").writeAll(patient_ids_test)
    scala.tools.nsc.io.File("scala/mortality.labels.test").writeAll(labels_test)
    scala.tools.nsc.io.File("scala/mortality.seqs.test").writeAll(seq_data_test.replace("List(", "[").replace(")", "]"))

    println("Construct validation set")
    val (patient_ids_valid, labels_valid, seq_data_valid) = createDatasets(data_validation, featureMap)
    scala.tools.nsc.io.File("scala/mortality.ids.validation").writeAll(patient_ids_valid)
    scala.tools.nsc.io.File("scala/mortality.labels.validation").writeAll(labels_valid)
    scala.tools.nsc.io.File("scala/mortality.seqs.validation").writeAll(seq_data_valid.replace("List(", "[").replace(")", "]"))
    println("Data processing completed!")

  }
  def createDatasets(path: String, featureMap: Map[String, Int]): (String, String, String) = {
    val spark = SparkHelper.spark
    val sc = spark.sparkContext
    val (admission, mortality, diagnostic) = loadRddRawData(spark, path)
    val conv_diag = diagnostic.map { f =>
      if (f.code.startsWith("E"))
        (f.patientID, f.hadmID, f.code.substring(0, 4))
      else
        (f.patientID, f.hadmID, f.code.substring(0, 3))
    }
    val jn_diag = conv_diag.map(f => (f._1, f))
    val jn_mort = mortality.map(f => (f.patientID, f))
    val jn_diag_mort = jn_diag.join(jn_mort).map(f => (f._2._1._1, f._2._1._2, f._2._1._3, f._2._2.mortality)).map(f => (f._2, f))
    val jn_adm = admission.map(f => (f.hadmID, f))
    val jn_diag_mort_adm = jn_diag_mort.join(jn_adm).map(f => (f._2._2.patientID, f._2._2.date, f._2._1._3, f._2._1._4))

    val bc_featuremap = sc.broadcast(featureMap)
    val map_diag_mort_adm = jn_diag_mort_adm.map {
      case (patientID, date, code, mortality) =>
        if (featureMap.contains(code))
          (patientID, date, bc_featuremap.value(code), mortality)
        else
          (patientID, date, "NOCODE", mortality)

    }.filter(f => (f._3 != "NOCODE"))

    val sorted_df = map_diag_mort_adm.sortBy(f => (f._1.toInt, f._2.toString)).map(f => ((f._1, f._4), f._2, f._3))
    val grpPatients = sorted_df.groupBy(f => f._1).sortBy(f => f._1._1.toInt).map(_._2)

    val patient_diagnoses = grpPatients.map { diagnoses =>
      val patients = diagnoses.map(_._1._1).take(1).head
      val labels = diagnoses.map(_._1._2).take(1).head
      val lst = diagnoses.groupBy(_._2).map {
        case (patientTuple, grdDiag) => grdDiag.map(f => f._3).toList
      }
      (patients, labels, lst.toList)
    }

    val patient_ids = patient_diagnoses.map(_._1).collect.toList.mkString("[", ",", "]")
    val labels = patient_diagnoses.map(_._2).collect.toList.mkString("[", ",", "]")
    val seq_data = patient_diagnoses.map(_._3).collect.toList.mkString("[", ",", "]")

    (patient_ids, labels, seq_data)

  }

  def loadRddRawData(spark: SparkSession, path: String): (RDD[Admissions], RDD[Mortality], RDD[Diagnostic]) = {
    /* the sql queries in spark required to import sparkSession.implicits._ */
    import spark.implicits._
    val sqlContext = spark.sqlContext

    val admission_file = new File(path, "ADMISSIONS.csv").getPath
    val diag_file = new File(path, "DIAGNOSES_ICD.csv").getPath
    val mort_file = new File(path, "MORTALITY.csv").getPath

    val df_admissions = sqlContext.read
      .format("com.databricks.spark.csv")
      .option("header", "true")
      .option("mode", "DROPMALFORMED")
      .option("delimiter", ",")
      .load(admission_file)

    df_admissions.createOrReplaceTempView("admissions")

    val df_admit = spark.sql("SELECT CAST(SUBJECT_ID AS STRING) AS patientID, CAST (HADM_ID AS STRING) AS hadmID, to_date(ADMITTIME) AS date, to_date(DEATHTIME) AS deathDate FROM admissions")

    val df_diagnoses = sqlContext.read
      .format("com.databricks.spark.csv")
      .option("header", "true")
      .option("mode", "DROPMALFORMED")
      .option("delimiter", ",")
      .load(diag_file)

    df_diagnoses.createOrReplaceTempView("diagnoses")

    val df_diag = spark.sql("SELECT CAST(SUBJECT_ID AS STRING) AS patientID, CAST(HADM_ID AS STRING) AS hadmID, CAST(ICD9_CODE AS STRING) AS code  FROM diagnoses WHERE ICD9_CODE != ''")

    val df_patients = sqlContext.read
      .format("com.databricks.spark.csv")
      .option("header", "true")
      .option("mode", "DROPMALFORMED")
      .option("delimiter", ",")
      .load(mort_file)

    df_patients.createOrReplaceTempView("patients")

    val df_mort = spark.sql("SELECT CAST(SUBJECT_ID AS STRING) AS patientID, MORTALITY  AS mortality FROM patients")

    val adt = df_admit.as[Admissions]
    val admissions: RDD[Admissions] = adt.rdd
    val mort = df_mort.as[Mortality]
    val mortality: RDD[Mortality] = mort.rdd
    val diag = df_diag.as[Diagnostic]
    val diagnostic: RDD[Diagnostic] = diag.rdd
    (admissions, mortality, diagnostic)
  }

}

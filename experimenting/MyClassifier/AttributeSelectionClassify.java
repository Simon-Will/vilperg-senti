package MyClassifier;

import weka.core.Instances;

import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

import weka.classifiers.Classifier;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.trees.RandomTree;
import weka.classifiers.bayes.NaiveBayes;

import weka.classifiers.Evaluation;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.io.PrintWriter;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.HashMap;

public class AttributeSelectionClassify {

    public static void main(String[] args) {
        // Handle command line arguments.
        String trainArffFile = args[0];
        String outDirName = args[1];
        String classifier = "RandomForest";
        String testArffFile = null;
        if (args.length > 2) {
            classifier = args[2];
        }
        if (args.length > 3) {
            testArffFile=args[3];
        }

        // Get Instances from arff files
        Instances trainData = getInstances(trainArffFile);
        Instances testData =
            (testArffFile == null) ? null : getInstances(testArffFile);

        ClassifierType classifierType = null;
        try {
            classifierType = ClassifierType.valueOf(classifier);
        } catch (IllegalArgumentException e) {
            System.err.println("Classifier not supported: " + e.getMessage());
            System.exit(1);
        }

        // Output directory.
        File outDir = new File(outDirName);
        // Directory for generated arff files.
        File arffDir = new File(outDirName + "/arff_files/");
        // Directory for evaluation results.
        File resultsDir = new File(outDirName + "/results/");

        // Ensure that the directories exist.
        if (outDir.mkdirs()) {
            System.out.println("Created.");
        } else {
            System.out.println("Not created.");
        }
        arffDir.mkdirs();
        resultsDir.mkdirs();

        Map<String, Instances> trainDataMap = generateAllInstances(trainData, arffDir, "train");
        Map<String, Instances> testDataMap = null;
        if (testData != null) {
            testDataMap = generateAllInstances(testData, arffDir, "test");
        }

        // Train and evaluate models.
        for (String key : trainDataMap.keySet()) {
            Evaluation eval = null;
            if (testDataMap != null && testDataMap.containsKey(key)) {
                eval = trainAndEvaluate(
                        trainDataMap.get(key),
                        testDataMap.get(key),
                        classifierType
                        );
            } else {
                eval = trainAndEvaluate(
                        trainDataMap.get(key),
                        null,
                        classifierType
                        );
            }

            // Generate a string describing the evaluation that will be
            // written to a file.
            StringBuilder outString = new StringBuilder();
            try {
                outString.append("\nSummaryString\n=============\n");
                outString.append(eval.toSummaryString(true));
                outString.append("\nMatrixString\n============\n");
                outString.append(eval.toMatrixString());
                outString.append("\nClassDetailsString\n==================\n");
                outString.append(eval.toClassDetailsString());
                outString.append("\nCumulativeMarginDistributionString\n");
                outString.append("==================================\n");
                outString.append(eval.toCumulativeMarginDistributionString());
            } catch (Exception e) {
                System.err.println(e.getMessage());
            }

            PrintWriter writer = null;
            try {
                writer = new PrintWriter(resultsDir + "/eval_results_" + key);
                writer.println(outString.toString());
            } catch (FileNotFoundException e) {
                System.err.println("Cannot write on file: " + e.getMessage());
            } finally {
                if (writer != null) {
                    writer.close();
                }
            }
        }

        // Train model and evaluate it.
        //Evaluation eval = trainAndEvaluate(
        //        trainData, testData, classifierType);
        //String summary = eval.toSummaryString("\nResults\n======\n", false);
        //System.out.println(summary);

    }

    /**
     * Generate all possible permutations of the instances of one arff file.
     * @param original The instances of the original arff file.
     * @param outDir The directory the generated arff files are written to.
     * @param prefix A prefix that is prepended to the names of the resulting
     * arff files.
     * @return A Map mapping the indices to the generated Instances objects.
     */
    public static Map<String, Instances> generateAllInstances(
            Instances original, File outDir, String prefix) {

        // Create a set containing the indices of all non-class attributes.
        // The class attribute is excluded by not including the last index.
        Set<Integer> indicesSet = new HashSet<>();
        int highestIndex = original.numAttributes();
        for (int i = 1; i < highestIndex; ++i) {
            indicesSet.add(i);
        }
        // Get all possible permutations of the indices by calculating the
        // powerset.
        Set<Set<Integer>> indicesPowerSet = powerSet(indicesSet);

        Map<String, Instances> allInstances = new HashMap<>();
        for (Set<Integer> set : indicesPowerSet) {
            StringBuilder outFileName = new StringBuilder(prefix);
            StringBuilder indices = new StringBuilder();
            for (int i : set) {
                outFileName.append("-").append(original.attribute(i-1).name());
                indices.append(i).append(",");
            }
            indices.append(highestIndex);
            String indicesString = indices.toString();
            String completeOutFile = outDir + "/" + outFileName.toString();
            allInstances.put(
                    indicesString,
                    filterInstances(original, indicesString, completeOutFile)
                    );
        }

        return allInstances;
    }

    /**
     * Return the powerset of a set.
     * @param originalSet The original set.
     * @return The powerset of the original set.
     *
     * Code taken from Joao Silva's Stackoverflow answer:
     * http://stackoverflow.com/questions/1670862/obtaining-a-powerset-of-a-set-in-java
     */
    public static <T> Set<Set<T>> powerSet(Set<T> originalSet) {
        Set<Set<T>> sets = new HashSet<Set<T>>();
        if (originalSet.isEmpty()) {
            sets.add(new HashSet<T>());
            return sets;
        }
        List<T> list = new ArrayList<T>(originalSet);
        T head = list.get(0);
        Set<T> rest = new HashSet<T>(list.subList(1, list.size())); 
        for (Set<T> set : powerSet(rest)) {
            Set<T> newSet = new HashSet<T>();
            newSet.add(head);
            newSet.addAll(set);
            sets.add(newSet);
            sets.add(set);
        }           
        return sets;
    }

    /**
     * Copy some attributes to a new Instances object and write it to a file.
     * @param original The instances that are to be filtered.
     * @param indices The indices of the attributes that should appear in the
     * filtered instances.
     * @param outFile The file the Instances are written to.
     * @return The filtered instances.
     */
    public static Instances filterInstances(
            Instances original, String indices, String outFile) {

        Remove removeFilter = null;
        Instances filtered = null;
        // Filter original instances
        try {
            String[] options = new String[3];
            options[0] = "-R";
            options[1] = indices;
            options[2] = "-V";
            System.out.println(indices);
            removeFilter = new Remove();
            removeFilter.setOptions(options);
            removeFilter.setInputFormat(original);
            filtered = Filter.useFilter(original, removeFilter);
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }

        // Write filtered instances to a file.
        PrintWriter writer = null;
        try {
            writer = new PrintWriter(outFile);
            writer.println(filtered.toString());
        } catch (FileNotFoundException e) {
            System.err.println("Cannot write on file: " + e.getMessage());
        } finally {
            if (writer != null) {
                writer.close();
            }
        }
        return filtered;
    }

    /**
     * Train a classifier and evaluate it.
     * @param trainData The data used for training.
     * @param testData The data used for evaluating. If null, cross validation
     * is used.
     * @param classifierType The type of classifier that is to be trained.
     * @return The resulting Evaluation object.
     */
    public static Evaluation trainAndEvaluate(
            Instances trainData,
            Instances testData,
            ClassifierType classifierType) {

        Classifier cls = trainClassifier(trainData, classifierType);

        Evaluation eval = null;
        if (testData != null) {
            eval = evaluateClassifier(cls, trainData, testData);
        } else {
            eval = crossEvaluateClassifier(cls, trainData);
        }
        return eval;
    }

    /**
     * Evaluate a J48 decision tree model using cross evaluation.
     * @param tree The J48 decision tree model that is to be evaluated.
     * @param data The data on which the evaluation is to be performed.
     * @return The resulting Evaluation object.
     */
    private static Evaluation crossEvaluateClassifier(
            Classifier cls, Instances data) {

        Evaluation eval = null;
        try {
            eval = new Evaluation(data);
            eval.crossValidateModel(cls, data, 10, new Random(1));
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return eval;
    }

    /**
     * Evaluate a trained classifier on test data.
     * @param cls The trained classifier that is to be evaluated.
     * @param trainData The data that was used for training the classifier.
     * @param testData The data against which the classifier is to be evaluated.
     * @return The resulting Evaluation object.
     */
    private static Evaluation evaluateClassifier(
            Classifier cls, Instances trainData, Instances testData) {

        Evaluation eval = null;
        try {
            eval = new Evaluation(trainData);
            eval.evaluateModel(cls, testData);
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return eval;
    }

    /**
     * Train a classifier the type of which is defined by the second argument.
     * @param trainData The training data.
     * @param classifierType The type of the classifier that is to be used.
     * @return A trained classfier.
     */
    private static Classifier trainClassifier(
            Instances trainData, ClassifierType classifierType) {

        Classifier cls = null;
        switch (classifierType) {
            case J48:
                try {
                    String[] options = new String[1];
                    // Use an unpruned tree.
                    options[0] = "-U";
                    cls = new J48();
                    cls.setOptions(options);
                    cls.buildClassifier(trainData);
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                }
                break;

            case RandomForest:
                try {
                    String[] options = new String[8];
                    // These are the options the GUI version sets by default.
                    options[0] = "-K";
                    options[1] = "0";
                    options[2] = "-I";
                    options[3] = "10";
                    options[4] = "-S";
                    options[5] = "1";
                    // Set depth to 50.
                    // With the default depth of 0, a StackOverflowError occurs.
                    options[6] = "-depth";
                    options[7] = "200";
                    cls = new RandomForest();
                    cls.setOptions(options);
                    cls.buildClassifier(trainData);
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                }
                break;

            case RandomTree:
                try {
                    String[] options = new String[8];
                    // These are the options the GUI version sets by default.
                    options[0] = "-K";
                    options[1] = "0";
                    options[2] = "-M";
                    options[3] = "1.0";
                    options[4] = "-S";
                    options[5] = "1";
                    // Set depth to 50.
                    // With the default depth of 0, a StackOverflowError occurs.
                    options[6] = "-depth";
                    options[7] = "200";
                    cls = new RandomTree();
                    cls.setOptions(options);
                    cls.buildClassifier(trainData);
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                }
                break;

            case NaiveBayes:
                try {
                    cls = new NaiveBayes();
                    cls.buildClassifier(trainData);
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                }
                break;
        }
        return cls;
    }

    /**
     * Train a J48 decision tree classifier.
     * @param Instances The training data.
     * @return A trained J48 decision tree model.
     */
    private static J48 trainTree(Instances trainData) {

        J48 tree = null;
        try {
            String[] options = new String[1];
            // Use an unpruned tree.
            options[0] = "-U";
            tree = new J48();
            tree.setOptions(options);
            tree.buildClassifier(trainData);
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return tree;
    }

    /**
     * Read Instances from an arff file.
     * @param path The path to the arff file.
     * @return An Instances object containing the instances.
     */
    private static Instances getInstances(String path) {

        BufferedReader reader = null;
        Instances data = null;
        try {
            reader = new BufferedReader(new FileReader(path));
            data = new Instances(reader);
        } catch (IOException e) {
            System.err.println("IOException: " + e.getMessage());
            System.exit(1);
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    System.err.println("IOException: " + e.getMessage());
                    System.exit(1);
                }
            }
        }

        // Choose last column as the classes.
        data.setClassIndex(data.numAttributes() - 1);
        return data;
    }
}

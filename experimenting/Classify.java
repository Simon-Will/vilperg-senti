import weka.core.Instances;
import weka.classifiers.trees.J48;
import weka.classifiers.Evaluation;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Random;

public class Classify {

    /**
     * Classify the instances in the arff file.
     * @param args The command line arguments as an array.
     */
    public static void main(String[] args) {

        Instances trainData = null;
        Instances testData = null;
        try {
            trainData = getInstances(args[0]);
            if (args.length > 1) {
                testData = getInstances(args[1]);
            }
        } catch (IOException e) {
            System.err.println("IOException:" + e.getMessage());
            System.exit(1);
        }

        J48 tree = trainTree(trainData);

        Evaluation eval = null;
        if (args.length > 1) {
            eval = evaluateTree(tree, trainData, testData);
        } else {
            eval = crossEvaluateTree(tree, trainData);
        }

        String summary = eval.toSummaryString("\nResults\n======\n", false);
        System.out.println(summary);
    }

    /**
     * Evaluate a J48 decision tree model using cross evaluation.
     * @param tree The J48 decision tree model that is to be evaluated.
     * @param data The data on which the evaluation is to be performed.
     * @return The resulting Evaluation object.
     */
    private static Evaluation crossEvaluateTree(J48 tree, Instances data) {

        Evaluation eval = null;
        try {
            eval = new Evaluation(data);
            eval.crossValidateModel(tree, data, 10, new Random(1));
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return eval;
    }

    private static Evaluation evaluateTree(
            J48 tree, Instances trainData, Instances testData) {

        Evaluation eval = null;
        try {
            eval = new Evaluation(trainData);
            eval.evaluateModel(tree, testData);
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return eval;
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
     * @throws IOException
     */
    private static Instances getInstances(String path) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader(path));
        Instances data = new Instances(reader);
        reader.close();
        // Choose last column as the classes.
        data.setClassIndex(data.numAttributes() - 1);
        return data;
    }
}

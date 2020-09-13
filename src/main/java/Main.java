import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.Collection;

public class Main {
    public static void main(String[] args) {
        long startTime = Instant.now().toEpochMilli();

        // Parsing the options
        OptionsParser.ParseOptions(args);

        try {
            // Parsing the initial configuration
            ConfigurationParser.ParseConfiguration(OptionsParser.staticFile, OptionsParser.dynamicFile);
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
            System.exit(1);
        }

        // Creating the brownian motion instance
        BrownianMotion bm = new BrownianMotion(ConfigurationParser.areaLength, ConfigurationParser.particles);

        // Variable for output particles
        Collection<Particle> stepOutput;

        // Variables for the iteration
        double limitTime = OptionsParser.maxTime;
        double currentTime = 0;
        boolean mainHitWall = false;

        // Simulating multiple steps
        while (currentTime < limitTime && !mainHitWall){
            // Step simulation
            stepOutput = bm.simulateUntilCollision();

            // Updating the variables for conditions
            currentTime = bm.getElapsedTime();
            mainHitWall = bm.mainHasHitWall();

            // Write the output
            GenerateOutputFile(stepOutput, currentTime);
        }

        long endTime = Instant.now().toEpochMilli();

        long total = endTime - startTime;

        if (mainHitWall){
            System.out.format("Total Time %d millis - Main particle wall collision\n", total);
        } else {
            System.out.format("Total Time %d millis - Time limit of %d reached\n", total, limitTime);
        }

        //AddToEvolutionStatisticsFile(ConfigurationParser.is2D, ConfigurationParser.livingLimitedPercentage, OptionsParser.ruleSet, livingVsTime, LIVING_PERCENT_FILE);
        //AddToEvolutionStatisticsFile(ConfigurationParser.is2D, ConfigurationParser.livingLimitedPercentage, OptionsParser.ruleSet, radiusVsTime, RADIUS_FILE);
    }

    private static void GenerateOutputFile(Collection<Particle> particles, double time) {
        try {
            BufferedWriter bf = new BufferedWriter(new FileWriter(OptionsParser.dynamicFile, true));
            bf.append(String.format("%f\n", time));

            // Creating the output for the file
            particles.forEach(p -> {
                try {
                    bf.append(String.format("%f %f %f %f\n", p.getX(), p.getY(), p.getVx(), p.getVy()));
                } catch (IOException e) {
                    System.out.println("Error writing to the output file");
                }
            });

            bf.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
        } catch (IOException e) {
            System.out.println("Error writing to the output file");
        }
    }

    /**
     * Generates the evolution vs time statistics file
     *
     * @param evolution Data of living cell % or maximum displacement based on time
     */
   /* private static void AddToEvolutionStatisticsFile(boolean is2D, double initialPercentage, RuleSet rule, List<Double> evolution, String file) {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%d %.3f %d", is2D ? 2 : 3, initialPercentage, rule.getRuleId()));
        for (Double aDouble : evolution) {
            sb.append(String.format(" %.3f", aDouble));
        }
        sb.append("\n");
        try {
            Files.write(Paths.get(file), sb.toString().getBytes(), StandardOpenOption.APPEND);
        } catch (FileNotFoundException e) {
            System.out.println(file + " not found");
        } catch (IOException e) {
            System.out.println("Error writing to the statistics file: " + file);
        }
    }*/
}


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
            System.out.format("Total Time %d millis - Main particle wall collision in %f seconds\n", total, currentTime);
        } else {
            System.out.format("Total Time %d millis - Time limit of %f reached\n", total, limitTime);
        }
    }

    private static void GenerateOutputFile(Collection<Particle> particles, double time) {
        try {
            BufferedWriter bf = new BufferedWriter(new FileWriter(OptionsParser.dynamicFile, true));
            bf.append(String.format("%f\n", time));

            // Creating the output for the file
            particles.forEach(p -> {
                String line = p.getX() + " " + p.getY() + " " + p.getVx() + " " + p.getVy() + "\n";
                try {
                    bf.append(line);
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
}


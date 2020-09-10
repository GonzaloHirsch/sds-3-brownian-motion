import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

// TODO: HACER ESTO
public class ConfigurationParser {
    public static double areaLength;
    public static Map<Integer, Particle> particles = new HashMap<>();

    /**
     * Parses the files given with the static and dynamic information in order to configure the initial state of GOL
     *
     * @param staticFileName  File path for the static file
     * @param dynamicFileName File path for the dynamic file
     */
    public static void ParseConfiguration(String staticFileName, String dynamicFileName) throws FileNotFoundException {
        ParseStaticData(staticFileName);
        ParseDynamicData(dynamicFileName);
    }

    private static void ParseStaticData(String staticFileName) throws FileNotFoundException {
        File file = new File(staticFileName);
        Scanner sc = new Scanner(file);

        // Parsing the area length
        areaLength = sc.nextDouble();

        int particleCount = 0;

        while (sc.hasNext()){
            // Extracting data
            double mass = sc.nextDouble();
            double radius = sc.nextDouble();

            // Generating the particle and adding it
            Particle p = new Particle(particleCount, radius, mass);
            particles.put(particleCount, p);

            particleCount++;
        }
    }

    private static void ParseDynamicData(String dynamicFileName) throws FileNotFoundException {
        File file = new File(dynamicFileName);
        Scanner sc = new Scanner(file);

        // Skipping the time of the file which is 0
        sc.nextDouble();

        int particleCount = 0;

        while (sc.hasNext()){
            // Extracting data
            double x = sc.nextDouble();
            double y = sc.nextDouble();
            double vx = sc.nextDouble();
            double vy = sc.nextDouble();

            // Adding the positions and velocity to the particle
            Particle p = particles.get(particleCount);
            p.setX(x);
            p.setY(y);
            p.setVx(vx);
            p.setVy(vy);
            particles.put(particleCount, p);

            particleCount++;
        }
    }
}

import org.apache.commons.cli.*;

// TODO: HACER ESTO Y DEFINIR OPCIONES
public class OptionsParser {
    protected static Integer timeInterval = 100;
    protected static String staticFile;
    protected static String dynamicFile;

    private static final String PARAM_T = "t";
    private static final String PARAM_R = "r";
    private static final String PARAM_H = "h";
    private static final String PARAM_SF = "sf";
    private static final String PARAM_DF = "df";

    /**
     * Generates the options for the help.
     *
     * @return Options object with the options
     */
    private static Options GenerateOptions() {
        Options options = new Options();
        options.addOption(PARAM_H, "help", false, "Shows the system help.");
        options.addOption(PARAM_T, "time_iteration", true, "Amount of iterations (or time) to run the Game Of Life for.");
        options.addOption(PARAM_R, "rule_set", true, "Id of the rule set to apply to the Game Of Life");
        options.addOption(PARAM_SF, "static_file", true, "Path to the file with the static values.");
        options.addOption(PARAM_DF, "dynamic_file", true, "Path to the file with the dynamic values.");
        return options;
    }

    /**
     * Public
     *
     * @param args
     */
    public static void ParseOptions(String[] args) {
        // Generating the options
        Options options = GenerateOptions();

        // Creating the parser
        CommandLineParser parser = new DefaultParser();

        try {
            // Parsing the options
            CommandLine cmd = parser.parse(options, args);

            // Parsing the help
            if (cmd.hasOption(PARAM_H)){
                help(options);
            }

            // Checking if the time amount is present
            if (!cmd.hasOption(PARAM_T)){
                System.out.println("A time frame amount must be specified");
                System.exit(1);
            }
            // Retrieving the amount of "time" to iterate with
            timeInterval = Integer.parseInt(cmd.getOptionValue(PARAM_T));

            // Checking if the files were present
            if (!cmd.hasOption(PARAM_SF) | !cmd.hasOption(PARAM_DF)){
                System.out.println("The dynamic and static file path are needed");
                System.exit(1);
            }

            // Parsing the file paths
            staticFile = cmd.getOptionValue(PARAM_SF);
            dynamicFile = cmd.getOptionValue(PARAM_DF);

        } catch (ParseException e) {
            System.out.println("Unknown command used");

            // Display the help again
            help(options);
        }
    }

    /**
     * Prints the help for the system to the standard output, given the options
     *
     * @param options Options to be printed as help
     */
    private static void help(Options options) {
        HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp("Main", options);
        System.exit(0);
    }
}

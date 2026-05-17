//Parabi Uddin
public class Stats{
    private static int nbMorts = 0;
    private static int nbReproductions = 0;

    public static void incrementerMorts(int n) {
        nbMorts += n;
    }

    public static void incrementerReproductions() {
        nbReproductions++;
    }

    public static void afficher() {
        System.out.println("Stats : morts = " + nbMorts + "\n" +"reproductions = " + nbReproductions);
    }


}

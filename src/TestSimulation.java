//Parabi Uddin
public class TestSimulation {
    public static void main(String[] args) {

        // Simulation 1 : peu d'agents sur un terrain petit
        System.out.println("########## SIMULATION 1 ##########");
        Simulation sim1 = new Simulation(5, 5, 8, 3, 2, 2, 1, 1, 0, 7);
        sim1.lancer();

        // Simulation 2 : beaucoup d'herbivores et peu de predateurs
        System.out.println("########## SIMULATION 2 ##########");
        Simulation sim2 = new Simulation(8, 8, 15, 5, 5, 4, 1, 1, 0, 6);
        sim2.lancer();

        // Simulation 3 : beaucoup de predateurs et peu d'herbivores
        System.out.println("########## SIMULATION 3 ##########");
        Simulation sim3 = new Simulation(8, 8, 10, 2, 2, 2, 3, 3, 1, 8);
        sim3.lancer();
    }
}
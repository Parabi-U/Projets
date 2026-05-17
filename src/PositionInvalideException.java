//Parabi Uddin
public class PositionInvalideException extends Exception {
    
    public PositionInvalideException(int l, int c) {
        super("Position invalide : (" + l + "," + c + ")");
    }
}
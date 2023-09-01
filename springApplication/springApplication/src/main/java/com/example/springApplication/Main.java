package com.example.springApplication;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        boolean initRequested = false;
        Scanner scanner = new Scanner(System.in);

        while (!initRequested) {
            System.out.println("Haben Sie die Application.properties-Datei nach ihren Wünschen eingestellt und möchten Sie die Anwendung initialisieren? (ja/nein)");
            String userInput = scanner.nextLine();

            if ("ja".equalsIgnoreCase(userInput)) {
                initRequested = true;
                Application app = new Application();
                app.init(args);
                scanner.close();
            } else if ("nein".equalsIgnoreCase(userInput)) {
                initRequested = true;
                scanner.close();
            } else {
                System.out.println("Ungültige Eingabe. Bitte 'ja' oder 'nein' eingeben.");
            }
        }

    }
}

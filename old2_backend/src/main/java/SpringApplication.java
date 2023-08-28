import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/*
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import java.util.Scanner;
*/

@SpringBootApplication
@RestController
public class SpringApplication {

	public static void main(String[] args) {

		//original
		org.springframework.boot.SpringApplication.run(SpringApplication.class, args);





		/* //VERSUCH MIT INIT METHODE:
		boolean initRequested = false;
		Scanner scanner = new Scanner(System.in);

		while (!initRequested) {
			System.out.println("Haben Sie die Application.properties-Datei nach ihren Wünschen eingestellt und möchten Sie die Anwendung initialisieren? (ja/nein)");
			String userInput = scanner.nextLine();

			if ("ja".equalsIgnoreCase(userInput)) {
				initRequested = true;
				ConfigurableApplicationContext context = initApplication();
				SpringApplication.run(SpringApplication.class, args);
				scanner.close();
			} else if ("nein".equalsIgnoreCase(userInput)) {
				initRequested = true;
				scanner.close();
			} else {
				System.out.println("Ungültige Eingabe. Bitte 'ja' oder 'nein' eingeben.");
			}
		}
	}

	// Benutzerdefinierte Funktion zum Initialisieren der Anwendung
	private static ConfigurableApplicationContext initApplication() {
		// Hier können Sie den Datenbankzugriff initialisieren oder andere Initialisierungsaufgaben durchführen
		System.out.println("Anwendung wurde initialisiert.");
		return SpringApplication.run(SpringApplication.class);
	}
	*/


	}


}

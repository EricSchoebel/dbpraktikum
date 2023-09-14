package com.example.springApplication.api;

import com.example.springApplication.database.repositories.TestRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class checking_API_Services {

    @Autowired
    TestRepository testRepository;

    public String testDatabase() {
        int result = testRepository.testDatabaseConnection();
        if (result == 1) {
            System.out.println("Datenbankverbindung erfolgreich!");
            return "Datenbankverbindung erfolgreich!";
        } else {
            System.err.println("Fehler bei der Datenbankverbindung.");
            return "Fehler bei der Datenbankverbindung.";
        }
    }


}
package com.example.springApplication;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication

public class Application {

	public static void init(String[] args){
		SpringApplication.run(Application.class, args);
	}

}

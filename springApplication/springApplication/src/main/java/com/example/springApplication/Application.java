package com.example.springApplication;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


import org.springframework.context.annotation.ComponentScan;


@SpringBootApplication
// @ComponentScan(basePackages = {"com.example.springApplication", "com/example/springApplication/api", "com/example/springApplication/database","database.repositories"})
public class Application {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

}

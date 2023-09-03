package com.example.springApplication;

import com.example.springApplication.api.API_Controller;
import com.example.springApplication.api.API_Services;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication

public class Application {

	//@Autowired
	//API_Services api_services;

	public static void init(String[] args){
		SpringApplication.run(Application.class, args);
		//System.out.println(api_services.getCategoryTree());
	}

}

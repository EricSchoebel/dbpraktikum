package com.example.springApplication.api;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class checking {


    @Qualifier("checking_API_Services")
    @Autowired
    checking_API_Services api_services;



    @GetMapping("/hellotz")
    public String hello(@RequestParam(value = "digit", defaultValue = "0") String digit) {
        return String.format("%d", (15 + Integer.parseInt(digit)));
    }

    @GetMapping("/dbverbindungcheck")
    public String dbverbindungcheck() {
        return api_services.testDatabase();
    }


}

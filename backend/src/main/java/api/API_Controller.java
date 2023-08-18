package api;

import database.entities.*;
import database.repositories.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
//import org.springframework.web.bind.annotation.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@CrossOrigin
@RestController
public class API_Controller {

    @Qualifier("API_Services")
    @Autowired
    API_Services api_services;

    //nur Testzweck:
    @RequestMapping(value = "/get/TestProductInformationForID", method = RequestMethod.GET)
    public List<ProduktEntity> oldGetTestAllInformationForSpecificProduct(@RequestParam(value = "pid") String pid) {
        return api_services.oldGetTestProductInfoForID(pid);
    }


    @RequestMapping(value = "/get/getProduct", method = RequestMethod.GET)
    public List<Object[]> getProduct(@RequestParam(value = "pid") String pid) {
        return api_services.getProductInfoForID(pid);
    }

    @RequestMapping(value = "/get/getProducts", method = RequestMethod.GET)
    public List<ProduktEntity[]> getProducts(@RequestParam(value = "pattern") String pattern) {
        return api_services.getProductsForPattern(pattern);
    }



}

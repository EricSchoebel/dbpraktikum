package com.example.springApplication.api;

import com.example.springApplication.database.entities.*;
import com.example.springApplication.database.repositories.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;





//API mit geforderten Funktionen

@CrossOrigin
@RestController
public class API_Controller {

    @Qualifier("API_Services")
    @Autowired
    API_Services api_services;


    //nur Testzweck:
    //muss man das returnte noch jsonifyen?
    @RequestMapping(value = "/get/TestProductInformationForID", method = RequestMethod.GET)
    public List<ProduktEntity> oldGetTestAllInformationForSpecificProduct(@RequestParam(value = "pid") String pid) {
        return api_services.oldGetTestProductInfoForID(pid);
    }

    @RequestMapping(value = "/get/getProduct", method = RequestMethod.GET)
    public List<Object> getProduct(@RequestParam(value = "pid") String pid) {
        return api_services.getProductInfoForID(pid);
    }

    @RequestMapping(value = "/get/getProducts", method = RequestMethod.GET)
    public List<ProduktEntity> getProducts(@RequestParam(value = "pattern") String pattern) {
        return api_services.getProductsForPattern(pattern);
    }

    /*

    @RequestMapping(value = "/get/getProductsByCategoryPath", method = RequestMethod.GET)
    public List<ProduktEntity> getProductsByCategoryPath(@RequestParam(value = "path") String path) {
        return api_services.getProductsByCategoryPath(path); //jede einzelne ProduktEntity der Liste enthält jeweils pid und titel
    }

     */

    @RequestMapping(value = "/get/getTopProducts", method = RequestMethod.GET)
    public List<ProduktEntity> getTopProducts(@RequestParam(value = "k") int k) {
        return api_services.getTopProducts(k); //jede einzelne ProduktEntity der Liste enthält jeweils pid, titel und rating
    }

    @RequestMapping(value = "/get/getSimilarCheaperProduct", method = RequestMethod.GET)
    public List<String> getSimilarCheaperProduct(@RequestParam(value = "pid") String pid) {
        return api_services.getSimilarCheaperProduct(pid);
    }

    @RequestMapping(value = "/get/getReview", method = RequestMethod.GET)
    public List<KundenrezensionEntity> getReview(@RequestParam(value = "kundenid") String kundenid, @RequestParam(value = "pid") String pid) {
        return api_services.getReview(kundenid, pid);
    }

    @RequestMapping(value = "/get/getTrolls", method = RequestMethod.GET)
    public List<String> getTrolls(@RequestParam(value = "rating") Double rating) {
        return api_services.getTrolls(rating);
    }

    @RequestMapping(value = "/get/getOffers", method = RequestMethod.GET)
    public List<Object[]> getOffers(@RequestParam(value = "pid") String pid) {
        return api_services.getOffers(pid);
    }



}

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
    //nur Testzweck:
    @RequestMapping(value = "/get/getTestKunde", method = RequestMethod.GET)
    public Optional<KundeEntity> getTestKunde(@RequestParam(value = "kundenid") String kundenid) {
        return api_services.oldGetTestKunde(kundenid);
    }





    @RequestMapping(value = "/get/getProduct", method = RequestMethod.GET)
    public List<Object> getProduct(@RequestParam(value = "pid") String pid) {
        return api_services.getProductInfoForID(pid);
    }

    @RequestMapping(value = "/get/getProducts", method = RequestMethod.GET)
    public List<ProduktEntity> getProducts(@RequestParam(value = "pattern") String pattern) {
        return api_services.getProductsForPattern(pattern);
    }

    // /*

    @RequestMapping(value = "/get/getProductsByCategoryPath", method = RequestMethod.GET)
    public List<ProduktEntity> getProductsByCategoryPath(@RequestParam(value = "path") String path) {
        return api_services.getProductsByCategoryPath(path); //jede einzelne ProduktEntity der Liste enthält jeweils pid und titel
    }

    // */

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

    @PostMapping("/post/addNewReview")
    public ResponseEntity<String> addNewReview( //reviewdate wird automatisch auf jeweiliges Datum gesetzt
            @RequestParam(value ="kundenid") String kundenid,
            @RequestParam(value ="pid") String pid,
            @RequestParam(value = "punkte") int punkte,
            @RequestParam(value = "helpful", required = false)  Optional<Integer> helpful,
            @RequestParam(value = "summary", required = false) Optional<String> summary,
            @RequestParam(value = "content", required = false) Optional<String> content) {

        // Validiere die Daten, z.B. ob "punkte" zwischen 1 und 5 liegt
        if ( ( !(punkte==1) && !(punkte==2) && !(punkte==3) && !(punkte==4) && !(punkte==5) ) ) {
            return ResponseEntity.badRequest().body("Punktbewertung muss ganzzahlig im Bereich 1 bis 5 sein.");
        }

        if( 0 == api_services.addNewReview(kundenid, pid, punkte, helpful, summary, content) ) {
            return ResponseEntity.ok("Bewertung wurde erfolgreich hinzugefügt.");
        }
        else{
            return ResponseEntity.ok("Es ist ein Fehler aufgetreten. " +
                    "Mögliche Ursachen: ProduktID nicht gefunden, " +
                    "Unter dieser KundenID wurde für diese ProduktID schon eine Rezension angelegt," +
                    "Punktbewertung keine Ganzzahl von 1 bis 5, ...");
        }
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

package com.example.springApplication.api;

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

    @RequestMapping(value = "/finish", method = RequestMethod.GET)
    public String finish() {
        return api_services.finishApplication();
    }

    @RequestMapping(value = "/get/getProduct", method = RequestMethod.GET)
    public List<Object> getProduct(@RequestParam(value = "pid") String pid) {
        return api_services.getProductInfoForID(pid);
    }

    @RequestMapping(value = "/get/getProduct2", method = RequestMethod.GET)
    public String getProduct2(@RequestParam(value = "pid") String pid) {
        return api_services.getProductInfoForID2(pid);
    }

    @RequestMapping(value = "/get/getProducts", method = RequestMethod.GET)
    public List<String> getProducts(@RequestParam(value = "pattern") String pattern) {
        return api_services.getProductsForPattern(pattern);
    }

    @RequestMapping(value = "/get/getCategoryTree", method = RequestMethod.GET)
    public String getCategoryTree(){
        return api_services.getCategoryTree();
    }

    @RequestMapping(value = "/get/getProductsByCategoryPath", method = RequestMethod.GET)
    public List<String> getProductsByCategoryPath(@RequestParam(value = "path") String path) {
        return api_services.getProductsByCategoryPath(path); //jede einzelne ProduktEntity der Liste enthält jeweils pid und titel
    }

    @RequestMapping(value = "/get/getTopProducts", method = RequestMethod.GET)
    public List<String> getTopProducts(@RequestParam(value = "k") int k) {
        return api_services.getTopProducts(k); //jede einzelne ProduktEntity der Liste enthält jeweils pid, titel und rating
    }

    @RequestMapping(value = "/get/getSimilarCheaperProduct", method = RequestMethod.GET)
    public List<String> getSimilarCheaperProduct(@RequestParam(value = "pid") String pid) {
        return api_services.getSimilarCheaperProduct(pid);
    }

    @RequestMapping(value = "/get/getReview", method = RequestMethod.GET)
    public List<String> getReview(@RequestParam(value = "identifier") String identifier) {
        return api_services.getReview(identifier);
    }

    @RequestMapping(value= "/post/addNewReview", method = RequestMethod.POST)
    public ResponseEntity<String> addNewReview(@RequestBody ReviewRequest reviewRequest) {

        String kundenid = reviewRequest.getKundenid();
        String pid = reviewRequest.getPid();
        int punkte = reviewRequest.getPunkte();
        Optional<Integer> helpful = reviewRequest.getHelpful();
        Optional<String> summary = reviewRequest.getSummary();
        Optional<String> content = reviewRequest.getContent();
        //reviewdate wird automatisch auf jeweiliges Datum gesetzt

        // Validiere die Daten, z.B. ob "punkte" zwischen 1 und 5 liegt
        if ( ( !(punkte==1) && !(punkte==2) && !(punkte==3) && !(punkte==4) && !(punkte==5) ) ) {
            return ResponseEntity.badRequest().body("Punktbewertung muss ganzzahlig im Bereich 1 bis 5 sein.");
        }

        if( 0 == api_services.addNewReview(kundenid, pid, punkte, helpful, summary, content) ) {
            return ResponseEntity.ok("Bewertung wurde erfolgreich hinzugefügt.");
        }
        else{
            return ResponseEntity.ok("Es ist ein Fehler aufgetreten. " +
                 //alt:   "Mögliche Ursachen: ProduktID nicht gefunden, " +
                //alt:    "Unter dieser KundenID wurde für diese ProduktID schon eine Rezension angelegt," +
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

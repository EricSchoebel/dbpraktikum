package com.example.springApplication.api;


import com.example.springApplication.database.repositories.*;
import com.example.springApplication.database.entities.*;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class API_Services {

    @Autowired
    ProduktRepository produktRepository;
    @Autowired
    KategorieRepository kategorieRepository;
    @Autowired
    ProduktKategorieRepository produktKategorieRepository;
    @Autowired
    AngebotRepository angebotRepository;
    @Autowired
    KundenrezensionRepository kundenrezensionRepository;
    @Autowired
    AehnlichkeitRepository aehnlichkeitRepository;
    @Autowired
    KundeRepository kundeRepository;

    private final ApplicationContext context;

    @Autowired
    public API_Services(ApplicationContext context) {
        this.context = context;
    }

    public String finishApplication() {
        SpringApplication.exit(context, () -> 0);
        return "Die Anwendung wurde beendet. Bitte schließen Sie Ihren Browser.";
    }

    //nur Testzweck:
    public List<ProduktEntity> oldGetTestProductInfoForID(String pid) {
        List<ProduktEntity> resultList = produktRepository.findAllByPid(pid);
        return resultList;
    }
    //nur Testzweck:
    public Optional<KundeEntity> oldGetTestKunde(String kundenid) {
        Optional<KundeEntity>  test = kundeRepository.findByKundenid(kundenid);
        return test;
    }

    public List<Object> getProductInfoForID(String pid) {
        List<Object> resultList = produktRepository.getProduct(pid);
        return resultList;
    }

    public List<String> getProductsForPattern(String pattern) {

        List<String> resultList = produktRepository.getProducts(pattern);
        return resultList;
    }

    /*
    Idee: du kriegst mit Slashen separierten Pfad,
    aus dem musst du dann in der Kategorietabelle herausfinden was die korrekte unterste Kategorie ist
    (kannst nicht einfach das Pfad ende in der Kategorietabelle suchen, weil Kategorien mehrfach vorkommen können).
    Und dann aus dieser untersten Kategorie die Katid nehmen und in der produkt_kategorie-Tabelle danach suchen
    um alle pid (potenziell mehrere) rauszuziehen. dann kannst pid und produktitel aus der Produkt-Tabelle nehmen
     */
    public List<String> getProductsByCategoryPath(String path) {
        try {
            //übergebenen path in einzelteile aufteilen
            List<String> pathlist = new ArrayList<>(Arrays.asList(path.split("/")));

            String hauptkategoriename = pathlist.get(0);
            int initialkategorieId = kategorieRepository.getKatidHauptkategorieHilfs(hauptkategoriename); // = hauptkategorieKatid

            //obersten pathteil abgearbeitet
            if (!pathlist.isEmpty()) {
                pathlist.remove(0);
            }

            //die unterste katid finden
            for (String jetzigerKategorienname : pathlist) {
                initialkategorieId = kategorieRepository.getKatidViaLastkategorieIdHilfs(initialkategorieId, jetzigerKategorienname);
            }

            //zu der untersten katid alle zugehörigen productids (als Liste) finden
            List<String> hilfsliste = produktKategorieRepository.getPidsToSpecificKatIdHilfs(initialkategorieId);
            List<String> productIds = new ArrayList<>();
            for (String ent : hilfsliste) {
                productIds.add(ent);
            }

            //pid und titel zu den gefundenen productids ziehen
            List<String> resultList = produktRepository.getProductsByCategoryPathHilfsteil(productIds);
            return resultList;
        }
        catch (Exception e){
            List<String> exitList = new ArrayList<>();
            return exitList;
        }
    }

    public List<String> getTopProducts(int k) { //bei gleichem Rating nach Titel (aufsteigend) geordnet
        List<String> zwischenList = produktRepository.findByRatingIsNotNullOrderByRatingDescTitelAsc(k);
        zwischenList = zwischenList.subList(0, k);
        return zwischenList;
    }

    //Hilfsfkt.
    public List<String> findIntersection(String pid) { //intersection of similar and cheaper
        List<String> listSimilarA = aehnlichkeitRepository.getSimilarProductsForPid1Hilfs(pid);
        List<String> listSimilarB = aehnlichkeitRepository.getSimilarProductsForPid2Hilfs(pid);

        List<String> combinedList = new ArrayList<>(listSimilarA);
        combinedList.addAll(listSimilarB);
        Set<String> uniqueSet = new HashSet<>(combinedList);
        List<String> listSimilar = new ArrayList<>(uniqueSet);

        List<String> listCheaper = angebotRepository.getCheaperProductsForPidHilfs(pid);

        List<String> intersection = new ArrayList<>();
        for (String a : listSimilar) {
            for (String b : listCheaper) {
                if ( a.equals(b) ) {
                    intersection.add(a);
                    break;
                }
            }
        }
        return intersection;
    }

    public List<String> getSimilarCheaperProduct(String pid) {
        List<String> resultList = this.findIntersection(pid);
        return resultList;
    }

    public List<String> getReview(String identifier) {

        if (identifier.contains("/") && identifier.indexOf("/") == identifier.lastIndexOf("/")) {
            String[] parts = identifier.split("/");
            String kundenid = parts[0];
            String pid = parts[1];

            if (kundenid != null && pid.equals("*")) {
                List<String> resultList = kundenrezensionRepository.getReviewsSonderfall(kundenid);
                return resultList;
            } else if (pid != null && kundenid.equals("*")) {
                List<String> resultList = kundenrezensionRepository.getReviewsSonderfallZwei(kundenid);
                return resultList;
            } else {
                List<String> resultList = kundenrezensionRepository.getReview(kundenid, pid);
                return resultList;
            }
        }
        else {
            List<String> exitList = new ArrayList<>();
            return exitList;
        }
    }

    public int addNewReview(String kundenid, String pid, int punkte,
                            Optional<Integer> helpful, Optional<String> summary, Optional<String> content) {
        try {

            //musst ja erstmal checken obs die kundenid im kundentabelle gibt:
            //wenn ja, einfach review anlegen; wenn nein, dann erst kunden anlegen (sonst Primärschlüsselverletzung)
            Optional<KundeEntity> vorhandenerKunde = kundeRepository.findByKundenid(kundenid);

            if (!vorhandenerKunde.isPresent()){ //Fall, dass KundenID noch nicht in Kundentabelle
                KundeEntity neuerKunde = new KundeEntity();
                neuerKunde.setKundenid(kundenid);
                kundeRepository.save(neuerKunde);
            }

            KundenrezensionEntity review = new KundenrezensionEntity();
            review.setKundenid(kundenid);
            review.setPid(pid);
            review.setPunkte(punkte);

            helpful.ifPresent(review::setHelpful);
            summary.ifPresent(review::setSummary);
            content.ifPresent(review::setContent);

            java.util.Date utilDate = Calendar.getInstance().getTime();
            java.sql.Date sqlDate = new java.sql.Date(utilDate.getTime());
            review.setReviewdate(sqlDate);

            kundenrezensionRepository.save(review); // pid muss es geben
            return 0;
        }
        catch (Exception e)
        {
            return 1;
        }
    }

    public List<String> getTrolls(Double rating) {

        // liste = [ [kundenid1,durchschn.bewert.] , [kundenid2,durchschn.bewert.], ... ]
        List<Object[]> zwischenList = kundenrezensionRepository.findDurchschnittsbewertungen();

        //Objektentfernung deren Durchschnittsbewertung größerGleich spezifizierter Ratinggrenze
        zwischenList.removeIf(obj -> {
            Double durchschnittsbewertung = (Double) obj[1];
            return durchschnittsbewertung >= rating;
        });

        //übrig gebliebene kundenids in Liste packen
        List<String> kundenidList = new ArrayList<>();
        for (Object[] obj : zwischenList) {
            String kundenid = (String) obj[0];
            kundenidList.add(kundenid);
        }

        return kundenidList;

    }

    public List<Object[]> getOffers(String pid) {
        List<Object[]> resultList = angebotRepository.getOffers(pid);
        return resultList;
    }



}

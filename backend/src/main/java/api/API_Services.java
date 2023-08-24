package api;
import database.entities.*;
import database.repositories.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.io.IOException;
import java.time.Instant;
import java.util.*;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Service;

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

    //IDEE FINISH METHODE   ---------
    /*
    private final ApplicationContext context;

    @Autowired
    public API_Services(ApplicationContext context) {
        this.context = context;
    }

    public String finishApplication() {
        SpringApplication.exit(context, () -> 0);
        return "Die Anwendung wurde beendet. Bitte schließen Sie Ihren Browser.";
    }
    */
    //---------





    //nur Testzweck:
    public List<ProduktEntity> oldGetTestProductInfoForID(String pid) {
        List<ProduktEntity> resultList = produktRepository.findAllByPid(pid);
        return resultList;
    }


    public List<Object> getProductInfoForID(String pid) {
        List<Object> resultList = produktRepository.getProduct(pid);
        return resultList;
    }

    public List<ProduktEntity> getProductsForPattern(String pattern) {
        List<ProduktEntity> resultList = produktRepository.getProducts(pattern);
        return resultList;
    }





    /*
    Idee: du kriegst mit Backslashen separierten Pfad,
    aus dem musst du dann in der Kategorietabelle herausfinden was die korrekte unterste Kategorie ist
    (kannst nicht einfach das Pfad ende in der Kategorietabelle suchen, weil Kategorien mehrfach vorkommen können).
    Und dann aus dieser untersten Kategorie die Katid nehmen und in der produkt_kategorie-Tabelle danach suchen
    um alle pid (potenziell mehrere) rauszuziehen. dann kannst pid und produktitel aus der Produkt-Tabelle nehmen
     */
    public List<ProduktEntity> getProductsByCategoryPath(String path) {

        //übergebenen path in einzelteile aufteilen
        List<String> pathlist = new ArrayList<>(Arrays.asList(path.split("/")));

        String hauptkategoriename = pathlist.get(0);
        int initialkategorieId = kategorieRepository.getKatidHauptkategorieHilfs(hauptkategoriename).getKatid(); // = hauptkategorieKatid

        //obersten pathteil abgearbeitet
        if (!pathlist.isEmpty()) {
            pathlist.remove(0);
        }

        //die unterste katid finden
        for (String jetzigerKategorienname : pathlist){
            initialkategorieId = kategorieRepository.getKatidViaLastkategorieIdHilfs(initialkategorieId, jetzigerKategorienname).getKatid();
        }

        //zu der untersten katid alle zugehörigen productids (als Liste) finden
        List<ProduktKategorieEntity> hilfsliste = produktKategorieRepository.getPidsToSpecificKatIdHilfs(initialkategorieId);
        List<String> productIds = new ArrayList<>();
        for (ProduktKategorieEntity ent : hilfsliste){
            productIds.add(ent.getPid());
        }

        //pid und titel zu den gefundenen productids ziehen
        List<ProduktEntity> resultList = produktRepository.getProductsByCategoryPathHilfsteil(productIds);
        return resultList;
    }

    public List<ProduktEntity> getTopProducts(int k) {
        List<ProduktEntity> resultList = produktRepository.findTopKByRatingIsNotNullOrderByRatingDescTitelAsc(k);
        return resultList;
    }

    //Hilfsfkt.
    public List<ProduktEntity> findIntersection(String pid) { //intersection of similar and cheaper
        List<ProduktEntity> listSimilar = produktRepository.getSimilarProductsForPid1Hilfs(pid);
        List<ProduktEntity> listSimilar2 = produktRepository.getSimilarProductsForPid2Hilfs(pid);
        listSimilar.addAll(listSimilar2);

        List<ProduktEntity> listCheaper = produktRepository.getCheaperProductsForPidHilfs(pid);

        List<ProduktEntity> intersection = new ArrayList<>();
        for (ProduktEntity a : listSimilar) {
            for (ProduktEntity b : listCheaper) {
                if (a.getPid().equals(b.getPid())) {
                    intersection.add(a);
                    break;
                }
            }
        }
        return intersection;
    }

    public List<ProduktEntity> getSimilarCheaperProduct(String pid) {
        List<ProduktEntity> resultList = this.findIntersection(pid);
        return resultList;
    }

    public List<KundenrezensionEntity> getReview(String kundenid, String pid) {
        if (kundenid != null && pid.equals("*")) {
            List<KundenrezensionEntity> resultList = kundenrezensionRepository.getReviewsSonderfall(kundenid);
            return resultList;
        }
        else {
            List<KundenrezensionEntity> resultList = kundenrezensionRepository.getReview(kundenid, pid);
            return resultList;
        }
    }

    public int addNewReview(String kundenid, String pid, int punkte,
                         Optional<Integer> helpful, Optional<String> summary, Optional<String> content) {
        try {
            KundenrezensionEntity review = new KundenrezensionEntity();
            review.setKundenid(kundenid);
            review.setPid(pid);
            review.setPunkte(punkte);

            helpful.ifPresent(review::setHelpful);
            summary.ifPresent(review::setSummary);
            content.ifPresent(review::setContent);
            kundenrezensionRepository.save(review);
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

        //Objektentfernung deren Durchschnittsbewertung unter spezifizierter Ratinggrenze
        zwischenList.removeIf(obj -> {
            Double durchschnittsbewertung = (Double) obj[1];
            return durchschnittsbewertung < rating;
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

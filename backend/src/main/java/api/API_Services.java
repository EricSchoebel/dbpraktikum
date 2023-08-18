package api;


import database.entities.*;
import database.repositories.KategorieRepository;
import database.repositories.ProduktKategorieRepository;
import database.repositories.ProduktRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.Instant;
import java.util.*;

@Service
public class API_Services {

    @Autowired
    ProduktRepository produktRepository;
    @Autowired
    KategorieRepository kategorieRepository;
    @Autowired
    ProduktKategorieRepository produktKategorieRepository;

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


}

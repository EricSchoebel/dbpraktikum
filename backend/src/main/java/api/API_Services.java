package api;


import database.entities.*;
import database.repositories.KategorieRepository;
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

    //nur Testzweck:
    public List<ProduktEntity> oldGetTestProductInfoForID(String pid) {
        List<ProduktEntity> resultList = produktRepository.findAllByPid(pid);
        return resultList;
    }

    public List<Object[]> getProductInfoForID(String pid) {
        List<Object[]> resultList = produktRepository.getProduct(pid);
        return resultList;
    }

    public List<ProduktEntity[]> getProductsForPattern(String pattern) {
        List<ProduktEntity[]> resultList = produktRepository.getProducts(pattern);
        return resultList;
    }




    /*
    Idee: du kriegst mit Backslashen separierten Pfad,
    aus dem musst du dann in der Kategorietabelle herausfinden was die korrekte unterste Kategorie ist
    (kannst nicht einfach das Pfad ende in der Kategorietabelle suchen, weil Kategorien mehrfach vorkommen können).
    Und dann aus dieser untersten Kategorie die Katid nehmen und in der produkt_kategorie-Tabelle danach suchen
    um alle pid (potenziell mehrere) rauszuziehen. dann kannst pid und produktitel aus der Produkt-Tabelle nehmen
     */
    public List<ProduktEntity[]> getProductsByCategoryPath(String path) {

        //übergebenen path in einzelteile aufteilen
        List<String> pathlist = new ArrayList<>(Arrays.asList(path.split("/")));
        // quatsch: List<Integer> pathlistInKatids = new ArrayList<>();

        String hauptkategoriename = pathlist.get(0);
        Integer hauptkategorieKatid = kategorieRepository.getKatidHauptkategorieHilfs(hauptkategoriename).getKatid();

        // quatsch:for (String kategorienname : pathlist){ }

        //Zum Weitermachen:
        /*
        mit where oberkategorie = id von vorher
        und kategroeiname = jetziger pathTeil
         */




        //vielleicht besser ovn hinten durchgen (also von Unterkategorie bis hoch?)
        for (int i = 1; i < pathlist.size(); i++) {


            //System.out.println("Wert von i: " + i);
        }


        List<ProduktEntity[]> resultList = produktRepository.getProductsByCategoryPath(productIds);
        return resultList;
    }

}

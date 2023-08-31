package database.repositories;

//import database.entities.RechnerId;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import org.springframework.data.repository.query.Param;


import org.springframework.stereotype.Repository;


import java.util.List;

@Repository
public interface ProduktRepository extends JpaRepository<ProduktEntity, String>  { // zwei Argumente: <EntityKlasse, PrimaryKeyTyp>

      //nur zu Testzwecken:
      //  @Override
      //  List<ProduktEntity> findAllById(Iterable<String> strings);
      List<ProduktEntity> findAllByPid(String pid);
      // Äquivalent:
      //@Query("SELECT p FROM ProduktEntity p WHERE p.pid = :pid")
      //List<ProduktEntity> findProductsByPid(@Param("pid") String pid);

    @Query("SELECT p, b.seitenzahl, b.erscheinungsdatum, b.isbn, b.verlag "+
            "d.format, d.laufzeit, d.regioncode "+
            "c.label, c.erscheinungsdatum "+
            "FROM ProduktEntity p " +
            "LEFT JOIN BuchEntity b ON p.pid = b.pid " +
            "LEFT JOIN DvdEntity d ON p.pid = d.pid " +
            "LEFT JOIN CdEntity c ON p.pid = c.pid " +
            "WHERE p.pid = :productId")
    List<Object> getProduct(@Param("productId") String productId);

    @Query("SELECT p FROM ProduktEntity p WHERE :pattern IS NULL OR p.titel LIKE %:pattern%")
    List<ProduktEntity> getProducts(@Param("pattern") String pattern);


    /*
    Idee: du kriegst mit Backslashen separierten Pfad,
    aus dem musst du dann in der Kategorietabelle herausfinden was die korrekte unterste Kategorie ist
    (kannst nicht einfach das Pfad ende in der Kategorietabelle suchen, weil Kategorien mehrfach vorkommen können).
    Und dann aus dieser untersten Kategorie die Katid nehmen und in der produkt_kategorie-Tabelle danach suchen
    um alle pid (potenziell mehrere) rauszuziehen. dann kannst pid und produktitel aus der Produkt-Tabelle nehmen
     */
    @Query("SELECT p.pid, p.titel FROM ProduktEntity p WHERE p.pid IN :productIds")
    List<ProduktEntity> getProductsByCategoryPathHilfsteil(@Param("productIds") List<String> productIds);

    //hier das public mit hinschreiben, sonst denkt IDE, dass Methode nicht genutzt wird
    public List<ProduktEntity> findTopKByRatingIsNotNullOrderByRatingDescTitelAsc(int k); //fuer getTopProducts

    // ...
    @Query("SELECT DISTINCT p.pid2 "+
            "FROM ProduktEntity p " +
            "WHERE p.pid1 = :productId")
    List<ProduktEntity> getSimilarProductsForPid1Hilfs(@Param("productId") String productId);

    @Query("SELECT DISTINCT p.pid1 "+
            "FROM ProduktEntity p " +
            "WHERE p.pid2 = :productId")
    List<ProduktEntity> getSimilarProductsForPid2Hilfs(@Param("productId") String productId);

    @Query("SELECT DISTINCT a.pid FROM angebot a "+
            "WHERE a.preis IS NOT NULL AND a.preis < (SELECT b.preis FROM angebot b WHERE b.pid = :productId ")
    List<ProduktEntity> getCheaperProductsForPidHilfs(@Param("productId") String productId);




}
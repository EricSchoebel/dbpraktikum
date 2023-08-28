package com.example.springApplication.database.repositories;


//import database.entities.RechnerId;

import com.example.springApplication.database.entities.ProduktKategorieEntity;
import com.example.springApplication.database.entities.ProduktKategorieEntityPK;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProduktKategorieRepository extends JpaRepository<ProduktKategorieEntity, ProduktKategorieEntityPK>{

    /*
    @Query("SELECT pk.pid FROM ProduktKategorieEntity pk WHERE pk.katid = :untersteKatId")
    List<ProduktKategorieEntity> getPidsToSpecificKatIdHilfs(@Param("untersteKatId") int untersteKatId);
    */

    @Query("SELECT pk.pid FROM ProduktKategorieEntity pk WHERE pk.katid = :untersteKatId")
    List<ProduktKategorieEntity> getPidsToSpecificKatIdHilfs(@Param("untersteKatId") int untersteKatId);

}

package com.example.springApplication.database.repositories;

//import database.entities.RechnerId;

import com.example.springApplication.database.entities.AngebotEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AngebotRepository extends JpaRepository<AngebotEntity, Integer>  {

    @Query("SELECT DISTINCT a.pid FROM AngebotEntity a "+
            "WHERE a.preis IS NOT NULL AND a.preis < (SELECT b.preis FROM AngebotEntity b WHERE b.pid = :productId) ")
    List<String> getCheaperProductsForPidHilfs(@Param("productId") String productId);


}

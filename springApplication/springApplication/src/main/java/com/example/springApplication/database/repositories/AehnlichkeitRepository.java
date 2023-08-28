package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.AehnlichkeitEntity;
import com.example.springApplication.database.entities.AehnlichkeitEntityPK;
import com.example.springApplication.database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;


import java.util.List;

public interface AehnlichkeitRepository extends JpaRepository<AehnlichkeitEntity, AehnlichkeitEntityPK> {


    // ...
    @Query("SELECT DISTINCT p.pid2 "+
            "FROM AehnlichkeitEntity p " +
            "WHERE p.pid1 = :productId")
    List<String> getSimilarProductsForPid1Hilfs(@Param("productId") String productId);

    @Query("SELECT DISTINCT p.pid1 "+
            "FROM AehnlichkeitEntity p " +
            "WHERE p.pid2 = :productId")
    List<String> getSimilarProductsForPid2Hilfs(@Param("productId") String productId);


}

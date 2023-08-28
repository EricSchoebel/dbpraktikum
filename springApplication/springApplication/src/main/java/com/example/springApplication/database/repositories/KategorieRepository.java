package com.example.springApplication.database.repositories;

//import database.entities.RechnerId;

import com.example.springApplication.database.entities.KategorieEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface KategorieRepository extends JpaRepository<KategorieEntity, Integer>{

    @Query("SELECT k.katid FROM KategorieEntity k WHERE k.kategoriename = :kategoriename and k.oberkategorie IS NULL")
    Integer getKatidHauptkategorieHilfs(@Param("kategoriename") String kategoriename);

    @Query("SELECT k.katid FROM KategorieEntity k WHERE k.oberkategorie = :lastkategorieId and k.kategoriename = :jetzigerKategoriename")
    Integer getKatidViaLastkategorieIdHilfs(@Param("lastkategorieId") int lastkategorieId, @Param("jetzigerKategoriename") String jetzigerKategoriename);



}

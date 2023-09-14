package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.KategorieEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface KategorieRepository extends JpaRepository<KategorieEntity, Integer>{

    //gibt KatId zu gegebenem Namen zurück, wenn die gegebene Kategorie Hauptkategorie ist
    @Query("SELECT k.katid FROM KategorieEntity k WHERE k.kategoriename = :kategoriename and k.oberkategorie IS NULL")
    Integer getKatidHauptkategorieHilfs(@Param("kategoriename") String kategoriename);

    //2 Infos: Kategorienname, Oberkategoriennamen, Rueckgabe: KatId
    @Query("SELECT k.katid FROM KategorieEntity k WHERE k.oberkategorie = :lastkategorieId and k.kategoriename = :jetzigerKategoriename")
    Integer getKatidViaLastkategorieIdHilfs(@Param("lastkategorieId") int lastkategorieId, @Param("jetzigerKategoriename") String jetzigerKategoriename);

    @Query ("SELECT k FROM KategorieEntity k WHERE k.oberkategorie = :katId")
    List<KategorieEntity> getUnterkategorienByKategorienId(@Param ("katId") int katId);

    @Query ("SELECT k FROM KategorieEntity k WHERE k.oberkategorie IS NULL")
    List<KategorieEntity> getHauptkategorien();



}

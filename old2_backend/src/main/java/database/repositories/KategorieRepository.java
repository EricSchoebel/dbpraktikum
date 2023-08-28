package database.repositories;

//import database.entities.RechnerId;
import database.entities.KategorieEntity;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import org.springframework.data.repository.query.Param;


import org.springframework.stereotype.Repository;


import java.util.List;

@Repository
public interface KategorieRepository extends JpaRepository<KategorieEntity, Integer>{


    @Query("SELECT k.kid FROM KategorieEntity k WHERE k.kategoriename = :kategoriename and k.oberkategorie IS NULL")
    KategorieEntity getKatidHauptkategorieHilfs(@Param("kategoriename") String kategoriename);

    @Query("SELECT k.kid FROM KategorieEntity k WHERE k.oberkategorie = :lastkategorieId and k.kategoriename = :jetzigerKategoriename")
    KategorieEntity getKatidViaLastkategorieIdHilfs(@Param("lastkategorieId") int lastkategorieId, @Param("jetztigerKategoriename") String jetzigerKategoriename);


}

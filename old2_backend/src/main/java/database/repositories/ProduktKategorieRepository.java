package database.repositories;


//import database.entities.RechnerId;
import database.entities.KategorieEntity;
import database.entities.ProduktKategorieEntity;
import database.entities.ProduktKategorieEntityPK;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import org.springframework.data.repository.query.Param;


import org.springframework.stereotype.Repository;


import java.util.List;

@Repository
public interface ProduktKategorieRepository extends JpaRepository<ProduktKategorieEntity, ProduktKategorieEntityPK>{

    @Query("SELECT pk.pid FROM ProduktKategorieEntity pk WHERE pk.katid = :untersteKatId")
    List<ProduktKategorieEntity> getPidsToSpecificKatIdHilfs(@Param("untersteKatId") int untersteKatId);

}

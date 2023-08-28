package database.repositories;

//import database.entities.RechnerId;
import database.entities.KundeEntity;
import database.entities.KundenrezensionEntity;
import database.entities.KundenrezensionEntityPK;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import org.springframework.data.repository.query.Param;


import org.springframework.stereotype.Repository;


import java.util.List;
import java.util.Optional;

@Repository
public interface KundeRepository extends JpaRepository<KundeEntity, String>{

    Optional<KundeEntity> findByKundenid(String kundenid);

}

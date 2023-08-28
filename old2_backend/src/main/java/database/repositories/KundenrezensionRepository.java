package database.repositories;

//import database.entities.RechnerId;
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

@Repository
public interface KundenrezensionRepository extends JpaRepository<KundenrezensionEntity, KundenrezensionEntityPK> {

    @Query("SELECT kr FROM KundenrezensionEntity kr WHERE kr.kundenid = :kundenid AND kr.pid = :pid")
    List<KundenrezensionEntity> getReview(@Param("kundenid") String kundenid, @Param("pid") String pid);

    @Query("SELECT kr FROM KundenrezensionEntity kr WHERE kr.kundenid = :kundenid")
    List<KundenrezensionEntity> getReviewsSonderfall(@Param("kundenid") String kundenid);

    @Query("SELECT kr.kundenid, AVG(kr.punkte) AS durchschnittsbewertung FROM KundenrezensionEntity kr GROUP BY kr.kundenid")
    List<Object[]> findDurchschnittsbewertungen();


}


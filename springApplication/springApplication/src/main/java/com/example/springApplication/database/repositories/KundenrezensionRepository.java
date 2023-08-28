package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.KundenrezensionEntity;
import com.example.springApplication.database.entities.KundenrezensionEntityPK;
import org.springframework.data.jpa.repository.JpaRepository;
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


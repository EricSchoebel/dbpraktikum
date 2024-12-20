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

    @Query("SELECT kr.kundenid, kr.pid, kr.punkte, kr.helpful, kr.summary, kr.content, kr.reviewdate FROM KundenrezensionEntity kr WHERE kr.kundenid = :kundenid AND kr.pid = :pid")
    List<String> getReview(@Param("kundenid") String kundenid, @Param("pid") String pid);

    @Query("SELECT kr.kundenid, kr.pid, kr.punkte, kr.helpful, kr.summary, kr.content, kr.reviewdate FROM KundenrezensionEntity kr WHERE kr.kundenid = :kundenid")
    List<String> getReviewsSonderfall(@Param("kundenid") String kundenid);

    @Query("SELECT kr.kundenid, kr.pid, kr.punkte, kr.helpful, kr.summary, kr.content, kr.reviewdate FROM KundenrezensionEntity kr WHERE kr.pid = :pid")
    List<String> getReviewsSonderfallZwei(@Param("pid") String pid);

    @Query("SELECT kr.kundenid, AVG(kr.punkte) AS durchschnittsbewertung FROM KundenrezensionEntity kr GROUP BY kr.kundenid")
    List<Object[]> findDurchschnittsbewertungen();


}


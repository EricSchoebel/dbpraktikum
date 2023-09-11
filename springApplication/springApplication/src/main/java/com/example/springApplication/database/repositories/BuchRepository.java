package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.BuchEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface BuchRepository extends JpaRepository<BuchEntity, String> {

    @Query("SELECT b FROM BuchEntity b WHERE b.pid = :productId")
    BuchEntity getBuch(@Param("productId") String productId);

}

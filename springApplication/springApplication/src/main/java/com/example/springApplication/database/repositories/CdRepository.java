package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.BuchEntity;
import com.example.springApplication.database.entities.CdEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CdRepository extends JpaRepository<CdEntity, String> {
    @Query("SELECT c FROM CdEntity c WHERE c.pid = :productId")
    CdEntity getCd(@Param("productId") String productId);
}

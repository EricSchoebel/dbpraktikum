package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.DvdEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface DvdRepository extends JpaRepository<DvdEntity, String> {

    @Query("SELECT d FROM DvdEntity d WHERE d.pid = :productId")
    DvdEntity getDvd(@Param("productId") String productId);
}

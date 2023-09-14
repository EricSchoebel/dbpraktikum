package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface TestRepository extends JpaRepository<ProduktEntity, String> {

    @Query(value = "SELECT 1", nativeQuery = true)
    int testDatabaseConnection();
}

package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.CdEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CdRepository extends JpaRepository<CdEntity, String> {
}

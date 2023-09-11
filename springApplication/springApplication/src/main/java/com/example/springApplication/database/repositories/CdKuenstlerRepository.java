package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.CdKuenstlerEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CdKuenstlerRepository extends JpaRepository<CdKuenstlerEntity, String> {
}

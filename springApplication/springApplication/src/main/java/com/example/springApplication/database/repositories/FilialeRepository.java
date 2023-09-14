package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.FilialeEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FilialeRepository extends JpaRepository<FilialeEntity, String> {
}

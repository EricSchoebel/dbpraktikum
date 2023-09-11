package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.KaufEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface KontoRepository extends JpaRepository<KaufEntity, String> {
}
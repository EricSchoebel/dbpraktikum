package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.BuchAutorEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BuchAutorRepository extends JpaRepository<BuchAutorEntity, String> {
}

package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.AutorEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AutorRepository extends JpaRepository<AutorEntity, String> {
}

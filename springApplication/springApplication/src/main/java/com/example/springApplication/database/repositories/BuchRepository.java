package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.BuchEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BuchRepository extends JpaRepository<BuchEntity, String> {
}

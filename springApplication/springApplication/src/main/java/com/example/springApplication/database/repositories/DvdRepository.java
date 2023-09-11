package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.DvdEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DvdRepository extends JpaRepository<DvdEntity, String> {
}

package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.DvdBeteiligungenEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DvdBeteiligungenRepository extends JpaRepository<DvdBeteiligungenEntity, String> {
}

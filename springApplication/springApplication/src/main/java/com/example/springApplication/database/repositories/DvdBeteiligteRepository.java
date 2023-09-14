package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.DvdBeteiligteEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DvdBeteiligteRepository extends JpaRepository<DvdBeteiligteEntity, String> {
}

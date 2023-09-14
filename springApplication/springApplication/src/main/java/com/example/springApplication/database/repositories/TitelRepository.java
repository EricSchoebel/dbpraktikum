package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.TitelEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TitelRepository extends JpaRepository<TitelEntity, String> {
}

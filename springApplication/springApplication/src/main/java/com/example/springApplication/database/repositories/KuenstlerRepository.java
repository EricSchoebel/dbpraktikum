package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.KuenstlerEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface KuenstlerRepository extends JpaRepository<KuenstlerEntity, String> {
}

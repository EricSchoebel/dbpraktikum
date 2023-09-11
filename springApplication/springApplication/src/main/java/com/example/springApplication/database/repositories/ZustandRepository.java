package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.ZustandEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ZustandRepository extends JpaRepository<ZustandEntity, String> {
}

package com.example.springApplication.database.repositories;

import com.example.springApplication.database.entities.AnschriftEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AnschriftRepository extends JpaRepository <AnschriftEntity, String> {
}

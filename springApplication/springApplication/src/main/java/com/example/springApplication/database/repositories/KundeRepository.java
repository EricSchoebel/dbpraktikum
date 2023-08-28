package com.example.springApplication.database.repositories;

//import database.entities.RechnerId;

import com.example.springApplication.database.entities.KundeEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface KundeRepository extends JpaRepository<KundeEntity, String>{



}

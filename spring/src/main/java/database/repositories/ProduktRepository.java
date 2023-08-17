package database.repositories;

//import database.entities.RechnerId;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import database.entities.ProduktEntity;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import org.springframework.data.repository.query.Param;


import org.springframework.stereotype.Repository;


import java.util.List;

@Repository
public interface ProduktRepository extends JpaRepository<ProduktEntity, String>  { // zwei Argumente: <EntityKlasse, PrimaryKeyTyp>

  //  @Override
  //  List<ProduktEntity> findAllById(Iterable<String> strings);

    List<ProduktEntity> findAllByPid(String pid);

    // nicht zu verwendendes Äquivalent:
    // @Query("SELECT p FROM ProduktEntity p WHERE p.pid = :pid")
    // List<ProduktEntity> findProductsByPid(@Param("pid") String pid);


}

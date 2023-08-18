package database.repositories;

//import database.entities.RechnerId;
import database.entities.AngebotEntity;
import org.springframework.data.jpa.repository.JpaRepository;


import org.springframework.stereotype.Repository;


import java.util.List;

@Repository
public interface AngebotRepository extends JpaRepository<AngebotEntity, Integer>  {

    public List<AngebotEntity> findByPid(String pid); // für getOffers
    /*
    Alternativ "reines HQL", anderes Naming:
    @Query("SELECT a FROM AngebotEntity a WHERE a.pid = :pid")
    List<AngebotEntity> getOffers(@Param("pid") String pid);
     */

}

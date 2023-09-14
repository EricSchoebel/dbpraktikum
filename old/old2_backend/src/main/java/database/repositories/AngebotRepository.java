package database.repositories;

//import database.entities.RechnerId;
import database.entities.AngebotEntity;
import org.springframework.data.jpa.repository.JpaRepository;


import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;


import java.util.List;

@Repository
public interface AngebotRepository extends JpaRepository<AngebotEntity, Integer>  {

    @Query("SELECT a, f.filialname, z.beschreibung FROM AngebotEntity a " +
            "JOIN FilialeEntity f ON a.fid = f.fid " +
            "JOIN ZustandEntity z ON a.zustandsnummer = z.zustandsnummer " +
            "WHERE a.pid = :pid")
    List<Object[]> getOffers(@Param("pid") String pid);

    /* ALT:
    public List<AngebotEntity> findByPid(String pid); // für getOffers
    */
    /*
    Alternativ "reines HQL", anderes Naming:
    @Query("SELECT a FROM AngebotEntity a WHERE a.pid = :pid")
    List<AngebotEntity> getOffers(@Param("pid") String pid);
     */

}

package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "fehlerlog", schema = "public", catalog = "dbprak_postgres")
public class FehlerlogEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "fehlerid")
    private int fehlerid;
    @Basic
    @Column(name = "fehlernachricht")
    private String fehlernachricht;

    public int getFehlerid() {
        return fehlerid;
    }

    public void setFehlerid(int fehlerid) {
        this.fehlerid = fehlerid;
    }

    public String getFehlernachricht() {
        return fehlernachricht;
    }

    public void setFehlernachricht(String fehlernachricht) {
        this.fehlernachricht = fehlernachricht;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        FehlerlogEntity that = (FehlerlogEntity) o;
        return fehlerid == that.fehlerid && Objects.equals(fehlernachricht, that.fehlernachricht);
    }

    @Override
    public int hashCode() {
        return Objects.hash(fehlerid, fehlernachricht);
    }
}

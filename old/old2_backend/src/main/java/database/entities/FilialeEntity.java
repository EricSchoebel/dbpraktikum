package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "filiale", schema = "public", catalog = "dbprak_postgres")
public class FilialeEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "fid")
    private int fid;
    @Basic
    @Column(name = "filialname")
    private String filialname;

    public int getFid() {
        return fid;
    }

    public void setFid(int fid) {
        this.fid = fid;
    }

    public String getFilialname() {
        return filialname;
    }

    public void setFilialname(String filialname) {
        this.filialname = filialname;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        FilialeEntity that = (FilialeEntity) o;
        return fid == that.fid && Objects.equals(filialname, that.filialname);
    }

    @Override
    public int hashCode() {
        return Objects.hash(fid, filialname);
    }
}

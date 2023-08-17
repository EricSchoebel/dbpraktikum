package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "cd_kuenstler", schema = "public", catalog = "dbprak_postgres")
@IdClass(CdKuenstlerEntityPK.class)
public class CdKuenstlerEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "kuenstlerid")
    private int kuenstlerid;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public int getKuenstlerid() {
        return kuenstlerid;
    }

    public void setKuenstlerid(int kuenstlerid) {
        this.kuenstlerid = kuenstlerid;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        CdKuenstlerEntity that = (CdKuenstlerEntity) o;
        return kuenstlerid == that.kuenstlerid && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, kuenstlerid);
    }
}

package database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class CdKuenstlerEntityPK implements Serializable {
    @Column(name = "pid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String pid;
    @Column(name = "kuenstlerid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
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
        CdKuenstlerEntityPK that = (CdKuenstlerEntityPK) o;
        return kuenstlerid == that.kuenstlerid && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, kuenstlerid);
    }
}

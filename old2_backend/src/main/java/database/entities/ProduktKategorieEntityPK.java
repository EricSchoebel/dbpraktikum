package database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class ProduktKategorieEntityPK implements Serializable {
    @Column(name = "katid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int katid;
    @Column(name = "pid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String pid;

    public int getKatid() {
        return katid;
    }

    public void setKatid(int katid) {
        this.katid = katid;
    }

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ProduktKategorieEntityPK that = (ProduktKategorieEntityPK) o;
        return katid == that.katid && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(katid, pid);
    }
}

package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "produkt_kategorie", schema = "public", catalog = "dbprak_postgres")
@IdClass(ProduktKategorieEntityPK.class)
public class ProduktKategorieEntity {
    @Id
    @Column(name = "katid")
    private int katid;
    @Id
    @Column(name = "pid")
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
        ProduktKategorieEntity that = (ProduktKategorieEntity) o;
        return katid == that.katid && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(katid, pid);
    }
}

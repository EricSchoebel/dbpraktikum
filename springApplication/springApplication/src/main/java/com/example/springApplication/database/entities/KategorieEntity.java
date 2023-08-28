package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "kategorie", schema = "public", catalog = "dbprak_postgres")
public class KategorieEntity {
    @Id
    @Column(name = "katid")
    private int katid;
    @Basic
    @Column(name = "kategoriename")
    private String kategoriename;
    @Basic
    @Column(name = "oberkategorie")
    private Integer oberkategorie;

    public int getKatid() {
        return katid;
    }

    public void setKatid(int katid) {
        this.katid = katid;
    }

    public String getKategoriename() {
        return kategoriename;
    }

    public void setKategoriename(String kategoriename) {
        this.kategoriename = kategoriename;
    }

    public Integer getOberkategorie() {
        return oberkategorie;
    }

    public void setOberkategorie(Integer oberkategorie) {
        this.oberkategorie = oberkategorie;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KategorieEntity that = (KategorieEntity) o;
        return katid == that.katid && Objects.equals(kategoriename, that.kategoriename) && Objects.equals(oberkategorie, that.oberkategorie);
    }

    @Override
    public int hashCode() {
        return Objects.hash(katid, kategoriename, oberkategorie);
    }
}

package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "kuenstler", schema = "public", catalog = "dbprak_postgres")
public class KuenstlerEntity {
    @Id
    @Column(name = "kuenstlerid")
    private int kuenstlerid;
    @Basic
    @Column(name = "kuenstlername")
    private String kuenstlername;

    public int getKuenstlerid() {
        return kuenstlerid;
    }

    public void setKuenstlerid(int kuenstlerid) {
        this.kuenstlerid = kuenstlerid;
    }

    public String getKuenstlername() {
        return kuenstlername;
    }

    public void setKuenstlername(String kuenstlername) {
        this.kuenstlername = kuenstlername;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KuenstlerEntity that = (KuenstlerEntity) o;
        return kuenstlerid == that.kuenstlerid && Objects.equals(kuenstlername, that.kuenstlername);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kuenstlerid, kuenstlername);
    }
}

package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "autor", schema = "public", catalog = "dbprak_postgres")
public class AutorEntity {
    @Id
    @Column(name = "autorid")
    private int autorid;
    @Basic
    @Column(name = "autorname")
    private String autorname;

    public int getAutorid() {
        return autorid;
    }

    public void setAutorid(int autorid) {
        this.autorid = autorid;
    }

    public String getAutorname() {
        return autorname;
    }

    public void setAutorname(String autorname) {
        this.autorname = autorname;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AutorEntity that = (AutorEntity) o;
        return autorid == that.autorid && Objects.equals(autorname, that.autorname);
    }

    @Override
    public int hashCode() {
        return Objects.hash(autorid, autorname);
    }
}

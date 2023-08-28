package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "buch_autor", schema = "public", catalog = "dbprak_postgres")
@IdClass(BuchAutorEntityPK.class)
public class BuchAutorEntity {
    @Id
    @Column(name = "pid")
    private String pid;
    @Id
    @Column(name = "autorid")
    private int autorid;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public int getAutorid() {
        return autorid;
    }

    public void setAutorid(int autorid) {
        this.autorid = autorid;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        BuchAutorEntity that = (BuchAutorEntity) o;
        return autorid == that.autorid && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, autorid);
    }
}

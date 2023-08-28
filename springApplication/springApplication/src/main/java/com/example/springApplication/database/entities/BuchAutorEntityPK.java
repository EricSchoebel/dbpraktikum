package com.example.springApplication.database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class BuchAutorEntityPK implements Serializable {
    @Column(name = "pid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String pid;
    @Column(name = "autorid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
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
        BuchAutorEntityPK that = (BuchAutorEntityPK) o;
        return autorid == that.autorid && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, autorid);
    }
}

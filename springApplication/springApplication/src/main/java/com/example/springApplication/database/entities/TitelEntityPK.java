package com.example.springApplication.database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class TitelEntityPK implements Serializable {
    @Column(name = "pid")
    @Id
    private String pid;
    @Column(name = "titelname")
    @Id
    private String titelname;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public String getTitelname() {
        return titelname;
    }

    public void setTitelname(String titelname) {
        this.titelname = titelname;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TitelEntityPK that = (TitelEntityPK) o;
        return Objects.equals(pid, that.pid) && Objects.equals(titelname, that.titelname);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, titelname);
    }
}

package com.example.springApplication.database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class DvdBeteiligungenEntityPK implements Serializable {
    @Column(name = "pid")
    @Id
    private String pid;
    @Column(name = "beteiligtenid")
    @Id
    private int beteiligtenid;
    @Column(name = "rolle")
    @Id
    private String rolle;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public int getBeteiligtenid() {
        return beteiligtenid;
    }

    public void setBeteiligtenid(int beteiligtenid) {
        this.beteiligtenid = beteiligtenid;
    }

    public String getRolle() {
        return rolle;
    }

    public void setRolle(String rolle) {
        this.rolle = rolle;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DvdBeteiligungenEntityPK that = (DvdBeteiligungenEntityPK) o;
        return beteiligtenid == that.beteiligtenid && Objects.equals(pid, that.pid) && Objects.equals(rolle, that.rolle);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, beteiligtenid, rolle);
    }
}

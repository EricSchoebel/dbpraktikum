package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Objects;

@Entity
@Table(name = "angebot", schema = "public", catalog = "dbprak_postgres")
public class AngebotEntity {
    @Id
    @Column(name = "angebotsid")
    private int angebotsid;
    @Basic
    @Column(name = "pid")
    private String pid;
    @Basic
    @Column(name = "fid")
    private Integer fid;
    @Basic
    @Column(name = "preis")
    private BigDecimal preis;
    @Basic
    @Column(name = "zustandsnummer")
    private Integer zustandsnummer;
    @Basic
    @Column(name = "menge")
    private Integer menge;

    public int getAngebotsid() {
        return angebotsid;
    }

    public void setAngebotsid(int angebotsid) {
        this.angebotsid = angebotsid;
    }

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public Integer getFid() {
        return fid;
    }

    public void setFid(Integer fid) {
        this.fid = fid;
    }

    public BigDecimal getPreis() {
        return preis;
    }

    public void setPreis(BigDecimal preis) {
        this.preis = preis;
    }

    public Integer getZustandsnummer() {
        return zustandsnummer;
    }

    public void setZustandsnummer(Integer zustandsnummer) {
        this.zustandsnummer = zustandsnummer;
    }

    public Integer getMenge() {
        return menge;
    }

    public void setMenge(Integer menge) {
        this.menge = menge;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AngebotEntity that = (AngebotEntity) o;
        return angebotsid == that.angebotsid && Objects.equals(pid, that.pid) && Objects.equals(fid, that.fid) && Objects.equals(preis, that.preis) && Objects.equals(zustandsnummer, that.zustandsnummer) && Objects.equals(menge, that.menge);
    }

    @Override
    public int hashCode() {
        return Objects.hash(angebotsid, pid, fid, preis, zustandsnummer, menge);
    }
}

package com.example.springApplication.database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.sql.Timestamp;
import java.util.Objects;

public class KaufEntityPK implements Serializable {
    @Column(name = "angebotsid")
    @Id
    private int angebotsid;
    @Column(name = "kundenid")
    @Id
    private String kundenid;
    @Column(name = "zeitpunkt")
    @Id
    private Timestamp zeitpunkt;

    public int getAngebotsid() {
        return angebotsid;
    }

    public void setAngebotsid(int angebotsid) {
        this.angebotsid = angebotsid;
    }

    public String getKundenid() {
        return kundenid;
    }

    public void setKundenid(String kundenid) {
        this.kundenid = kundenid;
    }

    public Timestamp getZeitpunkt() {
        return zeitpunkt;
    }

    public void setZeitpunkt(Timestamp zeitpunkt) {
        this.zeitpunkt = zeitpunkt;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KaufEntityPK that = (KaufEntityPK) o;
        return angebotsid == that.angebotsid && Objects.equals(kundenid, that.kundenid) && Objects.equals(zeitpunkt, that.zeitpunkt);
    }

    @Override
    public int hashCode() {
        return Objects.hash(angebotsid, kundenid, zeitpunkt);
    }
}

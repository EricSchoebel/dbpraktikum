package com.example.springApplication.database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class KontoEntityPK implements Serializable {
    @Column(name = "kundenid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String kundenid;
    @Column(name = "kontonummer")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int kontonummer;

    public String getKundenid() {
        return kundenid;
    }

    public void setKundenid(String kundenid) {
        this.kundenid = kundenid;
    }

    public int getKontonummer() {
        return kontonummer;
    }

    public void setKontonummer(int kontonummer) {
        this.kontonummer = kontonummer;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KontoEntityPK that = (KontoEntityPK) o;
        return kontonummer == that.kontonummer && Objects.equals(kundenid, that.kundenid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, kontonummer);
    }
}

package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "zustand", schema = "public", catalog = "dbprak_postgres")
public class ZustandEntity {
    @Id
    @Column(name = "zustandsnummer")
    private int zustandsnummer;
    @Basic
    @Column(name = "beschreibung")
    private String beschreibung;

    public int getZustandsnummer() {
        return zustandsnummer;
    }

    public void setZustandsnummer(int zustandsnummer) {
        this.zustandsnummer = zustandsnummer;
    }

    public String getBeschreibung() {
        return beschreibung;
    }

    public void setBeschreibung(String beschreibung) {
        this.beschreibung = beschreibung;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ZustandEntity that = (ZustandEntity) o;
        return zustandsnummer == that.zustandsnummer && Objects.equals(beschreibung, that.beschreibung);
    }

    @Override
    public int hashCode() {
        return Objects.hash(zustandsnummer, beschreibung);
    }
}

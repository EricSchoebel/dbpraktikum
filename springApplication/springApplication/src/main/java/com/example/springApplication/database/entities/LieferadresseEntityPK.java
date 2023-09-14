package com.example.springApplication.database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;
public class LieferadresseEntityPK implements Serializable{
    @Column(name = "kundenid")
    @Id
    private String kundenid;
    @Column(name = "strasse")
    @Id
    private String strasse;

    @Column(name="hausnummer")
    @Id
    private String hausnummer;

    @Column(name="plz")
    @Id
    private String plz;

    public String getKundenid() {
        return kundenid;
    }

    public void setKundenid(String kundenid) {
        this.kundenid = kundenid;
    }

    public String getStrasse() {
        return strasse;
    }

    public void setStrasse(String strasse) {
        this.strasse = strasse;
    }

    public String getHausnummer() {
        return hausnummer;
    }

    public void setHausnummer(String hausnummer) {this.hausnummer = hausnummer;}

    public String getPlz() {
        return plz;
    }

    public void setPlz(String plz) {
        this.plz = plz;
    }


    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        LieferadresseEntityPK that = (LieferadresseEntityPK) o;
        return Objects.equals(kundenid, that.kundenid) && Objects.equals(strasse, that.strasse) && Objects.equals(hausnummer, that.hausnummer) && Objects.equals(plz, that.plz);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, strasse, hausnummer, plz);
    }
}

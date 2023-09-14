package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "lieferadresse", schema = "public", catalog = "dbprak_postgres")
@IdClass(LieferadresseEntityPK.class)
public class LieferadresseEntity {
    @Id
    @Column(name = "kundenid")
    private String kundenid;

    @Id
    @Column(name = "strasse")
    private String strasse;

    @Id
    @Column(name = "hausnummer")
    private String hausnummer;

    @Id
    @Column(name = "plz")
    private String plz;

    public String getKundenid(){return this.kundenid;}

    public void setKundenid(String kundenid){this.kundenid = kundenid;}

    public String getHausnummer(){return this.hausnummer;}

    public void setHausnummer(String hausnummer){this.hausnummer = hausnummer;}

    public String getStrasse(){return this.strasse;}

    public void setStrasse(String strasse){this.strasse = strasse;}

    public String getPlz(){return this.plz;}

    public void setPlz(String plz){this.plz = plz;}

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        LieferadresseEntity that = (LieferadresseEntity) o;
        return Objects.equals(kundenid, that.kundenid) && Objects.equals(strasse, that.strasse) && Objects.equals(hausnummer, that.hausnummer) && Objects.equals(plz, that.plz);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, strasse, hausnummer, plz);
    }

}

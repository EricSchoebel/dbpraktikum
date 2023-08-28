package database.entities;

import jakarta.persistence.Basic;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

import java.util.Objects;

@Entity
@Table(name = "lieferadresse", schema = "public", catalog = "dbprak_postgres")
public class LieferadresseEntity {
    @Basic
    @Column(name = "kundenid")
    private String kundenid;
    @Basic
    @Column(name = "strasse")
    private String strasse;
    @Basic
    @Column(name = "hausnummer")
    private String hausnummer;
    @Basic
    @Column(name = "plz")
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

    public void setHausnummer(String hausnummer) {
        this.hausnummer = hausnummer;
    }

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
        LieferadresseEntity that = (LieferadresseEntity) o;
        return Objects.equals(kundenid, that.kundenid) && Objects.equals(strasse, that.strasse) && Objects.equals(hausnummer, that.hausnummer) && Objects.equals(plz, that.plz);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, strasse, hausnummer, plz);
    }
}

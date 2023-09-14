package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "anschrift", schema = "public", catalog = "dbprak_postgres")
public class AnschriftEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "fid")
    private int fid;
    @Basic
    @Column(name = "strasse")
    private String strasse;
    @Basic
    @Column(name = "hausnummer")
    private String hausnummer;
    @Basic
    @Column(name = "plz")
    private String plz;

    public int getFid() {
        return fid;
    }

    public void setFid(int fid) {
        this.fid = fid;
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
        AnschriftEntity that = (AnschriftEntity) o;
        return fid == that.fid && Objects.equals(strasse, that.strasse) && Objects.equals(hausnummer, that.hausnummer) && Objects.equals(plz, that.plz);
    }

    @Override
    public int hashCode() {
        return Objects.hash(fid, strasse, hausnummer, plz);
    }
}

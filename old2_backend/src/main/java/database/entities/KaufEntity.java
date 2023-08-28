package database.entities;

import jakarta.persistence.*;

import java.sql.Timestamp;
import java.util.Objects;

@Entity
@Table(name = "kauf", schema = "public", catalog = "dbprak_postgres")
@IdClass(KaufEntityPK.class)
public class KaufEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "angebotsid")
    private int angebotsid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "kundenid")
    private String kundenid;
    @Basic
    @Column(name = "menge")
    private Integer menge;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "zeitpunkt")
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

    public Integer getMenge() {
        return menge;
    }

    public void setMenge(Integer menge) {
        this.menge = menge;
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
        KaufEntity that = (KaufEntity) o;
        return angebotsid == that.angebotsid && Objects.equals(kundenid, that.kundenid) && Objects.equals(menge, that.menge) && Objects.equals(zeitpunkt, that.zeitpunkt);
    }

    @Override
    public int hashCode() {
        return Objects.hash(angebotsid, kundenid, menge, zeitpunkt);
    }
}

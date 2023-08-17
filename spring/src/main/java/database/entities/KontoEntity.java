package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "konto", schema = "public", catalog = "dbprak_postgres")
@IdClass(KontoEntityPK.class)
public class KontoEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "kundenid")
    private String kundenid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "kontonummer")
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
        KontoEntity that = (KontoEntity) o;
        return kontonummer == that.kontonummer && Objects.equals(kundenid, that.kundenid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, kontonummer);
    }
}

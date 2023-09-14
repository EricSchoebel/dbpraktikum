package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "kunde", schema = "public", catalog = "dbprak_postgres")
public class KundeEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "kundenid")
    private String kundenid;
    @Basic
    @Column(name = "kundenname")
    private String kundenname;

    public String getKundenid() {
        return kundenid;
    }

    public void setKundenid(String kundenid) {
        this.kundenid = kundenid;
    }

    public String getKundenname() {
        return kundenname;
    }

    public void setKundenname(String kundenname) {
        this.kundenname = kundenname;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KundeEntity that = (KundeEntity) o;
        return Objects.equals(kundenid, that.kundenid) && Objects.equals(kundenname, that.kundenname);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, kundenname);
    }
}

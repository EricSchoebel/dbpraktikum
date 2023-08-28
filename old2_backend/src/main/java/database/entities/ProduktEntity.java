package database.entities;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Objects;

@Entity
@Table(name = "produkt", schema = "public", catalog = "dbprak_postgres")
public class ProduktEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @Basic
    @Column(name = "titel")
    private String titel;
    @Basic
    @Column(name = "rating")
    private BigDecimal rating;
    @Basic
    @Column(name = "verkaufsrang")
    private Integer verkaufsrang;
    @Basic
    @Column(name = "bild")
    private byte[] bild;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public String getTitel() {
        return titel;
    }

    public void setTitel(String titel) {
        this.titel = titel;
    }

    public BigDecimal getRating() {
        return rating;
    }

    public void setRating(BigDecimal rating) {
        this.rating = rating;
    }

    public Integer getVerkaufsrang() {
        return verkaufsrang;
    }

    public void setVerkaufsrang(Integer verkaufsrang) {
        this.verkaufsrang = verkaufsrang;
    }

    public byte[] getBild() {
        return bild;
    }

    public void setBild(byte[] bild) {
        this.bild = bild;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ProduktEntity that = (ProduktEntity) o;
        return Objects.equals(pid, that.pid) && Objects.equals(titel, that.titel) && Objects.equals(rating, that.rating) && Objects.equals(verkaufsrang, that.verkaufsrang) && Arrays.equals(bild, that.bild);
    }

    @Override
    public int hashCode() {
        int result = Objects.hash(pid, titel, rating, verkaufsrang);
        result = 31 * result + Arrays.hashCode(bild);
        return result;
    }
}

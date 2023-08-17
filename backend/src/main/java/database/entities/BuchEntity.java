package database.entities;

import jakarta.persistence.*;

import java.sql.Date;
import java.util.Objects;

@Entity
@Table(name = "buch", schema = "public", catalog = "dbprak_postgres")
public class BuchEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @Basic
    @Column(name = "seitenzahl")
    private Integer seitenzahl;
    @Basic
    @Column(name = "erscheinungsdatum")
    private Date erscheinungsdatum;
    @Basic
    @Column(name = "isbn")
    private String isbn;
    @Basic
    @Column(name = "verlag")
    private String verlag;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public Integer getSeitenzahl() {
        return seitenzahl;
    }

    public void setSeitenzahl(Integer seitenzahl) {
        this.seitenzahl = seitenzahl;
    }

    public Date getErscheinungsdatum() {
        return erscheinungsdatum;
    }

    public void setErscheinungsdatum(Date erscheinungsdatum) {
        this.erscheinungsdatum = erscheinungsdatum;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public String getVerlag() {
        return verlag;
    }

    public void setVerlag(String verlag) {
        this.verlag = verlag;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        BuchEntity that = (BuchEntity) o;
        return Objects.equals(pid, that.pid) && Objects.equals(seitenzahl, that.seitenzahl) && Objects.equals(erscheinungsdatum, that.erscheinungsdatum) && Objects.equals(isbn, that.isbn) && Objects.equals(verlag, that.verlag);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, seitenzahl, erscheinungsdatum, isbn, verlag);
    }
}

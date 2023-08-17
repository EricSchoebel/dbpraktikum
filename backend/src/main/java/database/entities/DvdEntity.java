package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "dvd", schema = "public", catalog = "dbprak_postgres")
public class DvdEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @Basic
    @Column(name = "format")
    private String format;
    @Basic
    @Column(name = "laufzeit")
    private Integer laufzeit;
    @Basic
    @Column(name = "regioncode")
    private String regioncode;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public String getFormat() {
        return format;
    }

    public void setFormat(String format) {
        this.format = format;
    }

    public Integer getLaufzeit() {
        return laufzeit;
    }

    public void setLaufzeit(Integer laufzeit) {
        this.laufzeit = laufzeit;
    }

    public String getRegioncode() {
        return regioncode;
    }

    public void setRegioncode(String regioncode) {
        this.regioncode = regioncode;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DvdEntity dvdEntity = (DvdEntity) o;
        return Objects.equals(pid, dvdEntity.pid) && Objects.equals(format, dvdEntity.format) && Objects.equals(laufzeit, dvdEntity.laufzeit) && Objects.equals(regioncode, dvdEntity.regioncode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, format, laufzeit, regioncode);
    }
}

package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "titel", schema = "public", catalog = "dbprak_postgres")
@IdClass(TitelEntityPK.class)
public class TitelEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "titelname")
    private String titelname;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public String getTitelname() {
        return titelname;
    }

    public void setTitelname(String titelname) {
        this.titelname = titelname;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TitelEntity that = (TitelEntity) o;
        return Objects.equals(pid, that.pid) && Objects.equals(titelname, that.titelname);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, titelname);
    }
}

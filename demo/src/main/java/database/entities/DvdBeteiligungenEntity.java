package database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "dvd_beteiligungen", schema = "public", catalog = "dbprak_postgres")
@IdClass(DvdBeteiligungenEntityPK.class)
public class DvdBeteiligungenEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "beteiligtenid")
    private int beteiligtenid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "rolle")
    private String rolle;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public int getBeteiligtenid() {
        return beteiligtenid;
    }

    public void setBeteiligtenid(int beteiligtenid) {
        this.beteiligtenid = beteiligtenid;
    }

    public String getRolle() {
        return rolle;
    }

    public void setRolle(String rolle) {
        this.rolle = rolle;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DvdBeteiligungenEntity that = (DvdBeteiligungenEntity) o;
        return beteiligtenid == that.beteiligtenid && Objects.equals(pid, that.pid) && Objects.equals(rolle, that.rolle);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, beteiligtenid, rolle);
    }
}

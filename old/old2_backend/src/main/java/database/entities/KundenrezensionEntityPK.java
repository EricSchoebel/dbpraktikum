package database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class KundenrezensionEntityPK implements Serializable {
    @Column(name = "kundenid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String kundenid;
    @Column(name = "pid")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String pid;

    public String getKundenid() {
        return kundenid;
    }

    public void setKundenid(String kundenid) {
        this.kundenid = kundenid;
    }

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KundenrezensionEntityPK that = (KundenrezensionEntityPK) o;
        return Objects.equals(kundenid, that.kundenid) && Objects.equals(pid, that.pid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, pid);
    }
}

package database.entities;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.util.Objects;

public class AehnlichkeitEntityPK implements Serializable {
    @Column(name = "pid1")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String pid1;
    @Column(name = "pid2")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String pid2;

    public String getPid1() {
        return pid1;
    }

    public void setPid1(String pid1) {
        this.pid1 = pid1;
    }

    public String getPid2() {
        return pid2;
    }

    public void setPid2(String pid2) {
        this.pid2 = pid2;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AehnlichkeitEntityPK that = (AehnlichkeitEntityPK) o;
        return Objects.equals(pid1, that.pid1) && Objects.equals(pid2, that.pid2);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid1, pid2);
    }
}

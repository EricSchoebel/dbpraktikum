package com.example.springApplication.database.entities;

import jakarta.persistence.*;

import java.util.Objects;

@Entity
@Table(name = "dvd_beteiligte", schema = "public", catalog = "dbprak_postgres")
public class DvdBeteiligteEntity {
    @Id
    @Column(name = "beteiligtenid")
    private int beteiligtenid;
    @Basic
    @Column(name = "beteiligtenname")
    private String beteiligtenname;

    public int getBeteiligtenid() {
        return beteiligtenid;
    }

    public void setBeteiligtenid(int beteiligtenid) {
        this.beteiligtenid = beteiligtenid;
    }

    public String getBeteiligtenname() {
        return beteiligtenname;
    }

    public void setBeteiligtenname(String beteiligtenname) {
        this.beteiligtenname = beteiligtenname;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DvdBeteiligteEntity that = (DvdBeteiligteEntity) o;
        return beteiligtenid == that.beteiligtenid && Objects.equals(beteiligtenname, that.beteiligtenname);
    }

    @Override
    public int hashCode() {
        return Objects.hash(beteiligtenid, beteiligtenname);
    }
}

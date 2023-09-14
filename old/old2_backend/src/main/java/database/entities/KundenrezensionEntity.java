package database.entities;

import jakarta.persistence.*;

import java.sql.Date;
import java.util.Objects;

@Entity
@Table(name = "kundenrezension", schema = "public", catalog = "dbprak_postgres")
@IdClass(KundenrezensionEntityPK.class)
public class KundenrezensionEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "kundenid")
    private String kundenid;
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @Basic
    @Column(name = "punkte")
    private Integer punkte;
    @Basic
    @Column(name = "helpful")
    private Integer helpful;
    @Basic
    @Column(name = "summary")
    private String summary;
    @Basic
    @Column(name = "content")
    private String content;
    @Basic
    @Column(name = "reviewdate")
    private Date reviewdate;

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

    public Integer getPunkte() {
        return punkte;
    }

    public void setPunkte(Integer punkte) {
        this.punkte = punkte;
    }

    public Integer getHelpful() {
        return helpful;
    }

    public void setHelpful(Integer helpful) {
        this.helpful = helpful;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Date getReviewdate() {
        return reviewdate;
    }

    public void setReviewdate(Date reviewdate) {
        this.reviewdate = reviewdate;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        KundenrezensionEntity that = (KundenrezensionEntity) o;
        return Objects.equals(kundenid, that.kundenid) && Objects.equals(pid, that.pid) && Objects.equals(punkte, that.punkte) && Objects.equals(helpful, that.helpful) && Objects.equals(summary, that.summary) && Objects.equals(content, that.content) && Objects.equals(reviewdate, that.reviewdate);
    }

    @Override
    public int hashCode() {
        return Objects.hash(kundenid, pid, punkte, helpful, summary, content, reviewdate);
    }
}

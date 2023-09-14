package database.entities;

import jakarta.persistence.*;

import java.sql.Date;
import java.util.Objects;

@Entity
@Table(name = "cd", schema = "public", catalog = "dbprak_postgres")
public class CdEntity {
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "pid")
    private String pid;
    @Basic
    @Column(name = "label")
    private String label;
    @Basic
    @Column(name = "erscheinungsdatum")
    private Date erscheinungsdatum;

    public String getPid() {
        return pid;
    }

    public void setPid(String pid) {
        this.pid = pid;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public Date getErscheinungsdatum() {
        return erscheinungsdatum;
    }

    public void setErscheinungsdatum(Date erscheinungsdatum) {
        this.erscheinungsdatum = erscheinungsdatum;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        CdEntity cdEntity = (CdEntity) o;
        return Objects.equals(pid, cdEntity.pid) && Objects.equals(label, cdEntity.label) && Objects.equals(erscheinungsdatum, cdEntity.erscheinungsdatum);
    }

    @Override
    public int hashCode() {
        return Objects.hash(pid, label, erscheinungsdatum);
    }
}

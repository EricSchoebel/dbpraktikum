package com.example.springApplication.api;

import java.util.Optional;

public class ReviewRequest {

    private String kundenid;
    private String pid;
    private int punkte;
    private Optional<Integer> helpful;
    private Optional<String> summary;
    private Optional<String> content;


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

    public int getPunkte() {
        return punkte;
    }

    public void setPunkte(int punkte) {
        this.punkte = punkte;
    }

    public Optional<Integer> getHelpful() {
        return helpful;
    }

    public void setHelpful(Optional<Integer> helpful) {
        this.helpful = helpful;
    }

    public Optional<String> getSummary() {
        return summary;
    }

    public void setSummary(Optional<String> summary) {
        this.summary = summary;
    }

    public Optional<String> getContent() {
        return content;
    }

    public void setContent(Optional<String> content) {
        this.content = content;
    }

}
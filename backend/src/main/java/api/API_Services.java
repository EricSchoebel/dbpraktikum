package api;


import database.entities.*;
import database.repositories.ProduktRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.Instant;
import java.util.*;

@Service
public class API_Services {

    @Autowired
    ProduktRepository produktRepository;

    //nur Testzweck:
    public List<ProduktEntity> oldGetTestProductInfoForID(String pid) {
        List<ProduktEntity> resultList = produktRepository.findAllByPid(pid);
        return resultList;
    }

    public List<Object[]> getProductInfoForID(String pid) {
        List<Object[]> resultList = produktRepository.getProduct(pid);
        return resultList;
    }

    public List<ProduktEntity[]> getProductsForPattern(String pattern) {
        List<ProduktEntity[]> resultList = produktRepository.getProducts(pattern);
        return resultList;
    }

}

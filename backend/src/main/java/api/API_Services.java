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

    public List<ProduktEntity> getProductInfoForID(String pid) {
        List<ProduktEntity> resultList = produktRepository.findAllByPid(pid);
        return resultList;
    }


}

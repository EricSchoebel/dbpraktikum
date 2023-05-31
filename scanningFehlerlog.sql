--nur die 4 Sachen
select * from fehlerlog
where fehlernachricht NOT LIKE '%WARNING%'
AND fehlernachricht NOT LIKE '%ERROR%'
AND fehlernachricht NOT LIKE '%UniqueViolation%'
AND fehlernachricht NOT LIKE '%CheckViolation%'
;

--Anzahl z.B.
select count(*) from fehlerlog
where fehlernachricht LIKE '%UniqueViolation%';

--spezielle Sache angucken
select * from fehlerlog
where fehlernachricht LIKE '%WARNING%' ORDER BY fehlernachricht ASC;

select * from fehlerlog
where fehlernachricht LIKE '%UniqueViolation%' ORDER BY fehlernachricht ASC;

select * from fehlerlog
where fehlernachricht LIKE '%CheckViolation%' ORDER BY fehlernachricht ASC;

select * from fehlerlog
where fehlernachricht LIKE '%ERROR%' ORDER BY fehlernachricht ASC;






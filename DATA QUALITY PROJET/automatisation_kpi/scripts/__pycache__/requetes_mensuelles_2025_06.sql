-- REQUÊTES AUTOMATISÉES POUR 06/2025
-- Générées le 2025-06-11 15:17:14


-- PARC ACTIF - Vérification segment marché
SELECT concat(year, month) as periode, segment_marche, count(distinct msisdn) as parc
FROM monthly_clients
WHERE year = 2025 AND month = 6 AND parc = 1
GROUP BY year, month, segment_marche
ORDER BY month;

--------------------------------------------------------------------------------


-- CA RECHARGE - Comparaison reporting monthly vs recharge detail
SELECT year, month, formule_dmgp, segment_marche, segment_recharge,
    sum(ca_cartes) as cartes,
    sum(ca_credit_om) as credit,
    sum(ca_iah) as iah,
    sum(ca_pass_glob_om_jour) as pass1_glob_om,
    sum(ca_seddo) as seddo,
    sum(ca_recharges) as recharges,
    sum(ca_wave) as wave,
    sum(ca_ht) as ht,
    sum(nb_subs) as parc
FROM refined_vue360.reporting_ca_monthly
WHERE year = 2025 AND parc = 1
GROUP BY year, month, formule_dmgp, segment_marche, segment_recharge
ORDER BY month;

-- Requête complémentaire pour recharge detail
SELECT sum(montant)/1239 as ca_ht_year_month_canal_recharge
FROM refined_recharge.recharge_in_detail
WHERE year IN (LastYear) AND month IN (LastMonth) AND lower(canal_recharge)
IN ('ca wave', 'ca seddo', 'ca pass glob om jour', 'ca credit om', 'ca cartes', 'ca iah')
GROUP BY msisdn, year, month, canal_recharge;

--------------------------------------------------------------------------------


-- TRAFIC DATA - Comparaison reporting monthly vs dump otarie
SELECT concat(year, month) as periode, year, month, segment_marche,
    sum(total_volume_go) as total,
    sum(trafic_4g_go) as traf_4G,
    sum(parc_4g) as parc_4g,
    sum(trafic_5g_go) as traf_5G,
    sum(parc_5g) as parc_5g
FROM refined_vue360.reporting_trafic_data_monthly
GROUP BY year, month, segment_marche;

-- Requête complémentaire pour dump otarie
SELECT concat(year, month) as periode, year, month, substr(msisdn, 4, 2) as debut_numero,
    sum(total_volume)/1000000000 as volume
FROM trusted_pfs.dump_otarie
WHERE year = 2025 AND month = 6
GROUP BY year, month, substr(msisdn, 4, 2);

--------------------------------------------------------------------------------


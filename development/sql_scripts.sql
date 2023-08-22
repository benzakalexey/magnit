INSERT INTO app.contract_services (name, source_id, type)
VALUES ('Услуги по накоплению отходов строительных и ремонтных работ (V класс) с последующей их обработкой и утилизацией',
        null, 'CONSTRUCTION_WASTE');
INSERT INTO app.contract_services (name, source_id, type)
VALUES ('Услуги по накоплению отходов строительных и ремонтных работ ( IV-V класс) с последующей их обработкой и утилизацией',
        null, 'CONSTRUCTION_WASTE');
INSERT INTO app.contract_services (name, source_id, type)
VALUES ('Услуги по накоплению растительных и древесных отходов V класса опасности с последующей их обработкой и реализацией',
        null, 'WOOD_WASTE');
INSERT INTO app.contract_services (name, source_id, type)
VALUES ('Услуги по накоплению растительных и древесных отходов V класса опасности, с последующей их утилизацией', null,
        'WOOD_WASTE');

INSERT INTO app.executor_storage_areas (polygon_id, contract_id)
VALUES (10, _);
INSERT INTO app.executor_storage_areas (polygon_id, contract_id)
VALUES (2, _);


INSERT INTO app.service_contracts (number,
                                   valid_from,
                                   valid_to,
                                   permit_id,
                                   contract_service_id,
                                   executor_id,
                                   executor_person,
                                   executor_acts_basis,
                                   customer_id,
                                   customer_person,
                                   customer_acts_basis,
                                   tariff,
                                   total_cost,
                                   balance_limit)
VALUES ('123-РДО', '2023-01-01 00:00:00.000', '2023-12-31 23:59:59.000', 436, 1, 1, 'Gurgen', 'By me', 9,
        'General ECOS', 'Himself proof', 1234.56, 1234567.89, 12345.67);


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

select v.invoice_num,
       v.checked_out,
       c.number      as contract,
       c.valid_to    as contract_exp,
       p.name        as carrier,
       p2.name       as receiver,
       p3.name       as sender,
       permit.number as permit,
       o.name
from app.visits v
         join app.contracts c on c.id = v.contract_id
         join app.permissions perm on perm.id = v.permission_id
         join app.partners o on o.id = perm.owner_id
         join app.permits permit on permit.id = perm.permit_id
         join app.partners p on p.id = c.carrier_id
         join app.partners p2 on p2.id = c.receiver_id
         join app.partners p3 on p3.id = c.sender_id

where v.id = 132443

select c.number,
       p4.name as destination,
       c.valid_from,
       c.valid_to,
       p.name  as carrier,
       p2.name as receiver,
       p3.name as sender
from app.contracts c
         join app.partners p on p.id = c.carrier_id
         join app.partners p2 on p2.id = c.receiver_id
         join app.partners p3 on p3.id = c.sender_id
         join app.polygons p4 on p4.id = c.destination_id
         join app.polygons p5 on p5.id = c.departure_point_id
where p.name = 'Общество с ограниченной ответственностью «Экоспецпром»'


select *
from app.contracts c
where c.number = '16-2024ЭА от 05.02.2024'

select v.invoice_num, pd.address, pd.valid_from, pd.valid_to
from app.visits v
         join app.contracts c on c.id = v.contract_id
         join app.polygon_details pd on c.destination_id = pd.polygon_id
where v.id = 156451
order by pd.valid_to desc;


with cte as (select visit.id              as id,
                    visit.checked_out,
                    valid_contract.valid_from,
                    valid_contract.valid_to,
                    valid_contract.id     as contract_id,
                    valid_contract.number as contract_number,
                    carrier.short_name    as carrier
             from visits visit
                      join permissions perm on perm.id = visit.permission_id
                      join contracts current_contract on current_contract.id = visit.contract_id
                      left join contracts valid_contract
                                on valid_contract.carrier_id = perm.owner_id and
                                   valid_contract.destination_id = current_contract.destination_id
                                    and visit.checked_out between valid_contract.valid_from and valid_contract.valid_to
                      join partners carrier on carrier.id = valid_contract.carrier_id
             where current_contract.carrier_id != perm.owner_id
               and visit.is_deleted = 'false'
             order by visit.checked_out desc)

select v.invoice_num                                             "Номер накладной",
       v.checked_out at time zone 'utc' at time zone 'Asia/Omsk' "Дата выезда",
       pol.name                                                  "Направление",
       p2.short_name as                                          "Пропуск выдан на",
       p3.short_name as                                          "Перевозчик из договора",
       c.number                                                  "Номер договора",
       cte.contract_number                                       "Валидный номер договора"
from visits v
         join contracts c on c.id = v.contract_id
         join polygons pol on pol.id = c.destination_id
         join permissions p on p.id = v.permission_id
         join partners p2 on p2.id = p.owner_id
         join partners p3 on p3.id = c.carrier_id
         join cte on cte.id = v.id
where c.carrier_id != p.owner_id
  and v.is_deleted = 'false'
order by v.checked_out desc;

select v.invoice_num                                             "Номер накладной",
       v.checked_out at time zone 'utc' at time zone 'Asia/Omsk' "Дата выезда",
       pol.name                                                  "Направление",
       p2.short_name as                                          "Пропуск выдан на",
       p3.short_name as                                          "Перевозчик из договора",
       c.number                                                  "Номер договора"
from visits v
         join contracts c on c.id = v.contract_id
         join polygons pol on pol.id = c.destination_id
         join permissions p on p.id = v.permission_id
         join partners p2 on p2.id = p.owner_id
         join partners p3 on p3.id = c.carrier_id
where c.carrier_id != p.owner_id
  and v.is_deleted = 'false'
order by v.checked_out desc;





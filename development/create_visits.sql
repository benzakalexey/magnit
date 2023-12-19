CREATE TEMP TABLE new_visits
(
    permit            int,
    polygon           varchar(255),
    date_out          date,
    brutto            int,
    tara              int,
    netto             int,
    direction         varchar(255),
    driver_first_name varchar(255),
    driver_last_name  varchar(255)
);

insert into new_visits
values (925, 'Кировский', '1/12/2023', 27620, 19620, 8000, 'Таврический', 'Локтионов', 'Сергей'),
       (925, 'Кировский', '1/24/2023', 29100, 20040, 9060, 'Шербакульский', 'Ледовский', 'Сергей'),
       (925, 'Кировский', '1/27/2023', 27660, 20120, 7540, 'Шербакульский', 'Локтионов', 'Сергей'),
       (925, 'Кировский', '1/27/2023', 27040, 19300, 7740, 'Шербакульский', 'Локтионов', 'Сергей'),
       (927, 'Кировский', '1/30/2023', 29000, 19880, 9120, 'Шербакульский', 'Перепелица', 'Владимир'),
       (893, 'Кировский', '1/31/2023', 35700, 20180, 15520, 'Шербакульский', 'Жилинский', 'Андрей'),
       (891, 'Кировский', '1/31/2023', 33080, 19460, 13620, 'Шербакульский', 'Зубаков', 'Денис'),
       (894, 'Кировский', '1/31/2023', 33440, 19520, 13920, 'Шербакульский', 'Браун', 'Владимир'),
       (894, 'Кировский', '2/7/2023', 25300, 19520, 5780, 'Шербакульский', 'Фомичев', 'Сергей'),
       (892, 'Кировский', '2/8/2023', 24960, 19660, 5300, 'Шербакульский', 'Ялкапов', 'Анатолий'),
       (891, 'Кировский', '2/10/2023', 25940, 19500, 6440, 'Шербакульский', 'Зигунов', 'Виктор'),
       (892, 'Кировский', '2/11/2023', 27360, 19640, 7720, 'Шербакульский', 'Канищев', 'Петр'),
       (891, 'Кировский', '2/12/2023', 30300, 19440, 10860, 'Шербакульский', 'Евтеев', 'Олег'),
       (893, 'Кировский', '2/12/2023', 30920, 20020, 10900, 'Шербакульский', 'Зигунов', 'Сергей'),
       (928, 'Кировский', '2/12/2023', 31880, 19800, 12080, 'Шербакульский', 'Дьячук', 'Алексей'),
       (924, 'Кировский', '2/12/2023', 30440, 19880, 10560, 'Шербакульский', 'Саушев', 'Александр'),
       (927, 'Кировский', '2/12/2023', 32920, 19620, 13300, 'Шербакульский', 'Немешев', 'Вячеслав'),
       (926, 'Кировский', '2/12/2023', 29500, 19480, 10020, 'Шербакульский', 'Колесник', 'Сергей'),
       (925, 'Кировский', '2/14/2023', 27420, 19480, 7940, 'Таврический', 'Морозов', 'Сергей'),
       (927, 'Кировский', '2/17/2023', 29480, 19780, 9700, 'Таврический', 'Борисов', 'Андрей'),
       (892, 'Кировский', '2/21/2023', 33520, 19600, 13920, 'Шербакульский', 'Канищев', 'Петр'),
       (927, 'Кировский', '2/25/2023', 31720, 19680, 12040, 'Таврический', 'Немешев', 'Вячеслав'),
       (892, 'Кировский', '2/28/2023', 28420, 19420, 9000, 'Шербакульский', 'Канищев', 'Петр'),
       (891, 'Кировский', '2/28/2023', 29190, 19350, 9840, 'Шербакульский', 'Зубаков', 'Денис');

insert into app.visits (checked_in, checked_out, contract_id, invoice_num, driver_id, operator_in_id, operator_out_id,
                        permission_id, polygon_id, weight_in, weight_out)
select v.date_out as checked_in,
       v.date_out as checked_out,
       c.id       as contract_id,
       CASE
           WHEN v.date_out > '2023-02-01' THEN 'КИР-ФЕВ.2023-'
           WHEN v.date_out <= '2023-02-01' THEN 'КИР-ЯНВ.2023-'
           END    as invoice_num,
       d.id       as driver_id,
       1          as operator_in_id,
       1          as operator_out_id,
       p4.id      as permission_id,
       p.id       as polygon_id,
       v.brutto   as weight_in,
       v.tara     as weight_out
from new_visits v
         join app.polygons p on v.polygon = p.name
         join app.drivers d on d.surname = v.driver_first_name and d.name = v.driver_last_name
         join app.polygons p2 on p2.name = v.direction
         join app.contracts c on p.id = c.departure_point_id and p2.id = c.destination_id
         join app.permits p3 on v.permit = p3.number
         join app.permissions p4 on p3.id = p4.permit_id
where c.valid_from < v.date_out
  and c.valid_to > v.date_out
  and p4.expired_at > v.date_out
  and p4.added_at < v.date_out
  and p4.is_active = 'true';


update app.visits v
set invoice_num = v.invoice_num || v.id
where v.invoice_num = 'КИР-ЯНВ.2023-';

update app.visits v
set invoice_num = v.invoice_num || v.id
where v.invoice_num = 'КИР-ФЕВ.2023-';


drop table new_visits;


-- Для проверки
select v.invoice_num              as ТН,
       p3.number                  as Пропуск,
       t.reg_number               as ТС,
       polygon.name               as Полигон,
       v.checked_in               as Въезд,
       v.checked_out              as Выезд,
       v.weight_in                as Брутто,
       v.weight_in - v.weight_out as Нетто,
       v.weight_out               as Тара,
       p.short_name               as Контрагент,
       destination.name           as Направление,
       d.surname || ' ' || d.name as Водитель
from app.visits v
         join app.drivers d on d.id = v.driver_id
         join app.contracts c on c.id = v.contract_id
         join app.polygons polygon on polygon.id = c.departure_point_id
         join app.polygons destination on destination.id = c.destination_id
         join app.partners p on p.id = c.carrier_id
         join app.permissions p2 on p2.id = v.permission_id
         join app.permits p3 on p3.id = p2.permit_id
         join app.trucks t on t.id = p3.truck_id
where v.invoice_num in ('КИР-ФЕВ.2023-136617',
                        'КИР-ЯНВ.2023-136616',
                        'КИР-ФЕВ.2023-136615',
                        'КИР-ФЕВ.2023-136614',
                        'КИР-ФЕВ.2023-136613',
                        'КИР-ФЕВ.2023-136612',
                        'КИР-ФЕВ.2023-136611',
                        'КИР-ЯНВ.2023-136610',
                        'КИР-ЯНВ.2023-136609',
                        'КИР-ЯНВ.2023-136608',
                        'КИР-ЯНВ.2023-136607',
                        'КИР-ФЕВ.2023-136606',
                        'КИР-ЯНВ.2023-136605',
                        'КИР-ФЕВ.2023-136604',
                        'КИР-ЯНВ.2023-136603',
                        'КИР-ФЕВ.2023-136602',
                        'КИР-ФЕВ.2023-136601',
                        'КИР-ФЕВ.2023-136600',
                        'КИР-ФЕВ.2023-136599',
                        'КИР-ФЕВ.2023-136598',
                        'КИР-ЯНВ.2023-136597',
                        'КИР-ФЕВ.2023-136596',
                        'КИР-ФЕВ.2023-136595'
    );
select v.invoice_num,
       v.is_deleted,
       v.delete_reason,
       v.checked_in,
       v.checked_out,
       v.weight_in,
       v.weight_out,
       p.name         "polygon",
       d.name         "destination",
       drivers.name,
       drivers.surname,
       drivers.patronymic,
       op_in.phone    "operator_in",
       op_out.phone   "operator_out",
       permits.number "permit"

from app.visits v
         join app.polygons p on v.polygon_id = p.id
         left outer join app.contracts c on v.contract_id = c.id
         left outer join app.polygons d on c.destination_id = d.id
         left outer join app.drivers on v.driver_id = drivers.id
         left outer join app.users op_in on v.operator_in_id = op_in.id
         left outer join app.users op_out on v.operator_out_id = op_out.id
         left outer join app.permissions on v.permission_id = permissions.id
         left outer join app.permits on permissions.permit_id = permits.id

order by v.checked_in desc
limit 100;

DROP TYPE "trucktype";
DROP TYPE "userrole";

-- Давыдова Анастасия Владимировна,Весовщик, Калачинск,89048272784
-- Коряков Денис, Заказчик логист, Все, 79831186248

insert into app.users(phone, password_hash, surname, name, is_staff, is_active)
values (9048272784,
        0xE8789D0C556E5F0222A5043B364984590339AA007216EB56AD184AADDB5F4ACE16F3297B3B08DD7CD2B2D9A087337F067032BE5E3DE7517A1C1936D3D1118F52,
        'Коряков', 'Денис', true, true);

insert into app.staff(user_id, role, added_by_id, added_at)
VALUES (18, 'LOGISTIC', 1, '2023-04-16 00:00:00');

insert into app.users(phone, password_hash, surname, name, patronymic, is_staff, is_active)
values (9048272784,
        E'\\xE8789D0C556E5F0222A5043B364984590339AA007216EB56AD184AADDB5F4ACE16F3297B3B08DD7CD2B2D9A087337F067032BE5E3DE7517A1C1936D3D1118F52',
        'Давыдова', 'Анастасия', 'Владимировна', true, true);

insert into app.staff(user_id, role, added_by_id, added_at, polygon_id)
VALUES (19, 'LOGISTIC', 1, '2023-04-16 00:00:00', 1);

UPDATE app.staff SET role = cast('CONTROLLER' as userrole) WHERE id = 19;

alter type userrole add value 'LOGISTIC';
select v.invoice_num,
       v.is_deleted,
       v.delete_reason,
       v.checked_in,
       v.checked_out,
       v.weight_in,
       v.weight_out,
       p.name            "polygon",
       d.name            "destination",
       drivers.name,
       drivers.surname,
       drivers.patronymic,
       op_in.phone       "operator_in",
       op_out.phone      "operator_out",
       trucks.reg_number "reg_num"

from app.visits v
         join app.polygons p on v.polygon_id = p.id
         left outer join app.contracts c on v.contract_id = c.id
         left outer join app.polygons d on c.destination_id = d.id
         left outer join app.drivers on v.driver_id = drivers.id
         left outer join app.users op_in on v.operator_in_id = op_in.id
         left outer join app.users op_out on v.operator_out_id = op_out.id
         left outer join app.permissions on v.permission_id = permissions.id
         left outer join app.permits on permissions.permit_id = permits.id
         left outer join app.trucks on permits.truck_id = trucks.id

where v.checked_in > '2023-04-10 00:00:00.000'
order by v.checked_in;

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

insert into app.users(phone, password_hash, surname, name, is_staff, is_active)
values (9503327700,
        E'\\xE8789D0C556E5F0222A5043B364984590339AA007216EB56AD184AADDB5F4ACE16F3297B3B08DD7CD2B2D9A087337F067032BE5E3DE7517A1C1936D3D1118F52',
        'Гашпорт', 'Анатолий', true, true);

insert into app.staff(user_id, role, added_by_id, added_at)
VALUES (23, 'TONARS_EDITOR', 1, '2023-04-16 00:00:00');

UPDATE app.staff
SET role = cast('CONTROLLER' as userrole)
WHERE id = 19;

alter type userrole add value 'LOGISTIC';

INSERT INTO app.staff (id, user_id, role, polygon_id, added_by_id, added_at) VALUES (DEFAULT, 21, 'GARBAGE_TRUCK_ANALYSIS', null, 1, '2023-02-23 14:32:30.000000')

update app.users SET app.users.password_hash = b'\xc6e\x00(\xd5N\x87m;\xeb\xe8\xc1\xb7:C]\xfb+\x11\xbf\xa8\x0c/\xdd@\xa5_\xaf\r\x80\xfe\x1f\xad\xe8\x7f\x90\x98\xe7\xf0:C\xbf\x1b\x80\x87\xbc\xa7D\xff\xe0t\xf3\x9f\x064V"\'\xec\xea\xc6\x16\xad\x9a' where id = 1
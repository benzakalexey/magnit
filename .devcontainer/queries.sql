select
    v.invoice_num,
    v.is_deleted,
    v.delete_reason,
    v.checked_in,
    v.checked_out,
    v.weight_in,
    v.weight_out,
    p.name "polygon",
    d.name "destination",
    drivers.name,
    drivers.surname,
    drivers.patronymic,
    op_in.phone "operator_in",
    op_out.phone "operator_out",
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

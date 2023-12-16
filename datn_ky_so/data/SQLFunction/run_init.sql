CREATE OR REPLACE FUNCTION public.fn_check_is_kyso(_department_id INTEGER, _loai TEXT)
RETURNS boolean AS
$BODY$
DECLARE
    _is_kyso boolean := false;
BEGIN
    WHILE _department_id IS NOT NULL and _is_kyso = false LOOP
        select parent_id, (_loai = 'guixacnhan' and coalesce(hr_department.kyso_tukhai, false))
                              or (_loai = 'xacnhan' and coalesce(hr_department.kyso_duyet_tukhai, false)) as is_kyso
            into _department_id, _is_kyso
        from hr_department where id = _department_id;
    END LOOP;
    RETURN _is_kyso;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;
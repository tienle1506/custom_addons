CREATE OR REPLACE FUNCTION public.get_list_parent_department(child_department INTEGER)
RETURNS INT4 [] AS
$BODY$
DECLARE
    parent INT;
    parents    INT4 [];
BEGIN
    parent = child_department;
    WHILE parent IS NOT NULL LOOP
        parent = (SELECT parent_id FROM hr_department WHERE id = parent);
        IF parent IS NOT NULL THEN
        parents := parents || parent;
        END IF;
    END LOOP;
    parents := parents || child_department;
    RETURN parents;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

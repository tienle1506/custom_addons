-- Select khoitinhluong
CREATE OR REPLACE FUNCTION public.get_all_children_hr_department(use_parent integer)
  RETURNS integer[] AS
$BODY$
DECLARE
  process_parents INT4 [] := ARRAY [use_parent];
  children        INT4 [] := '{}';
  new_children    INT4 [];
BEGIN
  WHILE (array_upper(process_parents, 1) IS NOT NULL) LOOP
    new_children := ARRAY(SELECT id
                          FROM hr_department
                          WHERE parent_id = ANY (process_parents) AND id <> ALL (children));
    children := children || new_children;
    process_parents := new_children;
  END LOOP;
  children = array_append(children, use_parent);
  RETURN children;
END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION public.get_all_children_hr_department_active_and_none_active(use_parent integer) returns integer[]
  language plpgsql
as
$$
DECLARE
  process_parents INT4 [] := ARRAY [use_parent];
  children        INT4 [] := '{}';
  new_children    INT4 [];
BEGIN
  WHILE (array_upper(process_parents, 1) IS NOT NULL) LOOP
    new_children := ARRAY(SELECT id
                          FROM hr_department
                          WHERE parent_id = ANY (process_parents) AND id <> ALL (children));
    children := children || new_children;
    process_parents := new_children;
  END LOOP;
  children = array_append(children, use_parent);
  RETURN children;
END;
$$;


CREATE OR REPLACE VIEW public.child_department AS
SELECT a.parent_id, a.child_ids
FROM (SELECT child_department.id AS parent_id,
        get_all_children_hr_department(department.id) AS child_ids
    FROM hr_department department
    UNION
    SELECT 1 AS parent_id,
        get_all_children_hr_department(1) AS child_ids) a
ORDER BY a.parent_id;
  
CREATE OR REPLACE VIEW public.all_children_department AS
SELECT a.parent_id, a.child_ids
FROM (SELECT department.id AS parent_id,
        get_all_children_hr_department_active_and_none_active(department.id) AS child_ids
    FROM hr_department department
    UNION
    SELECT 1 AS parent_id,
        get_all_children_hr_department_active_and_none_active(1) AS child_ids) a
ORDER BY a.parent_id;
# Supabase database setup

## Apply the schema and demo data

1. Open the project in the Supabase Dashboard and select **SQL Editor**.
2. Open `schema.sql`, paste its contents into a new query, and run it as the project owner.
   It creates the enums, tables, indexes, triggers, helper functions, RLS policies, and
   default application settings. It is safe to run again.
3. In **Authentication → Users**, create the first administrator. Copy that user's UUID.
4. Open `seed.sql`. Replace the example UUID, name, and email in the commented
   **FIRST SUPER_ADMIN TEMPLATE** statement; uncomment and run that statement.
5. Run the rest of `seed.sql` to add 40 synthetic demo students and one matching skill
   assessment per student. Re-running it updates those demo student records without adding
   duplicate demo assessments. Do not use synthetic demo rows as real outcomes.

The SQL editor runs with owner privileges and bypasses row-level security. Bootstrap and
seed data there; do not expose a service-role key to the browser.

## Verify row-level security

Every application table has RLS enabled and has no policy for the `anon` role. The schema
grants `anon` only `SELECT`, so PostgREST can perform a read that RLS filters to zero rows;
anonymous writes are denied by table privileges. In **Authentication → Policies**, verify
there are no policies targeting `anon`.

To check the anonymous result through the Supabase client or REST API, use only the project
URL and publishable/anon key (never a service-role key):

```js
const { data, error } = await supabase.from('students').select('id').limit(1)
console.log(data, error) // [] and null when the request is made with the anon key
```

In the SQL editor, `SET ROLE anon; SELECT id FROM public.students; RESET ROLE;` also returns
zero rows because of RLS (provided the SQL editor session permits role switching). Repeat
for the other tables if desired. An authenticated user without an active `admin_profiles`
row likewise sees no rows; role-specific writes are restricted by the policies.
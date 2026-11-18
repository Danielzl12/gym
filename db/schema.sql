-- GymBarrio - esquema básico (Supabase / PostgreSQL)
-- Vive en su propio schema "gym" para no mezclarse con otras tablas del proyecto.

create schema if not exists gym;

create table gym.planes (
  id bigint generated always as identity primary key,
  nombre text not null,
  duracion_dias int not null check (duracion_dias > 0),
  precio int not null check (precio >= 0)
);

create table gym.clientes (
  id bigint generated always as identity primary key,
  nombre text not null,
  documento text not null unique,
  telefono text,
  email text,
  creado_en timestamptz not null default now()
);

create table gym.membresias (
  id bigint generated always as identity primary key,
  cliente_id bigint not null references gym.clientes(id) on delete cascade,
  plan_id bigint not null references gym.planes(id),
  fecha_inicio date not null,
  fecha_vencimiento date not null
);

create table gym.pagos (
  id bigint generated always as identity primary key,
  membresia_id bigint not null references gym.membresias(id) on delete cascade,
  valor int not null check (valor >= 0),
  fecha date not null default current_date
);

create table gym.asistencias (
  id bigint generated always as identity primary key,
  cliente_id bigint not null references gym.clientes(id) on delete cascade,
  fecha_hora timestamptz not null default now()
);

-- Correos autorizados como administradores del gimnasio
create table gym.admins (
  email text primary key
);

create function gym.es_admin() returns boolean
language sql stable security definer set search_path = ''
as $$
  select exists (select 1 from gym.admins where email = (auth.jwt() ->> 'email'));
$$;

-- Seguridad: solo los administradores autorizados leen y escriben
alter table gym.planes enable row level security;
alter table gym.clientes enable row level security;
alter table gym.membresias enable row level security;
alter table gym.pagos enable row level security;
alter table gym.asistencias enable row level security;
alter table gym.admins enable row level security;

create policy "admin planes" on gym.planes for all to authenticated using (gym.es_admin()) with check (gym.es_admin());
create policy "admin clientes" on gym.clientes for all to authenticated using (gym.es_admin()) with check (gym.es_admin());
create policy "admin membresias" on gym.membresias for all to authenticated using (gym.es_admin()) with check (gym.es_admin());
create policy "admin pagos" on gym.pagos for all to authenticated using (gym.es_admin()) with check (gym.es_admin());
create policy "admin asistencias" on gym.asistencias for all to authenticated using (gym.es_admin()) with check (gym.es_admin());

-- Permisos para la API
grant usage on schema gym to authenticated;
grant select, insert, update, delete on all tables in schema gym to authenticated;
grant usage, select on all sequences in schema gym to authenticated;
grant execute on function gym.es_admin() to authenticated;

-- Planes iniciales
insert into gym.planes (nombre, duracion_dias, precio) values
  ('Diario', 1, 8000),
  ('Mensual', 30, 60000),
  ('Trimestral', 90, 160000);

-- Para exponer el schema en la API (Supabase > Settings > API > Exposed schemas) o con SQL:
-- alter role authenticator set pgrst.db_schemas = 'public, graphql_public, gym';
-- notify pgrst, 'reload config';
-- notify pgrst, 'reload schema';

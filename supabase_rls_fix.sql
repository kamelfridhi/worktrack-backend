-- =====================================================
-- Supabase RLS (Row Level Security) Fix
-- =====================================================
-- This script enables RLS on all tables that are exposed
-- to PostgREST and creates appropriate policies.
--
-- Run this in Supabase SQL Editor:
-- 1. Go to your Supabase project dashboard
-- 2. Navigate to SQL Editor
-- 3. Paste this entire script
-- 4. Click "Run" or press Ctrl+Enter
-- =====================================================

-- =====================================================
-- 1. Enable RLS on Django System Tables
-- =====================================================

-- Django migrations table (internal use only)
ALTER TABLE public.django_migrations ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Service role can manage django_migrations" ON public.django_migrations;
DROP POLICY IF EXISTS "Public cannot access django_migrations" ON public.django_migrations;

-- Allow service role (Django backend) full access
CREATE POLICY "Service role can manage django_migrations"
ON public.django_migrations
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Deny public access
CREATE POLICY "Public cannot access django_migrations"
ON public.django_migrations
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Django content types
ALTER TABLE public.django_content_type ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage django_content_type" ON public.django_content_type;
DROP POLICY IF EXISTS "Public cannot access django_content_type" ON public.django_content_type;

CREATE POLICY "Service role can manage django_content_type"
ON public.django_content_type
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access django_content_type"
ON public.django_content_type
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Django admin log
ALTER TABLE public.django_admin_log ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage django_admin_log" ON public.django_admin_log;
DROP POLICY IF EXISTS "Public cannot access django_admin_log" ON public.django_admin_log;

CREATE POLICY "Service role can manage django_admin_log"
ON public.django_admin_log
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access django_admin_log"
ON public.django_admin_log
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Django sessions
ALTER TABLE public.django_session ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage django_session" ON public.django_session;
DROP POLICY IF EXISTS "Public cannot access django_session" ON public.django_session;

CREATE POLICY "Service role can manage django_session"
ON public.django_session
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access django_session"
ON public.django_session
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================
-- 2. Enable RLS on Django Auth Tables
-- =====================================================

-- Auth permissions
ALTER TABLE public.auth_permission ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage auth_permission" ON public.auth_permission;
DROP POLICY IF EXISTS "Public cannot access auth_permission" ON public.auth_permission;

CREATE POLICY "Service role can manage auth_permission"
ON public.auth_permission
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access auth_permission"
ON public.auth_permission
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Auth groups
ALTER TABLE public.auth_group ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage auth_group" ON public.auth_group;
DROP POLICY IF EXISTS "Public cannot access auth_group" ON public.auth_group;

CREATE POLICY "Service role can manage auth_group"
ON public.auth_group
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access auth_group"
ON public.auth_group
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Auth group permissions
ALTER TABLE public.auth_group_permissions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage auth_group_permissions" ON public.auth_group_permissions;
DROP POLICY IF EXISTS "Public cannot access auth_group_permissions" ON public.auth_group_permissions;

CREATE POLICY "Service role can manage auth_group_permissions"
ON public.auth_group_permissions
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access auth_group_permissions"
ON public.auth_group_permissions
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Auth user groups
ALTER TABLE public.auth_user_groups ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage auth_user_groups" ON public.auth_user_groups;
DROP POLICY IF EXISTS "Public cannot access auth_user_groups" ON public.auth_user_groups;

CREATE POLICY "Service role can manage auth_user_groups"
ON public.auth_user_groups
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access auth_user_groups"
ON public.auth_user_groups
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Auth user user permissions
ALTER TABLE public.auth_user_user_permissions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage auth_user_user_permissions" ON public.auth_user_user_permissions;
DROP POLICY IF EXISTS "Public cannot access auth_user_user_permissions" ON public.auth_user_user_permissions;

CREATE POLICY "Service role can manage auth_user_user_permissions"
ON public.auth_user_user_permissions
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access auth_user_user_permissions"
ON public.auth_user_user_permissions
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Auth users (sensitive - needs careful handling)
ALTER TABLE public.auth_user ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage auth_user" ON public.auth_user;
DROP POLICY IF EXISTS "Public cannot access auth_user" ON public.auth_user;

CREATE POLICY "Service role can manage auth_user"
ON public.auth_user
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access auth_user"
ON public.auth_user
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================
-- 3. Enable RLS on Custom Application Tables
-- =====================================================

-- Core employees
ALTER TABLE public.core_employee ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage core_employee" ON public.core_employee;
DROP POLICY IF EXISTS "Public cannot access core_employee" ON public.core_employee;

CREATE POLICY "Service role can manage core_employee"
ON public.core_employee
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access core_employee"
ON public.core_employee
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Core projects
ALTER TABLE public.core_project ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage core_project" ON public.core_project;
DROP POLICY IF EXISTS "Public cannot access core_project" ON public.core_project;

CREATE POLICY "Service role can manage core_project"
ON public.core_project
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access core_project"
ON public.core_project
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================

-- Core employee projects
ALTER TABLE public.core_employeeproject ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Service role can manage core_employeeproject" ON public.core_employeeproject;
DROP POLICY IF EXISTS "Public cannot access core_employeeproject" ON public.core_employeeproject;

CREATE POLICY "Service role can manage core_employeeproject"
ON public.core_employeeproject
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Public cannot access core_employeeproject"
ON public.core_employeeproject
FOR ALL
TO public
USING (false)
WITH CHECK (false);

-- =====================================================
-- Verification Query (Optional - run to check RLS status)
-- =====================================================
-- Uncomment the following to verify RLS is enabled:
/*
SELECT
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN (
        'django_migrations',
        'django_content_type',
        'django_admin_log',
        'django_session',
        'auth_permission',
        'auth_group',
        'auth_group_permissions',
        'auth_user_groups',
        'auth_user_user_permissions',
        'auth_user',
        'core_employee',
        'core_project',
        'core_employeeproject'
    )
ORDER BY tablename;
*/


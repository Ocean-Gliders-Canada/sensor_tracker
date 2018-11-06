ALTER TABLE platforms_platformcomment DROP CONSTRAINT platforms_platformcomment_platform_comment_box_id_fkey;
ALTER TABLE platforms_platformcomment DROP CONSTRAINT platforms_platformcomment_user_id_fkey;
ALTER TABLE platforms_platformcommentbox DROP CONSTRAINT platforms_platformcommentbox_platform_id_fkey;
ALTER TABLE platforms_platformdeployment DROP CONSTRAINT platforms_platformdeployment_power_type_id_fkey;
ALTER TABLE platforms_platformdeploymentcomment DROP CONSTRAINT platforms_platformdeploymentc_platform_deployment_comment__fkey;
ALTER TABLE platforms_platformdeploymentcomment DROP CONSTRAINT platforms_platformdeploymentcomment_user_id_fkey;
ALTER TABLE platforms_platformdeploymentcommentbox DROP CONSTRAINT platforms_platformdeploymentcomment_platform_deployment_id_fkey;
ALTER TABLE platforms_platformcomment ALTER COLUMN comment SET NOT NULL;
ALTER TABLE platforms_platformcomment ALTER COLUMN created_date TYPE timestamp with time zone USING created_date::timestamp with time zone;
ALTER TABLE platforms_platformcomment ALTER COLUMN id TYPE integer USING id::integer;
ALTER TABLE platforms_platformcomment ALTER COLUMN platform_comment_box_id SET NOT NULL;
ALTER TABLE platforms_platformcomment ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE platforms_platformcommentbox ALTER COLUMN id TYPE integer USING id::integer;
ALTER TABLE platforms_platformcommentbox ALTER COLUMN platform_id SET NOT NULL;
ALTER TABLE platforms_platformdeployment ALTER COLUMN platform_name TYPE varchar(500) USING platform_name::varchar(500);
UPDATE platforms_platformdeployment SET testing_mission = False WHERE testing_mission IS NULL;
ALTER TABLE platforms_platformdeployment ALTER COLUMN testing_mission SET NOT NULL;
ALTER TABLE platforms_platformdeploymentcomment ALTER COLUMN comment SET NOT NULL;
ALTER TABLE platforms_platformdeploymentcomment ALTER COLUMN created_date TYPE timestamp with time zone USING created_date::timestamp with time zone;
ALTER TABLE platforms_platformdeploymentcomment ALTER COLUMN id TYPE integer USING id::integer;
ALTER TABLE platforms_platformdeploymentcomment ALTER COLUMN platform_deployment_comment_box_id SET NOT NULL;
ALTER TABLE platforms_platformdeploymentcomment ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE platforms_platformdeploymentcommentbox ALTER COLUMN id TYPE integer USING id::integer;
ALTER TABLE platforms_platformdeploymentcommentbox ALTER COLUMN platform_deployment_id SET NOT NULL;
ALTER TABLE platforms_platformpowertype ALTER COLUMN id TYPE integer USING id::integer;
ALTER TABLE platforms_platformpowertype ALTER COLUMN name SET NOT NULL;
ALTER TABLE platforms_platformcomment
ADD CONSTRAINT "D7e8ea4164f496b73825bdcd324df307"
FOREIGN KEY (platform_comment_box_id) REFERENCES platforms_platformcommentbox (id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX platforms_platformcomment_5f18b865 ON platforms_platformcomment (platform_comment_box_id);
CREATE INDEX platforms_platformcomment_e8701ad4 ON platforms_platformcomment (user_id);
ALTER TABLE platforms_platformcomment
ADD CONSTRAINT platforms_platformcomment_user_id_00d78222_fk_auth_user_id
FOREIGN KEY (user_id) REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE platforms_platformcommentbox
ADD CONSTRAINT platforms_platfor_platform_id_079baa00_fk_platforms_platform_id
FOREIGN KEY (platform_id) REFERENCES platforms_platform (id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE platforms_platformdeployment
ADD CONSTRAINT platfo_power_type_id_4d134eb8_fk_platforms_platformpowertype_id
FOREIGN KEY (power_type_id) REFERENCES platforms_platformpowertype (id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX platforms_platformdeployment_ba2b6f8d ON platforms_platformdeployment (power_type_id);
ALTER TABLE platforms_platformdeploymentcomment
ADD CONSTRAINT b8eedf13c34d59be1ec07ff2c3f6930b
FOREIGN KEY (platform_deployment_comment_box_id) REFERENCES platforms_platformdeploymentcommentbox (id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE platforms_platformdeploymentcomment
ADD CONSTRAINT platforms_platformdeploymentco_user_id_f5f1db99_fk_auth_user_id
FOREIGN KEY (user_id) REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX platforms_platformdeploymentcomment_78fb5a55 ON platforms_platformdeploymentcomment (platform_deployment_comment_box_id);
CREATE INDEX platforms_platformdeploymentcomment_e8701ad4 ON platforms_platformdeploymentcomment (user_id);
ALTER TABLE platforms_platformdeploymentcommentbox
ADD CONSTRAINT "D9a5be41479c38162ef4fe14f98f1366"
FOREIGN KEY (platform_deployment_id) REFERENCES platforms_platformdeployment (id) DEFERRABLE INITIALLY DEFERRED;

DELETE FROM django_migrations;
INSERT INTO django_migrations (id, app, name, applied) VALUES
  (1,		'contenttypes',	'0001_initial',								              now()),
  (2,		'auth',			    '0001_initial',								              now()),
  (3,		'admin',		    '0001_initial',								              now()),
  (4,		'admin',		    '0002_logentry_remove_auto_add',			      now()),
  (5,		'contenttypes',	'0002_remove_content_type_name',			      now()),
  (6,		'auth',			    '0002_alter_permission_name_max_length',    now()),
  (7,		'auth',			    '0003_alter_user_email_max_length',			    now()),
  (8,		'auth',			    '0004_alter_user_username_opts',			      now()),
  (9,		'auth',			    '0005_alter_user_last_login_null',			    now()),
  (10,	'auth',			    '0006_require_contenttypes_0002',			      now()),
  (11,	'auth',			    '0007_alter_validators_add_error_messages',	now()),
  (12,	'auth',			    '0008_alter_user_username_max_length',		  now()),
  (13,	'authtoken',  	'0001_initial',                             now()),
  (14,	'authtoken',	  '0002_auto_20160226_1747',					        now()),
  (15,	'general',		  '0001_initial',								              now()),
  (16,	'platforms',	  '0001_initial',								              now()),
  (17,	'instruments',	'0001_initial',								              now()),
  (18,	'sessions',	  	'0001_initial',								              now());
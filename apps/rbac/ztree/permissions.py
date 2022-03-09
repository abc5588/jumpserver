# @ 分割符  $ 企业版 # ! 系统级别 # # 组织级别 # 控制台
flag_sep = '@'
flag_license = '$'
flag_scop_system = '!'
# flag_scop_org = '#'

permission_paths = [
    # format: 权限树路径 / app.codename @ 企业版、系统级别
    '/root/view/view_console/rbac.view_adminview',
    '/root/view/view_console/rbac.view_resourcestatistics',
    '/root/view/view_console/user_management/user_list/users.view_user',
    '/root/view/view_console/user_management/user_list/users.add_user',
    '/root/view/view_console/user_management/user_list/users.change_user',
    '/root/view/view_console/user_management/user_list/users.delete_user',
    '/root/view/view_console/user_management/user_list/users.invite_user',
    '/root/view/view_console/user_management/user_list/users.remove_user',
    '/root/view/view_console/user_management/user_list/user_detail/perms.view_userassets',
    '/root/view/view_console/user_management/user_list/user_detail/asset_perm/perms.view_assetpermission',
    '/root/view/view_console/user_management/user_list/user_detail/asset_perm/perms.change_assetpermission',
    '/root/view/view_console/user_management/user_list/user_detail/asset_perm/perms.delete_assetpermission',
    '/root/view/view_console/user_management/user_list/user_detail/perms.view_userapps',
    '/root/view/view_console/user_management/user_list/user_detail/app_perm/perms.view_applicationpermission',
    '/root/view/view_console/user_management/user_list/user_detail/app_perm/perms.change_applicationpermission',
    '/root/view/view_console/user_management/user_list/user_detail/app_perm/perms.delete_applicationpermission',
    '/root/view/view_console/user_management/user_list/user_detail/user_login_acl/acls.view_loginacl',
    '/root/view/view_console/user_management/user_list/user_detail/user_login_acl/acls.add_loginacl',
    '/root/view/view_console/user_management/user_list/user_detail/user_login_acl/acls.change_loginacl',
    '/root/view/view_console/user_management/user_list/user_detail/user_login_acl/acls.delete_loginacl',
    '/root/view/view_console/user_management/user_group_list/users.view_usergroup',
    '/root/view/view_console/user_management/user_group_list/users.add_usergroup',
    '/root/view/view_console/user_management/user_group_list/users.change_usergroup',
    '/root/view/view_console/user_management/user_group_list/users.delete_usergroup',
    '/root/view/view_console/user_management/user_group_list/user_group_detail/perms.view_permusergroupasset',
    '/root/view/view_console/user_management/role_list/permission_list/rbac.view_permission',
    '/root/view/view_console/user_management/role_list/org_role/rbac.view_orgrole',
    '/root/view/view_console/user_management/role_list/org_role/rbac.add_orgrole',
    '/root/view/view_console/user_management/role_list/org_role/rbac.change_orgrole',
    '/root/view/view_console/user_management/role_list/org_role/rbac.delete_orgrole',
    '/root/view/view_console/user_management/role_list/org_role/org_role_detail/rbac.view_orgrolebinding',
    '/root/view/view_console/user_management/role_list/org_role/org_role_detail/rbac.add_orgrolebinding',
    '/root/view/view_console/user_management/role_list/org_role/org_role_detail/rbac.change_orgrolebinding',
    '/root/view/view_console/user_management/role_list/org_role/org_role_detail/rbac.delete_orgrolebinding',
    '/root/view/view_console/user_management/role_list/system_role/rbac.view_systemrole',
    '/root/view/view_console/user_management/role_list/system_role/rbac.add_systemrole',
    '/root/view/view_console/user_management/role_list/system_role/rbac.change_systemrole',
    '/root/view/view_console/user_management/role_list/system_role/rbac.delete_systemrole',
    '/root/view/view_console/user_management/role_list/system_role/system_role_detail/rbac.view_systemrolebinding',
    '/root/view/view_console/user_management/role_list/system_role/system_role_detail/rbac.add_systemrolebinding',
    '/root/view/view_console/user_management/role_list/system_role/system_role_detail/rbac.change_systemrolebinding',
    '/root/view/view_console/user_management/role_list/system_role/system_role_detail/rbac.delete_systemrolebinding',

    '/root/view/view_console/asset_management/asset_list/assets.view_asset',
    '/root/view/view_console/asset_management/asset_list/assets.add_asset',
    '/root/view/view_console/asset_management/asset_list/assets.change_asset',
    '/root/view/view_console/asset_management/asset_list/assets.delete_asset',
    '/root/view/view_console/asset_management/asset_list/assets.test_assetconnectivity',
    '/root/view/view_console/asset_management/asset_list/assets.refresh_assethardwareinfo',
    '/root/view/view_console/asset_management/asset_list/assets.push_assetsystemuser',
    '/root/view/view_console/asset_management/asset_list/assets.match_asset',
    '/root/view/view_console/asset_management/asset_list/node_tree/assets.view_node',
    '/root/view/view_console/asset_management/asset_list/node_tree/assets.add_node',
    '/root/view/view_console/asset_management/asset_list/node_tree/assets.change_node',
    '/root/view/view_console/asset_management/asset_list/node_tree/assets.delete_node',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/sync_instance_task_list/xpack.view_syncinstancetask',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/sync_instance_task_list/xpack.add_syncinstancetask',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/sync_instance_task_list/xpack.change_syncinstancetask',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/sync_instance_task_list/xpack.delete_syncinstancetask',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/sync_instance_task_list/sync_instance_task_detail/xpack.view_syncinstancetaskexecution',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/sync_instance_task_list/sync_instance_task_detail/xpack.view_syncinstancedetail',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/account_list/xpack.view_account',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/account_list/xpack.add_account',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/account_list/xpack.change_account',
    '/root/view/view_console/asset_management/asset_list/cloud_sync/account_list/xpack.delete_account',
    '/root/view/view_console/asset_management/domain_list/assets.view_domain',
    '/root/view/view_console/asset_management/domain_list/assets.add_domain',
    '/root/view/view_console/asset_management/domain_list/assets.change_domain',
    '/root/view/view_console/asset_management/domain_list/assets.delete_domain',
    '/root/view/view_console/asset_management/domain_list/gateway_list/assets.view_gateway',
    '/root/view/view_console/asset_management/domain_list/gateway_list/assets.add_gateway',
    '/root/view/view_console/asset_management/domain_list/gateway_list/assets.change_gateway',
    '/root/view/view_console/asset_management/domain_list/gateway_list/assets.delete_gateway',
    '/root/view/view_console/asset_management/system_user/assets.view_systemuser',
    '/root/view/view_console/asset_management/system_user/assets.add_systemuser',
    '/root/view/view_console/asset_management/system_user/assets.change_systemuser',
    '/root/view/view_console/asset_management/system_user/assets.delete_systemuser',
    '/root/view/view_console/asset_management/system_user/assets.test_assetconnectivity',
    '/root/view/view_console/asset_management/system_user/assets.push_assetsystemuser',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_asset_list/assets.view_systemuserasset',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_asset_list/assets.add_systemuserasset',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_asset_list/assets.remove_systemuserasset',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_account_list/assets.view_authbook',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_account_list/assets.change_authbook',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_account_list/assets.delete_authbook',
    '/root/view/view_console/asset_management/system_user/system_user_detail/system_user_account_list/assets.test_authbook',
    '/root/view/view_console/asset_management/command_filter/assets.view_commandfilter',
    '/root/view/view_console/asset_management/command_filter/assets.add_commandfilter',
    '/root/view/view_console/asset_management/command_filter/assets.change_commandfilter',
    '/root/view/view_console/asset_management/command_filter/assets.delete_commandfilter',
    '/root/view/view_console/asset_management/command_filter/command_filter_rule/assets.view_commandfilterrule',
    '/root/view/view_console/asset_management/command_filter/command_filter_rule/assets.add_commandfilterrule',
    '/root/view/view_console/asset_management/command_filter/command_filter_rule/assets.change_commandfilterrule',
    '/root/view/view_console/asset_management/command_filter/command_filter_rule/assets.delete_commandfilterrule',
    '/root/view/view_console/asset_management/platform_list/assets.view_platform',
    '/root/view/view_console/asset_management/platform_list/assets.add_platform',
    '/root/view/view_console/asset_management/platform_list/assets.change_platform',
    '/root/view/view_console/asset_management/platform_list/assets.delete_platform',
    '/root/view/view_console/asset_management/label_management/assets.view_label',
    '/root/view/view_console/asset_management/label_management/assets.add_label',
    '/root/view/view_console/asset_management/label_management/assets.change_label',
    '/root/view/view_console/asset_management/label_management/assets.delete_label',

    '/root/view/view_console/app_management/remote_app/applications.view_remoteapp',
    '/root/view/view_console/app_management/remote_app/applications.add_remoteapp',
    '/root/view/view_console/app_management/remote_app/applications.change_remoteapp',
    '/root/view/view_console/app_management/remote_app/applications.delete_remoteapp',
    '/root/view/view_console/app_management/db_app/applications.view_databaseapp',
    '/root/view/view_console/app_management/db_app/applications.add_databaseapp',
    '/root/view/view_console/app_management/db_app/applications.change_databaseapp',
    '/root/view/view_console/app_management/db_app/applications.delete_databaseapp',
    '/root/view/view_console/app_management/k8s_app/applications.view_kubernetesapp',
    '/root/view/view_console/app_management/k8s_app/applications.add_kubernetesapp',
    '/root/view/view_console/app_management/k8s_app/applications.change_kubernetesapp',
    '/root/view/view_console/app_management/k8s_app/applications.delete_kubernetesapp',

    '/root/view/view_console/account_management/asset_account/assets.view_authbook',
    '/root/view/view_console/account_management/asset_account/assets.add_authbook',
    '/root/view/view_console/account_management/asset_account/assets.change_authbook',
    '/root/view/view_console/account_management/asset_account/assets.delete_authbook',
    '/root/view/view_console/account_management/asset_account/assets.test_authbook',
    '/root/view/view_console/account_management/application_account/applications.view_account',
    '/root/view/view_console/account_management/application_account/applications.add_account',
    '/root/view/view_console/account_management/application_account/applications.change_account',
    '/root/view/view_console/account_management/application_account/applications.delete_account',
    '/root/view/view_console/account_management/gather_user/gather_user_list/assets.view_gathereduser',
    '/root/view/view_console/account_management/gather_user/gather_user_task_list/xpack.view_gatherusertask',
    '/root/view/view_console/account_management/gather_user/gather_user_task_list/xpack.add_gatherusertask',
    '/root/view/view_console/account_management/gather_user/gather_user_task_list/xpack.change_gatherusertask',
    '/root/view/view_console/account_management/gather_user/gather_user_task_list/xpack.delete_gatherusertask',
    '/root/view/view_console/account_management/gather_user/gather_user_task_list/xpack.add_gatherusertaskexecution',
    '/root/view/view_console/account_management/gather_user/gather_user_task_list/xpack.view_gatherusertaskexecution',
    '/root/view/view_console/account_management/change_auth_plan/asset_change_auth_plan/xpack.view_changeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/asset_change_auth_plan/xpack.add_changeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/asset_change_auth_plan/xpack.change_changeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/asset_change_auth_plan/xpack.delete_changeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/asset_change_auth_plan/xpack.add_changeauthplanexecution',
    '/root/view/view_console/account_management/change_auth_plan/asset_change_auth_plan/xpack.view_changeauthplanexecution',
    '/root/view/view_console/account_management/change_auth_plan/app_change_auth_plan/xpack.view_applicationchangeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/app_change_auth_plan/xpack.add_applicationchangeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/app_change_auth_plan/xpack.change_applicationchangeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/app_change_auth_plan/xpack.delete_applicationchangeauthplan',
    '/root/view/view_console/account_management/change_auth_plan/app_change_auth_plan/xpack.add_applicationchangeauthplanexecution',
    '/root/view/view_console/account_management/change_auth_plan/app_change_auth_plan/xpack.view_applicationchangeauthplanexecution',
    '/root/view/view_console/account_management/account_backup/assets.view_accountbackupplan',
    '/root/view/view_console/account_management/account_backup/assets.add_accountbackupplan',
    '/root/view/view_console/account_management/account_backup/assets.change_accountbackupplan',
    '/root/view/view_console/account_management/account_backup/assets.delete_accountbackupplan',
    '/root/view/view_console/account_management/account_backup/assets.add_accountbackupplanexecution',
    '/root/view/view_console/account_management/account_backup/assets.view_accountbackupplanexecution',

    '/root/view/view_console/perm_management/asset_permission/perms.view_assetpermission',
    '/root/view/view_console/perm_management/asset_permission/perms.add_assetpermission',
    '/root/view/view_console/perm_management/asset_permission/perms.change_assetpermission',
    '/root/view/view_console/perm_management/asset_permission/perms.delete_assetpermission',
    '/root/view/view_console/perm_management/app_permission/perms.view_applicationpermission',
    '/root/view/view_console/perm_management/app_permission/perms.add_applicationpermission',
    '/root/view/view_console/perm_management/app_permission/perms.change_applicationpermission',
    '/root/view/view_console/perm_management/app_permission/perms.delete_applicationpermission',

    '/root/view/view_console/access_control/asset_login/acls.view_loginassetacl',
    '/root/view/view_console/access_control/asset_login/acls.add_loginassetacl',
    '/root/view/view_console/access_control/asset_login/acls.change_loginassetacl',
    '/root/view/view_console/access_control/asset_login/acls.delete_loginassetacl',

    '/root/view/view_console/job_center/task_list/ops.view_task',
    '/root/view/view_console/job_center/task_list/ops.delete_task',
    '/root/view/view_console/job_center/task_list/ops.add_adhocexecution',
    '/root/view/view_console/job_center/task_list/task_list_detail/ops.view_adhoc',
    '/root/view/view_console/job_center/task_list/task_list_detail/ops.view_adhocexecution',
    '/root/view/view_console/job_center/ops.view_taskmonitor',

    '/root/view/view_audit/rbac.view_auditview',
    '/root/view/view_audit/rbac.view_resourcestatistics',
    '/root/view/view_audit/session_audit/session_record/terminal.view_session',
    '/root/view/view_audit/session_audit/session_record/terminal.terminate_session',
    '/root/view/view_audit/session_audit/session_record/terminal.monitor_session',
    '/root/view/view_audit/session_audit/session_record/session_detail/terminal.view_command',
    '/root/view/view_audit/session_audit/session_record/session_detail/terminal.view_sessionjoinrecord',
    '/root/view/view_audit/session_audit/command_record/terminal.view_command',
    '/root/view/view_audit/session_audit/command_record/terminal.view_commandstorage',
    '/root/view/view_audit/session_audit/file_transfer/audits.view_ftplog',
    '/root/view/view_audit/log_audit/audits.view_userloginlog',
    '/root/view/view_audit/log_audit/audits.view_operatelog',
    '/root/view/view_audit/log_audit/audits.view_passwordchangelog',
    '/root/view/view_audit/log_audit/ops.view_commandexecution',

    '/root/view/view_workspace/rbac.view_userview',
    '/root/view/view_workspace/rbac.overview(any)',
    '/root/view/view_workspace/my_asset/perms.view_myassets',
    '/root/view/view_workspace/my_asset/perms.connect_myassets',
    '/root/view/view_workspace/my_app/my_remote_app/perms.view_myremoteapp',
    '/root/view/view_workspace/my_app/my_remote_app/perms.connect_myremoteapp',
    '/root/view/view_workspace/my_app/my_db_app/perms.view_mydatabaseapp',
    '/root/view/view_workspace/my_app/my_db_app/perms.connect_mydatabaseapp',
    '/root/view/view_workspace/my_app/my_k8s_app/perms.view_mykubernetesapp',
    '/root/view/view_workspace/my_app/my_k8s_app/perms.connect_mykubernetesapp',
    '/root/view/view_workspace/ops.add_commandexecution',
    '/root/view/view_workspace/rbac.view_webterminal',
    '/root/view/view_workspace/rbac.view_filemanager',

    '/root/notifications.view_sitemessage',
    '/root/rbac.view_webterminal',

    '/root/system_setting/settings.change_basic',
    '/root/system_setting/settings.change_email',
    '/root/system_setting/settings.change_auth',
    '/root/system_setting/notifications.change_systemmsgsubscription',
    '/root/system_setting/settings.change_sms',
    '/root/system_setting/terminal_setting/settings.change_terminal_basic_setting',
    '/root/system_setting/terminal_setting/terminal_management/terminal.view_terminal',
    '/root/system_setting/terminal_setting/terminal_management/terminal.change_terminal',
    '/root/system_setting/terminal_setting/terminal_management/terminal.delete_terminal',
    '/root/system_setting/terminal_setting/replay_storage/terminal.view_replaystorage',
    '/root/system_setting/terminal_setting/replay_storage/terminal.add_replaystorage',
    '/root/system_setting/terminal_setting/replay_storage/terminal.change_replaystorage',
    '/root/system_setting/terminal_setting/replay_storage/terminal.delete_replaystorage',
    '/root/system_setting/terminal_setting/command_storage/terminal.view_commandstorage',
    '/root/system_setting/terminal_setting/command_storage/terminal.add_commandstorage',
    '/root/system_setting/terminal_setting/command_storage/terminal.change_commandstorage',
    '/root/system_setting/terminal_setting/command_storage/terminal.delete_commandstorage',
    '/root/system_setting/terminal_setting/terminal.view_status',
    '/root/system_setting/settings.change_security',
    '/root/system_setting/settings.change_clean',
    '/root/system_setting/org_management/orgs.view_rootorg',
    '/root/system_setting/org_management/orgs.view_organization',
    '/root/system_setting/org_management/orgs.add_organization',
    '/root/system_setting/org_management/orgs.change_organization',
    '/root/system_setting/org_management/orgs.delete_organization',
    '/root/system_setting/settings.change_other',
    '/root/system_setting/license/xpack.view_license',
    '/root/system_setting/license/xpack.add_license',

    '/root/ticket/tickets.view_ticket',
    '/root/ticket/tickets.add_ticket',
    '/root/ticket/ticket_detail/tickets.change_ticket',
    '/root/ticket/ticket_detail/tickets.add_comment',
    '/root/ticket/ticket_detail/tickets.view_comment',
    '/root/ticket/ticket_detail/tickets.view_ticketsession',

    # '/root/rbac.view_help',
    # '/root/api_permission/',
]
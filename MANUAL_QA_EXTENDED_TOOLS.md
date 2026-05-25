# Manual QA: Extended REST Coverage (58 tools)

## Task + Checklist + DataTags

1. `planfix_task_create` -> `{"payload":{"name":"QA task"}}`
2. `planfix_task_get` -> `{"task_id":12345}`
3. `planfix_task_update` -> `{"task_id":12345,"payload":{"name":"QA updated"}}`
4. `planfix_task_list` -> `{"payload":{}}`
5. `planfix_task_update_custom_fields` -> `{"task_id":12345,"payload":{"customFieldData":[]}}`
6. `planfix_task_accept` -> `{"task_id":12345,"payload":{}}`
7. `planfix_task_reject` -> `{"task_id":12345,"payload":{}}`
8. `planfix_task_change_status` -> `{"task_id":12345,"payload":{"status":{"name":"В работе"}}}`
9. `planfix_task_get_statuses` -> `{"task_id":12345,"payload":{"process_id":100206}}`
10. `planfix_task_change_assignees` -> `{"task_id":12345,"payload":{"assignees":{"users":[{"id":"user:1942"}]}}}`
11. `planfix_task_change_dates` -> `{"task_id":12345,"payload":{"startDateTime":"2026-02-18 10:00:00","endDateTime":"2026-02-19 18:00:00"}}`
12. `planfix_task_comments_list` -> `{"task_id":12345,"payload":{}}`
13. `planfix_task_comment_add` -> `{"task_id":12345,"payload":{"description":"QA comment"}}`
14. `planfix_task_comment_update` -> `{"task_id":12345,"comment_id":67890,"payload":{"description":"QA comment updated"}}`
15. `planfix_task_datatag_add` -> `{"task_id":12345,"payload":{"dataTag":{"id":10},"items":[]}}`
16. `planfix_task_datatag_to_comment` -> `{"task_id":12345,"comment_id":67890,"payload":{"dataTag":{"id":10},"items":[]}}`
17. `planfix_task_files` -> `{"task_id":12345,"payload":{}}`
18. `planfix_task_templates` -> `{"payload":{}}`
19. `planfix_task_recurring` -> `{"payload":{}}`
20. `planfix_task_filters` -> `{"payload":{}}`
21. `planfix_task_checklist_create` -> `{"task_id":12345,"payload":{"name":"Checklist item"}}`
22. `planfix_task_checklist_get` -> `{"task_id":12345,"payload":{}}`
23. `planfix_task_checklist_item_get` -> `{"task_id":12345,"item_id":777}`
24. `planfix_task_checklist_update` -> `{"task_id":12345,"item_id":777,"payload":{"isDone":true}}`

## Comments (global)

25. `planfix_comment_get` -> `{"comment_id":67890}`
26. `planfix_comment_delete` -> `{"comment_id":67890}`

## Projects

27. `planfix_project_create` -> `{"payload":{"name":"QA project"}}`
28. `planfix_project_groups` -> `{"payload":{}}`
29. `planfix_project_list` -> `{"payload":{}}`
30. `planfix_project_templates` -> `{"payload":{}}`
31. `planfix_project_get` -> `{"project_id":3}`
32. `planfix_project_update` -> `{"project_id":3,"payload":{"name":"QA project updated"}}`
33. `planfix_project_files` -> `{"project_id":3,"payload":{}}`

## Directories

34. `planfix_directory_groups` -> `{"payload":{}}`
35. `planfix_directory_list` -> `{"payload":{}}`
36. `planfix_directory_get` -> `{"directory_id":10}`
37. `planfix_directory_entry_add` -> `{"directory_id":10,"payload":{"name":"QA entry"}}`
38. `planfix_directory_entry_list` -> `{"directory_id":10,"payload":{}}`
39. `planfix_directory_entry_get` -> `{"directory_id":10,"key":"1"}`
40. `planfix_directory_entry_update` -> `{"directory_id":10,"key":"1","payload":{"name":"QA entry updated"}}`
41. `planfix_directory_entry_delete` -> `{"directory_id":10,"key":"1"}`
42. `planfix_directory_filters` -> `{"directory_id":10,"payload":{}}`

## Process + Object

43. `planfix_process_contact_list` -> `{"payload":{}}`
44. `planfix_process_task_list` -> `{"payload":{}}`
45. `planfix_process_task_statuses` -> `{"process_id":100206,"payload":{}}`
46. `planfix_object_list` -> `{"payload":{}}`
47. `planfix_object_get` -> `{"object_id":100}`
48. `planfix_object_statuses` -> `{"object_id":100,"payload":{}}`

## Custom fields (Task + Project)

49. `planfix_customfield_task_group_list` -> `{"payload":{}}`
50. `planfix_customfield_task_group_create` -> `{"payload":{"name":"QA task field set"}}`
51. `planfix_customfield_task_list` -> `{"payload":{}}`
52. `planfix_customfield_task_create` -> `{"payload":{"name":"QA task field"}}`
53. `planfix_customfield_task_get` -> `{"field_id":10}`
54. `planfix_customfield_project_group_list` -> `{"payload":{}}`
55. `planfix_customfield_project_group_create` -> `{"payload":{"name":"QA project field set"}}`
56. `planfix_customfield_project_list` -> `{"payload":{}}`
57. `planfix_customfield_project_create` -> `{"payload":{"name":"QA project field"}}`
58. `planfix_customfield_project_get` -> `{"field_id":10}`


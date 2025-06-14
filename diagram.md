# Django ER Diagram

```mermaid
erDiagram
LogEntry {
    AutoField id
    DateTimeField action_time
    ForeignKey user
    ForeignKey content_type
    TextField object_id
    CharField object_repr
    PositiveSmallIntegerField action_flag
    TextField change_message
}
Permission {
    AutoField id
    CharField name
    ForeignKey content_type
    CharField codename
}
Group {
    AutoField id
    CharField name
    ManyToManyField permissions
}
ContentType {
    AutoField id
    CharField app_label
    CharField model
}
Session {
    CharField session_key
    TextField session_data
    DateTimeField expire_date
}
MyUser {
    BigAutoField id
    CharField password
    DateTimeField last_login
    BooleanField is_superuser
    CharField username
    CharField first_name
    CharField last_name
    CharField email
    BooleanField is_staff
    BooleanField is_active
    DateTimeField date_joined
    ManyToManyField groups
    ManyToManyField user_permissions
}
DocumentMetrics {
    BigAutoField id
    PositiveIntegerField statistics_requests
    DateTimeField latest_statistics_processed_timestamp
    FloatField min_time_processed
    FloatField total_time_processed
    FloatField avg_time_processed
    FloatField max_time_processed
}
CollectionMetrics {
    BigAutoField id
    PositiveIntegerField statistics_requests
    DateTimeField latest_statistics_processed_timestamp
    FloatField min_time_processed
    FloatField total_time_processed
    FloatField avg_time_processed
    FloatField max_time_processed
}
Collections {
    BigAutoField id
    CharField name
    TextField description
    ForeignKey owner
}
Document {
    BigAutoField id
    CharField title
    TextField content
    ForeignKey owner
    ManyToManyField collections
}
LogEntry }|--|| MyUser : user
LogEntry }|--|| ContentType : content_type
Permission }|--|| ContentType : content_type
Group }|--|{ Permission : permissions
MyUser }|--|{ Group : groups
MyUser }|--|{ Permission : user_permissions
Collections }|--|| MyUser : owner
Document }|--|| MyUser : owner
Document }|--|{ Collections : collections
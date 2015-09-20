{% if subscribed %}
{% if subscribed|length > 1 %}NEW SUBSCRIPTIONS{% else %}NEW SUBSCRIPTION{% endif %} :
{% for c in subscribed %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if unsubscribed %}
{% if unsubscribed|length > 1 %}CANCELLED SUBSCRIPTIONS{% else %}CANCELLED SUBSCRIPTION{% endif %} :
{% for c in unsubscribed %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if published %}
{% if published|length > 1 %}PUBLISHED COMMENTS{% else %}PUBLISHED COMMENT{% endif %} :
{% for c in published %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if rejected %}
{% if rejected|length > 1 %}REJECTED COMMENTS{% else %}REJECTED COMMENT{% endif %} :
{% for c in rejected %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if standbys %}
{% if standbys|length > 1 %}STANDBY COMMENTS{% else %}STANDBY COMMENT{% endif %} :
{% for c in standbys %}
- {{ c.name }} ({{ c.created }}) => {{ c.url }}
{{ c.content }}

  Accepter : {{ root_url}}/accept?secret={{ secret}}&comment={{ c.id }}
  Rejeter  : {{ root_url}}/reject?secret={{ secret}}&comment={{ c.id }}

{% endfor %}
{% endif %}
--
Stacosys


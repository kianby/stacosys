{% if subscribed %}
{% if subscribed|length > 1 %}NOUVEAUX ABONNEMENTS{% else %}NOUVEL ABONNEMENT{% endif %} :
{% for c in subscribed %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if unsubscribed %}
{% if unsubscribed|length > 1 %}ABONNEMENTS RESILIES{% else %}ABONNEMENT RESILIE{% endif %} :
{% for c in unsubscribed %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if published %}
{% if published|length > 1 %}COMMENTAIRES PUBLIES{% else %}COMMENTAIRE PUBLIE{% endif %} :
{% for c in published %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if rejected %}
{% if rejected|length > 1 %}COMMENTAIRES REJETES{% else %}COMMENTAIRE REJETE{% endif %} :
{% for c in rejected %}
- {{ c.name }} ({{ c.email }}) => {{ c.url }}
{% endfor %}

{% endif %}
{% if standbys %}
{% if standbys|length > 1 %}COMMENTAIRES EN ATTENTE{% else %}COMMENTAIRE EN ATTENTE{% endif %} :
{% for c in standbys %}
- {{ c.name }} ({{ c.created }}) => {{ c.url }}
{{ c.content }}

  Accepter : {{ root_url}}/accept?secret={{ secret}}&comment={{ c.id }}
  Rejeter  : {{ root_url}}/reject?secret={{ secret}}&comment={{ c.id }}

{% endfor %}
{% endif %}
--
Stacosys


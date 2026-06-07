{% macro get_brand_name(column_name) %}
	{# Inline regex extraction for Postgres #}
	REGEXP_REPLACE({{ column_name }}, '.+/brand/', '')
{% endmacro %}

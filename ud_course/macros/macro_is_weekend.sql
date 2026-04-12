{%- macro is_weekend(date_column) -%}
	EXTRACT(DOW FROM {{ date_column }}) IN (0, 6)
{%- endmacro -%}
